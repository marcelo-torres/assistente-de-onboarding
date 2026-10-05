"""Entrypoint nativo para a CLI do Google ADK (ex: adk run . ou adk web .)."""

import os
import sys

# Garante que a raiz do projeto esteja no sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.tutor_agent import tutor_agent

# Exporta root_agent conforme a convenção do Google ADK
root_agent = tutor_agent
agent = tutor_agent

__all__ = ["root_agent", "agent"]
