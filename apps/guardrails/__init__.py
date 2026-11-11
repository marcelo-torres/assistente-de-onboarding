"""Camada de Guardrails para os Agentes de Onboarding."""

from .config import (
    ALLOWED_KNOWLEDGE_TOOLS,
    ALLOWED_TUTOR_TOOLS,
    BV_GUARD_MODE,
    get_safety_settings,
)
from .contracts import GuardrailAction, RailType, RiskCategory, Verdict
from .plugins import (
    ADKGuardrailPlugin,
    build_blocked_response,
    guardrail_after_model_callback,
    guardrail_before_model_callback,
    guardrail_before_tool_callback,
    guardrail_on_model_error_callback,
)
from .rails import ExecutionRail, InputRail, OutputRail, ScopeRail

__all__ = [
    "Verdict",
    "RiskCategory",
    "GuardrailAction",
    "RailType",
    "InputRail",
    "ScopeRail",
    "ExecutionRail",
    "OutputRail",
    "ADKGuardrailPlugin",
    "guardrail_before_model_callback",
    "guardrail_before_tool_callback",
    "guardrail_after_model_callback",
    "guardrail_on_model_error_callback",
    "build_blocked_response",
    "get_safety_settings",
    "ALLOWED_KNOWLEDGE_TOOLS",
    "ALLOWED_TUTOR_TOOLS",
    "BV_GUARD_MODE",
]
