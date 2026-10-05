from enum import Enum
from typing import List, Optional, Dict
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class MissionType(str, Enum):
    BUSINESS = "business"
    TECHNICAL = "technical"


class MissionStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class MissionStep(BaseModel):
    step_number: int = Field(description="Número sequencial do passo (1-indexado)")
    title: str = Field(description="Título curto da etapa")
    instruction: str = Field(description="Instrução clara do que o desenvolvedor deve fazer")
    expected_action: str = Field(description="Ação prática que o dev deve realizar ou validar")
    hint: Optional[str] = Field(default="", description="Dica técnica ou de processo para apoio")
    success_criteria: Optional[str] = Field(default="", description="Critério para considerar a etapa concluída")


class Mission(BaseModel):
    id: str = Field(description="Identificador único da missão (ex: biz-01, tech-01)")
    title: str = Field(description="Título da missão")
    description: str = Field(description="Objetivo de aprendizado da missão")
    type: MissionType = Field(description="Tipo da missão: business (negócio) ou technical (técnica)")
    target_area: str = Field(default="all", description="Área alvo: backend, frontend ou all")
    compatible_stacks: List[str] = Field(default_factory=lambda: ["all"], description="Tecnologias compatíveis")
    min_experience_level: str = Field(default="junior", description="Nível mínimo recomendado")
    estimated_minutes: int = Field(default=30, description="Tempo estimado de conclusão em minutos")
    prerequisites: List[str] = Field(default_factory=list, description="Pré-requisitos necessários")
    steps: List[MissionStep] = Field(default_factory=list, description="Lista ordenada de etapas da missão")

    @property
    def total_steps(self) -> int:
        return len(self.steps)


class MissionProgress(BaseModel):
    mission_id: str
    status: MissionStatus = Field(default=MissionStatus.IN_PROGRESS)
    current_step_index: int = Field(default=0, description="Índice da etapa atual (0-indexado)")
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    step_notes: Dict[int, str] = Field(default_factory=dict, description="Anotações ou respostas do dev por etapa")

    def is_finished(self, total_steps: int) -> bool:
        return self.current_step_index >= total_steps
