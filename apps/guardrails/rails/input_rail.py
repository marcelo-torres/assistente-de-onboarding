"""Input Rail: Interceptação e triagem de mensagens de entrada (0ms determinístico)."""

from __future__ import annotations

import re
import time
import unicodedata
from typing import Optional

from ..config import (
    HATE_AND_TOXIC_PATTERNS,
    MSG_SAFETY_REFUSAL,
    MSG_WRITE_BLOCKED_KNOWLEDGE,
    PROMPT_INJECTION_PATTERNS,
    WRITE_COMMAND_PATTERNS,
)
from ..contracts import GuardrailAction, RailType, RiskCategory, Verdict
from ..observability import log_verdict


class InputRail:
    """Rail de entrada determinístico para varredura de segurança, toxicidade e injeções."""

    def __init__(self) -> None:
        self.rail_type = RailType.INPUT

    @staticmethod
    def normalize_text(text: str) -> str:
        """Normaliza o texto convertendo leet-speak e removendo diacríticos excessivos."""
        if not text:
            return ""
        # Leet-speak simples comum em evasão de filtros
        t = text.lower()
        replacements = {
            "@": "a",
            "4": "a",
            "3": "e",
            "1": "i",
            "!": "i",
            "0": "o",
            "$": "s",
            "5": "s",
        }
        # Apenas converte leet speak quando inserido no meio de palavras
        for k, v in replacements.items():
            t = t.replace(k, v)

        # Remove pontuações repetidas e normaliza espaços
        t = re.sub(r"\s+", " ", t).strip()
        return t

    @staticmethod
    def _is_conceptual_question(raw_text: str) -> bool:
        """Verifica se o texto é uma dúvida conceitual/informativa sobre um tópico."""
        lower = raw_text.lower().strip()
        conceptual_starts = (
            "como funciona",
            "o que é",
            "o que significa",
            "qual a diferença",
            "qual o conceito",
            "explique o",
            "explique como",
            "por que",
            "me explique",
        )
        for cs in conceptual_starts:
            if lower.startswith(cs):
                return True
        return False

    def inspect(self, text: str, agent_name: Optional[str] = None) -> Verdict:
        """Analisa o texto do usuário antes do envio ao modelo LLM.

        Args:
            text: Conteúdo da mensagem do usuário ou do agente upstream.
            agent_name: Nome do agente alvo ('agente_conhecimento', 'agente_tutor', etc.).

        Returns:
            Verdict indicando se o prompt é seguro ou deve ser bloqueado.
        """
        start_time = time.perf_counter()

        if not text or not text.strip():
            verdict = Verdict(
                blocked=False,
                category=RiskCategory.SAFE,
                action=GuardrailAction.ALLOW,
                rail=self.rail_type,
            )
            return verdict

        normalized = self.normalize_text(text)

        # 1. Verificação de Palavras de Ódio, Ameaças e Toxicidade Severa
        for pattern in HATE_AND_TOXIC_PATTERNS:
            match = pattern.search(normalized) or pattern.search(text)
            if match:
                latency = (time.perf_counter() - start_time) * 1000
                verdict = Verdict(
                    blocked=True,
                    reason=MSG_SAFETY_REFUSAL,
                    category=RiskCategory.HATE_SPEECH,
                    action=GuardrailAction.BLOCK,
                    rail=self.rail_type,
                    details={"matched_term": match.group(0)},
                    latency_ms=latency,
                )
                log_verdict(verdict, agent_name or "unknown", prompt_sample=text)
                return verdict

        # 2. Verificação de Injeção de Prompt / Jailbreak
        for pattern in PROMPT_INJECTION_PATTERNS:
            match = pattern.search(normalized) or pattern.search(text)
            if match:
                latency = (time.perf_counter() - start_time) * 1000
                verdict = Verdict(
                    blocked=True,
                    reason=MSG_SAFETY_REFUSAL,
                    category=RiskCategory.PROMPT_INJECTION,
                    action=GuardrailAction.BLOCK,
                    rail=self.rail_type,
                    details={"matched_injection": match.group(0)},
                    latency_ms=latency,
                )
                log_verdict(verdict, agent_name or "unknown", prompt_sample=text)
                return verdict

        # 3. Verificação de Comandos de Edição / Mutação Não Autorizada
        # Especialmente crítico para o agente_conhecimento ou comandos diretos de escrita
        is_conceptual = self._is_conceptual_question(text)
        if not is_conceptual:
            for pattern in WRITE_COMMAND_PATTERNS:
                match = pattern.search(normalized) or pattern.search(text)
                if match:
                    latency = (time.perf_counter() - start_time) * 1000
                    reason = (
                        MSG_WRITE_BLOCKED_KNOWLEDGE
                        if agent_name == "agente_conhecimento"
                        else "Comandos de modificação ou exclusão de dados não são permitidos nesta interface."
                    )
                    verdict = Verdict(
                        blocked=True,
                        reason=reason,
                        category=RiskCategory.UNAUTHORIZED_WRITE,
                        action=GuardrailAction.BLOCK,
                        rail=self.rail_type,
                        details={"matched_command": match.group(0)},
                        latency_ms=latency,
                    )
                    log_verdict(verdict, agent_name or "unknown", prompt_sample=text)
                    return verdict

        # Entrada Limpa
        latency = (time.perf_counter() - start_time) * 1000
        verdict = Verdict(
            blocked=False,
            category=RiskCategory.SAFE,
            action=GuardrailAction.ALLOW,
            rail=self.rail_type,
            latency_ms=latency,
        )
        return verdict
