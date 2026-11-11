"""Scope Rail: Verificação de escopo, contexto e prevenção de fuga temática."""

from __future__ import annotations

import re
import time
from typing import Optional

from ..config import BV_GUARD_MODE, SCOPE_CONFIG
from ..contracts import GuardrailAction, RailType, RiskCategory, Verdict
from ..observability import log_verdict


class ScopeRail:
    """Rail de controle de tópico e escopo com avaliação em duas etapas."""

    def __init__(self) -> None:
        self.rail_type = RailType.SCOPE

    def inspect(self, text: str, agent_name: str) -> Verdict:
        """Avalia se a mensagem do usuário está dentro do escopo autorizado do agente.

        Args:
            text: Pergunta ou mensagem do usuário.
            agent_name: 'agente_conhecimento' ou 'agente_tutor'.

        Returns:
            Verdict com ALLOW caso esteja em escopo ou DEVIATE caso fora de escopo.
        """
        start_time = time.perf_counter()
        agent_key = (agent_name or "").strip()

        # Se o agente não tiver configuração específica de escopo, libera
        config = SCOPE_CONFIG.get(agent_key)
        if not config or not text or not text.strip():
            return Verdict(
                blocked=False,
                category=RiskCategory.SAFE,
                action=GuardrailAction.ALLOW,
                rail=self.rail_type,
            )

        lower_text = text.lower()

        # Etapa 1: Detecção de Marcadores Óbvios Fora de Escopo
        out_of_scope_indicators = config.get("out_of_scope_indicators", [])
        matched_out_of_scope = [
            ind for ind in out_of_scope_indicators
            if re.search(rf"\b{re.escape(ind)}\b", lower_text)
        ]

        # Etapa 2: Presença de Termos do Domínio Autorizado
        allowed_keywords = config.get("allowed_keywords", [])
        matched_in_scope = [
            kw for kw in allowed_keywords
            if re.search(rf"\b{re.escape(kw)}\b", lower_text)
        ]

        # Se houver marcador evidente fora de escopo e NENHUM termo de domínio
        if matched_out_of_scope and not matched_in_scope:
            latency = (time.perf_counter() - start_time) * 1000
            verdict = Verdict(
                blocked=True,
                reason=config.get("refusal_message", "Mensagem fora do escopo de atuação do agente."),
                category=RiskCategory.OUT_OF_SCOPE,
                action=GuardrailAction.DEVIATE,
                rail=self.rail_type,
                details={
                    "agent": agent_key,
                    "matched_out_of_scope": matched_out_of_scope,
                    "in_scope_count": 0,
                },
                latency_ms=latency,
            )
            log_verdict(verdict, agent_key, prompt_sample=text)
            return verdict

        # Se não há termos de domínio mas a pergunta é curta e genérica (ex: saudações como "olá", "bom dia")
        # Devemos permitir para manter a conversa fluida (Fail-open para saudações e ambiguidades)
        latency = (time.perf_counter() - start_time) * 1000
        verdict = Verdict(
            blocked=False,
            category=RiskCategory.SAFE,
            action=GuardrailAction.ALLOW,
            rail=self.rail_type,
            details={
                "agent": agent_key,
                "matched_in_scope": matched_in_scope,
            },
            latency_ms=latency,
        )
        return verdict
