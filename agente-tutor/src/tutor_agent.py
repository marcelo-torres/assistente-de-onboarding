"""Módulo de instanciação do Agente Tutor no Google ADK."""

from google.adk.agents import Agent
from config.settings import settings
from src.prompts import TUTOR_SYSTEM_INSTRUCTION
from src.tools.profile_tools import register_developer_profile, get_developer_profile
from src.tools.mission_tools import (
    list_available_missions,
    start_mission,
    get_current_mission_status,
    advance_mission_step,
    complete_current_mission
)
from src.tools.knowledge_tools import ask_knowledge_agent


def create_tutor_agent() -> Agent:
    """Cria e configura o Agente Tutor com todas as suas ferramentas e instruções."""
    tools = [
        register_developer_profile,
        get_developer_profile,
        list_available_missions,
        start_mission,
        get_current_mission_status,
        advance_mission_step,
        complete_current_mission,
        ask_knowledge_agent
    ]

    agent = Agent(
        name="agente_tutor",
        description="Agente Tutor de Onboarding para Desenvolvedores de Software",
        model=settings.tutor_model,
        instruction=TUTOR_SYSTEM_INSTRUCTION,
        tools=tools
    )

    return agent


# Instância raiz do agente para uso direto
tutor_agent = create_tutor_agent()
