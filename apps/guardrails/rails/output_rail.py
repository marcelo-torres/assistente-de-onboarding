"""Output Rail: Sanitização e validação de integridade da resposta gerada pelo LLM."""

from __future__ import annotations

import re
import time
from typing import Optional

from ..config import HATE_AND_TOXIC_PATTERNS, MSG_OUTPUT_VIOLATION
from ..contracts import GuardrailAction, RailType, RiskCategory, Verdict
from ..observability import log_verdict

# Expressões em que o modelo promete ou afirma falsamente ter modificado o sistema/arquivos
FALSE_MUTATION_PROMISES = [
    re.compile(r"\b(editei\s+(o\s+)?arquivo|gravei\s+(no\s+)?(banco|arquivo|base)|apaguei\s+(a\s+)?base|"
               r"modifiquei\s+os\s+dados\s+do\s+sistema|excluí\s+o\s+registro|salvei\s+no\s+disco)\b", re.IGNORECASE),
]


class OutputRail:
    """Rail de saída para verificação residual de toxicidade e garantia de imutabilidade."""

    def __init__(self) -> None:
        self.rail_type = RailType.OUTPUT

    def inspect(self, text: str, agent_name: Optional[str] = None) -> Verdict:
        """Verifica a resposta produzida pelo modelo antes de entregá-la ao usuário/agente upstream.

        Args:
            text: Texto da resposta gerada pelo modelo.
            agent_name: Nome do agente que gerou a resposta.

        Returns:
            Verdict indicando conformidade ou violação de integridade/segurança.
        """
        start_time = time.perf_counter()

        if not text or not text.strip():
            return Verdict(
                blocked=False,
                category=RiskCategory.SAFE,
                action=GuardrailAction.ALLOW,
                rail=self.rail_type,
            )

        # 1. Verificação residual de Palavras de Ódio / Toxicidade
        for pattern in HATE_AND_TOXIC_PATTERNS:
            match = pattern.search(text)
            if match:
                latency = (time.perf_counter() - start_time) * 1000
                verdict = Verdict(
                    blocked=True,
                    reason=MSG_OUTPUT_VIOLATION,
                    category=RiskCategory.HATE_SPEECH,
                    action=GuardrailAction.BLOCK,
                    rail=self.rail_type,
                    details={"matched_term": match.group(0)},
                    latency_ms=latency,
                )
                log_verdict(verdict, agent_name or "unknown", prompt_sample=text)
                return verdict

        # 2. Verificação de Promessas Indevidas de Mutação no agente consultivo
        if agent_name == "agente_conhecimento":
            for pattern in FALSE_MUTATION_PROMISES:
                match = pattern.search(text)
                if match:
                    latency = (time.perf_counter() - start_time) * 1000
                    verdict = Verdict(
                        blocked=True,
                        reason="O modelo gerou afirmação indevida de modificação de estado em modo somente-leitura. Violação das políticas de integridade do sistema.",
                        category=RiskCategory.INTEGRITY_VIOLATION,
                        action=GuardrailAction.BLOCK,
                        rail=self.rail_type,
                        details={"matched_promise": match.group(0)},
                        latency_ms=latency,
                    )
                    log_verdict(verdict, agent_name or "unknown", prompt_sample=text)
                    return verdict

        # Resposta Segura
        latency = (time.perf_counter() - start_time) * 1000
        return Verdict(
            blocked=False,
            category=RiskCategory.SAFE,
            action=GuardrailAction.ALLOW,
            rail=self.rail_type,
            latency_ms=latency,
        )
