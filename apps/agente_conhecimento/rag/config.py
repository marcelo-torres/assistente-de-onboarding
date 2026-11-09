"""Configuração do RAG da base de conhecimento."""

from pathlib import Path

RAIZ_DO_PROJETO = Path(__file__).resolve().parents[3]

PASTA_MARKDOWN = RAIZ_DO_PROJETO / "resources" / "base-conhecimento-md"
PASTA_CHROMA = RAIZ_DO_PROJETO / "data" / "chroma"

NOME_COLECAO = "base_conhecimento"
MODELO_EMBEDDING = "gemini-embedding-001"

# Limite do trecho em caracteres, incluindo o cabeçalho contextual (~800 tokens).
# Não há tamanho mínimo: juntar seções pequenas misturaria assuntos e quebraria a
# citação de seção. Ver docs/estrategia-de-chunking.md.
TAMANHO_MAXIMO_TRECHO = 3200

TOP_K = 5
# Provisório: calibrado na tarefa 05 (avaliação). Medição inicial com o arquivo
# rag__estrategias-de-chunking: perguntas da base com melhor score de 0,74 a 0,80;
# perguntas de IA fora da base até 0,66; fora do domínio até 0,57.
LIMIAR_SIMILARIDADE = 0.70
