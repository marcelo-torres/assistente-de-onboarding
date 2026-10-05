from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from google.adk.tools import ToolContext
from src.services.mission_service import mission_service
from src.models.mission import MissionType, MissionStatus, MissionProgress
from src.models.profile import DeveloperProfile
from src.tools.profile_tools import _LOCAL_TEST_STATE


def _get_state_dict(tool_context: Optional[ToolContext]) -> Dict[str, Any]:
    if tool_context and hasattr(tool_context, "state") and tool_context.state is not None:
        return tool_context.state  # type: ignore
    return _LOCAL_TEST_STATE


def list_available_missions(
    filter_type: Optional[str] = None,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """Lista as missões de onboarding disponíveis e recomendadas para o desenvolvedor.

    Utilize esta ferramenta para apresentar opções de missões (de negócio ou técnicas)
    compatíveis com a área e stack do desenvolvedor.

    Args:
        filter_type: Opcional. Filtrar por 'business' (negócio) ou 'technical' (técnica). Deixe vazio para listar ambas.
        tool_context: Contexto de sessão injetado pelo Google ADK.

    Returns:
        Lista de missões disponíveis com ID, título, tipo, tempo estimado e descrição.
    """
    state = _get_state_dict(tool_context)
    profile_data = state.get("developer_profile")
    completed_missions = state.get("completed_missions", [])

    profile = DeveloperProfile.model_validate(profile_data) if profile_data else None

    mission_type_enum = None
    if filter_type:
        f_clean = filter_type.strip().lower()
        if "biz" in f_clean or "neg" in f_clean or "bus" in f_clean:
            mission_type_enum = MissionType.BUSINESS
        elif "tech" in f_clean or "tec" in f_clean:
            mission_type_enum = MissionType.TECHNICAL

    missions = mission_service.filter_missions(
        profile=profile,
        mission_type=mission_type_enum,
        exclude_completed=completed_missions
    )

    missions_summary = [
        {
            "id": m.id,
            "title": m.title,
            "type": m.type.value,
            "description": m.description,
            "estimated_minutes": m.estimated_minutes,
            "total_steps": m.total_steps,
            "prerequisites": m.prerequisites
        }
        for m in missions
    ]

    return {
        "status": "success",
        "total_available": len(missions_summary),
        "missions": missions_summary
    }


def start_mission(
    mission_id: str,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """Inicia uma missão de onboarding para o desenvolvedor e apresenta a primeira etapa.

    Args:
        mission_id: O identificador único da missão escolhida (ex: 'biz-01' ou 'tech-01').
        tool_context: Contexto de sessão injetado pelo Google ADK.

    Returns:
        Detalhes completos da missão iniciada e instruções do Passo 1.
    """
    mission = mission_service.get_mission(mission_id)
    if not mission:
        return {
            "status": "error",
            "message": f"Missão com ID '{mission_id}' não encontrada no catálogo."
        }

    state = _get_state_dict(tool_context)

    progress = MissionProgress(
        mission_id=mission.id,
        status=MissionStatus.IN_PROGRESS,
        current_step_index=0,
        started_at=datetime.now(timezone.utc)
    )

    state["active_mission_id"] = mission.id
    state["mission_progress"] = progress.model_dump(mode="json")

    first_step = mission.steps[0] if mission.steps else None

    return {
        "status": "success",
        "message": f"Missão '{mission.title}' iniciada com sucesso!",
        "mission_id": mission.id,
        "mission_title": mission.title,
        "mission_type": mission.type.value,
        "total_steps": mission.total_steps,
        "current_step": {
            "step_number": 1,
            "total_steps": mission.total_steps,
            "title": first_step.title if first_step else "Sem etapas",
            "instruction": first_step.instruction if first_step else "",
            "expected_action": first_step.expected_action if first_step else "",
            "hint": first_step.hint if first_step else ""
        }
    }


def get_current_mission_status(tool_context: Optional[ToolContext] = None) -> Dict[str, Any]:
    """Retorna o status da missão em andamento e os detalhes da etapa atual.

    Use esta ferramenta para verificar em qual passo da missão o desenvolvedor está e quais são as instruções.

    Args:
        tool_context: Contexto de sessão injetado pelo Google ADK.

    Returns:
        Dados da missão ativa e do passo atual, ou not_found se não houver missão em curso.
    """
    state = _get_state_dict(tool_context)
    active_id = state.get("active_mission_id")
    progress_data = state.get("mission_progress")

    if not active_id or not progress_data:
        return {
            "status": "not_found",
            "message": "Nenhuma missão ativa no momento. O desenvolvedor pode escolher uma nova missão."
        }

    mission = mission_service.get_mission(active_id)
    if not mission:
        return {"status": "error", "message": "Missão ativa não localizada no catálogo."}

    progress = MissionProgress.model_validate(progress_data)
    step_idx = progress.current_step_index

    if step_idx < len(mission.steps):
        step = mission.steps[step_idx]
        return {
            "status": "in_progress",
            "mission_id": mission.id,
            "mission_title": mission.title,
            "step_number": step.step_number,
            "total_steps": mission.total_steps,
            "step_title": step.title,
            "instruction": step.instruction,
            "expected_action": step.expected_action,
            "hint": step.hint
        }
    else:
        return {
            "status": "ready_to_complete",
            "mission_id": mission.id,
            "message": "Todas as etapas da missão foram concluídas."
        }


def advance_mission_step(
    step_notes: str = "",
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """Avança a missão para a próxima etapa ou finaliza a missão se for o último passo.

    Chame esta ferramenta quando o desenvolvedor confirmar que concluiu o passo atual da missão.

    Args:
        step_notes: Breve resumo ou resposta fornecida pelo dev sobre a ação realizada no passo.
        tool_context: Contexto de sessão injetado pelo Google ADK.

    Returns:
        Instruções do próximo passo ou mensagem de parabéns pela conclusão da missão.
    """
    state = _get_state_dict(tool_context)
    active_id = state.get("active_mission_id")
    progress_data = state.get("mission_progress")

    if not active_id or not progress_data:
        return {
            "status": "error",
            "message": "Não há missão ativa para avançar."
        }

    mission = mission_service.get_mission(active_id)
    if not mission:
        return {"status": "error", "message": "Missão ativa não encontrada."}

    progress = MissionProgress.model_validate(progress_data)
    current_idx = progress.current_step_index

    if step_notes:
        progress.step_notes[current_idx] = step_notes

    next_idx = current_idx + 1
    progress.current_step_index = next_idx

    # Se ainda restam passos
    if next_idx < len(mission.steps):
        state["mission_progress"] = progress.model_dump(mode="json")
        next_step = mission.steps[next_idx]
        return {
            "status": "step_advanced",
            "message": f"Excelente! Etapa {current_idx + 1} concluída. Avançando para a etapa {next_idx + 1}.",
            "mission_id": mission.id,
            "mission_title": mission.title,
            "next_step": {
                "step_number": next_step.step_number,
                "total_steps": mission.total_steps,
                "title": next_step.title,
                "instruction": next_step.instruction,
                "expected_action": next_step.expected_action,
                "hint": next_step.hint
            }
        }
    else:
        # Missão concluída com sucesso
        progress.status = MissionStatus.COMPLETED
        progress.completed_at = datetime.now(timezone.utc)

        completed_list = state.get("completed_missions", [])
        if mission.id not in completed_list:
            completed_list.append(mission.id)
        state["completed_missions"] = completed_list

        state["active_mission_id"] = None
        state["mission_progress"] = None

        return {
            "status": "mission_completed",
            "message": f"🎉 Parabéns! Você concluiu com sucesso todas as etapas da missão '{mission.title}'!",
            "completed_mission_id": mission.id,
            "total_completed_missions": len(completed_list)
        }


def complete_current_mission(tool_context: Optional[ToolContext] = None) -> Dict[str, Any]:
    """Finaliza explicitamente a missão ativa no estado da sessão."""
    return advance_mission_step(step_notes="Concluída manualmente", tool_context=tool_context)
