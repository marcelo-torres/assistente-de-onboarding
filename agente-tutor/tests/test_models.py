from src.models.profile import DeveloperProfile, AreaEnum, ExperienceLevelEnum
from src.models.mission import Mission, MissionStep, MissionType, MissionProgress, MissionStatus
from src.models.state import OnboardingState


def test_developer_profile_compatibility():
    backend_dev = DeveloperProfile(
        developer_name="Ana",
        area=AreaEnum.BACKEND,
        primary_stack=["java", "spring"],
        experience_level=ExperienceLevelEnum.JUNIOR
    )

    # Compatível com área all
    assert backend_dev.is_compatible_with("all", ["all"]) is True

    # Compatível com backend e java
    assert backend_dev.is_compatible_with("backend", ["java"]) is True

    # Incompatível com frontend
    assert backend_dev.is_compatible_with("frontend", ["angular"]) is False

    # Dev fullstack é compatível com frontend e backend
    fullstack_dev = DeveloperProfile(
        developer_name="Bruno",
        area=AreaEnum.FULLSTACK,
        primary_stack=["angular", "python"]
    )
    assert fullstack_dev.is_compatible_with("backend", ["python"]) is True
    assert fullstack_dev.is_compatible_with("frontend", ["angular"]) is True


def test_mission_model():
    step1 = MissionStep(
        step_number=1,
        title="Passo 1",
        instruction="Fazer algo",
        expected_action="Ação 1"
    )
    step2 = MissionStep(
        step_number=2,
        title="Passo 2",
        instruction="Fazer outra coisa",
        expected_action="Ação 2"
    )

    mission = Mission(
        id="test-01",
        title="Missão Teste",
        description="Descrição teste",
        type=MissionType.TECHNICAL,
        steps=[step1, step2]
    )

    assert mission.total_steps == 2
    assert mission.steps[0].title == "Passo 1"


def test_onboarding_state():
    state = OnboardingState()
    assert state.has_profile() is False
    assert state.has_active_mission() is False

    profile = DeveloperProfile(
        developer_name="Carla",
        area=AreaEnum.BACKEND
    )
    state.profile = profile
    assert state.has_profile() is True
