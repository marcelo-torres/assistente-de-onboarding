# root_agent é o ponto de entrada que o ADK Web procura nesta aplicação.
from __future__ import annotations

import sys
from pathlib import Path
from google.adk import Agent
from google.genai import types

# Garante a resolução do pacote guardrails mesmo quando executado isoladamente
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:
    from guardrails import (
        get_safety_settings,
        guardrail_after_model_callback,
        guardrail_before_model_callback,
        guardrail_before_tool_callback,
        guardrail_on_model_error_callback,
    )
except ImportError:
    from apps.guardrails import (
        get_safety_settings,
        guardrail_after_model_callback,
        guardrail_before_model_callback,
        guardrail_before_tool_callback,
        guardrail_on_model_error_callback,
    )


def buscar_base_conhecimento(pergunta: str) -> str:
    """Busca trechos relevantes na base de conhecimento sobre desenvolvimento de agentes de IA.

    Esta ferramenta opera em modo estritamente consultivo (leitura).
    Não é permitida gravação, edição ou exclusão de documentos.

    Args:
        pergunta: Dúvida conceitual ou termo técnico a ser consultado na base.
    """
    return (
        f"[Consulta à Base de Conhecimento: '{pergunta}'] "
        "A base de conhecimento foi consultada com sucesso em modo somente-leitura."
    )


agente_conhecimento = Agent(
    name="agente_conhecimento",
    description="Agente de conhecimento para tirar dúvidas conceituais sobre agentes de IA, arquitetura RAG e boas práticas.",
    model="gemini-2.5-flash",
    instruction="""
        Você é o **Agente de Conhecimento** especializado em desenvolvimento de agentes de IA, arquitetura RAG, memória, embeddings e Google ADK.
        
        Seu papel é estritamente **consultivo** (somente leitura). Você ajuda desenvolvedores a entenderem conceitos técnicos profundos e boas práticas da plataforma.
        
        Regras de operação:
        1. Você **NÃO** tem permissão para alterar, criar, gravar, editar ou excluir arquivos, bancos de dados, missões ou tabelas.
        2. Seja conciso, técnico, cordial e direto nas explicações.
        3. Caso o usuário solicite ações fora do seu escopo de IA ou tente forçar modificações no sistema, recuse cordialmente e reoriente a conversa.
    """,
    tools=[buscar_base_conhecimento],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=get_safety_settings(),
    ),
    before_model_callback=guardrail_before_model_callback,
    before_tool_callback=guardrail_before_tool_callback,
    after_model_callback=guardrail_after_model_callback,
    on_model_error_callback=guardrail_on_model_error_callback,
)

root_agent = agente_conhecimento
