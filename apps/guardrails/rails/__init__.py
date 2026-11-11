"""Pacote contendo os Rails individuais da arquitetura."""

from .execution_rail import ExecutionRail
from .input_rail import InputRail
from .output_rail import OutputRail
from .scope_rail import ScopeRail

__all__ = ["InputRail", "ScopeRail", "ExecutionRail", "OutputRail"]
