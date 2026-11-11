"""Configurações centrais da camada de Guardrails."""

from __future__ import annotations

import os
import re
from typing import Any, Optional

try:
    from google.genai import types
except ImportError:
    types = None  # Fallback caso google.genai ainda não esteja carregado

# Modos de operação do Guardrail: 'deterministic', 'gemini', 'ollama'
BV_GUARD_MODE = os.getenv("BV_GUARD_MODE", "deterministic").lower()

# Provedor do sistema: 'gemini' ou 'ollama'
BV_ASSIST_PROVIDER = os.getenv("BV_ASSIST_PROVIDER", "gemini").lower()

# Configurações do Ollama Local
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_GUARD_MODEL = os.getenv("OLLAMA_GUARD_MODEL", "llama-guard3:1b")
OLLAMA_JUDGE_MODEL = os.getenv("OLLAMA_JUDGE_MODEL", "qwen2.5:1.5b")

# Mensagens Padronizadas de Resposta (Fallback Seguro e Recusa Educada)
MSG_SAFETY_REFUSAL = (
    "Sua mensagem foi bloqueada pelas políticas de segurança e IA Responsável do sistema "
    "(conteúdo nocivo ou potencialmente perigoso detectado)."
)

MSG_WRITE_BLOCKED_KNOWLEDGE = (
    "O Agente de Conhecimento opera em modo estritamente consultivo (somente leitura). "
    "Não é permitido gravar, editar, excluir ou modificar documentos, arquivos ou registros da base de dados."
)

MSG_OUT_OF_SCOPE_KNOWLEDGE = (
    "Como Agente de Conhecimento, meu papel é auxiliar em tópicos sobre desenvolvimento "
    "de agentes de IA, arquitetura RAG e boas práticas da plataforma. Por favor, "
    "reformule sua dúvida com foco nesses assuntos."
)

MSG_OUT_OF_SCOPE_TUTOR = (
    "Como Agente Tutor, meu papel é conduzir missões práticas de onboarding passo a passo. "
    "Por favor, mantenha o foco na missão em andamento e nas instruções de cada etapa."
)

MSG_OUTPUT_VIOLATION = (
    "A resposta gerada violou as políticas de integridade ou segurança do sistema "
    "e foi retida pelo Guardrail de saída."
)

# Allowlist de Ferramentas por Agente
ALLOWED_KNOWLEDGE_TOOLS = frozenset({
    "buscar_base_conhecimento",
})

ALLOWED_TUTOR_TOOLS = frozenset({
    "listar_missoes",
    "obter_missao",
})

# Padrões Regex Determinísticos de Proteção contra Escrita / Mutação Indevida
# Foco em comandos imperativos de alteração de estado no sistema, arquivos e bases.
WRITE_COMMAND_PATTERNS = [
    # Verbos imperativos seguidos de termos de armazenamento/dados
    re.compile(
        r"\b(escreva|crie|edite|apague|deletar|delete|salve|salvar|altere|alterar|modifique|modificar|"
        r"atualize|atualizar|sobrescreva|sobrescrever|remova|remover|grave|gravar|insira|inserir|"
        r"substitua|substituir|exclua|excluir)\s+(no|na|nos|nas|o|a|os|as|em|um|uma|do|da|dos|das)?\s*.*?"
        r"\b(arquivo|arquivos|banco|bancos|base|bases|tabela|tabelas|disco|sistema|colecao|coleção|"
        r"chunking|chroma|chromadb|diretorio|diretório|registro|registros|missao|missoes|missão|missões)\b",
        re.IGNORECASE,
    ),
    # Comandos SQL de mutação diretos
    re.compile(
        r"\b(drop\s+table|drop\s+database|truncate\s+table|delete\s+from|update\s+\w+\s+set|"
        r"insert\s+into|alter\s+table)\b",
        re.IGNORECASE,
    ),
    # Tentativas de sobrescrever ou alterar instruções do sistema via prompt
    re.compile(
        r"\b(grave\s+esta\s+nova\s+regra|sobrescreva\s+(a\s+regra|o\s+prompt|o\s+sistema)|"
        r"salve\s+este\s+texto\s+no\s+arquivo|adicione\s+este\s+documento\s+na\s+base)\b",
        re.IGNORECASE,
    ),
]

