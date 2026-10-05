from typing import Optional, Dict, Any
from google.adk.tools import ToolContext
from src.services.knowledge_client import knowledge_client


def ask_knowledge_agent(
    query: str,
    category: str = "geral",
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """Consulta o Subagente de Base de Conhecimento corporativa via protocolo A2A.

    Utilize esta ferramenta sempre que o desenvolvedor tiver dúvidas técnicas, conceituais,
    de regras de negócio ou de processos da empresa (ex: como funciona a VPN, qual o motor de armazenamento
    de determinado microsserviço, esteiras de CI/CD, políticas de branches ou regras de negócio).

    Args:
        query: A pergunta ou termo técnico a ser pesquisado na base de conhecimento corporativa.
        category: Categoria da dúvida (ex: 'tecnica', 'processo', 'negocio', 'arquitetura', 'geral').
        tool_context: Contexto de sessão injetado pelo Google ADK.

    Returns:
        Resposta obtida da Base de Conhecimento e a fonte da informação.
    """
    result = knowledge_client.query(question=query, context=category)
    return {
        "status": result.get("status", "success"),
        "source": result.get("source", "knowledge_base"),
        "query": query,
        "category": category,
        "answer": result.get("answer", "Nenhuma informação localizada na base de conhecimento.")
    }
