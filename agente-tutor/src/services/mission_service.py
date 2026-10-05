import json
from pathlib import Path
from typing import List, Optional, Dict
from config.settings import settings
from src.models.mission import Mission, MissionStep, MissionType
from src.models.profile import DeveloperProfile


class MissionService:
    """Serviço responsável por carregar e filtrar missões do Guia de Onboarding."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or settings.data_dir
        self._missions: Dict[str, Mission] = {}
        self.load_missions()

    def load_missions(self) -> None:
        """Carrega todas as missões técnicas e de negócio dos arquivos de dados."""
        self._missions.clear()

        # Arquivos para carregar
        mission_files = [
            self.data_dir / "business_missions.json",
            self.data_dir / "technical_missions.json",
        ]

        for file_path in mission_files:
            if not file_path.exists():
                continue
            with open(file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                for item in raw_data:
                    mission = Mission.model_validate(item)
                    self._missions[mission.id] = mission

    def get_mission(self, mission_id: str) -> Optional[Mission]:
        """Recupera uma missão pelo ID."""
        return self._missions.get(mission_id)

    def list_all_missions(self) -> List[Mission]:
        """Retorna todas as missões cadastradas."""
        return list(self._missions.values())

    def filter_missions(
        self,
        profile: Optional[DeveloperProfile] = None,
        mission_type: Optional[MissionType] = None,
        exclude_completed: Optional[List[str]] = None
    ) -> List[Mission]:
        """Filtra missões compatíveis com o perfil do desenvolvedor."""
        completed_set = set(exclude_completed or [])
        compatible: List[Mission] = []

        for mission in self._missions.values():
            if mission.id in completed_set:
                continue

            if mission_type and mission.type != mission_type:
                continue

            if profile:
                if not profile.is_compatible_with(mission.target_area, mission.compatible_stacks):
                    continue

            compatible.append(mission)

        return compatible

    def get_step(self, mission_id: str, step_index: int) -> Optional[MissionStep]:
        """Retorna a etapa específica de uma missão."""
        mission = self.get_mission(mission_id)
        if not mission or step_index < 0 or step_index >= len(mission.steps):
            return None
        return mission.steps[step_index]


# Instância global reutilizável
mission_service = MissionService()
