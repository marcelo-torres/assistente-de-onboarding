import logging
import httpx
from typing import Dict, Any, Optional
from config.settings import settings

logger = logging.getLogger(__name__)


# Base de conhecimento local simulada para fallback de desenvolvimento/testes
MOCK_KNOWLEDGE_DATA = {
    "motor de armazenamento": (
        "O microsserviço 'ms-documento-api' utiliza **PostgreSQL 16** como banco de dados relacional "
        "para metadados, controle de transições de status e auditoria, e **MinIO/AWS S3** como object storage "
        "para o armazenamento dos arquivos binários (PDFs gerados e anexos)."
    ),
    "banco de dados": (
        "Nos microsserviços da empresa, o padrão é **PostgreSQL** para bancos relacionais transacionais. "
        "Para cache de sessões e rate limit, utilizamos **Redis**. Para arquivos e mídias, utilizamos **S3 / MinIO**."
    ),
    "homologação": (
        "O ambiente de homologação fica acessível em `https://homolog.portal.interno`. Para acessá-lo, "
        "é indispensável estar conectado na **VPN corporativa** (perfil Engenharia). "
        "Credenciais temporárias podem ser solicitadas no canal `#dev-access` do Slack."
    ),
    "vpn": (
        "A VPN da empresa utiliza o cliente OpenVPN / Cisco AnyConnect. O endereço do gateway é `vpn.empresa.com.br`. "
        "Utilize sua autenticação corporativa com 2FA (MFA)."
    ),
    "deploy": (
        "Nosso fluxo de CI/CD roda via **GitHub Actions**. Commits na branch `develop` disparam deploy "
        "automático no ambiente de homologação (Kubernetes via ArgoCD). Deploys para produção necessitam "
        "de aprovação de PR para a branch `main` e tag de release."
    ),
    "documento": (
        "No domínio de negócio da empresa, um documento passa pelos seguintes estados: "
        "1. `MINUTA`: Criado pelo autor, editável;\n"
        "2. `EM PROCESSAMENTO`: Em análise automática por regras de negócio;\n"
        "3. `AGUARDANDO APROVAÇÃO`: Aguardando revisão manual se o valor exceder R$ 5.000;\n"
        "4. `APROVADO`: Emitido formalmente e registrado no cartório/bureau digital;\n"
        "5. `REJEITADO`: Caso haja inconformidade."
    ),
    "kafka": (
        "O cluster Apache Kafka é utilizado para mensageria assíncrona entre microsserviços. "
        "Eventos de domínio seguem o formato CloudEvents com serialização JSON Schema."
    )
}


class KnowledgeClient:
    """Cliente para consulta ao Subagente de Base de Conhecimento via protocolo A2A."""

    def __init__(self, agent_card_url: Optional[str] = None):
        self.agent_card_url = agent_card_url or settings.knowledge_agent_card_url
        self.mock_fallback_enabled = settings.knowledge_agent_mock_fallback

    def query(self, question: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Envia uma dúvida para a Base de Conhecimento via A2A ou fallback local."""
        # 1. Tentar comunicação A2A remota caso o serviço esteja acessível
        remote_response = self._try_remote_a2a(question, context)
        if remote_response is not None:
            return remote_response

        # 2. Se o serviço remoto não responder e o fallback estiver habilitado, usar mock simulado
        if self.mock_fallback_enabled:
            logger.info("Serviço A2A remoto indisponível. Utilizando fallback local da base de conhecimento.")
            return self._mock_lookup(question)

        return {
            "status": "error",
            "source": "a2a_remote",
            "answer": "Não foi possível conectar ao Subagente de Conhecimento A2A no endereço configurado."
        }

    def _try_remote_a2a(self, question: str, context: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Tenta consultar o agente A2A via HTTP JSON-RPC 2.0."""
        try:
            # Testar se o agent card responde com timeout curto
            with httpx.Client(timeout=2.0) as client:
                res = client.get(self.agent_card_url)
                if res.status_code == 200:
                    card = res.json()
                    endpoint = card.get("endpoint", self.agent_card_url.replace("/.well-known/agent-card.json", "/message"))
                    
                    # Chamada no formato A2A / JSON-RPC
                    payload = {
                        "jsonrpc": "2.0",
                        "method": "message",
                        "params": {
                            "content": question,
                            "context": context or "onboarding_tutor"
                        },
                        "id": 1
                    }
                    post_res = client.post(endpoint, json=payload, timeout=10.0)
                    if post_res.status_code == 200:
                        data = post_res.json()
                        answer = data.get("result", {}).get("answer", data.get("result", str(data)))
                        return {
                            "status": "success",
                            "source": "a2a_remote",
                            "answer": answer
                        }
        except Exception as e:
            logger.debug(f"A2A remoto não respondeu ({e}). Acionando lógica de contingência.")
            return None
        return None

    def _mock_lookup(self, question: str) -> Dict[str, Any]:
        """Busca resposta na base de conhecimento simulada baseada em palavras-chave."""
        q_lower = question.lower()
        for keyword, answer in MOCK_KNOWLEDGE_DATA.items():
            if keyword in q_lower:
                return {
                    "status": "success",
                    "source": "mock_knowledge_base",
                    "matched_topic": keyword,
                    "answer": answer
                }

        # Resposta genérica orientada a processos corporativos
        return {
            "status": "success",
            "source": "mock_knowledge_base",
            "matched_topic": "geral",
            "answer": (
                f"Informação corporativa sobre '{question}': "
                "Para mais detalhes sobre este tópico específico, consulte a documentação técnica no Confluence/GitHub "
                "ou acione o canal `#duvidas-onboarding` no Slack interno."
            )
        }


# Instância global reutilizável
knowledge_client = KnowledgeClient()
