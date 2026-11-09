"""Tool de busca na base de conhecimento."""

from chromadb.api.models.Collection import Collection

from .config import LIMIAR_SIMILARIDADE, TOP_K
from .embeddings import embedar_consulta
from .indice import abrir_colecao_existente

MENSAGEM_SEM_INDICE = (
    "Erro: o índice da base de conhecimento não existe. "
    "Rode `python scripts/indexar_base.py` antes de usar o agente."
)

# Aberta uma vez, na primeira busca que encontra o índice.
_colecao: Collection | None = None


def buscar_base_conhecimento(pergunta: str) -> list[dict] | str:
    """Busca trechos relevantes na base de conhecimento.

    Args:
        pergunta: consulta autônoma e específica sobre o assunto procurado.

    Returns:
        Os trechos mais relevantes [{texto, fonte, secao, score}], do mais
        ao menos relevante. Lista vazia quando nada relevante foi encontrado.
    """
    global _colecao
    if _colecao is None:
        _colecao = abrir_colecao_existente()
        if _colecao is None:
            return MENSAGEM_SEM_INDICE

    resultado = _colecao.query(
        query_embeddings=[embedar_consulta(pergunta)],
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )
    trechos = []
    for texto, metadados, distancia in zip(
        resultado["documents"][0], resultado["metadatas"][0], resultado["distances"][0]
    ):
        score = 1 - distancia
        if score >= LIMIAR_SIMILARIDADE:
            trechos.append(
                {
                    "texto": texto,
                    "fonte": metadados["fonte"],
                    "secao": metadados["secao"],
                    "score": round(score, 4),
                }
            )
    return trechos
