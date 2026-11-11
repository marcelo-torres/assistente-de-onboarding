"""Plugin e Callbacks do Google ADK para a Camada de Guardrails."""

from __future__ import annotations

import inspect
import logging
from typing import Any, Optional

from google.adk.plugins.base_plugin import BasePlugin
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.tools.base_tool import BaseTool
from google.genai import types

from ..config import MSG_OUTPUT_VIOLATION, MSG_SAFETY_REFUSAL
from ..contracts import RailType, RiskCategory, Verdict
from ..observability import log_verdict
from ..rails.execution_rail import ExecutionRail
from ..rails.input_rail import InputRail
from ..rails.output_rail import OutputRail
from ..rails.scope_rail import ScopeRail

logger = logging.getLogger(__name__)

# Instâncias singleton dos rails determinísticos
_input_rail = InputRail()
_scope_rail = ScopeRail()
_execution_rail = ExecutionRail()
_output_rail = OutputRail()


def build_blocked_response(text: str) -> LlmResponse:
    """Cria uma LlmResponse estandardizada do Google ADK contendo o texto de bloqueio/recusa."""
    return LlmResponse(
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(text=text)],
        )
    )


def extract_user_text_from_request(llm_request: LlmRequest) -> str:
    """Extrai a mensagem mais recente do usuário contida no LlmRequest."""
    if not llm_request or not llm_request.contents:
        return ""
    for content in reversed(llm_request.contents):
        role = getattr(content, "role", None)
        if role in ("user", None):
            parts = getattr(content, "parts", []) or []
            texts = [p.text for p in parts if hasattr(p, "text") and p.text]
            if texts:
                return "\n".join(texts)
    return ""


def extract_text_from_response(llm_response: LlmResponse) -> str:
    """Extrai o texto total gerado contido na LlmResponse."""
    if not llm_response or not llm_response.content:
        return ""
    parts = getattr(llm_response.content, "parts", []) or []
    texts = [p.text for p in parts if hasattr(p, "text") and p.text]
    return "\n".join(texts)


def guardrail_before_model_callback(
    callback_context: Any,
    llm_request: LlmRequest,
) -> Optional[LlmResponse]:
    """Callback pré-modelo para interceptação determinística de toxicidade, injeção e escopo."""
    agent_name = getattr(callback_context, "agent_name", "unknown")
    user_text = extract_user_text_from_request(llm_request)

    if not user_text:
        return None

    # 1. Input Rail: Palavras de ódio, comandos de escrita não autorizados, injeções
    input_verdict = _input_rail.inspect(user_text, agent_name=agent_name)
    if input_verdict.blocked:
        if hasattr(callback_context, "state") and isinstance(callback_context.state, dict):
            callback_context.state["guardrail_verdict"] = input_verdict.to_dict()
        return build_blocked_response(input_verdict.reason)

    # 2. Scope Rail: Controle de tópico e fuga de escopo
    scope_verdict = _scope_rail.inspect(user_text, agent_name=agent_name)
    if scope_verdict.blocked:
        if hasattr(callback_context, "state") and isinstance(callback_context.state, dict):
            callback_context.state["guardrail_verdict"] = scope_verdict.to_dict()
        return build_blocked_response(scope_verdict.reason)

    return None


def guardrail_before_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    callback_context: Any,
) -> Optional[dict[str, Any]]:
    """Callback pré-ferramenta: Bloqueio estrito de execução de escrita para agente_conhecimento."""
    agent_name = getattr(callback_context, "agent_name", "")
    if not agent_name and hasattr(callback_context, "agent"):
        agent_name = getattr(callback_context.agent, "name", "")

    tool_name = getattr(tool, "name", str(tool))
    # Fail-closed via PermissionError
    _execution_rail.enforce(agent_name=agent_name, tool_name=tool_name, tool_args=args)
    return None


def guardrail_after_model_callback(
    callback_context: Any,
    llm_response: LlmResponse,
) -> Optional[LlmResponse]:
    """Callback pós-modelo: Validação de resposta gerada e prevenção de promessas indevidas de edição."""
    agent_name = getattr(callback_context, "agent_name", "unknown")
    response_text = extract_text_from_response(llm_response)

    if not response_text:
        return None

    output_verdict = _output_rail.inspect(response_text, agent_name=agent_name)
    if output_verdict.blocked:
        if hasattr(callback_context, "state") and isinstance(callback_context.state, dict):
            callback_context.state["guardrail_verdict"] = output_verdict.to_dict()
        return build_blocked_response(output_verdict.reason or MSG_OUTPUT_VIOLATION)

    return None


def guardrail_on_model_error_callback(
    callback_context: Any,
    llm_request: LlmRequest,
    error: Exception,
) -> Optional[LlmResponse]:
    """Tratamento de exceções do modelo (incluindo bloqueios nativos de segurança do Gemini)."""
    error_str = str(error).upper()
    agent_name = getattr(callback_context, "agent_name", "unknown")

    # Verifica se a causa do erro foi bloqueio por políticas de segurança da plataforma
    is_safety_block = any(
        kw in error_str for kw in ("SAFETY", "BLOCKED", "HARM", "MODEL_ARMOR", "POLICY")
    )
    if is_safety_block:
        verdict = Verdict(
            blocked=True,
            reason=MSG_SAFETY_REFUSAL,
            category=RiskCategory.HATE_SPEECH,
            rail=RailType.PLATFORM_SAFETY,
            details={"original_error": str(error)},
        )
        log_verdict(verdict, agent_name=agent_name)
        if hasattr(callback_context, "state") and isinstance(callback_context.state, dict):
            callback_context.state["guardrail_verdict"] = verdict.to_dict()
        return build_blocked_response(MSG_SAFETY_REFUSAL)

    return None


class ADKGuardrailPlugin(BasePlugin):
    """Plugin global do Google ADK para aplicação uniforme dos Guardrails."""

    def __init__(self, name: str = "guardrails_plugin"):
        super().__init__(name=name)

    async def before_model_callback(
        self,
        *,
        callback_context: Any,
        llm_request: LlmRequest,
    ) -> Optional[LlmResponse]:
        res = guardrail_before_model_callback(callback_context, llm_request)
        if inspect.isawaitable(res):
            return await res
        return res

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: Any,
    ) -> Optional[dict[str, Any]]:
        res = guardrail_before_tool_callback(tool, tool_args, tool_context)
        if inspect.isawaitable(res):
            return await res
        return res

    async def after_model_callback(
        self,
        *,
        callback_context: Any,
        llm_response: LlmResponse,
    ) -> Optional[LlmResponse]:
        res = guardrail_after_model_callback(callback_context, llm_response)
        if inspect.isawaitable(res):
            return await res
        return res

    async def on_model_error_callback(
        self,
        *,
        callback_context: Any,
        llm_request: LlmRequest,
        error: Exception,
    ) -> Optional[LlmResponse]:
        res = guardrail_on_model_error_callback(callback_context, llm_request, error)
        if inspect.isawaitable(res):
            return await res
        return res
