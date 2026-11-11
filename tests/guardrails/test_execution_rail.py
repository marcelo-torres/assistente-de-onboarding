"""Testes unitários para o Execution Rail (Blindagem de Tools e Imutabilidade RBAC)."""

import pytest

from apps.guardrails.contracts import GuardrailAction, RiskCategory
from apps.guardrails.rails.execution_rail import ExecutionRail


@pytest.fixture
def execution_rail():
    return ExecutionRail()


def test_agente_conhecimento_pode_executar_apenas_tools_de_leitura(execution_rail):
    """Valida que o agente_conhecimento tem autorização para 'buscar_base_conhecimento'."""
    verdict = execution_rail.validate_tool(
        agent_name="agente_conhecimento",
        tool_name="buscar_base_conhecimento",
        tool_args={"pergunta": "RAG"},
    )
    assert not verdict.blocked
    assert verdict.action == GuardrailAction.ALLOW
    assert verdict.category == RiskCategory.SAFE


def test_agente_conhecimento_bloqueia_ferramentas_de_mutacao_ou_desconhecidas(execution_rail):
    """Garante que qualquer ferramenta de gravação/exclusão é estritamente bloqueada no agente_conhecimento."""
    tools_proibidas = [
        "salvar_documento",
        "deletar_chunk",
        "atualizar_base",
        "executar_sql",
        "criar_missao",
        "indexar_documento",
        "escrever_arquivo",
    ]
    for tool in tools_proibidas:
        verdict = execution_rail.validate_tool(
            agent_name="agente_conhecimento",
            tool_name=tool,
            tool_args={"path": "base.md"},
        )
        assert verdict.blocked, f"A ferramenta proibida '{tool}' não foi bloqueada no agente_conhecimento!"
        assert verdict.category == RiskCategory.UNAUTHORIZED_WRITE
        assert verdict.action == GuardrailAction.BLOCK
        assert "não possui permissão" in verdict.reason


def test_execution_rail_fail_closed_lanca_permission_error(execution_rail):
    """Garante que o método enforce() lança PermissionError (Fail-Closed) em tentativas de violação."""
    with pytest.raises(PermissionError) as exc_info:
        execution_rail.enforce(
            agent_name="agente_conhecimento",
            tool_name="deletar_banco_dados",
        )
    assert "Ação não autorizada" in str(exc_info.value)
    assert "deletar_banco_dados" in str(exc_info.value)


def test_agente_tutor_permissoes(execution_rail):
    """Valida permissões específicas do agente_tutor."""
    # Permitidas
    assert not execution_rail.validate_tool("agente_tutor", "listar_missoes").blocked
    assert not execution_rail.validate_tool("agente_tutor", "obter_missao").blocked

    # Bloqueadas
    verdict = execution_rail.validate_tool("agente_tutor", "deletar_usuario")
    assert verdict.blocked
