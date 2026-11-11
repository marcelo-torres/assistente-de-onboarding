"""Execution Rail: Blindagem e restrição de permissões de execução de ferramentas (RBAC)."""

from __future__ import annotations

import time
from typing import Any, Optional

from ..config import ALLOWED_KNOWLEDGE_TOOLS, ALLOWED_TUTOR_TOOLS
from ..contracts import GuardrailAction, RailType, RiskCategory, Verdict
from ..observability import log_verdict


class ExecutionRail:
    """Rail de execução que garante a imutabilidade e a política de privilégio mínimo."""

    def __init__(self) -> None:
        self.rail_type = RailType.EXECUTION

    def validate_tool(
        self,
        agent_name: str,
        tool_name: str,
        tool_args: Optional[dict[str, Any]] = None,
    ) -> Verdict:
        """Valida se o agente tem autorização explícita para invocar a ferramenta solicitada.

        Args:
            agent_name: Nome do agente que está disparando a ferramenta.
            tool_name: Nome da ferramenta solicitada.
            tool_args: Argumentos passados para a ferramenta (opcional).

        Returns:
            Verdict indicando se a execução é permitida ou bloqueada.
        """
        start_time = time.perf_counter()

        # Normaliza o nome do agente caso venha com prefixos
        clean_agent_name = (agent_name or "").strip()

        # 1. Regra Estrita para agente_conhecimento: Apenas leitura permitida
        if clean_agent_name == "agente_conhecimento":
            if tool_name not in ALLOWED_KNOWLEDGE_TOOLS:
                latency = (time.perf_counter() - start_time) * 1000
                reason = (
                    f"Ação não autorizada: o agente '{clean_agent_name}' não possui "
                    f"permissão para executar a ferramenta de modificação/não permitida '{tool_name}'."
                )
                verdict = Verdict(
                    blocked=True,
                    reason=reason,
                    category=RiskCategory.UNAUTHORIZED_WRITE,
                    action=GuardrailAction.BLOCK,
                    rail=self.rail_type,
                    details={
                        "agent": clean_agent_name,
                        "tool": tool_name,
                        "allowed_tools": list(ALLOWED_KNOWLEDGE_TOOLS),
                        "args": tool_args or {},
                    },
                    latency_ms=latency,
                )
                log_verdict(verdict, clean_agent_name)
                return verdict

        # 2. Regra para agente_tutor: Apenas tools da allowlist do tutor
        elif clean_agent_name == "agente_tutor":
            if tool_name not in ALLOWED_TUTOR_TOOLS:
                latency = (time.perf_counter() - start_time) * 1000
                reason = (
                    f"Ação não autorizada: o agente '{clean_agent_name}' não possui "
                    f"permissão para executar a ferramenta '{tool_name}'."
                )
                verdict = Verdict(
                    blocked=True,
                    reason=reason,
                    category=RiskCategory.UNAUTHORIZED_WRITE,
                    action=GuardrailAction.BLOCK,
                    rail=self.rail_type,
                    details={
                        "agent": clean_agent_name,
                        "tool": tool_name,
                        "allowed_tools": list(ALLOWED_TUTOR_TOOLS),
                    },
                    latency_ms=latency,
                )
                log_verdict(verdict, clean_agent_name)
                return verdict

        # Execução autorizada
        latency = (time.perf_counter() - start_time) * 1000
        verdict = Verdict(
            blocked=False,
            category=RiskCategory.SAFE,
            action=GuardrailAction.ALLOW,
            rail=self.rail_type,
            details={"agent": clean_agent_name, "tool": tool_name},
            latency_ms=latency,
        )
        return verdict

    def enforce(
        self,
        agent_name: str,
        tool_name: str,
        tool_args: Optional[dict[str, Any]] = None,
    ) -> None:
        """Aplica Fail-Closed: lança PermissionError caso a ferramenta não seja autorizada."""
        verdict = self.validate_tool(agent_name, tool_name, tool_args)
        if verdict.blocked:
            raise PermissionError(verdict.reason)
