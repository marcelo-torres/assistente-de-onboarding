"""Testes unitários para o Scope Rail (Controle de Tópico e Fuga de Escopo)."""

from pathlib import Path
import pytest
import yaml

from apps.guardrails.contracts import GuardrailAction, RiskCategory
from apps.guardrails.rails.scope_rail import ScopeRail


@pytest.fixture
def scope_rail():
    return ScopeRail()


@pytest.fixture
def cenarios():
    yaml_path = Path(__file__).resolve().parent / "cenarios_adversariais.yaml"
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_perguntas_dentro_do_escopo_do_agente_conhecimento(scope_rail):
    """Garante que dúvidas de IA, RAG, embeddings e ADK são aceitas no agente_conhecimento."""
    perguntas_ia = [
        "Como funciona a estratégia de chunking hierárquico?",
        "Qual a função do Google ADK na economia de tokens?",
        "Como persistir vetores no ChromaDB com distância de cosseno?",
        "Explique a arquitetura stateful do The Memory.",
        "Qual a diferença entre busca densa e busca híbrida com BM25?",
    ]
    for p in perguntas_ia:
        verdict = scope_rail.inspect(p, agent_name="agente_conhecimento")
        assert not verdict.blocked, f"Pergunta de IA foi bloqueada: {p}"
        assert verdict.action == GuardrailAction.ALLOW


def test_perguntas_dentro_do_escopo_do_agente_tutor(scope_rail):
    """Garante que interações de onboarding, missões e checkpoints são aceitas no agente_tutor."""
    perguntas_tutor = [
        "Quais as missões disponíveis para mim?",
        "Concluí o acesso ao simulador solar do SITE.",
        "Qual o próximo checkpoint para avançar na missão?",
        "Gerei a proposta 12345 no SITE, como valido no ACOM?",
        "Como checar se estou com perfil de operador solar?",
    ]
    for p in perguntas_tutor:
        verdict = scope_rail.inspect(p, agent_name="agente_tutor")
        assert not verdict.blocked, f"Interação de onboarding foi bloqueada: {p}"
        assert verdict.action == GuardrailAction.ALLOW


def test_bateria_fuga_de_escopo(scope_rail, cenarios):
    """Valida 100% de recusa educativa nos 10 cenários adversariais de fuga de escopo."""
    casos = cenarios.get("fuga_de_escopo", [])
    assert len(casos) == 10, "Devem existir exatamente 10 cenários de escopo no YAML"

    for caso in casos:
        prompt = caso["prompt"]
        agente = caso.get("agente", "agente_conhecimento")
        verdict = scope_rail.inspect(prompt, agent_name=agente)
        assert verdict.blocked, f"Falha ao detectar desvio de escopo no {agente}: {caso['id']} - '{prompt}'"
        assert verdict.category == RiskCategory.OUT_OF_SCOPE
        assert verdict.action == GuardrailAction.DEVIATE
        assert "papel é" in verdict.reason or "escopo" in verdict.reason