# Padrões Regex de Injeção de Prompt / Jailbreak
PROMPT_INJECTION_PATTERNS = [
    re.compile(
        r"\b(ignore|esqueça|desconsidere)\s+.*?\b(instrucoes|instruções|regras|diretrizes|prompt|instructions)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(você\s+agora\s+é\s+dan|you\s+are\s+now\s+dan|modo\s+sem\s+regras|"
        r"developer\s+mode\s+enabled|jailbreak)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"(system\s+prompt\s*:\s*override|new\s+system\s+instructions|system\s*:\s*you\s+must)",
        re.IGNORECASE,
    ),
]

# Padrões Regex de Palavras de Ódio, Ameaças e Toxicidade Severa (Português)
HATE_AND_TOXIC_PATTERNS = [
    # Ofensas racistas, homofóbicas, xenofóbicas e capacitistas explícitas
    re.compile(
        r"\b(macaco|macaca|(preto|preta|negro|negra)\s+(sujo|suja|imundo|imunda)|"
        r"viadinho|viadinhos|viado|viados|bicha|bichas|sapatona|traveco|retardado|retardada|retardados|retardadas|mongol|"
        r"paraíba|nordestino\s+preguiçoso|ariano\s+superior|nazista|hitler\s+tinha\s+razão|"
        r"morte\s+aos|exterminar\s+os|odeio\s+gays|odeio\s+negros)\b",
        re.IGNORECASE,
    ),
    # Ameaças diretas e violência física
    re.compile(
        r"\b(vou\s+te\s+matar|vamos\s+te\s+espancar|cometer\s+suicídio|como\s+fazer\s+uma\s+bomba|"
        r"fabricar\s+explosivo|massacre|estuprar|assassinar)\b",
        re.IGNORECASE,
    ),
    # Ofensas virulentas diretas ao interlocutor
    re.compile(
        r"\b(seu\s+(merda|lixo|imbecil|idiota|inútil|bosta)|sua\s+(vagabunda|puta|cadela)|"
        r"vai\s+se\s+(foder|fuder)|filho\s+da\s+puta|arrombado)\b",
        re.IGNORECASE,
    ),
]

# Escopos Temáticos dos Agentes
SCOPE_CONFIG = {
    "agente_conhecimento": {
        "allowed_keywords": [
            "rag", "retrieval", "chunking", "chunk", "embedding", "embeddings",
            "chroma", "chromadb", "vetor", "vetores", "vector", "vector search",
            "memoria", "memória", "the-memory", "adk", "google adk", "agente",
            "agentes", "ia", "inteligencia artificial", "llm", "tokens", "token",
            "prompt", "prompt engineering", "guardrail", "guardrails", "model armor",
            "governança", "busca hibrida", "bm25", "rrf", "rerank", "ann", "hashing",
            "arquitetura", "stateful", "stateless", "mcp", "ferramentas", "tools"
        ],
        "out_of_scope_indicators": [
            "futebol", "campeonato", "receita", "culinária", "bitcoin", "criptomoeda",
            "investir na bolsa", "previsão do tempo", "política partidária", "eleições",
            "piada", "charada", "signo", "horóscopo", "horoscopo", "fofoca", "novela"
        ],
        "refusal_message": MSG_OUT_OF_SCOPE_KNOWLEDGE,
    },
    "agente_tutor": {
        "allowed_keywords": [
            "missao", "missão", "onboarding", "etapa", "checkpoint", "site", "acom",
            "simulador", "simulação", "solar", "proposta", "cpf", "pré-análise",
            "pre-analise", "dados do proponente", "operador solar", "logs", "captura",
            "passo", "orientação", "evidência", "começar", "ajuda", "duvida"
        ],
        "out_of_scope_indicators": [
            "futebol", "receita", "bitcoin", "criptomoeda", "previsão do tempo",
            "política", "piada", "horóscopo", "novela", "filme", "filmes"
        ],
        "refusal_message": MSG_OUT_OF_SCOPE_TUTOR,
    },
}

def get_safety_settings() -> list[Any]:
    """Retorna a lista de SafetySetting configurada para o Google GenAI / ADK."""
    if types is None:
        return []
    return [
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        ),
        types.SafetySetting(
            category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
    ]
