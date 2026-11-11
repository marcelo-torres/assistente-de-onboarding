"""Testes de integração dos callbacks e plugins do Google ADK com a Camada de Guardrails."""

import asyncio
from unittest.mock import MagicMock
import pytest
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

from apps.guardrails.config import (
    MSG_SAFETY_REFUSAL,
    MSG_WRITE_BLOCKED_KNOWLEDGE,
)
from apps.guardrails.plugins.adk_plugin import (
    ADKGuardrailPlugin,
    extract_text_from_response,
    extract_user_text_from_request,
    guardrail_after_model_callback,
    guardrail_before_model_callback,
    guardrail_before_tool_callback,
    guardrail_on_model_error_callback,
)


class MockContext:
    def __init__(self, agent_name: str = "agente_conhecimento"):
        self.agent_name = agent_name
        self.state = {}


class MockTool:
    def __init__(self, name: str):
        self.name = name


def build_mock_request(user_text: str) -> LlmRequest:
    content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_text)],
    )
    return LlmRequest(contents=[content])


def test_before_model_callback_bloqueia_odio_e_retorna_llm_response():
    """Valida o veto pré-modelo de ódio (economia de tokens e short-circuit)."""
    ctx = MockContext(agent_name="agente_conhecimento")
    req = build_mock_request("Seu macaco imundo!")

    response = guardrail_before_model_callback(ctx, req)
    assert response is not None, "Deveria retornar uma LlmResponse com o veto"
    assert isinstance(response, LlmResponse)

    response_text = extract_text_from_response(response)
    assert MSG_SAFETY_REFUSAL in response_text
    assert "guardrail_verdict" in ctx.state
    assert ctx.state["guardrail_verdict"]["blocked"] is True


def test_before_model_callback_bloqueia_escrita_no_agente_conhecimento():
    """Valida que comandos imperativos de alteração de dados são barrados antes do modelo."""
    ctx = MockContext(agent_name="agente_conhecimento")
    req = build_mock_request("Edite o arquivo de chunking agora!")

    response = guardrail_before_model_callback(ctx, req)
    assert response is not None
    response_text = extract_text_from_response(response)
    assert MSG_WRITE_BLOCKED_KNOWLEDGE in response_text
    assert ctx.state["guardrail_verdict"]["category"] == "unauthorized_write"


def test_before_model_callback_permite_pergunta_limpa():
    """Valida que requisições limpas retornam None, permitindo que o LLM execute normalmente."""
    ctx = MockContext(agent_name="agente_conhecimento")
    req = build_mock_request("Como funciona a busca densa com embeddings no Chroma?")

    response = guardrail_before_model_callback(ctx, req)
    assert response is None, "Requisição legítima não deve ser interceptada com veto estático"


def test_before_tool_callback_valida_allowlist():
    """Valida que tools permitidas passam e tools de mutação geram PermissionError."""
    ctx = MockContext(agent_name="agente_conhecimento")

    # Tool de leitura permitida
    tool_valida = MockTool("buscar_base_conhecimento")
    res = guardrail_before_tool_callback(tool_valida, {"pergunta": "RAG"}, ctx)
    assert res is None  # Permite execução

    # Tool de gravação bloqueada
    tool_invalida = MockTool("apagar_colecao")
    with pytest.raises(PermissionError) as exc_info:
        guardrail_before_tool_callback(tool_invalida, {"target": "all"}, ctx)
    assert "Ação não autorizada" in str(exc_info.value)


def test_after_model_callback_retem_promessa_de_modificacao():
    """Valida que se o modelo tentar afirmar que alterou a base, a saída é sanitizada."""
    ctx = MockContext(agent_name="agente_conhecimento")
    llm_resp = LlmResponse(
        content=types.Content(
            role="model",
            parts=[types.Part.from_text(text="Com certeza, editei o arquivo com sucesso!")],
        )
    )
    sanitized = guardrail_after_model_callback(ctx, llm_resp)
    assert sanitized is not None
    text = extract_text_from_response(sanitized)
    assert "políticas de integridade" in text or "violação" in text.lower()


def test_on_model_error_callback_trata_bloqueio_nativo_gemini():
    """Valida tratamento gracioso quando a API do Gemini aciona o filtro de Safety nativo."""
    ctx = MockContext(agent_name="agente_conhecimento")
    req = build_mock_request("pergunta teste")
    error = RuntimeError("Google API Error: Content was blocked due to SAFETY policy violation.")

    recovered_response = guardrail_on_model_error_callback(ctx, req, error)
    assert recovered_response is not None
    text = extract_text_from_response(recovered_response)
    assert MSG_SAFETY_REFUSAL in text


def test_plugin_global_do_adk():
    """Valida a execução assíncrona do plugin global BasePlugin."""
    plugin = ADKGuardrailPlugin()
    ctx = MockContext(agent_name="agente_conhecimento")
    req = build_mock_request("Seu lixo inútil!")

    resp = asyncio.run(plugin.before_model_callback(callback_context=ctx, llm_request=req))
    assert resp is not None
    assert MSG_SAFETY_REFUSAL in extract_text_from_response(resp)
