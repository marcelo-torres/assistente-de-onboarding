# Aula 01: O Ecossistema ADK & A Economia dos Tokens | BV Agent Engineering

Aula 01 de 19

## O Ecossistema ADK & A Economia dos Tokens

Inicializar um projeto padronizado com Google ADK e criar um script que monitora o custo de execução em tempo real.

Duração

3h

Horário

08:00

Metodologia

PBL

Módulo

01

Problema

Scripts soltos em Python tornam-se inauditáveis e o uso indiscriminado de modelos caros gera desperdício financeiro invisível.

Solução

Projeto padronizado com Google ADK, estrutura auditável e monitoramento de custos em tempo real.

### Cronograma da Aula

08:00 Boas-vindas 10min

08:10 Apresentação do Curso 20min

08:30 Detalhamento Módulo 1 15min

08:45 O que são Agentes de IA? 30min

09:15 Níveis de Agentes 25min

09:40 Intervalo 10min

09:50 Anatomia do Agente 30min

10:20 Ambiente Vertex AI 20min

10:40 Validação do Setup 20min

## O que são Agentes de IA?

Nem todo problema precisa de um agente. Entenda quando usar cada abordagem.

### Automações

Regras fixas e determinísticas

- Scripts cron
- ETL pipelines
- Webhooks
- If/else chains

Quando usar

Fluxos previsíveis

### Automações Inteligentes

ML clássico + regras

- Classificadores
- Detecção de fraude
- Recomendação
- Predição de churn

Quando usar

Padrões históricos

### Agentes de IA

Raciocínio + Ação autônoma

- Planejamento
- Uso de ferramentas
- Auto-correção
- Contexto dinâmico

Quando usar

Tarefas complexas

### Definição Técnica

"Um agente é um loop de controle estocástico onde um LLM atua como o 'Kernel' de decisão, recebendo observações do ambiente e decidindo qual subrotina (Tool) executar para minimizar a distância até um estado objetivo."

Loop de Controle Estocasticidade Tool Use Estado Objetivo

### Estrutura Conceitual

```
class Agent(Loop):
          """Um agente é um loop que observa, pensa e age."""

          def run(self, goal: str):
              while not self.is_done():
                  observation = self.perceive()      # Observar o ambiente
                  thought = self.llm.reason(observation, goal)  # Raciocinar
                  action = self.decide(thought)      # Decidir ação
                  result = self.tools.execute(action)  # Executar
                  self.update_state(result)          # Atualizar estado
```

### Importante: Agente ≠ Assistente

Um simples "prompt → LLM → resposta" NÃO é um agente, é um assistente/chatbot. Agentes PRECISAM executar ferramentas (tools) para interagir com o mundo real.

## Tipos de Agentes de IA

Padrões de raciocínio e orquestração multi-agent baseados em fontes oficiais.

### Referências Oficiais

Microsoft Azure - AI Agent Orchestration Patterns Google Cloud - Agentic AI System Patterns LangGraph - Multi-Agent Supervisor OpenAI - Orchestrating Agents

### Esclarecimentos Importantes

#### Multi-Agent vs Supervisor/Worker

Multi-Agent é uma categoria que engloba qualquer sistema com 2+ agentes. Supervisor/Worker é um padrão específico de comunicação hierárquica.

Analogia: Multi-Agent é como "Veículo". Supervisor/Worker é como "Carro". Todo carro é um veículo, mas nem todo veículo é um carro.

#### Swarm vs Multi-Agent Geral

Coordenador Central: Multi-Agent ✓ | Swarm ✗

Comunicação: Varia | All-to-All

Hierarquia: Pode ter | Flat

## Padrões de Raciocínio Individual

COMO O AGENTE PENSA

Estes padrões definem como cada agente individual raciocina, não a arquitetura multi-agent.

### ReAct

Thought → Action → Observation

Loop básico de raciocínio e ação. O agente pensa, executa uma ferramenta e observa o resultado antes de decidir o próximo passo.

Ref: Google Cloud, Arxiv

### Plan-and-Solve

Planeja tudo antes de executar

Gera um plano completo com todos os passos antes de começar a executar. Ideal para tarefas complexas com múltiplas etapas interdependentes.

Ref: Google Cloud

### Reflexion

Auto-crítica e correção

O agente "lê" seu próprio output, identifica erros e os corrige. Melhora a qualidade através de iteração e auto-avaliação.

Ref: Microsoft Azure

### Chain-of-Thought (CoT)

Raciocínio passo a passo

O modelo explicita seu raciocínio em etapas sequenciais antes de chegar à resposta final. Aumenta a precisão em tarefas complexas.

Ref: OpenAI, Google

## Padrões de Orquestração Multi-Agent

COMO OS AGENTES SE COMUNICAM

Baseado na taxonomia oficial da Microsoft Azure e Google Cloud.

### Sequential (Pipeline)

Ordem predefinida e linear

Agentes executam em sequência determinística. O output de um agente é o input do próximo. Não requer modelo para orquestrar - workflow é hardcoded.

Microsoft Azure, Google Cloud

### Parallel (Concurrent)

Execução simultânea

Múltiplos agentes executam ao mesmo tempo e resultados são agregados. Não requer modelo para orquestrar - dispatch é predefinido.

Microsoft Azure, Google Cloud

### Coordinator (Supervisor/Worker)

Coordenador central hierárquico

Um agente coordenador usa o modelo para rotear dinamicamente tarefas para subagentes especializados. Workers comunicam apenas com o Supervisor. Requer modelo para orquestrar.

LangGraph, Microsoft Azure, Google Cloud

### Hierarchical Task Decomposition

Múltiplos níveis de coordenadores

Agente raiz decompõe problema complexo em sub-problemas. Sub-coordenadores podem decompor ainda mais. Requer modelo em múltiplos níveis. Complexidade alta.

Google Cloud, Microsoft Azure

### Handoff (Delegação Direta)

Agentes passam controle diretamente

Não há coordenador central. Cada agente decide quando delegar para outro agente específico. Requer modelo em cada agente para decidir handoff.

OpenAI Agents SDK, Microsoft Azure

### Swarm (Enxame)

Comunicação all-to-all sem coordenador

Agentes colaboram e debatem sem hierarquia. Inteligência emerge da interação. Sem coordenador central. Alto custo e latência. Ideal para brainstorming e design criativo.

Google Cloud, Microsoft Azure

## Padrões de Orquestração Multi-Agent

COMO OS AGENTES COLABORAM

Consenso da indústria (Microsoft, Google, LangGraph, OpenAI).

### Sequential (Pipeline)

Determinística

Ordem predefinida e linear

Agentes executam em sequência determinística. O output de um agente é o input do próximo. Não requer modelo para orquestrar - workflow é hardcoded.

Agente 1

Agente 2

Agente 3

Exemplo Real

Pipeline ETL: Extração → Limpeza → Validação → Carga

Fonte: Microsoft Azure, Google Cloud

### Parallel (Concurrent)

Determinística

Execução simultânea

Múltiplos agentes executam ao mesmo tempo e resultados são agregados. Não requer modelo para orquestrar - dispatch é predefinido.

Input

A1

A2

A3

Agregador

Exemplo Real

Análise de feedback: Sentimento + Keywords + Classificação (em paralelo)

Fonte: Microsoft Azure, Google Cloud

### Coordinator (Supervisor/Worker)

Dinâmica (LLM)

Coordenador central hierárquico

Um agente coordenador usa o modelo para rotear dinamicamente tarefas para subagentes especializados. Workers comunicam apenas com o Supervisor. Requer modelo para orquestrar.

Supervisor

Worker 1

Worker 2

Worker 3

Exemplo Real

Customer Service: Supervisor roteia para Technical Support | Billing | Account

Fonte: LangGraph, Microsoft Azure, Google Cloud

### Hierarchical Task Decomposition

Dinâmica (Multi-LLM)

Múltiplos níveis de coordenadores

Agente raiz decompõe problema complexo em sub-problemas. Sub-coordenadores podem decompor ainda mais. Requer modelo em múltiplos níveis. Complexidade e custo altos.

Root Agent

Sub-Coord 1

W1

W2

Sub-Coord 2

Exemplo Real

Pesquisa complexa: Coordenador → [Pesquisador → Sumarizer] + [Validador → Fact-checker]

Fonte: Google Cloud, Microsoft Azure

### Handoff (Delegação Direta)

Dinâmica (Peer-to-Peer)

Agentes passam controle diretamente

Não há coordenador central. Cada agente decide quando delegar para outro agente específico. Requer modelo em cada agente para decidir handoff. Comunicação peer-to-peer.

Agente A

Agente B

Agente C

Exemplo Real

Suporte: Triagem → Técnico → Financeiro → Escalação (delegação direta entre pares)

Fonte: OpenAI Agents SDK, Microsoft Azure

### Swarm (Enxame)

Emergente

Comunicação all-to-all sem coordenador

Agentes colaboram e debatem sem hierarquia. Sem coordenador central. Comunicação all-to-all. Inteligência emerge da colaboração. Alto custo e latência. Pode não convergir.

A1

A2

A3

Exemplo Real

Design Colaborativo: Market + Engineering + Finance debatem até consenso emergir

Fonte: Google Cloud, Microsoft Azure

### Comparação de Padrões

| Padrão | Orquestração | Coordenador | Custo | Complexidade |
| --- | --- | --- | --- | --- |
| Sequential | Determinística | Não | Baixo | Baixa |
| Parallel | Determinística | Não | Médio | Baixa |
| Coordinator | Dinâmica | Sim (1 nível) | Médio | Média |
| Hierarchical | Dinâmica | Sim (N níveis) | Alto | Alta |
| Handoff | Dinâmica | Não (P2P) | Médio | Média |
| Swarm | Emergente | Não (All-to-All) | Muito Alto | Muito Alta |

## Níveis de Agentes

Da simplicidade à complexidade corporativa.

### Nível Básico

SIMPLES

Prompt → LLM → Resposta. Sem estado, sem ferramentas.

Input

LLM

Output

Exemplo: Chatbot de FAQ, gerador de texto

### Nível Profissional

PRODUÇÃO

Adiciona memória, ferramentas e guardrails básicos.

Memória

Contexto de conversa

Ferramentas

APIs, calculadoras

Guardrails

Filtros básicos

Exemplo: Assistente corporativo com APIs

### Nível Avançado

ENTERPRISE

Arquitetura completa para ambientes corporativos.

#### Orquestração

- Estado
- Grafos
- Fluxos

#### RAG Avançado

- Embeddings
- RBAC
- Cache

#### Ferramentas

- Tool Calling
- Pydantic
- HITL

#### Governança

- Guardrails
- Evals
- Observabilidade

Exemplo: Sistema bancário multiagente

## Memória

Armazenamento e gerenciamento de contexto

Memória de agentes organiza-se em escopo temporal (short/long-term) e tipos funcionais (episodic, semantic, procedural, working). Baseado em LangGraph, Microsoft Azure e Google Cloud.

### Referências Oficiais

LangGraph Memory Azure Agent Memories Vertex AI Memory Bank Research: Mem^p

### Esclarecimentos Importantes

#### ⚠️ Checkpointer ≠ Episodic Memory

Checkpointer é um mecanismo de persistência do LangGraph para salvar estado do grafo (permite time-travel). Memória episódica refere-se a registros de interações passadas específicas armazenadas no Long-Term Store.

#### ⚠️ Procedural Memory ≠ Fine-tuning

Pesquisas recentes (2024-2025) mostram que memória procedural é uma alternativa ao fine-tuning. Armazena procedimentos/workflows externamente sem modificar pesos do modelo. Modelos menores + procedural memory podem superar modelos maiores.

1

### Short-Term (Working Memory)

Contexto da conversa atual mantido no context window. Inclui histórico de mensagens, resultados de tool calls, e estado intermediário.

Implementação

Checkpointer (InMemorySaver, PostgresSaver, RedisSaver)

Limite

Context window do modelo (128K-2M tokens)

Estratégias de Gerenciamento

Trim, Delete, Summarize messages

Exemplo

Últimas 10 mensagens da conversa atual, resultados da última chamada de API

2

### Long-Term (Persistent Memory)

Persiste conhecimento entre sessões e threads. Preferências do usuário, informações aprendidas, dados application-level.

Implementação

Memory Store (InMemoryStore, PostgresStore, RedisStore)

Limite

Limitado apenas pelo storage do DB

Estratégias de Gerenciamento

Busca semântica com embeddings, namespace isolation

Exemplo

Preferências de notificação do usuário, histórico de transações passadas

3

### Episodic Memory

Registros de eventos e interações específicas do passado. 'O que aconteceu na conversa de ontem às 14h?'

Implementação

Long-Term Store com timestamps e metadata

Limite

Sem limite prático

Estratégias de Gerenciamento

Filtragem por timestamp, user_id, session_id

Exemplo

Usuário reportou um bug em 15/01/2025, agente sugeriu workaround X

4

### Semantic Memory (RAG)

Conhecimento factual e conceitual. Fatos gerais sobre o mundo, documentos externos, manuais, políticas corporativas.

Implementação

Vector Database + Embeddings (Pinecone, ChromaDB, FAISS)

Limite

Milhões de documentos

Estratégias de Gerenciamento

Semantic search, re-ranking, hybrid search

Exemplo

Manual de compliance do banco, políticas de crédito, regulamentações BACEN

5

### Procedural Memory

Como executar tarefas - workflows, instruções passo-a-passo, templates de ações. Distinto de fine-tuning, armazena procedimentos externamente.

Implementação

External procedure store, não modifica pesos do modelo

Limite

Centenas a milhares de procedimentos

Estratégias de Gerenciamento

Retrieval based on task similarity, Bayesian reliability tracking

Exemplo

Procedimento de aprovação de crédito: 1) Validar docs 2) Calcular score 3) Aplicar políticas 4) Gerar proposta

### Comparação de Tipos de Memória

| Tipo | Escopo | Persistência | Implementação | Busca | Custo |
| --- | --- | --- | --- | --- | --- |
| Short-Term | Thread-level | Temporária | Checkpointer | Linear | Baixo |
| Long-Term | Cross-session | Permanente | Store | Semantic | Médio |
| Episodic | Historical events | Permanente | Store + timestamps | Temporal | Médio |
| Semantic | Factual knowledge | Permanente | Vector DB | Embeddings | Alto |
| Procedural | Task workflows | Permanente | Procedure store | Task-based | Baixo |

## Cérebro (Kernel)

LLM como núcleo de decisão e raciocínio

O cérebro do agente é composto pelo LLM (kernel), system prompt (persona), reasoning engine (capacidade de planejamento) e validação estruturada de outputs. Baseado em OpenAI, Google Gemini e Anthropic.

### Referências Oficiais

OpenAI Prompt Engineering Google Gemini Thinking Pydantic Structured Output

1

### System Prompt (Persona)

Define a persona, regras imutáveis, tom de voz e comportamento base do agente. É a instrução permanente que molda todas as interações.

#### Melhores Práticas

