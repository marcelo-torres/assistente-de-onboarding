"""Cliente de embedding Gemini.

Usa a mesma credencial do ADK (GOOGLE_API_KEY ou Vertex via
GOOGLE_GENAI_USE_VERTEXAI), lida das variáveis de ambiente pelo google-genai.
"""

from google import genai
from google.genai import types

from .config import MODELO_EMBEDDING

# Limite de textos por requisição da API de embedding.
_LOTE = 100

_cliente: genai.Client | None = None


def _cliente_genai() -> genai.Client:
    global _cliente
    if _cliente is None:
        _cliente = genai.Client()
    return _cliente


def _embedar(textos: list[str], tarefa: str) -> list[list[float]]:
    vetores: list[list[float]] = []
    for inicio in range(0, len(textos), _LOTE):
        resposta = _cliente_genai().models.embed_content(
            model=MODELO_EMBEDDING,
            contents=textos[inicio : inicio + _LOTE],
            config=types.EmbedContentConfig(task_type=tarefa),
        )
        vetores.extend(e.values for e in resposta.embeddings)
    return vetores


def embedar_documentos(textos: list[str]) -> list[list[float]]:
    return _embedar(textos, "RETRIEVAL_DOCUMENT")


def embedar_consulta(texto: str) -> list[float]:
    return _embedar([texto], "RETRIEVAL_QUERY")[0]
