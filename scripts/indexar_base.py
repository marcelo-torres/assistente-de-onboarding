"""Indexa o markdown revisado da base de conhecimento no Chroma.

Uso: python scripts/indexar_base.py

Pode ser rodado de novo sem duplicar trechos. Lê a credencial do Gemini do
ambiente ou do primeiro `.env` encontrado subindo a partir da pasta do agente,
como faz o `adk web`.
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "apps"))

from agente_conhecimento.rag.config import PASTA_MARKDOWN  # noqa: E402
from agente_conhecimento.rag.embeddings import embedar_documentos  # noqa: E402
from agente_conhecimento.rag.indice import abrir_ou_criar_colecao, sincronizar  # noqa: E402


def carregar_env() -> None:
    pasta = RAIZ / "apps" / "agente_conhecimento"
    for candidata in [pasta, *pasta.parents]:
        if (candidata / ".env").is_file():
            load_dotenv(candidata / ".env", override=False)
            return


def main() -> None:
    carregar_env()
    total = sincronizar(abrir_ou_criar_colecao(), PASTA_MARKDOWN, embedar_documentos)
    print(f"Índice atualizado: {total} trechos na coleção.")


if __name__ == "__main__":
    main()
