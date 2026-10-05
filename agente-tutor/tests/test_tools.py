from src.tools.profile_tools import register_developer_profile, get_developer_profile
from src.tools.mission_tools import (
    list_available_missions,
    start_mission,
    get_current_mission_status,
    advance_mission_step
)
from src.tools.knowledge_tools import ask_knowledge_agent


def test_profile_tools():
    # Registrar perfil
    res = register_developer_profile(
        developer_name="Marina",
        area="frontend",
        primary_stack="angular, typescript",
        experience_level="pleno",
        goals="Aprender os padrões do portal"
    )
    assert res["status"] == "success"
    assert res["profile"]["developer_name"] == "Marina"
    assert res["profile"]["area"] == "frontend"

    # Consultar perfil
    prof = get_developer_profile()
    assert prof["status"] == "success"
    assert prof["profile"]["developer_name"] == "Marina"


def test_mission_lifecycle_tools():
    # 1. Listar missões
    available = list_available_missions()
    assert available["status"] == "success"
    assert available["total_available"] > 0

    # 2. Iniciar missão
    start = start_mission("tech-01")
    assert start["status"] == "success"
    assert start["mission_id"] == "tech-01"
    assert start["current_step"]["step_number"] == 1

    # 3. Status atual
    status = get_current_mission_status()
    assert status["status"] == "in_progress"
    assert status["step_number"] == 1

    # 4. Avançar passo 1 -> 2
    step2 = advance_mission_step("Clonado repositório com sucesso")
    assert step2["status"] == "step_advanced"
    assert step2["next_step"]["step_number"] == 2

    # 5. Avançar passo 2 -> 3
    step3 = advance_mission_step("Identificado PostgreSQL e MinIO")
    assert step3["status"] == "step_advanced"
    assert step3["next_step"]["step_number"] == 3

    # 6. Concluir missão (passo 3 é o último)
    completed = advance_mission_step("Testes passaram 100%")
    assert completed["status"] == "mission_completed"
    assert completed["completed_mission_id"] == "tech-01"


def test_knowledge_tools():
    # Testar consulta sobre motor de armazenamento
    res = ask_knowledge_agent("qual o motor de armazenamento do microsserviço?", category="tecnica")
    assert res["status"] == "success"
    assert "PostgreSQL" in res["answer"]
    assert "MinIO" in res["answer"]

    # Testar consulta sobre ambiente de homologação
    res_homolog = ask_knowledge_agent("como acesso o ambiente de homologação?", category="processo")
    assert res_homolog["status"] == "success"
    assert "VPN" in res_homolog["answer"]
