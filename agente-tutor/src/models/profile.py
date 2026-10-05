from enum import Enum
from typing import Optional, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class AreaEnum(str, Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    FULLSTACK = "fullstack"
    OTHER = "other"


class ExperienceLevelEnum(str, Enum):
    JUNIOR = "junior"
    PLENO = "pleno"
    SENIOR = "senior"


class DeveloperProfile(BaseModel):
    developer_name: Optional[str] = Field(default="Novo Desenvolvedor", description="Nome ou identificador do dev")
    area: AreaEnum = Field(description="Área de atuação (backend, frontend, fullstack)")
    primary_stack: List[str] = Field(default_factory=list, description="Lista de tecnologias/linguagens principais (ex: java, angular, python)")
    experience_level: ExperienceLevelEnum = Field(default=ExperienceLevelEnum.JUNIOR, description="Nível de senioridade")
    goals: Optional[str] = Field(default="", description="Objetivos do dev no onboarding")
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Data de registro")

    def is_compatible_with(self, target_area: str, compatible_stacks: List[str]) -> bool:
        """Verifica se o perfil é compatível com os requisitos de uma missão."""
        # Verificação de área
        area_match = (
            target_area == "all"
            or self.area.value == "fullstack"
            or self.area.value == target_area
        )
        if not area_match:
            return False

        # Verificação de stack
        if "all" in compatible_stacks:
            return True

        user_stacks_lower = [s.lower() for s in self.primary_stack]
        for stack in compatible_stacks:
            if stack.lower() in user_stacks_lower:
                return True

        # Se não houver stack informada mas a área combinou, ainda é compatível
        return len(self.primary_stack) == 0