- Seja específico e detalhado - evite instruções vagas
- Use delimitadores claros (### ou """) para separar seções
- Forneça exemplos concretos (few-shot) quando necessário
- Defina formato de output esperado explicitamente
- Reduza ambiguidade com requisitos mensuráveis

#### Estrutura Recomendada

```
1. Papel/Persona
2. Contexto e domínio
3. Regras e restrições
4. Formato de resposta
5. Exemplos (optional)
```

#### Exemplo Prático

```
Você é um auditor sênior de compliance do Banco BV especializado em análise de risco de crédito.

# Contexto
Você analisa propostas de crédito para identificar riscos regulatórios e operacionais.

# Regras
- SEMPRE cite a regulamentação BACEN aplicável
- NUNCA aprove propostas sem validação de documentos
- Use tom formal e objetivo

# Output Format
JSON: {"aprovado": bool, "riscos": [], "recomendacoes": []}
```

Implementação: LangChain: SystemMessage, OpenAI: system role, Vertex AI: systemInstruction

2

### Reasoning Engine (Planejamento)

Capacidade do LLM de raciocinar, planejar e decompor tarefas complexas em sub-tarefas executáveis. Diferentes modelos e técnicas têm capacidades distintas.

#### Tipos de Reasoning

##### ReAct (Reasoning + Acting)

Thought → Action → Observation em loop. Padrão interleaved de raciocínio e ação.

Força: Flexível, corrige erros dinamicamente

Fraqueza: Lento - uma chamada LLM por ferramenta

Uso:

Tarefas exploratórias, debugging

##### Plan-and-Execute

Gera plano completo primeiro, depois executa todas as ações.

Força: Mais rápido, usa modelos menores para execução

Fraqueza: Menos adaptável a mudanças

Uso:

Workflows previsíveis, pipelines

##### Chain-of-Thought (CoT)

Explicita raciocínio passo-a-passo antes da resposta final.

Força: Melhora precisão em tarefas complexas

Fraqueza: Aumenta latência e custo

Uso:

Problemas matemáticos, análise lógica

##### Gemini Thinking Mode

Processo de pensamento interno (pre-reasoning) antes de responder. Acesso via includeThoughts=true.

Força: Estado da arte em raciocínio, 1M context window

Fraqueza: Custo mais alto

Uso:

Problemas complexos multi-domínio, code analysis

#### Capacidades por Modelo

| Modelo | Reasoning | Planning | Context | Especialidade |
| --- | --- | --- | --- | --- |
| Gemini 2.5 Pro | Excelente | Excelente | 1M tokens | Thinking mode, MoE |
| GPT-4o | Excelente | Muito Bom | 128K tokens | Multimodal |
| Claude 3.5 Sonnet | Excelente | Excelente | 200K tokens | Code, long context |
| GPT-4o-mini | Bom | Bom | 128K tokens | Custo/benefício |

3

### Output Estruturado (Validação)

Garantir que o LLM retorne dados em formato validado e tipado, não texto livre. Pydantic é o padrão de mercado.

#### Exemplo Prático

```
class PropostaCreditoOutput(BaseModel):
    aprovado: bool
    score_risco: float = Field(ge=0, le=100)
    valor_aprovado: Decimal
    restricoes: List[str] = []
    
    @field_validator('score_risco')
    def validar_score(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Score deve estar entre 0-100')
        return v
```

#### Workflow

```
1. Definir Pydantic Model
2. Gerar JSON Schema
3. Incluir schema no prompt
4. LLM gera JSON
5. Validar com model_validate_json()
```

#### Benefícios

Type safety Field validation Error handling Auto-completion (IDE) Documentação automática

Frameworks: Pydantic, Pydantic AI, LangChain Structured Output, OpenAI response_format

Error Handling: Retry com feedback da validação, fallback para formato livre, logging detalhado

## Ferramentas

Tool use (function calling) para ação no mundo real

Function calling (também chamado de tool use) permite que LLMs determinem inteligentemente quando ferramentas externas são necessárias e gerem dados estruturados especificando qual ferramenta chamar e seus parâmetros. Isso conecta o LLM a sistemas externos e estende suas capacidades para além de geração de texto, permitindo buscar dados atualizados e realizar ações no mundo real.

### Referências Oficiais

Google Vertex AI Function Calling OpenAI Function Calling Google ADK Tools LangChain Tools Documentation

1

### Funções Python Locais

Executam no mesmo processo. Rápidas, mas sem isolamento.

Exemplo

@tool def calcular_juros_compostos(principal: float, taxa: float, periodos: int) -> float: '''Calcula juros compostos para análise de crédito''' return principal * (1 + taxa) ** periodos

2

### APIs REST/HTTP

Chamadas HTTP externas. Máxima interoperabilidade.

Exemplo

@tool def consultar_saldo(agencia: str, conta: str) -> dict: '''Consulta saldo em tempo real no core banking''' response = requests.get(f'{CORE_BANKING_URL}/saldo/{agencia}/{conta}') return response.json()

3

### APIs gRPC

Comunicação binária de alta performance.

Exemplo

@tool def validar_documento_ocr(doc_base64: str) -> dict: '''Valida documento com OCR Vertex AI''' stub = OCRServiceStub(channel) request = ValidateRequest(document=doc_base64) return stub.Validate(request)

4

### MCP (Model Context Protocol)

Protocolo padronizado da Anthropic para ferramentas.

Exemplo

@mcp_tool def buscar_docs_confluence(query: str, space: str) -> list: '''Busca documentação interna no Confluence''' return confluence.search(query, space=space)

5

### Queries de Banco

Acesso a dados estruturados com SQL. CUIDADO: SQL injection.

Exemplo

@tool def query_readonly(sql: str) -> list: """Query read-only no DW. SQL deve começar com SELECT.""" if not sql.upper().startswith("SELECT"): raise ValueError("Only SELECT queries allowed") return db.execute(sql).fetchall()

6

### Ferramentas de Sistema

Comandos shell. PERIGOSO - requer sandbox rigoroso.

Exemplo

@tool def shell_safe(cmd: str) -> str: '''Executa comando whitelisted em sandbox''' if cmd.split()[0] not in WHITELIST: raise PermissionError('Command not allowed') return subprocess.check_output(cmd, shell=True, timeout=5)

### Anatomia do Tool Schema

O LLM não "vê" o código Python, apenas o JSON Schema OpenAPI. A qualidade do schema impacta diretamente a precisão das chamadas.

```
{
  "name": "consultar_saldo",
  "description": "Consulta saldo em tempo real no core banking do Banco BV. Use quando cliente perguntar sobre saldo, extrato ou posição financeira.",
  "parameters": {
    "type": "object",
    "properties": {
      "agencia": {
        "type": "string",
        "description": "Código da agência com 4 dígitos. Exemplo: 0001",
        "pattern": "^[0-9]{4}$"
      },
      "conta": {
        "type": "string",
        "description": "Número da conta com dígito verificador. Formato: XXXXXX-X"
      },
      "tipo_conta": {
        "type": "string",
        "enum": ["corrente", "poupanca", "investimento"],
        "description": "Tipo da conta bancária"
      }
    },
    "required": ["agencia", "conta"]
  }
}
```

Regra de Ouro: O campo 'description' é o PROMPT da ferramenta!

### Classificação por Risco

Read-Only

Baixo

Consultar saldo, buscar documentos

Logging + Rate limiting

Write

Médio

Enviar email, atualizar CRM

Validação + Approval workflow

Financial

Alto

Transferência, aprovação de crédito

Human-in-the-Loop obrigatório

System

Crítico

Shell commands, SQL write, infra changes

Whitelist estrito + Sandbox + Approval

### Melhores Práticas

- [object Object]
- [object Object]
- [object Object]
- [object Object]
- [object Object]
- [object Object]
- [object Object]

### Exemplos de Implementação

#### Google ADK Custom Function Tool

```
from agents import Agent
from agents.tools import FunctionTool
from typing import Annotated

# 1. Definir função Python
def consultar_limite_credito(
    cpf: Annotated[str, "CPF do cliente (11 dígitos)"],
    produto: Annotated[str, "Tipo de crédito: pessoal, veicular, imobiliario"]
) -> dict:
    """Consulta limite pré-aprovado de crédito no Banco BV
    
    Args:
        cpf: CPF do cliente no formato 12345678900
        produto: Tipo de produto de crédito
        
    Returns:
        dict com limite_aprovado, taxa_juros, prazo_max
    """
    # Lógica de consulta ao sistema de crédito
    response = credit_api.get_limit(cpf=cpf, product=produto)
    return {
        "limite_aprovado": response.limit,
        "taxa_juros_mes": response.rate,
        "prazo_maximo_meses": response.max_term
    }

# 2. Criar FunctionTool
credit_tool = FunctionTool(consultar_limite_credito)

# 3. Adicionar ao Agent
agent = Agent(
    model="gemini-2.5-flash",
    tools=[credit_tool],
    instructions="Você é assistente de crédito do Banco BV"
)
```

Google ADK usa type hints e docstrings para gerar automaticamente o schema. Simples e pythônico.

#### LangChain @tool Decorator

```
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_vertexai import ChatVertexAI

# 1. Decorator @tool gera schema automaticamente
@tool
def validar_score_credito(cpf: str, score_minimo: int = 600) -> dict:
    """Valida score de crédito do cliente no SPC/Serasa
    
    Args:
        cpf: CPF do cliente (11 dígitos)
        score_minimo: Score mínimo aceitável (padrão: 600)
        
    Returns:
        dict: {aprovado: bool, score: int, restricoes: list}
    """
    score_data = credit_bureau.check(cpf)
    return {
        "aprovado": score_data.score >= score_minimo,
        "score": score_data.score,
        "restricoes": score_data.restrictions
    }

# 2. Criar agent com tool
llm = ChatVertexAI(model="gemini-2.5-flash", temperature=0)
agent = create_react_agent(
    llm=llm,
    tools=[validar_score_credito],
    prompt=react_prompt
)
agent_executor = AgentExecutor(agent=agent, tools=[validar_score_credito])
```

LangChain @tool decorator é conveniente e se integra nativamente com AgentExecutor e LCEL chains.

#### OpenAPI Tool Generation

```
# 1. Definir OpenAPI spec (ou importar de API existente)
openapi_spec = """
openapi: 3.0.0
info:
  title: BV Core Banking API
  version: 1.0.0
paths:
  /accounts/{account_id}/balance:
    get:
      operationId: get_account_balance
      summary: Get current account balance
      parameters:
        - name: account_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Account balance
          content:
            application/json:
              schema:
                type: object
                properties:
                  balance:
                    type: number
                  currency:
                    type: string
"""

# 2. Gerar tools automaticamente do OpenAPI spec
from langchain_community.agent_toolkits.openapi import OpenAPIToolkit
from langchain_community.utilities.requests import RequestsWrapper

requests_wrapper = RequestsWrapper(
    headers={"Authorization": f"Bearer {API_KEY}"}
)

toolkit = OpenAPIToolkit.from_text(
    openapi_spec,
    requests_wrapper=requests_wrapper
)

tools = toolkit.get_tools()
# tools agora contém get_account_balance automaticamente
```

Ideal para integrar APIs REST existentes. Schema já definido, basta apontar para OpenAPI spec.

#### Error Handling & Retry Pattern

```
from tenacity import retry, stop_after_attempt, wait_exponential
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def execute_tool_with_retry(function_call, max_retries=3):
    """Executa tool com retry automático em caso de erro
    
    Pattern:
    1. Validar args com Pydantic
    2. Executar tool
    3. Validar response
    4. Retry com backoff exponencial se falhar
    """
    try:
        # 1. Validar input
        if function_call.name == 'transferir':
            params = TransferenciaParams(**function_call.args)
        
        # 2. Executar tool
        result = execute_tool(function_call.name, params.dict())
        
        # 3. Validar output
        if not result.get('success'):
            logger.warning(f"Tool execution failed: {result.get('error')}")
            raise Exception(result.get('error'))
        
        return result
        
    except ValidationError as e:
        # Retornar erro estruturado ao LLM para retry
        logger.error(f"Validation error: {e.errors()}")
        return {
            "error": "validation_failed",
            "details": e.errors(),
            "retry_suggestion": "Check parameter types and constraints"
        }
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        raise  # Retry via tenacity
```

Pattern robusto: validação Pydantic + retry com exponential backoff + logging + error feedback ao LLM.

## Tool Calling Flow

Fluxo completo de uma chamada de ferramenta do prompt até a resposta final

1

### 1. Declaração

Definir function declarations (schema OpenAPI) e enviar com user prompt ao LLM

```
tools = [Tool(function_declarations=[get_weather_func])]
response = model.generate_content("What's the weather in Boston?", tools=tools)
```

2

### 2. Decisão do LLM

LLM analisa o prompt e decide se precisa chamar uma ferramenta ou responder diretamente

```
# LLM retorna function_call se determinar que precisa de dados externos
if response.candidates[0].function_calls:
    function_call = response.candidates[0].function_calls[0]
```

3

### 3. Function Call

LLM retorna function_call com name e args estruturados (não executa, apenas sugere)

```
# Exemplo de resposta:
{
  "name": "get_current_weather",
  "args": {"location": "Boston, MA"}
}
```

4

### 4. Execução da Tool

Aplicação executa a ferramenta externa (API, DB, sistema) com os args fornecidos

```
# App executa a ferramenta
if function_call.name == 'get_current_weather':
    api_response = weather_api.get(function_call.args['location'])
    # api_response = {'temp': 38, 'desc': 'Partly Cloudy'}
```

5

### 5. Function Response

Resultado da ferramenta é enviado de volta ao LLM como function_response

```
function_response = Part.from_function_response(
    name=function_call.name,
    response={'content': api_response}
)
```

6

### 6. Resposta Final

LLM incorpora o resultado da ferramenta e gera resposta em linguagem natural

```
# LLM gera: "The weather in Boston is 38°F and partly cloudy."
final_response = model.generate_content(
    [user_prompt, function_call, function_response],
    tools=tools
)
```

## Tool Calling Modes

### AUTO

Comportamento padrão. O LLM decide autonomamente se chama função ou responde em linguagem natural baseado no contexto.

Força

Mais flexível e natural

Fraqueza

LLM pode não chamar tool quando deveria

Caso de Uso

Modo padrão. Use quando o agente deve ter flexibilidade total.

```
response = model.generate_content(
    "What is the weather in Boston?",
    tools=[weather_tool],
    tool_config=ToolConfig(
        function_calling_config=ToolConfig.FunctionCallingConfig(
            mode=ToolConfig.FunctionCallingConfig.Mode.AUTO
        )
    )
)
```

### ANY

Força o LLM a SEMPRE prever pelo menos uma function call. Garante adherência ao schema da função.

Força

Garante structured output

Fraqueza

Menos natural, pode forçar calls desnecessários

Caso de Uso

Quando você REQUER uma chamada de função em cada resposta (ex: classificação obrigatória, extração estruturada).

```
tool_config=ToolConfig(
    function_calling_config=ToolConfig.FunctionCallingConfig(
        mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
        # Opcional: restringir a funções específicas
        allowed_function_names=["get_weather"]
    )
)
```

### NONE

PROÍBE o LLM de fazer function calls. Equivalente a não enviar function declarations.

Força

Controle total

Fraqueza

Remove capacidade de ação do agente

Caso de Uso

Desabilitar temporariamente function calling sem remover tool definitions.

```
tool_config=ToolConfig(
    function_calling_config=ToolConfig.FunctionCallingConfig(
        mode=ToolConfig.FunctionCallingConfig.Mode.NONE
    )
)
```

### VALIDATED (Preview)

Preview

LLM pode prever function calls OU linguagem natural, mas garante schema compliance. Com Gemini 3+, valida presença de required parameters.

Força

Balanceia flexibilidade e validação

Fraqueza

Preview - disponibilidade limitada

Caso de Uso

Quando precisa de flexibilidade do AUTO mas com garantias de validação (ex: workflows críticos).

```
# Preview feature - Gemini 3+ only
tool_config=ToolConfig(
    function_calling_config=ToolConfig.FunctionCallingConfig(
        mode=ToolConfig.FunctionCallingConfig.Mode.VALIDATED,
        allowed_function_names=["approve_loan", "reject_loan"]
    )
)
```

## Parallel Tool Calling

Quando o prompt requer múltiplas ferramentas, LLMs modernos (Gemini 2.5+, GPT-4o) podem chamar várias functions em paralelo na mesma resposta, reduzindo latência.

Exemplo de Prompt

User: "What's the weather difference between Boston and San Francisco?"

Resposta do LLM

```
# LLM retorna 2 function calls em paralelo:
[
  {name: "get_weather", args: {location: "Boston"}},
  {name: "get_weather", args: {location: "San Francisco"}}
]
```

Implementação

```
# Processar parallel calls
function_responses = []
for function_call in response.candidates[0].function_calls:
    if function_call.args['location'] == 'Boston':
        api_response = {'temp': 38, 'desc': 'Partly Cloudy'}
    elif function_call.args['location'] == 'San Francisco':
        api_response = {'temp': 58, 'desc': 'Sunny'}
    
    function_responses.append(
        Part.from_function_response(
            name=function_call.name,
            response={'content': api_response}
        )
    )

# Enviar TODAS as respostas de volta ao LLM
final = model.generate_content(
    [user_prompt, response.candidates[0].content, *function_responses],
    tools=[weather_tool]
)
# LLM: 'Boston is 38°F (partly cloudy), SF is 58°F (sunny). Difference: 20°F.'
```

Benefícios

- Reduz latência (1 round-trip vs múltiplos)
- Mais eficiente para queries independentes
- Suportado nativamente por Gemini 2.5+, GPT-4o, Claude 3.5

## Tool Schema (OpenAPI)

O LLM não "vê" o código Python, apenas o JSON Schema OpenAPI. A qualidade do schema impacta diretamente a precisão das chamadas.

Atributos OpenAPI

- type (required): OBJECT, STRING, INTEGER, NUMBER, BOOLEAN, ARRAY
- description (critical): Seja específico. LLM usa isso para decidir quando chamar.
- properties: Schema de cada parâmetro
- required: Lista de parâmetros obrigatórios
- enum: Para valores de conjunto finito (preferível vs descrição)
- format: date-time, email, uri, etc

Exemplo Completo

```
{
  "name": "consultar_saldo",
  "description": "Consulta saldo em tempo real no core banking do Banco BV. Use quando cliente perguntar sobre saldo, extrato ou posição financeira.",
  "parameters": {
    "type": "object",
    "properties": {
      "agencia": {
        "type": "string",
        "description": "Código da agência com 4 dígitos. Exemplo: 0001",
        "pattern": "^[0-9]{4}$"
      },
      "conta": {
        "type": "string",
        "description": "Número da conta com dígito verificador. Formato: XXXXXX-X"
      },
      "tipo_conta": {
        "type": "string",
        "enum": ["corrente", "poupanca", "investimento"],
        "description": "Tipo da conta bancária"
      }
    },
    "required": ["agencia", "conta"]
  }
}
```

512 function declarations por request (Gemini)

## Best Practices

#### Nomenclatura Clara

Function names: iniciar com letra/underscore, apenas a-z A-Z 0-9 _. -, max 64 chars. Seja descritivo: get_customer_balance vs get_bal.

#### Descrições Específicas

Seja extremamente claro. Ruim: "get weather". Bom: "Get current weather in a city. Use when user asks about temperature, conditions, or forecast."

#### Strong Typing

Use enum para conjuntos finitos. Use integer (não number) para inteiros. Especifique format quando aplicável (date-time, email, uri).

#### System Instructions

Inclua data/hora/localização atuais na system instruction quando tools usam esses parâmetros. Ex: 'Today is 2026-02-01, location: São Paulo, Brazil.'

#### Validação antes de executar

Para operações críticas (transferências, aprovações), SEMPRE validar com usuário antes de executar. Usar Human-in-the-Loop.

#### Tool Selection

Máximo 10-20 tools ativas por vez. Muitas tools aumentam risco de seleção incorreta. Use dynamic tool selection baseado no contexto.

#### Temperature baixa

Use temperature=0 ou próximo para function calling. Reduz alucinações e aumenta precisão na seleção de tools.

## Validação com Pydantic

Pydantic é o padrão de mercado para validação de tool parameters. Garante type safety, field validation e error handling robusto.

Benefícios

Type safety automática

Validação de campos (ge, le, regex, custom validators)

Error messages claros

Auto-completion no IDE

Geração automática de JSON Schema

Documentação automática

Exemplo com Pydantic

```
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

class TransferenciaParams(BaseModel):
    """Parâmetros validados para transferência bancária"""
    conta_origem: str = Field(pattern=r"^\d{6}-\d$")
    conta_destino: str = Field(pattern=r"^\d{6}-\d$")
    valor: Decimal = Field(gt=0, le=100000, description="Valor em R$")
    descricao: str = Field(max_length=140)
    
    @field_validator('valor')
    def validar_valor(cls, v):
        if v <= 0:
            raise ValueError('Valor deve ser positivo')
        if v > 100000:
            raise ValueError('Valor excede limite de R$ 100.000')
        return v

# Usar com FunctionDeclaration.from_func
@tool
def transferir(params: TransferenciaParams) -> dict:
    """Realiza transferência entre contas"""
    # params já validado pelo Pydantic
    return executar_transferencia(params.dict())
```

Error Handling

```
# Retry com feedback da validação
try:
    params = TransferenciaParams(**function_call.args)
except ValidationError as e:
    # Enviar erro de volta ao LLM para retry
    error_msg = f'Validation failed: {e.errors()}'
    return Command(update={'error': error_msg}, goto='retry_node')
```

## Implementações Práticas

1

### Google ADK Custom Function Tool

```
from agents import Agent
from agents.tools import FunctionTool
from typing import Annotated

# 1. Definir função Python
def consultar_limite_credito(
    cpf: Annotated[str, "CPF do cliente (11 dígitos)"],
    produto: Annotated[str, "Tipo de crédito: pessoal, veicular, imobiliario"]
) -> dict:
    """Consulta limite pré-aprovado de crédito no Banco BV
    
    Args:
        cpf: CPF do cliente no formato 12345678900
        produto: Tipo de produto de crédito
        
    Returns:
        dict com limite_aprovado, taxa_juros, prazo_max
    """
    # Lógica de consulta ao sistema de crédito
    response = credit_api.get_limit(cpf=cpf, product=produto)
    return {
        "limite_aprovado": response.limit,
        "taxa_juros_mes": response.rate,
        "prazo_maximo_meses": response.max_term
    }

# 2. Criar FunctionTool
credit_tool = FunctionTool(consultar_limite_credito)

# 3. Adicionar ao Agent
agent = Agent(
    model="gemini-2.5-flash",
    tools=[credit_tool],
    instructions="Você é assistente de crédito do Banco BV"
)
```

Explicação

Google ADK usa type hints e docstrings para gerar automaticamente o schema. Simples e pythônico.

2

### LangChain @tool Decorator

```
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_vertexai import ChatVertexAI

# 1. Decorator @tool gera schema automaticamente
@tool
def validar_score_credito(cpf: str, score_minimo: int = 600) -> dict:
    """Valida score de crédito do cliente no SPC/Serasa
    
    Args:
        cpf: CPF do cliente (11 dígitos)
        score_minimo: Score mínimo aceitável (padrão: 600)
        
    Returns:
        dict: {aprovado: bool, score: int, restricoes: list}
    """
    score_data = credit_bureau.check(cpf)
    return {
        "aprovado": score_data.score >= score_minimo,
        "score": score_data.score,
        "restricoes": score_data.restrictions
    }

# 2. Criar agent com tool
llm = ChatVertexAI(model="gemini-2.5-flash", temperature=0)
agent = create_react_agent(
    llm=llm,
    tools=[validar_score_credito],
    prompt=react_prompt
)
agent_executor = AgentExecutor(agent=agent, tools=[validar_score_credito])
```

Explicação

LangChain @tool decorator é conveniente e se integra nativamente com AgentExecutor e LCEL chains.

3

### OpenAPI Tool Generation

```
# 1. Definir OpenAPI spec (ou importar de API existente)
openapi_spec = """
openapi: 3.0.0
info:
  title: BV Core Banking API
  version: 1.0.0
paths:
  /accounts/{account_id}/balance:
    get:
      operationId: get_account_balance
      summary: Get current account balance
      parameters:
        - name: account_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Account balance
          content:
            application/json:
              schema:
                type: object
                properties:
                  balance:
                    type: number
                  currency:
                    type: string
"""

# 2. Gerar tools automaticamente do OpenAPI spec
from langchain_community.agent_toolkits.openapi import OpenAPIToolkit
from langchain_community.utilities.requests import RequestsWrapper

requests_wrapper = RequestsWrapper(
    headers={"Authorization": f"Bearer {API_KEY}"}
)

toolkit = OpenAPIToolkit.from_text(
    openapi_spec,
    requests_wrapper=requests_wrapper
)

tools = toolkit.get_tools()
# tools agora contém get_account_balance automaticamente
```

Explicação

Ideal para integrar APIs REST existentes. Schema já definido, basta apontar para OpenAPI spec.

4

### Error Handling & Retry Pattern

```
from tenacity import retry, stop_after_attempt, wait_exponential
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def execute_tool_with_retry(function_call, max_retries=3):
    """Executa tool com retry automático em caso de erro
    
    Pattern:
    1. Validar args com Pydantic
    2. Executar tool
    3. Validar response
    4. Retry com backoff exponencial se falhar
    """
    try:
        # 1. Validar input
        if function_call.name == 'transferir':
            params = TransferenciaParams(**function_call.args)
        
        # 2. Executar tool
        result = execute_tool(function_call.name, params.dict())
        
        # 3. Validar output
        if not result.get('success'):
            logger.warning(f"Tool execution failed: {result.get('error')}")
            raise Exception(result.get('error'))
        
        return result
        
    except ValidationError as e:
        # Retornar erro estruturado ao LLM para retry
        logger.error(f"Validation error: {e.errors()}")
        return {
            "error": "validation_failed",
            "details": e.errors(),
            "retry_suggestion": "Check parameter types and constraints"
        }
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        raise  # Retry via tenacity
```

Explicação

Pattern robusto: validação Pydantic + retry com exponential backoff + logging + error feedback ao LLM.

## Comparação de Frameworks

| Framework | Tipo | Facilidade | Schema Generation | Ecosistema | Parallel | Melhor Para |
| --- | --- | --- | --- | --- | --- | --- |
| Google ADK | Native SDK | Muito fácil | Automático (type hints + docstring) | Google Cloud, Gemini, Vertex AI | Sim | Gemini + Vertex AI, projetos Google-first |
| LangChain | Framework | Fácil | Automático (@tool decorator) | Multi-provider (OpenAI, Anthropic, Google, etc) | Sim | Multi-LLM, complex workflows, RAG integration |
| OpenAI SDK | Native SDK | Médio | Manual (JSON schema) | OpenAI models | Sim | GPT-4o/o1, OpenAI-first projects |
| MCP (Anthropic) | Protocol | Médio | Manual (MCP schema) | Cross-platform (desktop apps, IDEs) | Depende do server | Desktop integrations, IDE extensions, enterprise tools |

## Guardrails

Proteção e limites de comportamento do agente

Guardrails são limites programáticos que previnem outputs indesejados, protegem contra jailbreaks e garantem conformidade. São aplicados em múltiplas camadas: antes do LLM (input), depois do LLM (output), durante a execução (topical) e para segurança de conteúdo (safety).

### Referências Oficiais

Google Model Armor Lakera Guard (Check Point) NeMo Guardrails (NVIDIA) Azure AI Content Safety OpenAI Moderation API

## Soluções Enterprise COMPARATIVO

1

### Google Model Armor

Google Cloud Managed Service

Runtime security for generative and agentic AI. Protege prompts, respostas e interações de agentes com defesa híbrida (rules + ML + AI reasoning).

#### Features

- Prompt injection & jailbreak detection
- Sensitive data protection (PII, credentials)
- Malware detection & safe browsing
- Inline protection for Vertex AI & Gemini
- Model & cloud agnostic (REST API)
- PDF content scanning

#### Pontos Fortes

- Integração nativa com Google Cloud (Vertex AI, GKE, Gemini)
- Defesa híbrida: rules + ML + AI reasoning models
- Templates customizáveis com thresholds (LOW, MEDIUM, HIGH)
- Free tier: 2M tokens/mês

Latência

Baixa (<50ms)

Deployment

Cloud-native, inline ou API

Pricing

Free até 2M tokens/mês, depois $0.10/1M tokens

Caso de Uso

Customer service chatbots, AI copilots, content generation

Documentação Oficial

2

### Lakera Guard

Lakera (Check Point) SaaS Platform

AI security platform com detecção em tempo real de ameaças. Especializado em prompt injection com 0.01% false-positive rate.

#### Features

- Prompt injection (direct & indirect)
- Jailbreak detection
- Content moderation
- Data leakage prevention
- Malicious links detection
- System prompt leakage protection

#### Pontos Fortes

- Detecção de 15K+ threats/dia
- 0.01% false-positive rate
- <12ms latency média
- Suporte a 100+ linguagens
- API simples (/v2/guard endpoint)

Latência

Muito baixa (<12ms)

Deployment

SaaS API

Pricing

Enterprise (contato com vendas)

Caso de Uso

Aplicações GenAI enterprise, SaaS companies

Documentação Oficial

3

### NVIDIA NeMo Guardrails

NVIDIA Open Source + Microservice

Toolkit open-source com microservice enterprise. Oferece guardrails programáveis via Colang DSL para conversational AI.

#### Features

- Colang DSL para regras customizadas
- Content safety (LlamaGuard, NemoGuard 8B)
- Topical guardrails
- Jailbreak detection
- LangChain/LangGraph integration
- Kubernetes deployment

#### Pontos Fortes

- Open-source (5.6K GitHub stars)
- Máxima customização com Colang
- Python library + Microservice K8s
- Múltiplos modelos de safety (Llama 3.1, ActiveFence)
- Centralized hub architecture

Latência

Configurável (depende do modelo)

Deployment

Self-hosted, K8s, local dev

Pricing

Free (open-source)

Caso de Uso

Conversational AI, chatbots customizados, multi-tenant

Documentação Oficial

4

### Azure AI Content Safety

Microsoft Azure Managed Service

Content filtering integrado ao Azure AI Foundry. Ensemble de classificadores ML para 4 categorias de harm em 4 níveis de severidade.

#### Features

- 4 categorias: Violence, Hate, Sexual, Self-harm
- 4 severity levels: Safe, Low, Medium, High
- Prompt Shield (jailbreak detection)
- Protected material detection
- Multi-language support

#### Pontos Fortes

- Integração nativa com Azure OpenAI Service
- Config padrão: Medium threshold
- Suporte a imagens (image generation models)
- Compliance enterprise

Latência

Baixa

Deployment

Azure-native, inline

Pricing

Incluído no Azure AI Foundry

Caso de Uso

Azure-native apps, enterprise compliance

Documentação Oficial

5

### OpenAI Moderation API

OpenAI API

API de moderação de conteúdo simples e rápida. Categoriza conteúdo em harmful categories com scores de confiança.

#### Features

- Hate, harassment, self-harm, sexual
- Violence, sexual/minors
- Confidence scores por categoria
- Flags binários (flagged: true/false)

#### Pontos Fortes

- Latência muito baixa (<50ms)
- API simples (1 endpoint)
- Free para uso com OpenAI models
- Fácil integração

Latência

Muito baixa (<50ms)

Deployment

API cloud

Pricing

Free (com OpenAI models)

Caso de Uso

Moderação básica, MVP, prototipagem

Documentação Oficial

### Melhores Práticas

- Aplicar guardrails em múltiplas camadas (defense in depth)
- Configurar thresholds baseados em análise de risco do caso de uso
- Monitorar e logar todas as violações para análise
- Implementar fallbacks graceful quando guardrails bloqueiam
- Testar guardrails com red teaming e adversarial prompts
- Atualizar regras baseado em novos padrões de ataque

### Frameworks Disponíveis

#### Google Model Armor

Cloud Service

Força: Defesa híbrida (rules+ML+AI), inline Vertex AI, cloud-agnostic

Uso: Runtime security para Gemini/Vertex AI, agentic AI

#### Lakera Guard

SaaS Platform

Força: Melhor latência (<12ms), 0.01% false-positive, 100+ langs

Uso: Prompt injection detection enterprise

#### NeMo Guardrails

Open-source

Força: Regras declarativas Colang, máxima customização

Uso: Guardrails customizados complexos

#### Azure AI Content Safety

Cloud Service

Força: 4 categorias + severidades, multi-language

Uso: Safety guardrails enterprise (Azure-native)

#### OpenAI Moderation

API

Força: Rápido, baixa latência, simples

Uso: Moderação básica de conteúdo

### Exemplos de Implementação

#### Google Model Armor (Vertex AI Inline)

```
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel

# 1. Configurar Model Armor template
template_id = 'projects/PROJECT_ID/locations/us/templates/TEMPLATE_ID'

# 2. Criar modelo com guardrails inline
model = GenerativeModel(
    'gemini-2.5-pro',
    safety_settings={
        'model_armor_template': template_id,
        'threshold': 'MEDIUM'
    }
)

# 3. Usar normalmente - guardrails aplicados automaticamente
response = model.generate_content('user input')
```

Model Armor aplica guardrails inline no Vertex AI, sem wrapper extra

#### Lakera Guard (API)

```
import requests

# 1. Validar input antes do LLM
response = requests.post(
    'https://api.lakera.ai/v2/guard',
    headers={'Authorization': f'Bearer {API_KEY}'},
    json={'input': user_prompt}
)

if response.json()['flagged']:
    return {'error': 'Prompt bloqueado', 'reason': response.json()['category']}

# 2. Se passou, chamar LLM
llm_response = llm.invoke(user_prompt)

# 3. Validar output
output_check = requests.post(..., json={'input': llm_response})
return llm_response if not output_check.json()['flagged'] else sanitize(llm_response)
```

Lakera Guard como validação externa via API antes/depois do LLM

#### NeMo Guardrails (Open Source)

```
from nemoguardrails import RailsConfig, LLMRails
from langchain.chat_models import ChatOpenAI

# 1. Definir configuração Colang
config = RailsConfig.from_path('./guardrails_config')

# 2. Criar LLM base
llm = ChatOpenAI(model='gpt-4')

# 3. Wrappear com guardrails
guarded_llm = LLMRails(config, llm=llm)

# 4. Usar normalmente
response = guarded_llm.invoke('user input')
```

NeMo wrappeia o LLM e aplica regras Colang automaticamente

### Comparação de Soluções de Guardrails

| Solução | Vendor | Deployment | Latência | Pricing | Especialidade | Open Source |
| --- | --- | --- | --- | --- | --- | --- |
| Model Armor | Google | Cloud/Inline | <50ms | $0.10/1M | Vertex AI native | Não |
| Lakera Guard | Check Point | SaaS API | <12ms | Enterprise | Prompt injection | Não |
| NeMo Guardrails | NVIDIA | Self-hosted | Variável | Free | Colang DSL | Sim |
| Azure AI | Microsoft | Cloud/Inline | Baixa | Incluído | Azure native | Não |
| OpenAI Mod | OpenAI | API | <50ms | Free | Simples | Não |

## Orquestração

StateGraph para workflows complexos e controle de fluxo

Orquestração em LangGraph modela agent workflows como grafos usando message passing inspirado no sistema Pregel do Google. O grafo procede em 'super-steps' discretos: nodes ativos executam suas funções, enviam mensagens (state updates) para outros nodes via edges, e o processo continua até todos nodes votarem halt. Isso permite criar workflows complexos, com loops, condicionais, paralelismo e human-in-the-loop.

### Referências Oficiais

LangGraph Graph API Overview LangGraph Persistence & Checkpointing LangGraph Human-in-the-Loop LangGraph Subgraphs

### StateGraph

StateGraph é o core component do LangGraph. Nodes comunicam-se lendo e escrevendo em um state object compartilhado (como um 'whiteboard colaborativo'). Cada node recebe o state atual e retorna um dict contendo apenas as partes que quer atualizar. LangGraph aplica essas atualizações usando reducer functions.

### Nodes

Nodes são funções Python (síncronas ou assíncronas) que aceitam state, config (opcional) e runtime (opcional). Retornam um dict parcial com state updates. Convertidos automaticamente em RunnableLambda para batch/async support e tracing nativo.

### Edges

Edges determinam qual node executar next. Um node pode ter múltiplas outgoing edges - TODOS os destination nodes executam em PARALELO no próximo super-step.

### Melhores Práticas

- [object Object]
- [object Object]
- [object Object]
- [object Object]
- [object Object]
- [object Object]

### Exemplos de Implementação

#### ReAct Agent Básico com LangGraph

```
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_vertexai import ChatVertexAI

# 1. Definir tools
tools = [get_weather_tool, search_tool]

# 2. Definir agent node
def call_model(state: MessagesState):
    llm = ChatVertexAI(model="gemini-2.5-flash").bind_tools(tools)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 3. Build graph
builder = StateGraph(MessagesState)

builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode(tools))  # Prebuilt tool executor

builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    tools_condition,  # Se tool call → tools, senão → END
)
builder.add_edge("tools", "agent")  # Loop: tools → agent

graph = builder.compile()

# 4. Run
result = graph.invoke({"messages": [("user", "What's the weather in Boston?")]})
```

ReAct loop: Agent → Tools → Agent até não ter mais tool calls. MessagesState + tools_condition tornam isso trivial.

#### Multi-Agent Supervisor

```
from langgraph.graph import StateGraph, START, END
from typing import Literal

class SupervisorState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str

def supervisor(state: SupervisorState) -> Command[Literal["researcher", "writer", "reviewer"]]:
    """Supervisor decide qual agente chamar next"""
    llm = ChatVertexAI(model="gemini-2.5-flash")
    
    system = """Você é supervisor de equipe de 3 agentes:
    - researcher: busca informações
    - writer: escreve conteúdo
    - reviewer: revisa qualidade
    
    Baseado na conversa, escolha o próximo agente ou FINISH.
    """
    
    response = llm.invoke([SystemMessage(system)] + state["messages"])
    
    if "FINISH" in response.content:
        return Command(goto=END)
    
    agent = extract_agent_name(response.content)  # "researcher", "writer", "reviewer"
    return Command(
        update={"messages": [response]},
        goto=agent
    )

# Build graph
builder = StateGraph(SupervisorState)
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", researcher_agent)
builder.add_node("writer", writer_agent)
builder.add_node("reviewer", reviewer_agent)

builder.add_edge(START, "supervisor")
builder.add_edge("researcher", "supervisor")
builder.add_edge("writer", "supervisor")
builder.add_edge("reviewer", "supervisor")

graph = builder.compile()
```

Supervisor agent coordena múltiplos specialist agents. Cada specialist retorna ao supervisor que decide o próximo.

#### Human-in-the-Loop Approval Workflow

```
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

class ApprovalState(TypedDict):
    loan_application: dict
    ai_decision: dict
    human_approved: bool | None
    final_status: str

def ai_analysis(state: ApprovalState):
    """AI analisa aplicação de crédito"""
    analysis = analyze_credit_risk(state["loan_application"])
    return {"ai_decision": analysis}

def approval_gate(state: ApprovalState):
    """Interrompe para aprovação humana se valor alto"""
    if state["ai_decision"]["amount"] > 100000:
        # Mostrar para humano e pausar
        human_input = interrupt({
            "message": "Aprovação requerida para R$ 100k+",
            "ai_recommendation": state["ai_decision"]["recommendation"],
            "risk_score": state["ai_decision"]["risk_score"]
        })
        
        # Continua quando humano responder
        approved = human_input.get("approved", False)
    else:
        # Auto-aprovar valores baixos
        approved = state["ai_decision"]["recommendation"] == "APPROVE"
    
    return {"human_approved": approved}

def execute_decision(state: ApprovalState):
    if state["human_approved"]:
        execute_loan_approval(state["loan_application"])
        return {"final_status": "APPROVED"}
    else:
        return {"final_status": "REJECTED"}

# Build
builder = StateGraph(ApprovalState)
builder.add_node("analyze", ai_analysis)
builder.add_node("approval", approval_gate)
builder.add_node("execute", execute_decision)

builder.add_edge(START, "analyze")
builder.add_edge("analyze", "approval")
builder.add_edge("approval", "execute")
builder.add_edge("execute", END)

graph = builder.compile(checkpointer=MemorySaver())  # Checkpointer obrigatório para HITL

# Uso
config = {"configurable": {"thread_id": "loan-123"}}

# 1. Start (vai pausar em approval_gate)
result = graph.invoke({"loan_application": loan_data}, config=config)
# Retorna: {interrupt info}

# 2. Humano aprova
result = graph.invoke(
    Command(resume={"approved": True, "comments": "Verified"}),
    config=config
)
# Continua e completa
```

HITL para aprovações críticas. interrupt() pausa, Command(resume=...) continua com input humano.

#### Checkpointed Multi-Turn Chat

```
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.checkpoint.postgres import PostgresSaver
import psycopg

class ChatState(MessagesState):
    user_id: str
    session_metadata: dict

def chatbot(state: ChatState):
    llm = ChatVertexAI(model="gemini-2.5-flash")
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Build
builder = StateGraph(ChatState)
builder.add_node("chat", chatbot)
builder.add_edge(START, "chat")
builder.add_edge("chat", "chat")  # Loop indefinido

# Compile com PostgreSQL checkpointer
DB_URI = "postgresql://user:pass@localhost/chatdb"
with psycopg.connect(DB_URI, autocommit=True, row_factory=dict_row) as conn:
    checkpointer = PostgresSaver(conn)
    checkpointer.setup()  # Primeira vez: criar tabelas
    graph = builder.compile(checkpointer=checkpointer)

# Multi-turn conversation
thread_id = f"user-{user_id}-{session_id}"
config = {"configurable": {"thread_id": thread_id}}

# Turn 1
graph.invoke({
    "messages": [("user", "Qual meu saldo?")],
    "user_id": user_id
}, config=config)

# Turn 2 (carrega state do turn 1 automaticamente)
graph.invoke({
    "messages": [("user", "E meu limite de crédito?")]
}, config=config)  # Mesmo thread_id

# Turn N...
# Checkpointer persiste histórico completo no PostgreSQL
```

Conversas multi-turn com state persistence. PostgresSaver garante que histórico sobreviva restarts.

#### Subgraph para Specialist Agent

```
from langgraph.graph import StateGraph, START, END

# 1. Subgraph: SQL Specialist
class SQLState(TypedDict):
    query: str
    sql: str
    results: list

def sql_generator(state: SQLState):
    llm = ChatVertexAI(model="gemini-2.5-flash")
    sql = llm.invoke(f"Generate SQL for: {state['query']}")
    return {"sql": sql.content}

def sql_executor(state: SQLState):
    results = db.execute(state["sql"])
    return {"results": results}

sql_builder = StateGraph(SQLState)
sql_builder.add_node("generate", sql_generator)
sql_builder.add_node("execute", sql_executor)
sql_builder.add_edge(START, "generate")
sql_builder.add_edge("generate", "execute")
sql_builder.add_edge("execute", END)
sql_subgraph = sql_builder.compile()

# 2. Parent graph usa SQL subgraph
class ParentState(TypedDict):
    user_query: str
    query_type: str
    sql_results: list
    final_answer: str

def classifier(state: ParentState):
    # Classifica tipo de query
    return {"query_type": classify_query(state["user_query"])}

def route_query(state: ParentState) -> str:
    if state["query_type"] == "sql":
        return "sql_agent"
    return "general_agent"

def format_answer(state: ParentState):
    return {"final_answer": format(state["sql_results"])}

parent_builder = StateGraph(ParentState)
parent_builder.add_node("classifier", classifier)
parent_builder.add_node("sql_agent", sql_subgraph)  # Subgraph como node!
parent_builder.add_node("general_agent", general_llm)
parent_builder.add_node("formatter", format_answer)

parent_builder.add_edge(START, "classifier")
parent_builder.add_conditional_edges("classifier", route_query)
parent_builder.add_edge("sql_agent", "formatter")
parent_builder.add_edge("general_agent", END)
parent_builder.add_edge("formatter", END)

graph = parent_builder.compile()
```

Subgraphs permitem modularização. SQL specialist é self-contained, reusável em múltiplos parent graphs.

## Best Practices

#### State Schema Design

Mantenha state flat quando possível. Use Pydantic apenas se precisa validation. TypedDict é mais rápido para maioria dos casos.

#### Reducer Selection

Default (override) para valores simples. operator.add para listas. add_messages para chat history. Custom reducer para lógica complexa de merge.

#### Checkpointing Strategy

MemorySaver para dev/test. PostgresSaver para production. Sempre use checkpointer se tiver HITL. Use thread_id único por usuário/sessão.

#### Error Handling

Nodes podem retornar errors no state. Adicione error_handler node que routes baseado em error type. Use try/except dentro de nodes.

#### Testing Patterns

Test nodes individualmente (são funções Python). Mock tools durante testes. Use MemorySaver para testes de integration. Test conditional edges separadamente.

#### Graph Complexity

Máximo 10-15 nodes por graph. Use subgraphs para modularizar. Prefira conditional edges a muitos nodes de routing. Documente decisões de routing.

## Implementações Práticas

1

### ReAct Agent Básico com LangGraph

```
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_vertexai import ChatVertexAI

# 1. Definir tools
tools = [get_weather_tool, search_tool]

# 2. Definir agent node
def call_model(state: MessagesState):
    llm = ChatVertexAI(model="gemini-2.5-flash").bind_tools(tools)
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# 3. Build graph
builder = StateGraph(MessagesState)

builder.add_node("agent", call_model)
builder.add_node("tools", ToolNode(tools))  # Prebuilt tool executor

builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    tools_condition,  # Se tool call → tools, senão → END
)
builder.add_edge("tools", "agent")  # Loop: tools → agent

graph = builder.compile()

# 4. Run
result = graph.invoke({"messages": [("user", "What's the weather in Boston?")]})
```

Explicação

ReAct loop: Agent → Tools → Agent até não ter mais tool calls. MessagesState + tools_condition tornam isso trivial.

2

### Multi-Agent Supervisor

```
from langgraph.graph import StateGraph, START, END
from typing import Literal

class SupervisorState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str

def supervisor(state: SupervisorState) -> Command[Literal["researcher", "writer", "reviewer"]]:
    """Supervisor decide qual agente chamar next"""
    llm = ChatVertexAI(model="gemini-2.5-flash")
    
    system = """Você é supervisor de equipe de 3 agentes:
    - researcher: busca informações
    - writer: escreve conteúdo
    - reviewer: revisa qualidade
    
    Baseado na conversa, escolha o próximo agente ou FINISH.
    """
    
    response = llm.invoke([SystemMessage(system)] + state["messages"])
    
    if "FINISH" in response.content:
        return Command(goto=END)
    
    agent = extract_agent_name(response.content)  # "researcher", "writer", "reviewer"
    return Command(
        update={"messages": [response]},
        goto=agent
    )

# Build graph
builder = StateGraph(SupervisorState)
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", researcher_agent)
builder.add_node("writer", writer_agent)
builder.add_node("reviewer", reviewer_agent)

builder.add_edge(START, "supervisor")
builder.add_edge("researcher", "supervisor")
builder.add_edge("writer", "supervisor")
builder.add_edge("reviewer", "supervisor")

graph = builder.compile()
```

Explicação

Supervisor agent coordena múltiplos specialist agents. Cada specialist retorna ao supervisor que decide o próximo.

3

### Human-in-the-Loop Approval Workflow

```
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

class ApprovalState(TypedDict):
    loan_application: dict
    ai_decision: dict
    human_approved: bool | None
    final_status: str

def ai_analysis(state: ApprovalState):
    """AI analisa aplicação de crédito"""
    analysis = analyze_credit_risk(state["loan_application"])
    return {"ai_decision": analysis}

def approval_gate(state: ApprovalState):
    """Interrompe para aprovação humana se valor alto"""
    if state["ai_decision"]["amount"] > 100000:
        # Mostrar para humano e pausar
        human_input = interrupt({
            "message": "Aprovação requerida para R$ 100k+",
            "ai_recommendation": state["ai_decision"]["recommendation"],
            "risk_score": state["ai_decision"]["risk_score"]
        })
        
        # Continua quando humano responder
        approved = human_input.get("approved", False)
    else:
        # Auto-aprovar valores baixos
        approved = state["ai_decision"]["recommendation"] == "APPROVE"
    
    return {"human_approved": approved}

def execute_decision(state: ApprovalState):
    if state["human_approved"]:
        execute_loan_approval(state["loan_application"])
        return {"final_status": "APPROVED"}
    else:
        return {"final_status": "REJECTED"}

# Build
builder = StateGraph(ApprovalState)
builder.add_node("analyze", ai_analysis)
builder.add_node("approval", approval_gate)
builder.add_node("execute", execute_decision)

builder.add_edge(START, "analyze")
builder.add_edge("analyze", "approval")
builder.add_edge("approval", "execute")
builder.add_edge("execute", END)

graph = builder.compile(checkpointer=MemorySaver())  # Checkpointer obrigatório para HITL

# Uso
config = {"configurable": {"thread_id": "loan-123"}}

# 1. Start (vai pausar em approval_gate)
result = graph.invoke({"loan_application": loan_data}, config=config)
# Retorna: {interrupt info}

# 2. Humano aprova
result = graph.invoke(
    Command(resume={"approved": True, "comments": "Verified"}),
    config=config
)
# Continua e completa
```

Explicação

HITL para aprovações críticas. interrupt() pausa, Command(resume=...) continua com input humano.

4

### Checkpointed Multi-Turn Chat

```
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.checkpoint.postgres import PostgresSaver
import psycopg

class ChatState(MessagesState):
    user_id: str
    session_metadata: dict

def chatbot(state: ChatState):
    llm = ChatVertexAI(model="gemini-2.5-flash")
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Build
builder = StateGraph(ChatState)
builder.add_node("chat", chatbot)
builder.add_edge(START, "chat")
builder.add_edge("chat", "chat")  # Loop indefinido

# Compile com PostgreSQL checkpointer
DB_URI = "postgresql://user:pass@localhost/chatdb"
with psycopg.connect(DB_URI, autocommit=True, row_factory=dict_row) as conn:
    checkpointer = PostgresSaver(conn)
    checkpointer.setup()  # Primeira vez: criar tabelas
    graph = builder.compile(checkpointer=checkpointer)

# Multi-turn conversation
thread_id = f"user-{user_id}-{session_id}"
config = {"configurable": {"thread_id": thread_id}}

# Turn 1
graph.invoke({
    "messages": [("user", "Qual meu saldo?")],
    "user_id": user_id
}, config=config)

# Turn 2 (carrega state do turn 1 automaticamente)
graph.invoke({
    "messages": [("user", "E meu limite de crédito?")]
}, config=config)  # Mesmo thread_id

# Turn N...
# Checkpointer persiste histórico completo no PostgreSQL
```

Explicação

Conversas multi-turn com state persistence. PostgresSaver garante que histórico sobreviva restarts.

5

### Subgraph para Specialist Agent

```
from langgraph.graph import StateGraph, START, END

# 1. Subgraph: SQL Specialist
class SQLState(TypedDict):
    query: str
    sql: str
    results: list

def sql_generator(state: SQLState):
    llm = ChatVertexAI(model="gemini-2.5-flash")
    sql = llm.invoke(f"Generate SQL for: {state['query']}")
    return {"sql": sql.content}

def sql_executor(state: SQLState):
    results = db.execute(state["sql"])
    return {"results": results}

sql_builder = StateGraph(SQLState)
sql_builder.add_node("generate", sql_generator)
sql_builder.add_node("execute", sql_executor)
sql_builder.add_edge(START, "generate")
sql_builder.add_edge("generate", "execute")
sql_builder.add_edge("execute", END)
sql_subgraph = sql_builder.compile()

# 2. Parent graph usa SQL subgraph
class ParentState(TypedDict):
    user_query: str
    query_type: str
    sql_results: list
    final_answer: str

def classifier(state: ParentState):
    # Classifica tipo de query
    return {"query_type": classify_query(state["user_query"])}

def route_query(state: ParentState) -> str:
    if state["query_type"] == "sql":
        return "sql_agent"
    return "general_agent"

def format_answer(state: ParentState):
    return {"final_answer": format(state["sql_results"])}

parent_builder = StateGraph(ParentState)
parent_builder.add_node("classifier", classifier)
parent_builder.add_node("sql_agent", sql_subgraph)  # Subgraph como node!
parent_builder.add_node("general_agent", general_llm)
parent_builder.add_node("formatter", format_answer)

parent_builder.add_edge(START, "classifier")
parent_builder.add_conditional_edges("classifier", route_query)
parent_builder.add_edge("sql_agent", "formatter")
parent_builder.add_edge("general_agent", END)
parent_builder.add_edge("formatter", END)

graph = parent_builder.compile()
```

Explicação

Subgraphs permitem modularização. SQL specialist é self-contained, reusável em múltiplos parent graphs.

## Conceitos Fundamentais

1

### StateGraph

Classe principal para construir grafos stateful

StateGraph é o core component do LangGraph. Nodes comunicam-se lendo e escrevendo em um state object compartilhado (como um 'whiteboard colaborativo'). Cada node recebe o state atual e retorna um dict contendo apenas as partes que quer atualizar. LangGraph aplica essas atualizações usando reducer functions.

#### State Schema

Define a estrutura do state usando TypedDict ou Pydantic BaseModel

```
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]  # Lista de mensagens com reducer
    documents: list[str]  # Override default
    approved: bool

# Ou com Pydantic (mais validation)
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    messages: list = Field(default_factory=list)
    query: str
    result: str | None = None
```

#### Reducers

Funções que determinam COMO aplicar state updates. Cada chave tem seu próprio reducer.

##### Default (Override)

Sem reducer explícito = sempre sobrescreve

```
class State(TypedDict):
    foo: int  # Sempre override
# Input: {'foo': 1}, Update: {'foo': 2} → State: {'foo': 2}
```

##### operator.add

Concatena listas, soma números

```
from operator import add

class State(TypedDict):
    bar: Annotated[list[str], add]
# Input: {'bar': ['hi']}, Update: {'bar': ['bye']} → State: {'bar': ['hi', 'bye']}
```

##### add_messages

Reducer especial para mensagens. Append novos + update existentes (por ID)

```
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
# Mantém IDs, permite updates de mensagens existentes
```

##### Custom Reducer

Função personalizada (current, update) -> new

```
def merge_dicts(current: dict, update: dict) -> dict:
    return {**current, **update}

class State(TypedDict):
    metadata: Annotated[dict, merge_dicts]
```

2

### Nodes

Python functions que executam a lógica do agente

Nodes são funções Python (síncronas ou assíncronas) que aceitam state, config (opcional) e runtime (opcional). Retornam um dict parcial com state updates. Convertidos automaticamente em RunnableLambda para batch/async support e tracing nativo.

Assinatura

```
def my_node(state: State) -> dict:
    return {'result': 'done'}

# Com config para thread_id, tags, etc
def node_with_config(state: State, config: RunnableConfig) -> dict:
    thread_id = config['configurable']['thread_id']
    return {'result': f'thread: {thread_id}'}

# Com runtime para context
def node_with_runtime(state: State, runtime: Runtime) -> dict:
    user_id = runtime.context.user_id
    return {'result': f'user: {user_id}'}
```

#### Special Nodes

##### START

Virtual node que envia user input ao graph. Referenciado para definir entry point.

```
from langgraph.graph import START
graph.add_edge(START, 'first_node')
```

##### END

Virtual node que representa terminal node. Referenciado quando não há mais ações.

```
from langgraph.graph import END
graph.add_edge('final_node', END)
```

3

### Edges

Definem routing e fluxo de execução entre nodes

Edges determinam qual node executar next. Um node pode ter múltiplas outgoing edges - TODOS os destination nodes executam em PARALELO no próximo super-step.

#### Tipos de Edges

##### Normal Edge

Sempre vai de A → B. Sem lógica condicional.

```
graph.add_edge('node_a', 'node_b')
# node_a sempre executa node_b em seguida
```

Caso de Uso: Fluxo linear determinístico

##### Conditional Edge

Chama routing function para decidir qual(is) node(s) executar next

```
def route_decision(state: State) -> str:
    if state['approved']:
        return 'execute_node'
    return 'reject_node'

graph.add_conditional_edges(
    'review_node',
    route_decision,
    {'execute_node': 'execute_node', 'reject_node': 'reject_node'}
)
```

Caso de Uso: Branching condicional, approval workflows

##### Entry Point

Primeiro(s) node(s) a executar quando graph inicia

```
from langgraph.graph import START
graph.add_edge(START, 'first_node')
```

Caso de Uso: Definir ponto de entrada do graph

##### Conditional Entry

Routing function decide qual node iniciar baseado em input

```
def route_start(state: State) -> str:
    if state['query_type'] == 'sql':
        return 'sql_agent'
    return 'general_agent'

graph.add_conditional_edges(START, route_start)
```

Caso de Uso: Dynamic entry point baseado em input type

##### Send (Map-Reduce)

Cria edges dinâmicos em runtime. Essencial para map-reduce patterns.

```
from langgraph.types import Send

def fan_out(state: State):
    # Criar um Send para cada item
    return [
        Send('process_item', {'item': item})
        for item in state['items']
    ]

graph.add_conditional_edges('generate_items', fan_out)
```

Caso de Uso: Fan-out/fan-in, processar lista de tarefas em paralelo

##### Command

Combina state update + routing na mesma função. Alternativa a conditional edges.

```
from langgraph.types import Command
from typing import Literal

def my_node(state: State) -> Command[Literal['next_node']]:
    # Atualizar state E rotear
    return Command(
        update={'status': 'processed'},
        goto='next_node'
    )

# Command não substitui static edges, adiciona dinâmico
```

Caso de Uso: Quando precisa ATUALIZAR state e DECIDIR routing no mesmo node

## Checkpointing & Persistence

Salva state do graph a cada super-step, permitindo pause/resume, time travel e debugging. Essencial para human-in-the-loop e long-running workflows.

#### Por que usar checkpointing?

- Pause/resume execution (HITL workflows)
- Time travel: voltar a estados anteriores
- Debugging: inspecionar state a cada passo
- Fault tolerance: continuar após crash
- Multi-turn conversations com state persistence

#### MemorySaver

In-memory checkpointer. Rápido, mas perde state ao reiniciar processo.

Caso de Uso: Development, testing, demos, single-session apps

Setup

```
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Invocar com thread_id para persistir state
config = {'configurable': {'thread_id': 'thread-1'}}
result = graph.invoke(input, config=config)
```

Prós

- Simples
- Sem deps externas
- Zero latência

Contras

- Não persiste entre restarts
- Não escalável (single process)

#### PostgresSaver

Persiste checkpoints em PostgreSQL. Production-ready, suporta múltiplos workers.

Caso de Uso: Production apps, multi-user, distributed systems, long-term persistence

Setup

```
from langgraph.checkpoint.postgres import PostgresSaver
import psycopg

# 1. Setup database (primeira vez)
DB_URI = 'postgresql://user:pass@localhost:5432/langgraph'

with psycopg.connect(DB_URI, autocommit=True, row_factory=dict_row) as conn:
    checkpointer = PostgresSaver(conn)
    checkpointer.setup()  # Cria tabelas

# 2. Usar com graph
with psycopg.connect(DB_URI, autocommit=True, row_factory=dict_row) as conn:
    checkpointer = PostgresSaver(conn)
    graph = builder.compile(checkpointer=checkpointer)
    
    result = graph.invoke(
        input,
        config={'configurable': {'thread_id': 'user-123'}}
    )
```

Prós

- Persistência durável
- Multi-worker support
- Time travel queries
- Escalável

Contras

- Requer PostgreSQL
- Latência de DB
- Mais complexidade

| Feature | MemorySaver | PostgresSaver |
| --- | --- | --- |
| Persistência | RAM (volátil) | PostgreSQL (durável) |
| Multi-worker | Não | Sim |
| Setup | Imediato | Requer DB + schema |
| Latência | Zero | ~10-50ms |
| Use Case | Dev/Test | Production |

Time Travel

```
# Time Travel: voltar a checkpoint anterior
from langgraph.checkpoint import CheckpointSelector

# Listar checkpoints
checkpoints = list(graph.checkpointer.list(
    config={'configurable': {'thread_id': 'thread-1'}}
))

# Voltar para checkpoint específico
old_config = checkpoints[2].config  # 3º checkpoint
result = graph.invoke(None, config=old_config)  # Continua daquele ponto
```

## Human-in-the-Loop (HITL)

Interromper execução do graph para aguardar input/approval humano, depois resumir. Essencial para workflows de alto risco.

#### Padrões Comuns

Pause using interrupt - Parar para revisão humana

Resume with input - Continuar com dados do usuário

Approve/Reject - Validação de decisões críticas

Review and edit state - Humano modifica state antes de continuar

#### Implementação com interrupt

Usar graph.interrupt() ou configurar interrupt_before/interrupt_after nos nodes

```
from langgraph.types import Command, interrupt

def approval_node(state: State):
    # Mostrar proposta ao usuário e interromper
    value_to_approve = interrupt({'proposal': state['proposal']})
    
    # Execução pausa aqui. Retorna control ao usuário.
    # Quando resumir, value_to_approve conterá o input do usuário
    
    if value_to_approve.get('approved'):
        return Command(update={'status': 'approved'}, goto='execute_node')
    else:
        return Command(update={'status': 'rejected'}, goto='reject_node')

# Ou configurar interrupt no compile
graph = builder.compile(
    checkpointer=memory,
    interrupt_before=['approval_node']  # Sempre pausa antes deste node
)
```

Workflow Completo

```
# 1. Start graph (pausa em approval_node)
config = {'configurable': {'thread_id': 'thread-1'}}
result = graph.invoke(input, config=config)
# Graph para em approval_node, retorna state atual

# 2. Usuário revisa e aprova
approval_input = {'approved': True, 'comments': 'LGTM'}

# 3. Resume com input do usuário
result = graph.invoke(
    Command(resume=approval_input),
    config=config  # Mesmo thread_id
)
# Graph continua de onde parou, usando approval_input
```

#### Casos de Uso

##### Aprovação de Crédito

LLM analisa, humano aprova valores acima de threshold

##### Code Review

Agent gera código, dev revisa antes de deploy

##### Content Moderation

AI filtra, moderador humano decide casos edge

##### Financial Transfers

Dupla aprovação para transferências grandes

## Subgraphs

Um graph pode ser usado como node dentro de outro graph. Permite composição hierárquica e arquitetura modular.

#### Casos de Uso

- Multi-agent systems: cada agente é um subgraph
- Reutilização: mesmo subgraph em múltiplos graphs
- Dev distribuído: times trabalham em subgraphs independentes
- Isolamento: subgraph com state privado

Implementação Básica

```
# 1. Criar subgraph
sub_builder = StateGraph(SubState)
sub_builder.add_node('sub_node', sub_function)
sub_builder.add_edge(START, 'sub_node')
sub_builder.add_edge('sub_node', END)
subgraph = sub_builder.compile()

# 2. Adicionar subgraph como node no parent graph
parent_builder = StateGraph(ParentState)
parent_builder.add_node('subgraph_node', subgraph)  # Subgraph como node!
parent_builder.add_edge(START, 'subgraph_node')
parent_builder.add_edge('subgraph_node', END)

parent_graph = parent_builder.compile()
```

#### Navegar para Parent Graph

De dentro de um subgraph node, pode navegar para node no parent graph usando Command.PARENT

```
from langgraph.types import Command
from typing import Literal

def subgraph_node(state: SubState) -> Command[Literal['other_parent_node']]:
    # Navegar para node no parent graph
    return Command(
        update={'result': 'done in subgraph'},
        goto='other_parent_node',  # Node no parent graph
        graph=Command.PARENT  # Especifica: vá para parent
    )

# IMPORTANTE: Se key é compartilhado entre parent e sub,
# DEVE definir reducer no parent state para a key
```

#### Limitações

- Com checkpointing: não pode chamar subgraph múltiplas vezes imperativamente dentro de um node
- Workaround: compile subgraph com checkpointer=False se não precisa de interrupts
- Ou: usar Send API em vez de chamadas imperativas

## Streaming

Stream outputs em real-time durante execução do graph. Essencial para UIs responsivas.

#### values

Stream o state COMPLETO após cada super-step

```
for chunk in graph.stream(input, stream_mode='values'):
    print(chunk)  # State completo a cada step
```

#### updates

Stream apenas os UPDATES (deltas) de cada node

```
for chunk in graph.stream(input, stream_mode='updates'):
    print(chunk)  # {'node_name': {'key': 'value'}}
```

#### debug

Stream informações detalhadas de debug (metadata, IDs, etc)

```
for chunk in graph.stream(input, stream_mode='debug'):
    print(chunk)  # Metadata, checkpoint IDs, node info
```

## Recursion Limit

Limite de super-steps que o graph pode executar. Previne loops infinitos.

Default

1000 steps (padrão desde v1.0.6)

Configuração

```
result = graph.invoke(
    input,
    config={'recursion_limit': 50}  # Limit para 50 steps
)
```

#### RemainingSteps Managed Value

Acessa quantos steps restam antes do limit. Permite graceful degradation.

```
from langgraph.managed import RemainingSteps

class State(TypedDict):
    remaining_steps: RemainingSteps  # Auto-populated

def reasoning_node(state: State):
    remaining = state['remaining_steps']
    
    if remaining <= 2:
        # Approaching limit, wrap up
        return {'result': 'Partial answer due to complexity'}
    
    # Continue normal processing
    return {'result': 'thinking...'}
```

#### Proactive vs Reactive Handling

```
# Proactive: detectar dentro do graph
def route_decision(state: State) -> Literal['continue', 'fallback']:
    if state['remaining_steps'] <= 5:
        return 'fallback'  # Route para fallback node
    return 'continue'

# Reactive: catch externamente
try:
    result = graph.invoke(input, config={'recursion_limit': 100})
except GraphRecursionError:
    result = {'error': 'Task too complex, try simpler query'}
```

## Percepção

Receber input do ambiente

Montagem de contexto, recuperação RAG, parsing de inputs multimodais

## Raciocínio

Processar e decidir

Chain-of-thought, planejamento multi-step, decomposição de tarefas

## Ação

Executar decisão

Tool calling, API requests, execução de código, interação com sistemas

## Observação

Avaliar resultado

Parse de respostas, atualização de estado, detecção de erros

## Vertex AI Agent Builder

Plataforma completa para construir, escalar e governar agentes de IA em produção

Vertex AI Agent Builder é uma suite de produtos que ajuda desenvolvedores a construir, escalar e governar agentes de IA em produção. Fornece uma base full-stack e segura que suporta todo o ciclo de vida dos agentes.

### Referências Oficiais

Vertex AI Agent Builder Documentation Agent Builder Overview Release Notes

## Componentes

1

### Build

Ferramentas para desenvolvimento de agentes

#### Agent Development Kit (ADK)

Framework open-source que simplifica a construção de sistemas multi-agent sofisticados mantendo controle preciso sobre comportamento

- Model-agnostic e deployment-agnostic
- Suporte a Python, TypeScript, Go, Java
- Patterns de orquestração built-in
- Avaliação integrada

#### Agent Garden (Preview)

Biblioteca no Google Cloud console com agentes pré-construídos e ferramentas reutilizáveis

- Templates prontos para uso
- Best practices incorporadas
- Acelera desenvolvimento
- Customização facilitada

#### Agent Designer (Preview)

Designer visual low-code disponível desde dezembro de 2025

- Design visual de workflows
- Teste antes de codificar
- Transição suave para código
- Prototipagem rápida

2

### Scale

Infraestrutura gerenciada para produção

#### Vertex AI Agent Engine

Conjunto de serviços para deploy, gerenciamento e escalabilidade de agentes em produção

- Fully-managed runtime
- Sessions (GA desde 17/12/2025)
- Memory Bank (GA desde 17/12/2025)
- Code Execution
- Evaluation built-in

3

### Govern

Controle, segurança e compliance

#### Cloud API Registry (Preview)

Gerenciamento de MCP servers e tools

- Registro centralizado de APIs
- Versionamento de tools
- Controle de acesso
- Auditoria

## Timeline de Lançamentos

### Dezembro 2025

- • Sessions e Memory Bank GA (17/12/2025)
- • Agent Designer Preview lançado
- • Agent Engine expandido para novos regions

### Janeiro-Fevereiro 2026

- • Redução de preços Agent Engine Runtime
- • Cloud API Registry Preview
- • Cobrança Sessions/Memory Bank/Code Execution inicia (11/02/2026)

## Regiões Disponíveis

us-central1 (Iowa)

europe-west1 (Belgium)

europe-west3 (Frankfurt)

europe-west4 (Netherlands)

europe-west8 (Milan)

europe-west9 (Paris)

europe-southwest1 (Madrid)

europe-north1 (Finland)

europe-west2 (London)

europe-west6 (Zurich)

asia-northeast1 (Tokyo)

asia-northeast3 (Seoul)

asia-southeast1 (Singapore)

asia-east1 (Taiwan)

asia-south1 (Mumbai)

australia-southeast1 (Sydney)

northamerica-northeast1 (Montreal)

southamerica-east1 (São Paulo)

## Vertex AI Agent Engine

Runtime gerenciado para deploy e escala de agentes em produção

Vertex AI Agent Engine é um conjunto de serviços gerenciados que permite deploy, gerenciamento e escalabilidade de agentes de IA em produção. Inclui runtime fully-managed, persistência de estado, memória de longo prazo e execução de código em sandbox seguro.

### Referências Oficiais

Agent Engine Overview Sessions Documentation Memory Bank Documentation Code Execution Documentation

## Serviços Gerenciados

### Sessions

GA desde 17/12/2025

Mantém histórico de interações entre usuários e agentes, fornecendo memória de longo prazo e contexto de conversação

#### Features

##### Session

Sequências cronológicas de mensagens e ações para interações usuário-agente em andamento

##### Event

Armazena conteúdo de conversação e ações do agente como chamadas de função

##### State

Mantém dados temporários relevantes durante conversas atuais

##### Memory

Informações personalizadas acessíveis através de múltiplas sessões para usuários individuais

#### Casos de Uso

- Iniciar novas conversas
- Resumir conversas existentes
- Salvar progresso
- Listar histórico de conversas
- Limpeza de dados

```
from vertexai import agent_engine

# Criar nova session
session = agent_engine.create_session(
    agent_id='my-agent',
    user_id='user-123'
)

# Enviar mensagem
response = session.send_message(
    'Qual meu saldo?',
    session_id=session.id
)

# Resumir session
resume_response = session.resume(
    session_id=session.id,
    new_message='E meu limite de crédito?'
)
```

### Memory Bank

GA desde 17/12/2025

Gera dinamicamente memórias de longo prazo baseadas em conversas de usuários, permitindo personalização e continuidade entre sessões

#### Features

##### Memory Generation

Criar, refinar e gerenciar memórias usando LLMs

##### Memory Extraction

Extrair informações significativas de dados fonte

##### Memory Consolidation

Consolidar novas informações com memórias existentes

##### Asynchronous Generation

Gerar memórias em background sem bloquear agentes

##### Customizable Extraction

Configurar tópicos significativos e exemplos few-shot

##### Multimodal Understanding

Processar informações multimodais para insights textuais

##### Data Isolation

Recuperação de memória isolada por identidades específicas

#### Arquitetura

Conversation → Extract → LLM Analysis → Consolidate → Memory Store → Retrieval

```
from vertexai import agent_engine

# Criar Memory Bank
memory_bank = agent_engine.MemoryBank(
    name='customer-memories',
    retention_days=365
)

# Adicionar memória
memory_bank.add_memory(
    user_id='user-123',
    content='Cliente prefere atendimento por chat',
    category='preference',
    metadata={'confidence': 0.95}
)

# Recuperar memórias relevantes
memories = memory_bank.search(
    user_id='user-123',
    query='preferências de atendimento',
    top_k=5
)
```

### Code Execution

Preview (us-central1 only)

Permite agentes gerarem e executarem código em ambientes sandbox seguros e isolados

#### Features

##### Fast Execution

Sandboxes criam e executam código em menos de 1 segundo

##### File I/O

Suporte para entrada/saída de arquivos até 100MB por request/response

##### Stateful Execution

Sandboxes mantêm estado (memória) por até 14 dias com TTL configurável

##### Framework Agnostic

Funciona com qualquer framework de agente e modelo generativo

#### Casos de Uso

- Análise de dados on-the-fly
- Geração de visualizações
- Cálculos complexos
- Processamento de arquivos
- Prototipagem rápida

#### Limitações

- • Apenas região us-central1
- • Máximo 100MB por arquivo
- • TTL máximo 14 dias
- • Sem acesso a rede externa do sandbox

```
from vertexai.agent_engine import CodeExecutor

# Criar executor
executor = CodeExecutor(
    runtime='python3.11',
    ttl_seconds=3600  # 1 hora
)

# Executar código
result = executor.execute("""
import pandas as pd
import numpy as np

# Análise de dados
df = pd.DataFrame({
    'valor': [100, 200, 150, 300],
    'categoria': ['A', 'B', 'A', 'B']
})

print(df.groupby('categoria')['valor'].mean())
""")

print(result.output)
print(result.execution_time)
```

## Pricing

Preços Agent Engine (cobrança iniciou 11/02/2026)

| Serviço | Preço | Notas |
| --- | --- | --- |
| Sessions | $0.0005 por event stored | Inclui storage e retrieval |
| Memory Bank | $0.001 por memory generation + storage | Retrieval incluído |
| Code Execution | $0.02 per execution minute | Storage de state incluído no TTL |
| Agent Engine Runtime | Reduzido em Jan/2026 | Varia por região e modelo |

## Google ADK (Agent Development Kit)

Framework open-source para construir sistemas multi-agent sofisticados

Google Agent Development Kit (ADK) é um framework flexível, model-agnostic e deployment-agnostic para desenvolver e fazer deploy de agentes de IA. Projetado para fazer o desenvolvimento de agentes se assemelhar ao desenvolvimento de software tradicional, com foco em sistemas multi-agent e orquestração hierárquica.

### Referências Oficiais

ADK Official Documentation Multi-Agent Systems in ADK Developer's Guide to Multi-Agent Patterns Building Collaborative AI with ADK

## Features Principais

- Model-agnostic: Funciona com qualquer LLM (Gemini, GPT, Claude, etc)
- Deployment-agnostic: Local, Vertex AI, Cloud Run, Docker, Kubernetes
- Multi-language: Python, TypeScript, Go, Java
- Evaluation built-in: Avalia resposta E trajectory
- Containerization pronto: Deploy imediato

## Tipos de Agentes

### LLM Agent

Agente baseado em LLM com ReAct loop

```
from adk import Agent

agent = Agent(
    name='customer_service',
    model='gemini-2.5-flash',
    instructions='Você é um assistente de atendimento do Banco BV',
    tools=[get_balance_tool, transfer_tool]
)
```

### Sequential Workflow Agent

Executa agentes em sequência (assembly line)

```
from adk import SequentialAgent

workflow = SequentialAgent(
    name='loan_approval',
    agents=[
        credit_analysis_agent,
        risk_assessment_agent,
        approval_decision_agent
    ]
)
```

### Parallel Agent

Executa agentes independentes concorrentemente

```
from adk import ParallelAgent

parallel = ParallelAgent(
    name='data_gathering',
    agents=[
        internal_db_agent,
        external_api_agent,
        document_analysis_agent
    ]
)
```

### Loop Agent

Cria ciclos iterativos de refinamento

```
from adk import LoopAgent

loop = LoopAgent(
    name='document_refinement',
    agent=document_writer_agent,
    max_iterations=5,
    stop_condition=lambda state: state['quality_score'] > 0.9
)
```

### Custom Agent

Agente customizado com lógica própria

```
from adk import Agent

class MyCustomAgent(Agent):
    def run(self, state):
        # Lógica customizada
        result = custom_logic(state)
        return result
```

## Padrões de Orquestração

### Sequential Pipeline

Workflows lineares assembly-line onde agentes passam trabalho sequencialmente

Caso de Uso

Processamento de documentos, aprovações multi-etapa

Diagrama

Agent A → Agent B → Agent C → Output

### Parallel Execution

Executar tarefas independentes concorrentemente

Caso de Uso

Coleta de dados de múltiplas fontes, análises paralelas

Diagrama

Input → [Agent A, Agent B, Agent C] → Aggregate → Output

### Loop/Iterative

Ciclos de refinamento iterativo

Caso de Uso

Geração de conteúdo com revisões, otimização iterativa

Diagrama

Input → Agent → Check Quality → [Loop if needed] → Output

### LLM-Driven Dynamic Routing

LLM decide qual agente chamar dinamicamente baseado no contexto

Caso de Uso

Roteamento inteligente, especialização por domínio

Diagrama

Input → Router LLM → [Specialist A | Specialist B | Specialist C] → Output

### Hierarchical Task Decomposition

Supervisor decompõe tarefas complexas e delega para sub-agentes

Caso de Uso

Projetos complexos, coordenação de equipes

Diagrama

Supervisor → [Sub-task 1, Sub-task 2, Sub-task 3] → Consolidate

### Agent as Tool

Um agente pode ser usado como ferramenta por outro agente

Caso de Uso

Modularização, reutilização, composição

```
# SQL agent como tool de outro agente
sql_agent = Agent(name='sql_expert', ...)

main_agent = Agent(
    name='data_analyst',
    tools=[sql_agent]  # SQL agent é uma tool!
)
```

## Evaluation Built-in

ADK possui capacidades de avaliação integradas para avaliar qualidade de resposta E trajectory de execução

#### Métricas

- Response Quality: Avalia a resposta final do agente
- Trajectory Quality: Avalia o caminho de execução (quais tools, ordem, eficiência)
- Custom Metrics: Defina métricas customizadas
- LLM-as-a-Judge: Use LLMs para avaliar outputs

```
from adk import Agent, Evaluator

# Definir evaluator
evaluator = Evaluator(
    metrics=['response_quality', 'trajectory_efficiency'],
    judge_model='gemini-2.5-flash'
)

# Avaliar agent
results = evaluator.evaluate(
    agent=my_agent,
    test_cases=test_dataset
)

print(f'Quality Score: {results.avg_quality}')
print(f'Trajectory Score: {results.avg_trajectory}')
```

## Opções de Deploy

### Local Development

Executar localmente para desenvolvimento e testes

python agent.py

### Vertex AI Agent Engine

Deploy gerenciado no Vertex AI com escalabilidade automática

adk deploy --target vertex-ai --agent-id my-agent

### Cloud Run

Deploy serverless no Cloud Run

adk deploy --target cloud-run --service my-agent-svc

### Docker Container

Containerização para qualquer plataforma

adk build --output docker --tag my-agent:v1

### Custom Infrastructure

Deploy em infraestrutura própria (on-prem, outros clouds)

docker run -p 8080:8080 my-agent:v1

## Arquitetura Hierárquica

ADK organiza agentes em estrutura de árvore com relacionamentos parent-child, proporcionando delegação controlada de tarefas e debuggability aprimorada

#### Root Agent

Agente principal que recebe input do usuário e coordena outros agentes

#### Sub-Agents

Agentes especializados que executam tarefas específicas

#### Tool Agents

Agentes que podem ser usados como tools por outros agentes

## Agent Designer & Garden

Ferramentas low-code para acelerar desenvolvimento de agentes

Agent Designer e Agent Garden são ferramentas complementares (ambas em Preview) que aceleram o desenvolvimento de agentes através de interface visual e templates pré-construídos.

### Referências Oficiais

Agent Designer Overview Agent Garden (Preview)

## Componentes

1

### Agent Designer

Designer visual low-code disponível no Google Cloud console

2

### Agent Garden

Biblioteca de agentes pré-construídos e tools reutilizáveis

## Comparação

| Aspecto | Agent Designer | Agent Garden |
| --- | --- | --- |
| Público-alvo | Desenvolvedores + não-desenvolvedores | Todos (ênfase em reutilização) |
| Abordagem | Visual design → código | Template → customização |
| Flexibilidade | Alta (design livre) | Média (partir de templates) |
| Velocidade | Rápido prototyping | Deploy imediato |
| Complexidade | Simples a médio | Simples (templates testados) |

## Workflow Combinado

```
1. Explore Agent Garden para templates relevantes
2. Customize template no Agent Designer visualmente
3. Teste no playground
4. Exporte código ADK
5. Refine código se necessário
6. Deploy no Agent Engine ou Cloud Run
```

## O que são Tokens

Unidades fundamentais de processamento de texto em LLMs

Tokens são as unidades básicas de texto que modelos de linguagem (LLMs) processam. Diferente de caracteres ou palavras, tokens são fragmentos de texto que podem ser palavras completas, partes de palavras, pontuação ou até espaços. Entender tokens é crucial para otimizar custos e performance de aplicações com LLMs.

### Referências

Tokenization Explained (OpenAI) How Tokenizers Work (Hugging Face) Vertex AI Token Counting

## O que é um Token?

Token é uma sequência de caracteres que o modelo trata como unidade única

"Hello, world!" 4 tokens

Hello, world!

"Banco BV" 2 tokens

Banco BV

"inadimplência" 3 tokens

in adim plência

## Por que não são palavras?

Palavras podem ser quebradas em múltiplos tokens, especialmente palavras raras ou compostas

- Palavras comuns = 1 token (ex: 'the', 'banco', 'crédito')
- Palavras raras = múltiplos tokens (ex: 'inadimplência' → 3 tokens)
- Números e códigos = 1+ tokens dependendo do formato
- Pontuação = geralmente 1 token cada

## Tokenização Multilíngue

Diferentes idiomas têm eficiências diferentes de tokenização

#### Inglês

Eficiência: Alta

Ratio: ~1.3 tokens por palavra

'machine learning' = 2 tokens

#### Português

Eficiência: Média

Ratio: ~1.5 tokens por palavra

'aprendizado de máquina' = 4 tokens

#### Chinês

Eficiência: Baixa

Ratio: ~2-3 tokens por caractere

'机器学习' (4 chars) = 8+ tokens

## Algoritmos de Tokenização

### Byte-Pair Encoding (BPE)

Algoritmo mais comum em LLMs modernos (GPT, Gemini)

```
1. Inicia com caracteres individuais
2. Identifica pares frequentes
3. Mescla pares em novos tokens
4. Repete até alcançar vocabulário desejado
```

Vocabulário típico: 32k-100k tokens

### WordPiece

Usado por BERT e modelos Google antigos

Similar a BPE mas usa likelihood em vez de frequência

### SentencePiece

Tokenização agnóstica de idioma, trata texto como sequência de bytes

✓ Melhor para idiomas sem espaços (chinês, japonês)

## Impacto dos Tokens

### Custo

Pricing de LLMs é POR TOKEN, não por caractere ou palavra

Gemini 2.5 Flash: $0.075 por 1M input tokens Um email de 500 palavras ≈ 650 tokens = $0.00005

### Context Window

Limite de tokens que o modelo pode processar de uma vez

- • Gemini 2.0 Flash: até 1M tokens
- • Gemini 2.5 Pro: até 2M tokens
- • GPT-4o: 128k tokens

### Latência

Mais tokens = mais tempo de processamento

Tempo ≈ (input_tokens + output_tokens) / throughput

### Performance

Modelos têm melhor performance com tokens que viram durante treinamento

💡 Evite tokenização excessivamente fragmentada (palavras muito raras)

## Best Practices

- Monitore contagem de tokens em prompts e respostas
- Use tiktoken ou APIs de contagem para estimativas precisas
- Otimize prompts removendo tokens desnecessários
- Considere trade-off: prompts mais curtos podem precisar de mais clareza
- Em português, espere ~30-50% mais tokens que em inglês
- Cache prompts longos e estáticos quando possível

## Como Calcular Tokens

Ferramentas e APIs para contagem precisa de tokens

Calcular tokens com precisão é essencial para estimar custos, gerenciar context windows e otimizar performance. Cada modelo pode tokenizar texto de forma ligeiramente diferente, então é importante usar a ferramenta certa para o modelo específico.

### Referências

Vertex AI Count Tokens API OpenAI Tokenizer tiktoken (Python)

## Métodos de Contagem

### Vertex AI Count Tokens API

Qualquer linguagem (REST API)

API oficial para contar tokens em modelos Gemini

Precisão: 100% preciso para modelos Vertex AI

#### Features

- Contagem precisa para Gemini
- Suporta multimodal (texto + imagem)
- Inclui tokens de system instruction
- Gratuito (não conta para cobrança)

```
from vertexai.generative_models import GenerativeModel

model = GenerativeModel('gemini-2.5-flash')

# Contar tokens de um prompt
response = model.count_tokens(
    contents='Qual o saldo da conta 123456-7 na agência 0001?'
)

print(f'Total tokens: {response.total_tokens}')
print(f'Input tokens: {response.prompt_token_count}')
# Output: Total tokens: 18
```

### tiktoken (OpenAI)

Python

Biblioteca Python para tokenização rápida e precisa

Precisão: 100% preciso para modelos OpenAI, aproximado para outros

#### Features

- Extremamente rápido (em Rust)
- Funciona offline
- Vários modelos suportados
- Encode e decode

```
import tiktoken

# Para GPT-4
encoding = tiktoken.encoding_for_model('gpt-4')

text = 'Qual o saldo da conta 123456-7 na agência 0001?'
tokens = encoding.encode(text)

print(f'Total tokens: {len(tokens)}')
print(f'Tokens: {tokens}')
# Output: Total tokens: 16
# Tokens: [48, 940, 297, 274, 4852, ...]
```

### OpenAI Tokenizer (Web)

Browser

Interface web interativa para explorar tokenização

Precisão: Visual e educacional

#### Features

- Visualização colorida de tokens
- Suporta múltiplos modelos
- Ótimo para aprendizado
- Sem necessidade de código

Acessar ferramenta

### LangChain Token Counting

Python

Integrado em LangChain para contagem automática

Precisão: Depende do callback usado

#### Features

- Contagem automática
- Tracking de custos
- Integrado em chains
- Callback system

```
from langchain.callbacks import get_openai_callback
from langchain_google_vertexai import ChatVertexAI

llm = ChatVertexAI(model='gemini-2.5-flash')

with get_openai_callback() as cb:
    response = llm.invoke('Qual o saldo da conta 123456-7?')
    print(f'Total tokens: {cb.total_tokens}')
    print(f'Prompt tokens: {cb.prompt_tokens}')
    print(f'Completion tokens: {cb.completion_tokens}')
    print(f'Total cost: ${cb.total_cost}')
```

## Regras de Estimativa

### Regra dos 4 caracteres (Inglês)

Precisão: ±20%

Em inglês, ~4 caracteres ≈ 1 token

100 palavras ≈ 500 chars ≈ 125 tokens

### Regra 1.5x (Português)

Precisão: ±25%

Em português, espere ~50% mais tokens que em inglês

100 palavras PT ≈ 750 chars ≈ 190 tokens

### Pontuação e Espaços

Cada pontuação geralmente é 1 token, espaços podem ser incluídos em tokens de palavras

'Hello, world!' = 4 tokens (Hello |, | world |!)

### Números

Números podem ser 1 ou múltiplos tokens dependendo do formato

- • '123' = 1 token
- • '123.456' = 3 tokens (123 |. | 456)
- • 'R$ 1.234,56' = 6 tokens

## Exemplo Prático: Análise de Crédito

#### Prompt Completo

```
Você é um analista de crédito do Banco BV. Analise o seguinte perfil:

Cliente: João Silva
CPF: 123.456.789-00
Renda: R$ 5.000,00
Score: 750
Dívidas: R$ 2.000,00

Forneça recomendação de crédito.
```

#### Breakdown de Tokens

System instruction

Você é um analista de crédito do Banco BV.

15 tokens

User prompt

Analise o seguinte perfil... (dados do cliente)

65 tokens

Expected response

(Estimativa de resposta estruturada)

150 tokens

TOTAL

Input: 80, Output: 150

230 tokens

#### Custo Estimado

```
Gemini 2.5 Flash: $0.075/1M input + $0.30/1M output = (80 * $0.075 + 150 * $0.30) / 1M = $0.000051
```

## Ferramentas Úteis

### Google Cloud Console

Token counting integrado no Vertex AI Studio

```
1. Abra Vertex AI Studio
2. Selecione modelo
3. Digite prompt
4. Veja contagem automática na interface
```

### VS Code Extension

Extensões que mostram contagem de tokens inline

- • Token Counter for OpenAI
- • LangChain Token Counter

### CLI Tools

Ferramentas de linha de comando para batch counting

echo 'Seu texto' | tiktoken -m gpt-4

## Preços Vertex AI

Precificação completa e estratégias de redução de custos para Gemini no Vertex AI (Fev/2026)

Vertex AI cobra por tokens processados, com preços diferenciados por modelo, tier de contexto, modalidade (texto/áudio/vídeo/imagem) e método de processamento (online/batch). Compreender a estrutura de preços é CRÍTICO para otimizar custos em agentes de IA de produção.

### Referências

Vertex AI Pricing (Oficial) Pricing Calculator Cost Optimization Guide

## Gemini 3 (Preview)

PREVIEW

| Modelo | Input ≤200k | Input >200k | Output | Cached | Batch | Context |
| --- | --- | --- | --- | --- | --- | --- |
| Gemini 3 Pro Thinking | $2.00 / 1M | $4.00 / 1M | $12.00 / 1M / $18.00 / 1M | $0.20 / 1M | 50% | 1M tokens |
| Gemini 3 Flash | $0.50 / 1M | $0.50 / 1M | $3.00 / 1M / $3.00 / 1M | $0.05 / 1M | 50% | 1M tokens |

Preços ≤200k tokens (Low) e >200k tokens (High). Output varia com/sem thinking mode.

## Gemini 2.5

GA

| Modelo | Input ≤200k | Input >200k | Output | Cached | Batch | Context |
| --- | --- | --- | --- | --- | --- | --- |
| Gemini 2.5 Pro Most Capable | $1.25 / 1M | $2.50 / 1M | $10.00 / 1M | $0.125 / 1M | 50% | 2M tokens |
| Gemini 2.5 Flash Balanced | $0.30 / 1M | $0.30 / 1M | $2.50 / 1M | $0.03 / 1M | 50% | 1M tokens |
| Gemini 2.5 Flash Lite Cost Optimized | $0.10 / 1M | $0.10 / 1M | $0.40 / 1M | $0.01 / 1M | 50% | 1M tokens |

Preços ≤200k tokens (Low) e >200k tokens (High). Thinking mode aplica preços de output mais altos.

## Gemini 2.0

STABLE

| Modelo | Input Online | Output Online | Input Batch | Output Batch | Context |
| --- | --- | --- | --- | --- | --- |
| Gemini 2.0 Flash Fast | $0.15 / 1M | $0.60 / 1M | $0.075 / 1M | $0.30 / 1M | 1M tokens |
| Gemini 2.0 Flash Lite Ultra-Fast | $0.075 / 1M | $0.30 / 1M | $0.0375 / 1M | $0.15 / 1M | 1M tokens |

Batch API oferece 50% de desconto em todos os modelos.

## Preços por Modalidade

Tokens são calculados diferentemente para cada tipo de mídia

### Texto

Preço: Preço base do modelo

Tokenização: ~4 caracteres = 1 token (inglês), ~2 caracteres = 1 token (português)

📐 Frase de 100 caracteres ≈ 25-50 tokens

### Áudio

Preço: Gemini 2.5 Flash: $0.075/1M | Pro: $3.00/1M

Tokenização: ~32 tokens por segundo de áudio

📐 1 minuto de áudio ≈ 1,920 tokens

### Vídeo

Preço: Igual ao preço de imagem + áudio

Tokenização: ~258 tokens por segundo (1 frame/seg) + áudio

📐 1 minuto de vídeo ≈ 15,480 tokens (sem áudio) + 1,920 (áudio)

### Imagem

Preço: Incluído no preço de input do modelo

Tokenização: ~1,290 tokens por imagem (1024x1024)

📐 Imagem menor = menos tokens (proporcional à área)

### Exemplo de Cálculo Multi-Modal

Análise de documento PDF com 10 páginas + 5 imagens

Texto (10 páginas)

~2k tokens/página 20,000 tokens

Imagens (5 × 1024px)

5 × 1,290 6,450 tokens

Prompt + Instructions

~500 tokens 500 tokens

TOTAL INPUT

26,950 tokens

Gemini 2.5 Flash: 26,950 × $0.30/1M = $0.008 por documento

## Context Caching: A Biblioteca de Acesso Rápido

O terceiro pilar da eficiência na Vertex AI - cache de contexto pesado para economia de até 90% e baixa latência

### Analogia dos 3 Pilares

1

#### Batch Prediction

"Análise Noturna"

Barata e lenta

Quando: Workloads não-urgentes

2

#### Memory Bank

"Memória da Conversa"

Dinâmica

Quando: Histórico de chat

3

#### Context Caching

"Biblioteca de Acesso Rápido"

Rápida e econômica

Quando: Consultas repetidas sobre conteúdo pesado

### 1. O Problema que Ele Resolve

Você quer fazer perguntas sobre um manual técnico de 500 páginas (~100k tokens) usando Gemini 2.5 Pro

#### ❌ Sem Caching

- Cada pergunta re-envia as 500 páginas completas
- Modelo processa tudo novamente a cada chamada
- Você paga 100k tokens × $1.25/1M = $0.125 por pergunta
- Latência alta: modelo lê 500 páginas antes de responder

Custo mensal

100 perguntas/dia = $12.50/dia = $375/mês

#### ✓ Com Caching

- Envia 500 páginas UMA ÚNICA VEZ
- Gemini processa e cria 'imagem mental' (cache) com ID
- Próximas perguntas: só envia pergunta + ID do cache
- Paga apenas pela pergunta (poucos tokens) + taxa de storage

Custo mensal

1ª: $0.125 | 99 seguintes: 99 × $0.0125 = $1.24 | Storage: $4.50/mês | TOTAL: $5.86/mês

💰 93% economia ($369/mês economizados)

### 2. Definição Técnica

Context Caching permite que desenvolvedores enviem grandes volumes de informação (tokens de entrada) para o modelo, processem esses tokens UMA VEZ e depois reutilizem esse contexto processado em múltiplas requisições subsequentes.

#### Pontos-Chave:

Cache é criado no PREFIXO do prompt

ID único identifica o cache

TTL (Time-to-Live) controla expiração

Renovação automática disponível

### 3. Triângulo de Valor (3 Benefícios Críticos)

#### Redução de Custo Drástica

Paga preço cheio apenas na criação. Chamadas seguintes: valor muito reduzido + pequena taxa de storage/hora.

Economia = (Preço_Normal - Preço_Cached) × Número_de_Chamadas - Custo_Storage

Vale a pena quando o mesmo contexto é consultado +10-20 vezes

```
Manual de 50k tokens consultado 100x:
Sem cache: 50k × 100 × $1.25/1M = $6.25
Com cache: $0.625 (1ª) + $0.625 (99×cached) + $0.11 (storage) = $1.36
Economia: 78%
```

#### Baixa Latência (Velocidade)

Modelo não precisa processar (tokenizar + analisar) documento gigante a cada chamada. Time to First Token (TTFT) cai drasticamente.

- Sem cache: ~3-5s de latência para 100k tokens
- Com cache: ~200-500ms (10x mais rápido)
- Streaming inicia quase instantaneamente

Crítico para aplicações interativas e real-time

#### Suporte a Contextos Massivos

Permite 'conversar' com vídeos de 1 hora, bases de código inteiras ou livros, mantendo performance de conversa curta.

##### Casos de Uso

Análise de código-fonte completo (500k tokens)

Vídeos longos (1h = ~900k tokens)

Documentação técnica volumosa

Processos judiciais extensos

### 4. Context Caching vs Memory Bank vs RAG

Seus alunos VÃO confundir - aqui está a 'cola' para a prova:

| Recurso | O que guarda? | Quando usar? | Analogia | Implementação | Escopo | Custo |
| --- | --- | --- | --- | --- | --- | --- |
| Memory Bank | Histórico da conversa (User + AI) | Chatbot lembrar o que usuário disse há 5 minutos | "Memória de Curto Prazo (RAM)" | Vertex AI Memory Bank, LangGraph Checkpointer | Thread-level | Baixo (poucos KB) |
| Context Caching | Dados pesados e ESTÁTICOS (Docs, Vídeos, Codebase) | Fazer várias perguntas sobre o MESMO material denso | "Livro aberto na mesa de estudos" | Vertex AI CachedContent API | Multi-thread (compartilhado) | Médio (storage/hora) |
| RAG (Vector Search) | Chunks de MILHARES de docs diferentes | 1 milhão de docs, precisa achar SÓ 1 parágrafo relevante | "Índice remissivo da biblioteca" | Vertex AI Vector Search, Pinecone, Weaviate | Cross-document search | Alto (embeddings + storage + QPS) |

IMPORTANTE: Eles NÃO são excludentes - use JUNTOS! Ex: RAG busca docs relevantes (3) → Context Cache os 3 docs → Memory Bank mantém conversa.

### 5. Regras de Ouro (Limitações Técnicas)

1

#### Mínimo de Tokens

Cache só é permitido (e só vale a pena) acima de 32.768 tokens

Abaixo disso, o overhead de gerenciar cache não compensa

```
❌ Não faça cache de um parágrafo de 500 tokens
✓ Faça cache de manual de 50k+ tokens
```

2

#### TTL (Time to Live)

Cache tem vida útil configurável (padrão: 1 hora)

Após expiração, precisa recriar (paga preço cheio novamente)

• Mínimo: 60 segundos

• Máximo: 1 hora (padrão)

• Renovação: Automática quando acessado

💡 Para workloads 24/7, considere renovação automática ou cache perpétuo

3

#### Cache DEVE Ser Prefixo

Conteúdo em cache precisa ser o INÍCIO do prompt, não o meio ou fim

Arquitetura de transformer processa tokens sequencialmente da esquerda para direita

```
✓ [CACHE: Manual 100k] + [Pergunta: 50 tokens]
❌ [Pergunta: 50] + [CACHE: Manual 100k] ← NÃO FUNCIONA
```

4

#### Dados Estáticos Apenas

Cache é para conteúdo que NÃO MUDA entre chamadas

##### ✓ Bons exemplos:

System instruction / Persona

Manual corporativo (atualiza raramente)

Few-shot examples

Base de código (snapshot)

##### ✗ Evite:

❌ Dados do usuário (muda a cada request)

❌ Resultados de API em tempo real

❌ Timestamp ou data atual

### Preços de Input (Cache vs Normal)

#### Gemini 2.5 Pro

Normal: $1.25 / 1M

Cached: $0.125 / 1M

Ratio: 10x mais barato

90% economia

#### Gemini 2.5 Flash

Normal: $0.30 / 1M

Cached: $0.03 / 1M

Ratio: 10x mais barato

90% economia

#### Gemini 2.5 Flash Lite

Normal: $0.10 / 1M

Cached: $0.01 / 1M

Ratio: 10x mais barato

90% economia

### Custo de Armazenamento (por hora)

Taxa adicional para manter cache ativo na memória

Gemini 2.5 Pro

$4.50 / 1M tokens / hora

Gemini 2.5 Flash

$1.00 / 1M tokens / hora

Gemini 2.5 Flash Lite

$0.25 / 1M tokens / hora

Custo Storage = (Tokens_Cached / 1M) × Preço_Storage × Horas_Ativo

Cache expira após TTL. Renovação automática: cache é renovado quando acessado (TTL reseta).

### 6. Exemplo Prático de Aula (Agente Advogado)

Contexto: Cenário: Criar um Agente Advogado para analisar processo judicial de 2.000 páginas

Tokens: 2.000 páginas × 500 tokens/página = 1.000.000 tokens (1M)

Modelo: Gemini 2.5 Pro

#### Sem Context Caching (API Normal)

- Pergunta 1: 'Qual o réu?' → Envia 1M tokens + pergunta
- Pergunta 2: 'Qual a sentença?' → Envia 1M tokens + pergunta NOVAMENTE
- ...50 perguntas = 50x processamento completo

Custo: 50 perguntas × 1M tokens × $1.25/1M = $62.50

Latência: ~5 segundos por resposta (processando 1M tokens)

#### Com Context Caching (Otimizado)

- 1ª vez: Cria cache do processo (1M tokens) → gera cache_id='abc123'
- Perguntas seguintes: Envia apenas pergunta + cache_id
- Modelo já tem o processo 'memorizado'

Custo: 1ª: $1.25 | 49 seguintes: 49 × $0.125 = $6.13 | Storage (24h): $4.50 | TOTAL: $11.88

Latência: ~200ms por resposta (cache hit)

$50.62 (81% economia) + 25x mais rápido

### Context Caching vs Memory Bank vs RAG

| Recurso | O que guarda? | Quando usar? | Analogia | Scope |
| --- | --- | --- | --- | --- |
| Memory Bank | Histórico conversa | Lembrar mensagens anteriores | "RAM (Memória de Curto Prazo)" | Thread-level |
| Context Caching | Docs pesados ESTÁTICOS | Várias perguntas sobre MESMO conteúdo | "Livro aberto na mesa" | Multi-thread |
| RAG (Vector Search) | Chunks de MILHARES de docs | Buscar 1 parágrafo em 1M docs | "Índice remissivo" | Cross-document |

### Implementação com Vertex AI

#### 1. Criar Cache

```
from vertexai.generative_models import GenerativeModel, caching
import datetime

# 1. Criar cache do processo judicial (1M tokens)
MANUAL_BV = open('manual-banco-bv.txt').read()  # 1M tokens

cached_content = caching.CachedContent.create(
    model_name='gemini-2.5-pro',
    system_instruction=MANUAL_BV,
    ttl=datetime.timedelta(hours=1),  # Expira em 1h
    display_name='Manual BV v2.0'
)

print(f'Cache criado: {cached_content.name}')
print(f'Expira em: {cached_content.expire_time}')
```

#### 2. Usar Cache

```
# 2. Usar cache em múltiplas queries
model = GenerativeModel.from_cached_content(cached_content)

# Query 1: Paga apenas pela pergunta (cached input = $0.125/1M)
response1 = model.generate_content('Qual a política de crédito?')

# Query 2: Novamente, só paga a pergunta
response2 = model.generate_content('Qual a taxa de juros?')

# Query 3-100: Todas baratas e rápidas
for question in questions:
    response = model.generate_content(question)  # Cache hit!
```

#### 3. Atualizar/Renovar Cache

```
# 3. Atualizar cache (quando manual mudar)
cached_content.update(ttl=datetime.timedelta(hours=2))  # Renovar TTL

# Ou deletar e recriar
cached_content.delete()
new_cache = caching.CachedContent.create(...)  # Com novo conteúdo
```

### Best Practices para Context Caching

#### Cache Conteúdo Grande e Reutilizável

Só vale a pena para contextos ≥32k tokens consultados múltiplas vezes

System instructions longas Manuais corporativos Few-shot examples extensos Documentação de API completa

#### Combine com Outras Técnicas

Context Caching + RAG + Memory Bank = Stack Completo

RAG busca 3 docs relevantes (10k cada) → Cache os 3 docs (30k total) → Memory Bank mantém conversa

#### Monitore TTL e Renovação

Para workloads 24/7, configure renovação automática ou recrie cache periodicamente

Use CloudWatch/Monitoring para alertar quando cache expirar

#### Prefixe Estrategicamente

Organize prompt com conteúdo estático primeiro

[System Instruction] + [Manual] + [Few-shots] + [User Query Dinâmica]

### Exemplo para a Aula (Pitch de Venda)

"Pessoal, imaginem que vamos criar um Agente Advogado. Ele precisa analisar um processo judicial de 2.000 páginas. Se usarmos a API normal, cada pergunta custa $10 dólares. Se usarmos Context Caching, pagamos $10 na primeira vez para 'carregar o processo'. As próximas 50 perguntas custarão centavos e serão respondidas em SEGUNDOS, porque o Gemini já 'memorizou' o processo."

Economia: 80-90%

Velocidade: 10-25x mais rápido

Experiência: Interativa e fluida

### Cenário Real: Agente de Documentação BV

System instruction com manual do banco (50k tokens), 10,000 queries/dia

#### ❌ Sem Cache

Diário: 50k × 10,000 × $1.25/1M = $625/dia

Mensal: $18,750/mês

#### ✓ Com Cache

Storage: $4.50 × 24h × 30 dias = $3,240/mês (amortizado)

Input: 50k × 10,000 × $0.125/1M × 30 = $1,875/mês

Total: $5,115/mês

$13,635/mês (73% economia)

#### Requisitos Técnicos

- Contexto mínimo: ≥32,768 tokens (32k)
- Cached content DEVE ser PREFIXO do prompt
- TTL configurável: 60s até 1 hora (padrão)
- Modelos suportados: Gemini 2.5+, 1.5+, Gemini 3
- Dados devem ser ESTÁTICOS (não mudam entre calls)

## Grounding (Search & Enterprise)

Preços para augmentar respostas com dados externos em tempo real

### Google Search

$35 / 1,000 requests

Grátis: Flash: 1,500/dia | Pro: 10,000/dia

Busca no Google Search em tempo real

📌 Informações atuais, notícias, dados públicos

### Enterprise Web (Vertex AI Search)

$45 / 1,000 requests

Grátis: Nenhum

Busca em websites corporativos indexados

📌 Documentação interna, intranet, knowledge base

### Google Maps

$25 / 1,000 requests

Grátis: Igual ao Google Search

Dados de localização e negócios

📌 Agências bancárias, ATMs, localização

### Estratégia de Otimização

Use Gemini 2.5 Pro para queries com grounding (quota gratuita maior: 10k/dia vs 1,500/dia do Flash)

```
5,000 queries/dia com Google Search:
• Flash: 1,500 grátis + 3,500 × $35/1000 = $122.50/dia
• Pro: 5,000 grátis (dentro da quota) = $0/dia*

*Modelo Pro é mais caro, mas grounding grátis compensa
```

## Batch API (50% Desconto)

Processamento assíncrono para workloads não-urgentes

50% de desconto em todos os modelos

Processamento em até 24 horas

Ideal para análises em lote, ETL, relatórios

Mesma qualidade, menor prioridade

### Comparativo de Preços

| Modelo | Online | Batch (50% off) |
| --- | --- | --- |
| Gemini 2.5 Pro | $1.25 input / $10.00 output | $0.625 input / $5.00 output |
| Gemini 2.5 Flash | $0.30 input / $2.50 output | $0.15 input / $1.25 output |
| Gemini 2.0 Flash | $0.15 input / $0.60 output | $0.075 input / $0.30 output |

### Casos de Uso Ideais

Análise de contratos/documentos em lote

Geração de relatórios noturnos

Processamento de logs históricos

Treinamento de dados / data labeling

Backfill de embeddings

#### Cenário: Análise de 1,000 Contratos/dia

Online

1,000 × 100k tokens × $1.25/1M = $125/dia

Batch

1,000 × 100k tokens × $0.625/1M = $62.50/dia

Economia: $62.50/dia = $1,875/mês

## Capacidade Provisionada (GSU)

Throughput garantido para workloads previsíveis de alta escala

GSU (Generative Service Units) garante QPS (queries por segundo) consistente, ideal para aplicações críticas com SLA.

### Tabela de Preços GSU

| Duração | Preço/GSU | Desconto |
| --- | --- | --- |
| 1 semana | $1,200 | - |
| 1 mês | $2,700 | ~10% vs semanal |
| 3 meses | $2,400/mês | ~20% vs semanal |
| 1 ano | $2,000/mês | ~32% vs semanal |

### Exemplo de Cálculo

Contact Center com 100 QPS constante

#### Pay-as-you-go

~$50,000/mês (variável)

Baseado em volume estimado

#### GSU Anual

~$34,000/mês (fixo)

Previsibilidade + desconto

Economia: $16,000/mês = $192,000/ano

### Quando Usar GSU

- Volume previsível e constante
- Requisitos de SLA rigorosos
- Budget fixo preferido
- Alta escala (>$30k/mês em tokens)

## Free Tier e Limites

Quotas gratuitas para experimentação

#### Gemini 2.5 Flash

Rate Limit: 15 RPM

Grounding: 1,500 requests/dia

Ideal para desenvolvimento e testes

#### Gemini 2.5 Pro

Rate Limit: 2 RPM

Grounding: 10,000 requests/dia

Quota de grounding generosa

#### Importante

- ⚠️ Quotas reiniciam mensalmente
- ⚠️ Sujeito a alterações sem aviso
- ⚠️ Para produção, sempre provisione além do free tier
- ⚠️ Rate limits podem ser aumentados via quota request

## Variação por Região

Preços podem variar por região (até ±10%)

📍 Base: us-central1 (Iowa) - preços base

europe-west1 (+5%) asia-northeast1 (+10%)

💡 Para minimizar custos, use us-central1 quando latência permitir

## 7 Estratégias de Redução de Custos

Técnicas comprovadas para otimizar custos em agentes de IA

1

### Model Tiering Inteligente

Roteamento automático para modelo apropriado baseado na complexidade da query

💰 Até 92% vs usar Pro para tudo

```
# Classificador de complexidade
def route_to_model(query: str) -> str:
    complexity = classify_complexity(query)  # LLM ou heurística
    
    if complexity == 'simple':  # FAQ, saldo, extrato
        return 'gemini-2.5-flash-lite'  # $0.10 input
    elif complexity == 'medium':  # produtos, simulações
        return 'gemini-2.5-flash'  # $0.30 input
    else:  # análise de crédito, complexo
        return 'gemini-2.5-pro'  # $1.25 input
```

#### Chatbot BV - 1M conversas/mês

Simples (70%)

Flash Lite $0.10/1M

Médias (25%)

Flash $0.30/1M

Complexas (5%)

Pro $1.25/1M

Sem otimização

$1,250/mês (tudo Pro)

Com tiering

$152.50/mês

Economia: $1,097.50/mês (88%)

2

### Context Caching Agressivo

Cache de system instructions, manuais e few-shot examples

💰 Até 90% em tokens de input

```
from vertexai.generative_models import GenerativeModel, caching

# Criar cache com manual do banco (50k tokens)
cached_content = caching.CachedContent.create(
    model_name='gemini-2.5-pro',
    system_instruction=MANUAL_BV,  # 50k tokens
    ttl='3600s'  # 1 hora
)

# Usar modelo com cache
model = GenerativeModel.from_cached_content(cached_content)

# Cada chamada: 50k tokens a $0.125/1M em vez de $1.25/1M
```

#### Agente de Compliance - 50k tokens de contexto

Sem cache

$625/dia

Com cache

$62.50/dia + $108/dia (storage) = $170.50/dia

Economia: $454.50/dia = $13,635/mês (73%)

3

### Batch Processing Noturno

Processar workloads não-urgentes em batch com 50% desconto

💰 50% em processamento batch

```
from vertexai.batch_prediction import BatchPredictionJob

# Criar job de batch para análise de contratos
job = BatchPredictionJob.create(
    model='gemini-2.5-pro',
    input_uri='gs://bucket/contracts/*.json',
    output_uri='gs://bucket/results/',
    # Processamento em até 24h com 50% desconto
)

# Monitorar
while job.state != 'JOB_STATE_SUCCEEDED':
    time.sleep(60)
    job.refresh()
```

#### Análise de Contratos - 1,000/dia

Online

$125/dia

Batch

$62.50/dia

Economia: $62.50/dia = $1,875/mês

4

### Grounding Otimizado

Usar modelo Pro para grounding (quota gratuita maior)

💰 Até 100% em custos de grounding

```
# Estratégia: Flash para queries normais, Pro para grounding
def smart_grounding(query: str, needs_realtime: bool) -> str:
    if needs_realtime:  # Precisa de dados atuais
        # Pro tem 10k grounding grátis/dia vs 1.5k do Flash
        return call_with_grounding(query, model='gemini-2.5-pro')
    else:
        return call_without_grounding(query, model='gemini-2.5-flash-lite')
```

#### Agente de Pesquisa - 5,000 queries/dia com grounding

Flash

1,500 grátis + 3,500 × $35/1000 = $122.50/dia

Pro

5,000 grátis (dentro da quota) = $0/dia

Economia: $122.50/dia = $3,675/mês

📝 Custo do Pro é maior, mas grounding grátis compensa

5

### Prompt Engineering Econômico

Reduzir verbosidade e usar structured output

💰 20-60% em tokens

#### Técnicas

- Remover saudações e formalidades
- Usar bullet points vs parágrafos
- JSON output vs texto livre
- Limitar max_output_tokens
- Few-shot mínimo necessário

```
# ❌ Prompt verboso (2,000 tokens)
prompt_ruim = '''
Olá! Por favor, você poderia gentilmente analisar o perfil do cliente 
abaixo e me fornecer uma recomendação detalhada e bem fundamentada sobre 
se devemos aprovar ou não o crédito solicitado?

Dados do cliente:
- Nome: João Silva
- CPF: 123.456.789-00
...
'''

# ✅ Prompt otimizado (800 tokens)
prompt_bom = '''
Analise crédito. Retorne JSON.
Cliente: {"nome": "João Silva", "cpf": "123.456.789-00", ...}
Output: {"aprovado": bool, "motivo": str, "limite": int}
'''
```

#### Otimização de Prompt

Antes

2,000 tokens × 100k calls = 200M tokens/mês

Depois

800 tokens × 100k calls = 80M tokens/mês

Economia: 120M tokens/mês = $36/mês (Flash) ou $150/mês (Pro)

6

### Streaming com Early Stop

Cancelar geração ao detectar erros ou alucinações

💰 Variável - evita tokens desperdiçados

```
async def stream_with_validation(prompt: str):
    response_text = ''
    
    async for chunk in model.generate_content_stream(prompt):
        response_text += chunk.text
        
        # Detectar problemas early
        if detect_hallucination(response_text):
            print('Alucinação detectada, cancelando...')
            break
        
        if detect_error_pattern(response_text):
            print('Erro detectado, retry com prompt diferente')
            break
    
    return response_text
```

#### Detecção de Alucinações

Economia: 800 tokens × 10% × 100k calls = 8M tokens/mês

7

### GSU para Alta Escala

Capacidade provisionada para workloads previsíveis

💰 Até 32% em custos fixos

#### Quando Usar

- ✓ Volume > $30k/mês em tokens
- ✓ Carga previsível e constante
- ✓ Requisitos de SLA rigorosos
- ✓ Preferência por budget fixo

#### Contact Center - 100 QPS constante

Pay-as-you-go

$50,000/mês (variável)

GSU Anual

$34,000/mês (contrato anual)

Economia: $16,000/mês = $192,000/ano (32%)

## Cenários Reais para Agentes

Breakdown completo de custos para diferentes tipos de agentes de IA

### Agente de Atendimento (Chatbot)

1M conversas/mês

Tokens médios por request:

500 input + 300 output por conversa

#### Sem Otimização (tudo Pro)

Input $625

Output $3,000

$3,625/mês

#### Com Tiering + Cache + Batch

Flash Lite (70%) $119

Flash (25%) $225

Pro Batch (5%) $91

$435/mês

$3,190/mês = $38,280/ano (88% economia)

### Agente de Análise de Crédito (HITL)

50k análises/mês

Tokens médios por request:

5k input (documentos) + 1k output

📋 Alta precisão, grounding enterprise, Human-in-the-Loop

#### Estratégia Otimizada

Modelo: Gemini 2.5 Pro (qualidade crítica)

Cache: Manual de crédito (100k tokens)

Grounding: Enterprise ($45/1000)

HITL: Interrupções para revisão humana

Cache storage

$4.50 × 720h ÷ 30 $108/mês (amortizado)

Input (cached)

250M × $0.125/1M $31.25

Output

50M × $10/1M $500

Grounding

50k × $45/1000 $2,250

Total: ~$2,890/mês

📝 Grounding domina o custo - considere cache de respostas comuns

### Agente Multi-Modal (Documentos + Imagens)

10k documentos/mês (PDF com imagens)

Tokens médios por request:

20 páginas × 5 imagens cada

#### Tokenização

Texto: ~2k tokens/página × 20 = 40k tokens

Imagens: ~1,290 tokens × 5 = 6,450 tokens

Total: ~47k tokens/documento

#### Flash Online

10k × 47k × $0.30/1M

$141/mês

#### Flash Lite Batch

10k × 47k × $0.05/1M

$23.50/mês

$117.50/mês (83% economia)

💡 Redimensione imagens antes de enviar - 512px é suficiente para OCR

## Calculadora de ROI

Estime o retorno sobre investimento em otimização

Volume mensal de requests

100000

Tokens de input médios

500

Tokens de output médios

300

Modelo atual

Pro | Flash | Flash Lite

Usa context caching?

Não

Pode usar batch?

Não

Pode usar tiering?

Não

#### Fórmula

ROI = (Custo_Atual - Custo_Otimizado) / Custo_Otimizado × 100%

### Exemplo de Cálculo

#### Atual (Sem Otimização)

Modelo: Gemini 2.5 Pro

Volume: 100k requests/mês

Input: 500 tokens × $1.25/1M × 100k = $62.50

Output: 300 tokens × $10/1M × 100k = $300

$362.50/mês

#### Otimizado

✓ Tiering (70/25/5)

✓ Cache (system prompt)

✓ Batch (20%)

$45.80/mês

691% de retorno = economia de $316.70/mês

Use a calculadora oficial do Google para estimativas precisas

## Otimização de Tokens

Técnicas para reduzir custos e melhorar eficiência

Otimizar uso de tokens é essencial para controlar custos em aplicações de produção. Pequenas otimizações podem resultar em economias significativas em escala.

### Referências

Prompt Engineering Guide Cost Optimization Best Practices

## Estratégias de Otimização

1

### Context Caching

Cache prompts longos e estáticos

💰 Economia: Até 75% em tokens de input

```
from vertexai.generative_models import GenerativeModel, caching

# Criar cache de context longo
cached_content = caching.CachedContent.create(
    model_name='gemini-2.5-flash',
    system_instruction='Manual do banco com 50k tokens...',
    ttl='3600s'  # 1 hora
)

# Usar com cache
model = GenerativeModel.from_cached_content(cached_content)
response = model.generate_content('Qual a taxa de juros?')

# Primeiras 50k tokens: 75% desconto
```

#### Quando Usar

- ✓ Prompts com ≥32k tokens
- ✓ System instructions longas
- ✓ Manuais e documentação
- ✓ Few-shot examples extensos

2

### Prompt Compression

Remova redundâncias e verbosidade

💰 Economia: 10-30% redução em tokens

#### Técnicas

- • Use linguagem concisa
- • Elimine palavras desnecessárias
- • Use bullet points em vez de parágrafos
- • Remova saudações e formalidades excessivas

```
❌ Ruim (35 tokens):
'Por favor, você poderia gentilmente analisar o perfil do cliente e me fornecer uma recomendação detalhada sobre se devemos aprovar ou não o crédito solicitado?'

✅ Bom (15 tokens):
'Analise perfil do cliente. Recomende: aprovar ou recusar crédito.'
```

3

### Model Selection

Use modelo apropriado para cada tarefa

💰 Economia: Até 90% em custos

Tarefas simples (FAQ, classificação)

→ Gemini 2.5 Flash

Rápido e barato

Análise complexa

→ Gemini 2.5 Pro

Melhor qualidade

Raciocínio multi-step

→ Gemini 2.0 Flash Thinking

Thinking mode

4

### Output Length Control

Limite tamanho de respostas

💰 Economia: Reduz output tokens

```
model = GenerativeModel('gemini-2.5-flash')

response = model.generate_content(
    'Resuma o documento',
    generation_config={
        'max_output_tokens': 200,  # Limite
        'temperature': 0.7
    }
)
```

💡 Output tokens são 4x mais caros que input (Flash)

5

### Batch Processing

Processe múltiplas requisições em batch quando possível

💰 Economia: Reutilização de context, menos overhead

```
# Em vez de 10 calls separadas
for doc in documents:
    analyze(doc)  # 10 × overhead

# Batch quando possível
analyze_batch(documents)  # 1 × overhead + shared context
```

6

### Smart Tool Use

Use tools para buscar dados em vez de incluir tudo no prompt

💰 Economia: Reduz drasticamente tokens de input

❌ Ruim: Incluir 100k tokens de dados no prompt ✅ Bom: Usar tool para buscar apenas dados relevantes (2k tokens)

7

### Response Format Optimization

Use structured output (JSON) em vez de texto livre quando possível

💰 Economia: Respostas mais curtas e parseáveis

```
# Texto livre (mais tokens)
'O cliente João Silva tem score 750, o que é considerado bom...'

# JSON estruturado (menos tokens)
{'cliente': 'João Silva', 'score': 750, 'status': 'bom'}
```

8

### Few-Shot Optimization

Use apenas exemplos necessários

💰 Economia: Cada exemplo = tokens extras

undefined

→ undefined

undefined

undefined

→ undefined

undefined

undefined

→ undefined

undefined

undefined

→ undefined

undefined

## Ferramentas de Tracking

### LangSmith

Observability e tracking de custos para LangChain

- • Token counting automático
- • Cost breakdown por call
- • Dashboard de custos
- • Alertas de budget

### Vertex AI Monitoring

Monitoring nativo do Google Cloud

- • Métricas de uso
- • Billing reports
- • Budget alerts
- • Usage forecasting

### Custom Tracking

Implemente tracking próprio

```
class TokenTracker:
    def __init__(self):
        self.total_input = 0
        self.total_output = 0
        self.total_cost = 0
    
    def track(self, response):
        self.total_input += response.usage.prompt_tokens
        self.total_output += response.usage.completion_tokens
        self.total_cost += self.calculate_cost(response)
    
    def calculate_cost(self, response):
        input_cost = response.usage.prompt_tokens * 0.075 / 1_000_000
        output_cost = response.usage.completion_tokens * 0.30 / 1_000_000
        return input_cost + output_cost
```

## Calculadora de Custos

Estime custos da sua aplicação

Modelo selecionado

Tokens de input médios

Tokens de output médios

Número de requisições/mês

Context caching (sim/não)

Grounding (sim/não)

#### Fórmula

Custo Total = (Input_Tokens × Input_Price + Output_Tokens × Output_Price) × Requests + Grounding_Cost

Use a calculadora oficial do Google para estimativas precisas: https://cloud.google.com/products/calculator

## Caso Real: Otimização de Chatbot

### ❌ Antes

Modelo: Gemini 2.5 Pro

Prompt: 2000 tokens

Response: 500 tokens

Requests: 100000

```
(2000 × $1.25 + 500 × $10) / 1M × 100k = $750/mês
```

### ✓ Depois

Modelo: Gemini 2.5 Flash

Prompt: 800 tokens

Response: 300 tokens

Requests: 100000

Cache: 60% dos input tokens em cache

```
((800×0.4×$0.075 + 800×0.6×$0.01875) + 300×$0.30) / 1M × 100k = $11.25/mês
```

#### Otimizações Aplicadas

- ✓ Mudou para Gemini 2.5 Flash (tarefas simples)
- ✓ Prompt compression (2000 → 800 tokens)
- ✓ Output limit (500 → 300 tokens)
- ✓ Context caching (system instruction)

#### Economia Total

$738.75/mês (98.5% redução!)

## Lab Prático: Estimativa de Custos com Calculadora Google

Cenário Real: Agente de Análise de Crédito Empresarial BV

## Contexto do Problema

### Assistente de Análise de Crédito Empresarial (BV Crédito PJ)

Um agente de IA avançado que auxilia gerentes de relacionamento do Banco BV na análise de crédito para empresas (Pessoas Jurídicas). O agente analisa documentos financeiros, consulta bureaus de crédito, avalia garantias e emite parecer técnico estruturado.

CS

#### Carlos Silva

Gerente de TI - Área de Crédito

A diretoria aprovou o projeto do agente de IA para análise de crédito PJ. Agora Carlos precisa apresentar o orçamento mensal de operação em produção. Ele tem 48 horas para entregar uma estimativa detalhada com cenário otimizado e cenário pessimista.

1

Estimar custo mensal do agente em produção

2

Comparar cenário otimizado vs não-otimizado

3

Identificar oportunidades de economia

4

Justificar ROI para a diretoria

## Dados Fornecidos para Cálculo

### Volume Mensal de Análises

2,500

Total/mês

1,500

Real-time (60%)

1,000

Batch (40%)

114

Por dia útil

### Composição de Tokens por Análise (Real-time)

Input Texto

8,000 tokens

Prompts + dados do cliente (CNPJ, faturamento, setor, histórico)

Input PDFs (Multi-modal)

135,000 tokens

• 3 documentos × 45,000 tokens cada

• Arquivos: Balanço Patrimonial, DRE (Demonstrativo de Resultados), Contratos sociais

Input Imagens (Multi-modal)

516 tokens

• 2 fotos × 258 tokens cada • Fotos de garantias (imóveis, equipamentos)

Grounding (Dados Externos)

4 consultas/análise

Serasa Experian

$35/1k

Cotação Dólar (PTAX)

$35/1k

Regulamentação Bacen

$35/1k

Score de Risco Setorial

$35/1k

Total mensal: 10,000 calls

Context Caching

80,000 tokens

Manual de Políticas de Crédito BV (v3.2 - atualizado trimestralmente)

Reutilizado: Sim TTL: 24 horas

Output (Structured)

2,500 tokens

Parecer técnico estruturado em JSON (score, recomendação, justificativa, alertas)

Thinking Mode

ATIVO

Análise de risco requer raciocínio complexo e decomposição de tarefas

Output tokens são DUPLICADOS (output regular + thinking)

### Modelo Recomendado

Gemini 2.5 Pro

Thinking Mode disponível

Quota gratuita de grounding maior (10k/dia vs 1.5k do Flash)

Melhor performance em raciocínio complexo

Context window de 2M tokens

## Seu Desafio

Use a calculadora oficial do Google Cloud para estimar os custos mensais nos dois cenários:

Abrir Google Cloud Pricing Calculator

### Cenário Otimizado

Context Caching ativo para o manual de 80k tokens

40% das análises processadas em Batch (madrugada)

Grounding dentro da quota gratuita do Pro (10k/dia = 220k/mês)

Output otimizado com schema enxuto (2.500 tokens)

Thinking Mode ativo

Sua estimativa:

$ _____ / mês

### Cenário Não-Otimizado

SEM Context Caching (re-envia manual 80k toda vez)

100% real-time (nenhum batch)

Grounding EXCEDE quota gratuita (paga tudo)

Output verboso (4.000 tokens em vez de 2.500)

Thinking Mode ativo

Sua estimativa:

$ _____ / mês

#### Análise Comparativa

Economia Absoluta

$ _____

Economia %

____%

Economia Anual

$ _____

## Gabarito Detalhado

### Cenário Otimizado (Melhores Práticas)

#### Real-time Input (1.500 análises)

Texto: 1.500 × 8.000 = 12.000.000 tokens

PDFs: 1.500 × 135.000 = 202.500.000 tokens

Imagens: 1.500 × 516 = 774.000 tokens

Cached: 1.500 × 80.000 cached = 120.000.000 tokens cached

Custo Input Real-time: $284.09

• Normal: 215.274.000 × $1.25/1M = $269.09 • Cached: 120.000.000 × $0.125/1M = $15.00

#### Real-time Output (1.500 análises)

Output regular: 1.500 × 2.500 = 3.750.000 tokens

Thinking mode: 1.500 × 2.500 = 3.750.000 tokens (thinking mode)

Total: 7.500.000 tokens

Custo Output Real-time: 7.500.000 × $5.00/1M = $37.50

#### Batch Input (1.000 análises) - 50% desconto

Texto: 1.000 × 8.000 = 8.000.000 tokens

PDFs: 1.000 × 135.000 = 135.000.000 tokens

Imagens: 1.000 × 516 = 516.000 tokens

Cached: 1.000 × 80.000 cached = 80.000.000 tokens cached

Custo Input Batch: $94.70

• Normal: 143.516.000 × $1.25/1M × 0.5 = $89.70 • Cached: 80.000.000 × $0.125/1M × 0.5 = $5.00

#### Batch Output (1.000 análises) - 50% desconto

Output regular: 1.000 × 2.500 = 2.500.000 tokens

Thinking mode: 1.000 × 2.500 = 2.500.000 tokens

Total: 5.000.000 tokens

Custo Output Batch: 5.000.000 × $5.00/1M × 0.5 = $12.50

#### Context Cache Storage

Tokens: 80.000 tokens

Período: 720 horas/mês (30 dias × 24h)

Custo Storage: (80.000 / 1.000.000) × $4.50 × 720 = $259.20

#### Grounding

2.500 análises × 4 calls = 10.000 calls/mês

10.000 calls/dia × 22 dias = 220.000 calls/mês (Pro)

Custo Grounding: $0.00 (dentro da quota gratuita)

#### Custo Total Mensal (Otimizado)

Input Real-time

$284.09

Output Real-time

$37.50

Input Batch

$94.70

Output Batch

$12.50

Cache Storage

$259.20

Grounding

$0.00

$687.99/mês

### Cenário Não-Otimizado (Sem Boas Práticas)

#### 100% Real-time Input (2.500 análises)

Texto: 2.500 × 8.000 = 20.000.000 tokens

PDFs: 2.500 × 135.000 = 337.500.000 tokens

Imagens: 2.500 × 516 = 1.290.000 tokens

Manual SEM cache: 2.500 × 80.000 = 200.000.000 tokens (SEM cache!)

Custo Input: 558.790.000 × $1.25/1M = $698.49

#### Output (2.500 análises, verboso)

Output regular: 2.500 × 4.000 = 10.000.000 tokens

Thinking mode: 2.500 × 4.000 = 10.000.000 tokens

Total: 20.000.000 tokens

Custo Output: 20.000.000 × $5.00/1M = $100.00

#### Grounding (PAGANDO TUDO)

2.500 análises × 4 calls = 10.000 calls/mês

Excedido (implementação incorreta, não usa quota Pro)

Custo Grounding: 10.000 × $35/1.000 = $350.00

#### Custo Total Mensal (Não-Otimizado)

Input

$698.49

Output

$100.00

Grounding

$350.00

$1.148.49/mês

### Economia com Otimizações

Economia Mensal

$460.50

Economia %

40%

Economia Anual

$5.526/ano

De $1.148.49 para $687.99 por mês

## Otimizações Avançadas PLUS

Técnicas arquiteturais que vão além do óbvio e podem economizar centenas de dólares adicionais por mês.

### 1. Tool Calling vs Grounding (ECONOMIA MASSIVA)

Dificuldade: Médio

Problema

Grounding Serasa custa $35/1.000 requests. Para 2.500 análises/mês com 1 consulta Serasa cada = 2.500 calls × $35/1k = $87.50/mês

Solução

Criar Tool personalizado que chama API REST interna do BV (que já tem contrato corporativo com Serasa Experian). O custo da API é zero para o projeto (já pago pelo banco).

Implementação

```
# Tool customizado para Serasa
      @tool
      def consultar_serasa_bv(cnpj: str) -> dict:
          """Consulta score Serasa via API interna BV."""
          response = requests.post(
              'https://api.bv.com.br/v1/serasa/score',
              headers={'Authorization': f'Bearer {BV_TOKEN}'},
              json={'cnpj': cnpj}
          )
          return response.json()

      # Usar no agente
      tools = [consultar_serasa_bv]
```

Em vez de grounding, o agente chama a tool que usa a API interna

Economia

Mensal

$87.50 (só Serasa) até $350.00 (todas as 4 consultas)

Anual

$1.050 a $4.200

2.500 consultas × $35/1k = $87.50 eliminados

Bônus

- Latência 60% menor (API direta vs grounding)
- Controle total sobre dados retornados
- Sem dependência de quota de grounding
- Logs e auditoria internos

Trade-offs

- Precisa manter API interna (DevOps)
- Requer contratos diretos com provedores
- Time de TI precisa gerenciar integrações

Quando já existe API interna ou contrato corporativo com o fornecedor de dados

### 2. Pré-processamento de PDFs

Dificuldade: Fácil

Problema

PDFs enviados como imagem custam ~45k tokens CADA. 3 PDFs × 45k = 135k tokens por análise.

Solução

Extrair texto do PDF antes de enviar para o LLM usando OCR (Tesseract) ou bibliotecas Python (pypdf, pdfplumber). Texto puro reduz 60-70% dos tokens.

Implementação

```
import pdfplumber

      def extract_pdf_text(pdf_path: str) -> str:
          """Extrai texto de PDF, reduz ~70% tokens."""
          with pdfplumber.open(pdf_path) as pdf:
              text = ""
              for page in pdf.pages:
                  text += page.extract_text()
          return text

      # Antes: 135k tokens (PDF como imagem)
      # Depois: ~40k tokens (texto extraído)
```

Envia texto puro em vez de imagem do PDF

Economia

Mensal

~$178 em input tokens

2.500 análises × 95k tokens economizados × $1.25/1M = $296.88 → $118.75 = $178.13 economia

Trade-offs

- Pode perder formatação/layout
- OCR tem custo computacional
- Precisa validar qualidade da extração

Quando NÃO usar

- • PDFs com tabelas complexas multi-coluna
- • Documentos com gráficos/charts essenciais
- • PDFs escaneados de baixa qualidade
- • Quando layout visual é importante

### 3. Cache de Dados Externos (Smart Caching)

Dificuldade: Médio

Problema

Cotação do dólar (PTAX) é consultada via grounding 2.500 vezes/mês, mas muda apenas 1x/dia. Custo: 2.500 × $35/1k = $87.50

Solução

Implementar cache Redis com TTL de 1 hora para dados que mudam pouco. Uma única consulta serve para ~100 análises.

Implementação

```
import redis
      from datetime import timedelta

      redis_client = redis.Redis(host='localhost')

      @tool
      def get_cotacao_dolar_cached() -> float:
          """Cotação PTAX com cache de 1h."""
          cached = redis_client.get('ptax:usd:brl')
          if cached:
              return float(cached)

          # Consulta real (grounding ou API)
          cotacao = consultar_bacen_ptax()
          redis_client.setex(
              'ptax:usd:brl',
              timedelta(hours=1),
              str(cotacao)
          )
          return cotacao
```

Cache reduz 95% das consultas redundantes

Economia

Mensal

~$83 (95% de $87.50)

2.500 consultas → 25 consultas reais (cache hit 99%)

Cotações (atualizam 1x/dia) Regulamentações (mudam raramente) Scores setoriais (semanais) Dados públicos estáticos

### 4. Modelo Tiering (Flash para Triagem)

Dificuldade: Alto

Problema

Gemini 2.5 Pro custa $1.25/1M input. Flash custa $0.30/1M (4.1x mais barato). Nem toda análise precisa do Pro.

Solução

Implementar pipeline de 2 estágios: (1) Flash faz triagem rápida e classifica complexidade, (2) Pro só para casos complexos/alto valor.

Implementação

```
def analyze_credit(data):
          # Estágio 1: Triagem com Flash
          flash_model = GenerativeModel('gemini-2.5-flash')
          triage = flash_model.generate_content(
              f"Classifique complexidade (1-10): {data}"
          )

          complexity = extract_score(triage.text)

          if complexity <= 6:
              # 70% dos casos: Flash resolve
              return flash_model.generate_content(
                  f"Análise completa: {data}"
              )
          else:
              # 30% dos casos: Pro + Thinking
              pro_model = GenerativeModel('gemini-2.5-pro')
              return pro_model.generate_content(
                  data,
                  generation_config={'thinking': True}
              )
```

```
Fluxo de 2 estágios:

      1. TRIAGEM (Flash):
         - Análise rápida dos dados básicos
         - Score de complexidade (1-10)
         - Casos simples (score ≤6): Flash emite parecer

      2. ANÁLISE PROFUNDA (Pro):
         - Casos complexos (score >6): ~30% dos casos
         - Thinking Mode + análise detalhada
         - PDFs completos + grounding
```

Economia

Mensal

~$400-500

70% das análises com modelo 4x mais barato = ~60% economia total no input

1.750 análises × Flash ($0.30) + 750 × Pro ($1.25)

Trade-offs

- Lógica de roteamento adicional
- Necessita calibração do threshold
- 2 chamadas para casos Pro (triagem + análise)

Critérios para Pro Model

- • Valores >R$ 500.000
- • Empresas com histórico irregular
- • Setores de alto risco
- • Garantias complexas

### 5. Structured Output Otimizado

Dificuldade: Fácil

Problema

Output JSON verboso com 2.500 tokens. Thinking mode dobra isso para 5.000 tokens efetivos. Output custa $5/1M, então 2.500 análises × 5k tokens = 12.5M tokens × $5 = $62.50

Solução

Criar schema JSON enxuto com apenas campos essenciais. Usar abbreviations e códigos em vez de textos longos.

Implementação

```
generation_config = {
          'response_mime_type': 'application/json',
          'response_schema': {
              'type': 'object',
              'properties': {
                  'rec': {'type': 'string', 'enum': ['APR', 'APR_RESS', 'REJ']},
                  'score': {'type': 'integer'},
                  'motivo': {'type': 'string', 'maxLength': 50},
                  'alerts': {'type': 'array', 'items': {'type': 'string'}}
              },
              'required': ['rec', 'score']
          }
      }
```

Economia

Mensal

~$42 em output

2.500 × (5.000 - 1.600) tokens = 8.5M tokens × $5/1M = $42.50

Trade-offs

- Menos legível para humanos
- Precisa de dicionário de códigos
- Front-end precisa expandir abreviações

Técnicas

- • Usar códigos (APR, REJ) em vez de textos longos
- • Limitar strings com maxLength
- • Remover campos opcionais não-críticos
- • Usar enums para valores fixos

### 6. Image Compression Inteligente

Dificuldade: Muito Fácil

Problema

Fotos de imóveis/garantias podem ter 5-10MB. Gemini tokeniza imagens grandes em mais tokens (~1.5-2x). 2 imagens × 516 tokens base, mas pode chegar a 1.000 tokens cada se não comprimidas.

Solução

Redimensionar imagens para resolução ótima (1024×768px) antes de enviar. Mantém qualidade visual mas reduz ~40% dos tokens.

Implementação

```
from PIL import Image

      def optimize_image_for_llm(image_path: str, max_size=1024):
          """Redimensiona imagem mantendo aspect ratio."""
          img = Image.open(image_path)

          # Redimensionar se maior que max_size
          if max(img.size) > max_size:
              img.thumbnail((max_size, max_size), Image.LANCZOS)

          # Converter para RGB se necessário
          if img.mode != 'RGB':
              img = img.convert('RGB')

          # Salvar otimizado
          output_path = f"{image_path}_optimized.jpg"
          img.save(output_path, 'JPEG', quality=85, optimize=True)
          return output_path

      # Antes: 5MB imagem = ~1.000 tokens
      # Depois: 500KB imagem = ~516 tokens (economia ~48%)
```

Gemini não precisa de resolução 4K para identificar um imóvel

Economia

Mensal

~$1-2 (pequeno, mas sem esforço)

2.500 análises × 2 imagens × 484 tokens economizados = 2.42M × $1.25/1M = $3.03

Guidelines

- • 1024px para documentos/fotos gerais
- • 2048px se detalhes finos são críticos
- • JPEG quality 85 (sweet spot)
- • Converter PNG → JPEG quando possível

### 7. Thinking Mode Condicional

Dificuldade: Médio

Problema

Thinking Mode DOBRA o custo de output ($5 → $10 efetivo por 1M tokens). Para 2.500 análises: 12.5M output tokens × $10 = $125/mês. Nem toda análise precisa de raciocínio profundo.

Solução

Ativar Thinking Mode apenas para análises de alto risco/alto valor (>R$ 500k). Para casos simples, modelo sem thinking é suficiente.

Implementação

```
def analyze_with_conditional_thinking(data):
          model = GenerativeModel('gemini-2.5-pro')

          # Critérios para Thinking Mode
          needs_thinking = (
              data['valor_credito'] > 500000 or  # >R$500k
              data['score_bureau'] < 600 or       # Score baixo
              data['setor'] in ['construção', 'agro']  # Setores voláteis
          )

          config = {
              'thinking': needs_thinking,
              'temperature': 0.2
          }

          return model.generate_content(data, generation_config=config)

      # Apenas ~20% das análises ativam thinking mode
```

Thinking Mode só quando realmente necessário

Economia

Mensal

~$50

80% análises (2.000) SEM thinking: 2.000 × 2.5k × ($10 - $5) / 1M = $25 economia × 2 = $50

Trade-offs

- Análises simples podem ser menos profundas
- Precisa definir thresholds
- Monitorar taxa de aprovação por categoria

Critérios para Thinking Mode

- • Crédito >R$ 500.000
- • Score bureau <600
- • Histórico com defaults
- • Setores de alto risco
- • Garantias complexas/múltiplas

Impacto: Alto - thinking mode é um dos maiores custos

### Discussão em Grupo

"Se você pudesse implementar APENAS 3 otimizações, quais escolheria e por quê? Calcule o ROI de cada uma."

Considere:

- • Economia absoluta ($)
- • Dificuldade de implementação
- • Tempo para implementar
- • Risco/complexidade de manutenção

## Pontos de Discussão

1

#### Por que Context Caching economiza tanto?

Porque o manual de 80k tokens seria enviado 2.500 vezes/mês SEM cache (200M tokens × $1.25 = $250). COM cache, paga apenas $15 (cached rate) + $259 (storage) = $274, mas elimina $250 de custo normal. A economia real vem de NÃO pagar o preço cheio repetidamente.

2

#### Tool Calling vs Grounding: quando usar cada um?

Tool Calling quando você já tem API/contrato (Serasa, CRM interno). Grounding quando precisa de dados públicos/web que você NÃO controla (cotações em tempo real, notícias, regulamentações que mudam).

3

#### Qual otimização tem o melhor ROI (Retorno sobre Investimento)?

Tool Calling ($350 economia) com dificuldade média. Structured Output ($42 economia) é fácil mas baixo retorno. Modelo Tiering ($400-500 economia) tem ROI altíssimo MAS é complexo de implementar.

4

#### Por que a quota de grounding do Pro é importante?

Pro tem 10k calls/dia gratuitos (220k/mês). Flash tem apenas 1.5k/dia (33k/mês). Com 10k calls/mês de grounding, Pro fica GRÁTIS enquanto Flash pagaria $350. Isso pode inverter a escolha de modelo!

### Armadilhas Comuns

##### Esquecer o custo de STORAGE do cache

Calculadora do Google tem campo separado. Muitos alunos somam só o 'cached input price' e esquecem os $4.50/1M/hora de armazenamento.

##### Não considerar Thinking Mode no output

Thinking Mode NÃO aparece explícito na calculadora. Output tokens são 'duplicados' (output normal + thinking), dobrando o custo efetivo.

##### Confundir quota de grounding Flash vs Pro

Flash: 1.5k/dia. Pro: 10k/dia. Diferença de 6.6x! Para 10k calls/mês, Flash paga $350 enquanto Pro é grátis.

##### Ignorar que Batch API precisa de processamento assíncrono

Batch não é para análises em tempo real. Se o gerente precisa da resposta na hora, não pode usar batch. Os 50% de desconto só valem se pode esperar horas.

##### Calcular tokens de PDF incorretamente

1 página ≠ X tokens fixos. Depende de: densidade do texto, tabelas, imagens embutidas. A estimativa de 45k por PDF (15 páginas) é média, pode variar 30-60k.

## Setup Guide

1

### Python

Versão 3.10+

```
# Verificar versão do Python
python --version
# Resultado esperado: Python 3.10+ (recomendado 3.11)
```

2

### Ambiente Virtual (venv)

Isolamento de dependências

```
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (PowerShell)
.\.venv\Scripts\Activate.ps1

# Verificar se ativou (deve aparecer (.venv) no prompt)
```

3

### Google Cloud CLI

Autenticação

```
# Verificar instalação do Google Cloud CLI
gcloud --version

# Autenticar na sua conta Google
gcloud auth login

# Configurar Application Default Credentials (ADC)
gcloud auth application-default login

# Configurar projeto (substitua pelo seu PROJECT_ID)
gcloud config set project SEU_PROJECT_ID

# Verificar configuração
gcloud config list
```

4

### Google ADK

Framework oficial

```
# Instalar Google ADK
pip install google-adk

# Verificar instalação
adk --version

# Criar primeiro projeto de agente
adk init meu-primeiro-agente

# Entrar no diretório criado
cd meu-primeiro-agente

# Ver estrutura do projeto
Get-ChildItem -Recurse
```

### Progresso do Setup

0/4

## Ambiente Vertex AI

### Google Cloud SDK

Infraestrutura geral

- CLI para todos os serviços GCP
- Autenticação (gcloud auth)
- Gerenciamento de projetos

### Google ADK

Agent Development Kit

- Framework para agentes de IA
- Estrutura padronizada
- Integração Gemini

### Estrutura ADK

```
meu-primeiro-agente/
      ├── prompts/  # System prompts
      ├── tools/    # Ferramentas Python
      ├── config/   # Configurações
      ├── agent.py     # Código principal
      └── requirements.txt
```
