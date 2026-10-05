"""Servidor Mock do Subagente de Conhecimento com suporte ao protocolo A2A.

Permite testar a integração A2A do Agente Tutor localmente, mesmo com o agente real
de base de conhecimento fora do escopo ou em desenvolvimento.
"""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from config.settings import settings
from src.services.knowledge_client import MOCK_KNOWLEDGE_DATA

app = FastAPI(title="Mock Knowledge Agent (A2A)", version="1.0.0")


@app.get("/.well-known/agent-card.json")
async def get_agent_card(request: Request):
    """Retorna o Agent Card descritor do agente A2A."""
    base_url = str(request.base_url).rstrip("/")
    return {
        "name": "knowledge_agent",
        "description": "Subagente de Base de Conhecimento corporativa para dúvidas técnicas e de negócio",
        "version": "1.0.0",
        "endpoint": f"{base_url}/message",
        "protocol": "A2A/1.0",
        "skills": [
            {
                "name": "query_docs",
                "description": "Consulta documentação de processos, microsserviços e regras de negócio"
            }
        ]
    }


@app.post("/message")
async def handle_message(request: Request):
    """Recebe mensagens JSON-RPC 2.0 no protocolo A2A e retorna respostas fundamentadas."""
    try:
        body = await request.json()
        params = body.get("params", {})
        content = params.get("content", "")
        req_id = body.get("id", 1)

        # Buscar resposta nos dados de conhecimento corporativo
        c_lower = content.lower()
        matched_answer = None
        for keyword, answer in MOCK_KNOWLEDGE_DATA.items():
            if keyword in c_lower:
                matched_answer = answer
                break

        if not matched_answer:
            matched_answer = (
                f"[A2A Knowledge Base] Informação oficial sobre '{content}': "
                "Consulte os manuais técnicos corporativos na pasta de arquitetura do GitHub."
            )

        return {
            "jsonrpc": "2.0",
            "result": {
                "answer": matched_answer,
                "agent": "knowledge_agent",
                "status": "success"
            },
            "id": req_id
        }
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "jsonrpc": "2.0",
                "error": {"code": -32600, "message": f"Erro na requisição A2A: {str(e)}"},
                "id": None
            }
        )


def start_mock_server(port: int = None):
    """Inicia o servidor Uvicorn para o Mock Knowledge Agent."""
    server_port = port or settings.mock_kb_port
    print(f"Iniciando Mock Knowledge Agent A2A na porta {server_port}...")
    uvicorn.run(app, host="0.0.0.0", port=server_port)


if __name__ == "__main__":
    start_mock_server()
