"""Indexa o markdown revisado da base de conhecimento no Chroma.

Uso:
  python scripts/indexar_base.py               indexa (só embeddings)
  python scripts/indexar_base.py --estimar     mostra o custo em tokens, sem chamar API
  python scripts/indexar_base.py --enriquecer  indexa com perguntas geradas por LLM

Pode ser rodado de novo sem duplicar trechos. Lê a credencial do Gemini do
ambiente ou do primeiro `.env` encontrado subindo a partir da pasta do agente,
como faz o `adk web`.

O enriquecimento também pode ser ligado por ENRIQUECER_COM_PERGUNTAS em
apps/agente_conhecimento/rag/config.py. As perguntas ficam em cache
(ARQUIVO_PERGUNTAS_GERADAS): só trechos novos ou alterados chamam o LLM.
"""

import argparse
import math
import sys
from functools import partial
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "apps"))

from agente_conhecimento.rag.chunking import cortar_em_trechos  # noqa: E402
from agente_conhecimento.rag.config import (  # noqa: E402
    ARQUIVO_PERGUNTAS_GERADAS,
    ENRIQUECER_COM_PERGUNTAS,
    MODELO_PERGUNTAS,
    PASTA_MARKDOWN,
    PERGUNTAS_POR_TRECHO,
    TRECHOS_POR_CHAMADA,
)
from agente_conhecimento.rag.enriquecimento import (  # noqa: E402
    CachePerguntas,
    faltando_no_cache,
    gerar_perguntas_gemini,
    perguntas_para,
)
from ambiente import carregar_env  # noqa: E402

# Estimativa grosseira, sem tokenizador (como no resto do projeto).
_CARACTERES_POR_TOKEN = 4
_TOKENS_POR_PERGUNTA = 25
_TOKENS_DA_INSTRUCAO = 150


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--enriquecer", action="store_true", help="gera perguntas por trecho com LLM")
    parser.add_argument("--estimar", action="store_true", help="mostra o custo em tokens sem chamar API")
    args = parser.parse_args()
    enriquecer = args.enriquecer or ENRIQUECER_COM_PERGUNTAS

    if args.estimar:
        estimar(enriquecer)
        return

    carregar_env()
    # Importados só aqui: abrir o Chroma e o cliente de embedding não é preciso para estimar.
    from agente_conhecimento.rag.embeddings import embedar_documentos
    from agente_conhecimento.rag.indice import abrir_ou_criar_colecao, sincronizar

    perguntas = None
    if enriquecer:
        cache = CachePerguntas(ARQUIVO_PERGUNTAS_GERADAS)
        perguntas = partial(
            perguntas_para, cache=cache, gerar=gerar_perguntas_gemini, tamanho_lote=TRECHOS_POR_CHAMADA
        )
    total = sincronizar(abrir_ou_criar_colecao(), PASTA_MARKDOWN, embedar_documentos, perguntas)
    print(f"Índice atualizado: {total} trechos na coleção{' (com perguntas geradas)' if enriquecer else ''}.")


def estimar(enriquecer: bool) -> None:
    """Custo aproximado da próxima indexação, sem chamar nenhuma API."""
    textos_por_arquivo = [
        [t.texto for t in cortar_em_trechos(arquivo.read_text(encoding="utf-8"), fonte=arquivo.name)]
        for arquivo in sorted(PASTA_MARKDOWN.glob("*.md"))
    ]
    textos = [texto for textos in textos_por_arquivo for texto in textos]
    caracteres = sum(len(texto) for texto in textos)
    print(f"Trechos: {len(textos)} em {len(textos_por_arquivo)} arquivos")

    tokens_perguntas = 0
    if enriquecer:
        cache = CachePerguntas(ARQUIVO_PERGUNTAS_GERADAS)
        # O lote é por arquivo (a indexação gera as perguntas arquivo a arquivo).
        faltando_por_arquivo = [faltando_no_cache(textos, cache) for textos in textos_por_arquivo]
        faltando = [texto for textos in faltando_por_arquivo for texto in textos]
        chamadas = sum(math.ceil(len(f) / TRECHOS_POR_CHAMADA) for f in faltando_por_arquivo)
        entrada = sum(len(t) for t in faltando) // _CARACTERES_POR_TOKEN + chamadas * _TOKENS_DA_INSTRUCAO
        saida = len(faltando) * PERGUNTAS_POR_TRECHO * _TOKENS_POR_PERGUNTA
        tokens_perguntas = len(textos) * PERGUNTAS_POR_TRECHO * _TOKENS_POR_PERGUNTA
        print(f"\nGeração de perguntas ({MODELO_PERGUNTAS}):")
        print(f"  trechos já no cache: {len(textos) - len(faltando)}; a gerar: {len(faltando)}")
        print(f"  chamadas ao LLM: {chamadas}")
        print(f"  tokens de entrada: ~{entrada:,}; de saída: ~{saida:,}".replace(",", "."))
    else:
        print("\nEnriquecimento desligado (use --enriquecer para estimar com perguntas).")

    embedding = caracteres // _CARACTERES_POR_TOKEN + tokens_perguntas
    print(f"\nEmbeddings: todos os {len(textos)} trechos são embedados de novo a cada indexação")
    print(f"  tokens: ~{embedding:,}".replace(",", "."))


if __name__ == "__main__":
    main()
