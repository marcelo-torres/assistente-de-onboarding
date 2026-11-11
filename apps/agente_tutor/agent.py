# root_agent é o ponto de entrada que o ADK Web procura nesta aplicação.
from pathlib import Path
from google.adk import Agent

from agente_conhecimento.agent import agente_conhecimento

PASTA_RECURSOS = Path(__file__).resolve().parents[2] / "resources"
PASTA_MISSOES = PASTA_RECURSOS / "missoes"
PROMPT_TUTOR = PASTA_RECURSOS / "prompt-tutor.md"


def listar_missoes() -> list[str]:
    """Devolve os nomes dos arquivos Markdown de missão disponíveis."""
    return sorted(arquivo.name for arquivo in PASTA_MISSOES.glob("*.md") if arquivo.is_file())


def obter_missao(missao: str) -> str:
    """Devolve o conteúdo do arquivo Markdown de missão escolhido.

    Args:
        missao: Nome do arquivo listado por listar_missoes, com ou sem extensão.
    """
    nome_arquivo = missao.strip()
    if not nome_arquivo.endswith(".md"):
        nome_arquivo += ".md"

    pasta = PASTA_MISSOES.resolve()
    caminho = (pasta / nome_arquivo).resolve()
    if caminho.parent != pasta or caminho.suffix.lower() != ".md":
        return f"Missão não encontrada: {missao}"
    try:
        return caminho.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"Missão não encontrada: {missao}"

root_agent = Agent(
    name='agente_tutor',
    description=(
        'Agente tutor de onboarding: conduz o novo desenvolvedor, etapa por etapa, '
        'em missões práticas com checkpoints e evidências de conclusão.'
    ),
    model='gemini-2.5-flash',
    instruction=PROMPT_TUTOR.read_text(encoding="utf-8"),
    tools=[obter_missao, listar_missoes],
    sub_agents=[agente_conhecimento]
)
