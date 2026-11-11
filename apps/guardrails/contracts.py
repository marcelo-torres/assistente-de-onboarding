"""Contratos e tipos de dados da camada de Guardrails."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class RiskCategory(str, Enum):
    """Categorias de risco avaliadas pelos Guardrails."""
    SAFE = "safe"
    HATE_SPEECH = "hate_speech"
    HARASSMENT = "harassment"
    DANGEROUS_CONTENT = "dangerous_content"
    SEXUALLY_EXPLICIT = "sexually_explicit"
    PROMPT_INJECTION = "prompt_injection"
    UNAUTHORIZED_WRITE = "unauthorized_write"
    OUT_OF_SCOPE = "out_of_scope"
    INTEGRITY_VIOLATION = "integrity_violation"


class GuardrailAction(str, Enum):
    """Ação recomendada pelo Guardrail."""
    ALLOW = "allow"
    BLOCK = "block"
    DEVIATE = "deviate"
    FLAG = "flag"


class RailType(str, Enum):
    """Identificador do rail de interceptação."""
    INPUT = "input_rail"
    DIALOG = "dialog_rail"
    SCOPE = "scope_rail"
    EXECUTION = "execution_rail"
    OUTPUT = "output_rail"
    PLATFORM_SAFETY = "platform_safety"


@dataclass
class Verdict:
    """Veredito emitido por um rail de segurança."""
    blocked: bool
    reason: str = ""
    category: RiskCategory = RiskCategory.SAFE
    action: GuardrailAction = GuardrailAction.ALLOW
    rail: Optional[RailType] = None
    details: dict[str, Any] = field(default_factory=dict)
    latency_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Converte o veredito em dicionário estruturado para logs/auditoria."""
        return {
            "timestamp": self.timestamp,
            "blocked": self.blocked,
            "reason": self.reason,
            "category": self.category.value if isinstance(self.category, RiskCategory) else str(self.category),
            "action": self.action.value if isinstance(self.action, GuardrailAction) else str(self.action),
            "rail": self.rail.value if isinstance(self.rail, RailType) else str(self.rail) if self.rail else None,
            "details": self.details,
            "latency_ms": round(self.latency_ms, 2),
        }
