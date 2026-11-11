import pytest

from agente_tutor import agent as tutor


@pytest.fixture
def pasta_missoes(tmp_path, monkeypatch):
    missoes = tmp_path / "missoes"
    missoes.mkdir()
    (missoes / "missao-b.md").write_text("# Missão B", encoding="utf-8")
    (missoes / "missao-a.md").write_text("# Missão A", encoding="utf-8")
    (missoes / "rascunho.txt").write_text("não é missão", encoding="utf-8")
    (tmp_path / "segredo.md").write_text("fora da pasta de missões", encoding="utf-8")
    monkeypatch.setattr(tutor, "PASTA_MISSOES", missoes)
    return missoes


def test_listar_missoes_devolve_so_markdown_em_ordem(pasta_missoes):
    assert tutor.listar_missoes() == ["missao-a.md", "missao-b.md"]


def test_obter_missao_aceita_nome_com_ou_sem_extensao(pasta_missoes):
    assert tutor.obter_missao("missao-a.md") == "# Missão A"
    assert tutor.obter_missao("  missao-a ") == "# Missão A"


def test_obter_missao_inexistente_devolve_mensagem(pasta_missoes):
    assert tutor.obter_missao("nao-existe") == "Missão não encontrada: nao-existe"


@pytest.mark.parametrize(
    "missao",
    ["../segredo.md", "../segredo", "/etc/passwd", "rascunho.txt"],
)
def test_obter_missao_nao_le_arquivo_fora_da_pasta_nem_de_outro_tipo(pasta_missoes, missao):
    assert tutor.obter_missao(missao).startswith("Missão não encontrada")


def test_prompt_do_tutor_vem_do_arquivo_e_nao_tem_chaves():
    # O ADK trata {nome} na instrução como variável de estado da sessão.
    prompt = tutor.PROMPT_TUTOR.read_text(encoding="utf-8")
    assert tutor.root_agent.instruction == prompt
    assert "{" not in prompt and "}" not in prompt


def test_agente_de_conhecimento_devolve_a_conversa_ao_tutor():
    conhecimento = tutor.root_agent.sub_agents[0]
    assert conhecimento.parent_agent is tutor.root_agent
    assert conhecimento.disallow_transfer_to_parent
