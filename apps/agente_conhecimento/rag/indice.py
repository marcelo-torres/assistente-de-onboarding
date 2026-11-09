"""Índice Chroma: sincronização idempotente com a pasta de markdown e consulta."""

from collections.abc import Callable
from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection
from chromadb.config import Settings
from chromadb.errors import NotFoundError

from .chunking import cortar_em_trechos
from .config import NOME_COLECAO, PASTA_CHROMA
from .enriquecimento import GerarPerguntas, texto_para_embedding

Embedar = Callable[[list[str]], list[list[float]]]


def _cliente(pasta: Path) -> chromadb.ClientAPI:
    return chromadb.PersistentClient(
        path=str(pasta), settings=Settings(anonymized_telemetry=False)
    )


def abrir_ou_criar_colecao(pasta: Path = PASTA_CHROMA) -> Collection:
    return _cliente(pasta).get_or_create_collection(
        NOME_COLECAO, metadata={"hnsw:space": "cosine"}
    )


def abrir_colecao_existente(pasta: Path = PASTA_CHROMA) -> Collection | None:
    """Abre a coleção sem criá-la; None se o índice ainda não foi gerado."""
    if not pasta.exists():
        return None
    try:
        return _cliente(pasta).get_collection(NOME_COLECAO)
    except NotFoundError:
        return None


def sincronizar(
    colecao: Collection,
    pasta_markdown: Path,
    embedar: Embedar,
    perguntas: GerarPerguntas | None = None,
) -> int:
    """Reindexa cada .md da pasta e apaga fontes que não existem mais.

    Por arquivo, apaga todos os trechos da `fonte` e reinsere com ID
    "fonte::indice_chunk", então rodar de novo não duplica nada.
    Com `perguntas` (enriquecimento opcional), o embedding de cada trecho inclui
    as perguntas que ele responde; o texto guardado continua sendo só o trecho.
    Devolve a contagem total de trechos na coleção.
    """
    arquivos = sorted(pasta_markdown.glob("*.md"))
    fontes_atuais = {arquivo.name for arquivo in arquivos}

    indexadas = {m["fonte"] for m in colecao.get(include=["metadatas"])["metadatas"]}
    for fonte in indexadas - fontes_atuais:
        colecao.delete(where={"fonte": fonte})

    for arquivo in arquivos:
        trechos = cortar_em_trechos(arquivo.read_text(encoding="utf-8"), fonte=arquivo.name)
        textos = [t.texto for t in trechos]
        metadados = [t.metadados() for t in trechos]
        textos_embedados = textos
        if perguntas and textos:
            por_trecho = perguntas(textos)
            textos_embedados = [texto_para_embedding(t, p) for t, p in zip(textos, por_trecho)]
            for meta, p in zip(metadados, por_trecho):
                meta["perguntas"] = "\n".join(p)
        # Embeda antes de apagar: se a API falhar, a versão anterior continua no índice.
        vetores = embedar(textos_embedados) if textos else []
        colecao.delete(where={"fonte": arquivo.name})
        if not trechos:
            continue
        colecao.add(
            ids=[t.id for t in trechos],
            documents=textos,
            metadatas=metadados,
            embeddings=vetores,
        )
    return colecao.count()
