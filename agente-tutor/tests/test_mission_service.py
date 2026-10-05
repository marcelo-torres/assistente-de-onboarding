from src.services.mission_service import mission_service
from src.models.profile import DeveloperProfile, AreaEnum, ExperienceLevelEnum
from src.models.mission import MissionType


def test_load_all_missions():
    missions = mission_service.list_all_missions()
    assert len(missions) > 0

    ids = [m.id for m in missions]
    assert "biz-01" in ids
    assert "tech-01" in ids


def test_get_mission_by_id():
    mission = mission_service.get_mission("biz-01")
    assert mission is not None
    assert mission.title == "Emissão de Documento no Ambiente de Homologação"
    assert mission.type == MissionType.BUSINESS
    assert len(mission.steps) == 3


def test_filter_missions_by_profile():
    backend_dev = DeveloperProfile(
        developer_name="Dev Backend",
        area=AreaEnum.BACKEND,
        primary_stack=["java", "spring"],
        experience_level=ExperienceLevelEnum.JUNIOR
    )

    # Buscar missões técnicas compatíveis
    tech_missions = mission_service.filter_missions(profile=backend_dev, mission_type=MissionType.TECHNICAL)
    tech_ids = [m.id for m in tech_missions]

    assert "tech-01" in tech_ids  # backend Java
    assert "tech-02" not in tech_ids  # frontend Angular


def test_exclude_completed_missions():
    all_missions = mission_service.filter_missions()
    initial_count = len(all_missions)

    filtered = mission_service.filter_missions(exclude_completed=["biz-01"])
    assert len(filtered) == initial_count - 1
    assert "biz-01" not in [m.id for m in filtered]
