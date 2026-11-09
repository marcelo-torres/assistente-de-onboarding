"""Carrega a credencial do Gemini como o `adk web` faz."""

from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[1]


def carregar_env() -> None:
    """Lê o primeiro `.env` encontrado subindo a partir da pasta do agente.

    Variáveis já definidas no ambiente têm prioridade sobre o arquivo.
    """
    pasta = RAIZ / "apps" / "agente_conhecimento"
    for candidata in [pasta, *pasta.parents]:
        if (candidata / ".env").is_file():
            load_dotenv(candidata / ".env", override=False)
            return
