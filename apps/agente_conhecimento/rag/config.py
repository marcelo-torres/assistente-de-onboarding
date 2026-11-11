"""Configuração do RAG da base de conhecimento."""

from pathlib import Path

RAIZ_DO_PROJETO = Path(__file__).resolve().parents[3]

PASTA_MARKDOWN = RAIZ_DO_PROJETO / "resources" / "base-conhecimento-md"
PASTA_CHROMA = RAIZ_DO_PROJETO / "data" / "chroma"

NOME_COLECAO = "base_conhecimento"
MODELO_EMBEDDING = "gemini-embedding-001"

# Calibrados na tarefa 05 com scripts/avaliar_rag.py (13 arquivos, 16 perguntas de
# tests/avaliacao/perguntas.yaml). Ver docs/estrategia-de-chunking.md.

# Limite do trecho em caracteres, incluindo o cabeçalho contextual (~500 tokens).
# Uma seção que cabe inteira, com as subseções, vira um trecho só.
# Com 2.000 e 3.200 os acertos e falsos positivos empatam; 2.000 tem notas um pouco
# melhores no acerto mais fraco (0,665 contra 0,626), diferença pequena para 13 perguntas.
TAMANHO_MAXIMO_TRECHO = 2000

TOP_K = 5
# Mantido em 0,70: hit@3 pela tool 85% (11/13) e 0/3 falsos positivos. A margem é
# de 0,009 (acerto mais fraco acima do limiar 0,701; maior nota fora da base 0,692),
# medida com só 3 perguntas negativas. Baixar para 0,69 cria falsos positivos;
# subir para 0,71 perde acertos. Rode a avaliação de novo sempre que a base mudar.
LIMIAR_SIMILARIDADE = 0.70

# Enriquecimento dos trechos com perguntas geradas por LLM (ver rag/enriquecimento.py).
# Ligado após a medição de 2026-11-11 (docs/estrategia-de-chunking.md): hit@3 pela tool
# de 85% para 92%, sem falsos positivos na busca direta. As perguntas já geradas estão
# versionadas em ARQUIVO_PERGUNTAS_GERADAS, então reindexar só chama o LLM para trechos
# novos ou alterados. Veja o custo antes com `python scripts/indexar_base.py --estimar`.
ENRIQUECER_COM_PERGUNTAS = True
MODELO_PERGUNTAS = "gemini-2.5-flash-lite"
PERGUNTAS_POR_TRECHO = 3
TRECHOS_POR_CHAMADA = 10
# Versionável: quem clonar o repositório reaproveita as perguntas sem gerar de novo.
ARQUIVO_PERGUNTAS_GERADAS = RAIZ_DO_PROJETO / "resources" / "perguntas-geradas.json"
