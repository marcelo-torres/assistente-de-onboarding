"""Módulo de Observabilidade, Auditoria e Logs Estruturados para Guardrails."""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Optional

from .contracts import Verdict

logger = logging.getLogger("guardrails.audit")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def log_verdict(verdict: Verdict, agent_name: str = "unknown", prompt_sample: str = "") -> None:
    """Emite log estruturado em formato JSON a cada avaliação de Guardrail."""
    record = {
        "timestamp": verdict.timestamp,
        "event_type": "guardrail_evaluation",
        "agent": agent_name,
        "rail": verdict.rail.value if hasattr(verdict.rail, "value") else str(verdict.rail),
        "verdict": "BLOCKED" if verdict.blocked else "SAFE",
        "category": verdict.category.value if hasattr(verdict.category, "value") else str(verdict.category),
        "reason": verdict.reason,
        "latency_ms": round(verdict.latency_ms, 2),
        "details": verdict.details,
    }
    if prompt_sample:
        # Registra apenas os primeiros 100 caracteres para auditoria sem vazar dados sensíveis
        record["prompt_preview"] = prompt_sample[:100]

    logger.info(json.dumps(record, ensure_ascii=False))


def get_telemetry_attributes(verdict: Verdict, agent_name: str) -> dict[str, Any]:
    """Retorna atributos compatíveis com OpenTelemetry / Tracing de IA."""
    return {
        "gen_ai.guardrail.blocked": verdict.blocked,
        "gen_ai.guardrail.reason": verdict.reason,
        "gen_ai.guardrail.category": verdict.category.value if hasattr(verdict.category, "value") else str(verdict.category),
        "gen_ai.guardrail.rail": verdict.rail.value if hasattr(verdict.rail, "value") else str(verdict.rail),
        "gen_ai.guardrail.agent": agent_name,
        "gen_ai.guardrail.latency_ms": verdict.latency_ms,
    }
