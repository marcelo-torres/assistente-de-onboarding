from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from .profile import DeveloperProfile
from .mission import MissionProgress, MissionStatus


class OnboardingState(BaseModel):
    profile: Optional[DeveloperProfile] = Field(default=None, description="Perfil do desenvolvedor tutorado")
    active_mission_id: Optional[str] = Field(default=None, description="ID da missão em andamento no momento")
    mission_progress: Optional[MissionProgress] = Field(default=None, description="Progresso na missão ativa")
    completed_missions: List[str] = Field(default_factory=list, description="Lista de IDs de missões concluídas com sucesso")
    current_intent: Optional[str] = Field(default="iniciar", description="Intenção atual detectada no diálogo")
    conversation_round_count: int = Field(default=0, description="Contador de interações/rounds no onboarding")

    def has_profile(self) -> bool:
        return self.profile is not None

    def has_active_mission(self) -> bool:
        return (
            self.active_mission_id is not None
            and self.mission_progress is not None
            and self.mission_progress.status == MissionStatus.IN_PROGRESS
        )
