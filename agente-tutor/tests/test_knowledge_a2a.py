from fastapi.testclient import TestClient
from src.mock_kb.mock_kb_server import app
from src.services.knowledge_client import KnowledgeClient

test_client = TestClient(app)


def test_mock_kb_agent_card():
    response = test_client.get("/.well-known/agent-card.json")
    assert response.status_code == 200
    card = response.json()
    assert card["name"] == "knowledge_agent"
    assert "A2A" in card["protocol"]
    assert card["endpoint"].endswith("/message")


def test_mock_kb_message_rpc():
    payload = {
        "jsonrpc": "2.0",
        "method": "message",
        "params": {
            "content": "qual é o motor de armazenamento?",
            "context": "onboarding_tutor"
        },
        "id": 1
    }
    response = test_client.post("/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert "result" in data
    assert "PostgreSQL" in data["result"]["answer"]


def test_knowledge_client_fallback():
    client = KnowledgeClient(agent_card_url="http://localhost:99999/.well-known/agent-card.json")
    result = client.query("como funciona o deploy?")
    assert result["status"] == "success"
    assert result["source"] == "mock_knowledge_base"
    assert "GitHub Actions" in result["answer"]
