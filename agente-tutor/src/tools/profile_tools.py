from typing import Optional, Dict, Any
from google.adk.tools import ToolContext
from src.models.profile import DeveloperProfile, AreaEnum, ExperienceLevelEnum

# Fallback local para testes sem contexto de sessão ativo
_LOCAL_TEST_STATE: Dict[str, Any] = {}


def register_developer_profile(
    developer_name: str,
    area: str,
    primary_stack: str,
    experience_level: str = "junior",
    goals: str = "",
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """Registra o perfil do novo desenvolvedor durante a entrevista de onboarding.

    Use esta ferramenta para salvar as informações de perfil do dev (backend/frontend, stack tecnológica,
    nível de senioridade e objetivos) no estado da sessão de onboarding.

    Args:
        developer_name: Nome do desenvolvedor (ex: 'Lucas' ou 'Mariana').
        area: Área principal de atuação. Opções: 'backend', 'frontend', 'fullstack'.
        primary_stack: Tecnologias principais separadas por vírgula (ex: 'java, spring, postgres' ou 'angular, typescript').
        experience_level: Nível de experiência. Opções: 'junior', 'pleno', 'senior'.
        goals: O que o desenvolvedor espera aprender ou focar no onboarding.
        tool_context: Contexto de sessão injetado pelo Google ADK.

    Returns:
        Dicionário com o status de sucesso e os dados do perfil cadastrado.
    """
    # Normalizar área
    area_clean = area.strip().lower()
    area_enum = AreaEnum.OTHER
    if "back" in area_clean:
        area_enum = AreaEnum.BACKEND
    elif "front" in area_clean:
        area_enum = AreaEnum.FRONTEND
    elif "full" in area_clean:
        area_enum = AreaEnum.FULLSTACK

    # Normalizar nível
    lvl_clean = experience_level.strip().lower()
    lvl_enum = ExperienceLevelEnum.JUNIOR
    if "pleno" in lvl_clean or "mid" in lvl_clean:
        lvl_enum = ExperienceLevelEnum.PLENO
    elif "senior" in lvl_clean or "sênior" in lvl_clean:
        lvl_enum = ExperienceLevelEnum.SENIOR

    # Normalizar stack
    stacks = [s.strip().lower() for s in primary_stack.split(",") if s.strip()]

    profile = DeveloperProfile(
        developer_name=developer_name,
        area=area_enum,
        primary_stack=stacks,
        experience_level=lvl_enum,
        goals=goals
    )

    state_dict = profile.model_dump(mode="json")

    if tool_context and hasattr(tool_context, "state") and tool_context.state is not None:
        tool_context.state["developer_profile"] = state_dict
        tool_context.state["current_intent"] = "onboarding"
    else:
        _LOCAL_TEST_STATE["developer_profile"] = state_dict
        _LOCAL_TEST_STATE["current_intent"] = "onboarding"

    return {
        "status": "success",
        "message": f"Perfil do desenvolvedor {developer_name} registrado com sucesso!",
        "profile": state_dict
    }


def get_developer_profile(tool_context: Optional[ToolContext] = None) -> Dict[str, Any]:
    """Retorna os dados do perfil do desenvolvedor registrado na sessão atual.

    Use esta ferramenta para verificar se o desenvolvedor já foi entrevistado e qual é o seu perfil.

    Args:
        tool_context: Contexto de sessão injetado pelo Google ADK.

    Returns:
        Perfil registrado ou indicação de que o perfil ainda não existe.
    """
    profile_data = None
    if tool_context and hasattr(tool_context, "state") and tool_context.state is not None:
        profile_data = tool_context.state.get("developer_profile")
    else:
        profile_data = _LOCAL_TEST_STATE.get("developer_profile")

    if not profile_data:
        return {
            "status": "not_found",
            "message": "Nenhum perfil de desenvolvedor cadastrado na sessão. É necessário entrevistar o usuário primeiro."
        }

    return {
        "status": "success",
        "profile": profile_data
    }
