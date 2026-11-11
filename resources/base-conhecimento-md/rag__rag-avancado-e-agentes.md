# Aula 2: RAG & Agentes Inteligentes | Bootcamp Itaú FIAP

Fundamentos

## Por que RAG?

O problema da janela de contexto e a necessidade de dados privados em tempo real.

### O Problema do Contexto

- • Alucinação: LLMs inventam fatos quando não possuem informação suficiente, criando respostas plausíveis mas incorretas.
- • Janela Limitada: GPT-4 tem ~128k tokens (~100k palavras). Você não pode colar 10.000 contratos simultaneamente.
- • Dados Desatualizados: Modelo treinado até 2023 não sabe sobre mudanças regulatórias de 2026 ou dados em tempo real do seu sistema.
- • Privacidade & Compliance: Dados sensíveis do Itaú não podem ser enviados para o treinamento de modelos públicos (OpenAI, Anthropic).

### A Solução RAG

- 1. Retrieval (Busca): Transforme a pergunta do usuário em embedding e busque os top-K chunks mais relevantes no Vector DB.
- 2. Augmentation (Aumento): Injete esses chunks diretamente no prompt do LLM como "contexto autoritativo".
- 3. Generation (Geração): Instrua o LLM: "Responda APENAS com base no contexto fornecido. Se não souber, diga que não sabe."

Resultado: LLM responde com dados privados atualizados, sem precisar retreinar o modelo.

### Casos de Uso no Itaú

📄

#### Análise de Contratos

Extrair cláusulas, garantias e riscos de contratos de crédito.

📊

#### Relatórios Regulatórios

Responder perguntas sobre compliance BACEN com base em manuais internos.

💬

#### Chatbot de Políticas

Assistente que responde dúvidas de funcionários sobre RH, benefícios, etc.

### RAG vs Fine-tuning: Custo

| Métrica | RAG | Fine-tuning |
| --- | --- | --- |
| Custo Inicial | $50-200 (embedding + indexing) | $10,000-100,000 (training epochs) |
| Atualização de Dados | Instantânea (re-index chunk) | Horas/dias (re-training) |
| Transparência | Alta (mostra fonte dos chunks) | Baixa (caixa-preta) |
| Melhor para | Conhecimento factual privado | Estilo de escrita, domínio específico |

Fundamentos

## Arquitetura RAG Básica

Os 3 componentes essenciais: Document Processing, Vector Store e Query Engine.

### Pipeline Completo

Documentos

PDFs, Contratos, Manuais

Chunking + Embedding

Vector Store

ChromaDB, Pinecone

Similarity Search

LLM

GPT-4, Claude

📝

#### 1. Document Processing

- Extraction: PDFs → texto puro
- Chunking: Dividir em parágrafos
- Embedding: texto → vetor (1536D)
- Indexing: Salvar no vector DB

🔍

#### 2. Retrieval

- Query Embedding: Pergunta → vetor
- Similarity: Cosine/Euclidean
- Top-K: Retorna 3-5 chunks
- Metadata: Filtros (data, tipo)

🤖

#### 3. Generation

- Prompt: System + Context + Query
- LLM Call: OpenAI/Anthropic API
- Parsing: JSON structured output
- Citation: Link para fonte

### Métricas de Performance

95%

Precision@5

Top-5 chunks relevantes

200ms

Latency

Tempo de retrieval

1M+

Vectors

Capacidade ChromaDB

$0.10

Cost/Query

Embedding + LLM

Fundamentos

## RAG vs Fine-tuning

Quando usar cada abordagem? Trade-offs e casos de uso ideais.

| Critério | RAG | Fine-tuning |
| --- | --- | --- |
| Propósito | Adicionar conhecimento factual externo | Ajustar comportamento e estilo de resposta |
| Custo | Baixo ($50-500) | Alto ($10k-100k) |
| Tempo de Setup | Minutos/Horas | Dias/Semanas |
| Atualização | Instantânea (re-index) | Lenta (re-training) |
| Transparência | Alta (mostra fontes) | Baixa (caixa-preta) |
| Escalabilidade | Excelente (milhões de docs) | Limitada (tamanho do dataset) |
| Melhor para | Documentos internos Dados em tempo real Compliance/Regulatório | Tom de voz específico Domínio técnico especializado Formato de saída consistente |

### Árvore de Decisão

PERGUNTA

Você precisa adicionar conhecimento novo/privado?

Ex: "Qual a cláusula de garantias no contrato X?"

→

RAG

PERGUNTA

Você quer mudar o comportamento do modelo?

Ex: "Sempre responda em formato JSON, usando linguagem formal bancária"

→

FINE-TUNE

HÍBRIDO

Melhor dos dois mundos

1. Fine-tune o modelo para entender jargão bancário 2. Use RAG para buscar contratos específicos → Resposta precisa em tom corporativo

#### Casos Ideais para RAG

- • Chatbot de Políticas Internas Manuais do RH, benefícios, compliance
- • Auditor de Contratos Buscar cláusulas específicas em 10k contratos
- • Q&A sobre Transações Dados em tempo real do sistema bancário

#### Casos Ideais para Fine-tuning

- • Gerador de Relatórios Sempre estruturado, formato BACEN
- • Assistente SQL Converter linguagem natural em queries específicas do Oracle
- • Classificador de Risco Modelo treinado em histórico de defaults

## Estratégias de Chunking

CHUNK ID: 0 | TOKENS: ~7.25 CONTRATO DE MÚTUO CONVERSÍVEL

CHUNK ID: 1 | TOKENS: ~80 CLÁUSULA PRIMEIRA - DO OBJETO 1.1. Pelo presente instrumento, a MUTUANTE disponibiliza à MUTUÁRIA a quantia de R$ 1.500.000,00 (um milhão e quinhentos mil reais), doravante denominada "Principal". 1.2. O recurso deverá ser utilizado exclusivamente para expansão tecnológica da MUTUÁRIA, conforme plano de negócios anexo.

CHUNK ID: 2 | TOKENS: ~53 CLÁUSULA SEGUNDA - DOS JUROS E CORREÇÃO 2.1. Sobre o Principal incidirão juros remuneratórios de 1% (um por cento) ao mês, calculados pro rata temporis. 2.2. O valor será corrigido anualmente pelo IPCA acumulado.

CHUNK ID: 3 | TOKENS: ~67 CLÁUSULA TERCEIRA - DO VENCIMENTO E PAGAMENTO 3.1. O vencimento deste contrato ocorrerá em 36 (trinta e seis) meses a contar da data de assinatura. 3.2. O pagamento será bullet (parcela única) ao final do período, salvo em caso de conversão em participação societária.

CHUNK ID: 4 | TOKENS: ~46 CLÁUSULA QUARTA - DAS GARANTIAS 4.1. Como garantia fiel do cumprimento das obrigações, a MUTUÁRIA oferece em alienação fiduciária o imóvel de matrícula nº 12345 do 2º CRI de São Paulo.

CHUNK ID: 5 | TOKENS: ~28.5 CLÁUSULA QUINTA - DO INADIMPLEMENTO 5.1. O atraso superior a 10 dias implicará multa de 10% sobre o saldo devedor.

Engenharia de Dados

## Embedding Models

Transformando texto em vetores numéricos para busca semântica.

### O que são Embeddings?

Embeddings são representações vetoriais de texto onde palavras/frases semanticamente similares ficam próximas no espaço vetorial.

"Contrato de mútuo"

→ [0.023, -0.145, 0.891,..., 0.234]

1536 dimensões

### Comparativo de Modelos

OpenAI ada-002 1536D

Cohere embed-v3 1024D

BGE-large-en 768D

### Vector Space Visualization

1536D → 2D (t-SNE)

#### Busca Semântica

Termo Score

Lucro 0.89

Dinheiro 0.85

Maçã 0.12

Engenharia de Dados

## Vector Databases

Armazenamento otimizado para busca por similaridade vetorial.

### Comparativo de Soluções

| Solução | Tipo | Escala | Custo | Melhor para |
| --- | --- | --- | --- | --- |
| ChromaDB | Embarcado | ~1M vectors | Gratuito | Protótipos, local dev |
| Pinecone | Cloud SaaS | Bilhões | $70+/mês | Produção, alta escala |
| Weaviate | Self-hosted | Milhões | Open-source | On-premise, compliance |
| Qdrant | Self/Cloud | Milhões | Variável | Performance, Rust |
| FAISS (Meta) | Biblioteca | Milhões | Gratuito | Research, embeddings |

### Por que ChromaDB?

- Zero Setup: Pip install e pronto, sem servidor externo
- Python-First: API intuitiva, integração direta com LangChain
- Metadata Filtering: Filtros por data, tipo, autor
- Persistência: SQLite embarcado, não precisa de DB externo

### Quando migrar para Pinecone?

- → Escala: Mais de 10M de vetores
- → Latência: Precisa de <50ms de resposta
- → Multi-tenancy: Milhares de collections isoladas
- → Produção: SLA, backups automáticos, suporte

### Algoritmos de Indexação

#### Flat (Brute Force)

Precisão: 100% (exato)

Velocidade: O(N) - lento

Uso: <10k vectors

#### HNSW (Hierarchical)

Precisão: ~95% (aproximado)

Velocidade: O(log N) - rápido

Uso: Padrão da indústria

#### IVF (Inverted File)

Precisão: ~90% (aproximado)

Velocidade: O(√N) - muito rápido

Uso: Bilhões de vectors

RAG Avançado

## Hybrid Search

Combinando Dense Retrieval (semântico) com Sparse Retrieval (keyword) para melhor precisão.

### O Problema da Busca Puramente Semântica

Embeddings capturam significado, mas podem falhar em buscas exatas de números, códigos ou nomes próprios específicos.

#### Falha Semântica

Query: "Contrato matrícula 12345"

Pode retornar "Contrato matrícula 54321" porque semanticamente é similar, mas o número exato é ignorado.

#### Solução Híbrida

Dense (70%) + Sparse (30%)

Busca semântica + keyword matching garante que "12345" seja encontrado exatamente.

### Arquitetura Hybrid Search

🔍

Query

"Garantia imóvel 12345"

Dense (Embedding)

[0.12, -0.45,..., 0.78]

70%

Sparse (BM25/TF-IDF)

["garantia": 0.8, "12345": 1.0]

30%

→

✅

Merged Results

Score: 0.94

### Quando Usar?

🔢

#### Identificadores Únicos

CPF, CNPJ, matrícula, protocolo

📅

#### Datas Específicas

"contratos de 2024", "vencimento 15/03"

👤

#### Nomes Próprios

Pessoas, empresas, lugares específicos

RAG Avançado

## Re-ranking

Melhorando a precisão dos resultados com Cross-Encoders e Cohere Rerank.

### Limitação da Busca Vetorial Simples

Embeddings capturam similaridade bi-encoder: Query e Document são codificados independentemente. Isso é rápido mas perde interação contextual.

Bi-Encoder (Rápido)

encode(query) → [0.1, 0.5,...] encode(doc) → [0.2, 0.4,...] cosine(query, doc) = 0.87

⚡ Milhões de docs em ~100ms

Cross-Encoder (Preciso)

encode(query + doc together) → relevance_score = 0.92

🐢 Apenas top-K docs (mais lento)

### Pipeline de 2 Estágios

Stage 1: Retrieval (Bi-Encoder)

Busca rápida no ChromaDB → Retorna top-100 candidatos

⏱️ ~50ms | Recall: 85%

→

Stage 2: Re-ranking (Cross-Encoder)

Re-score top-100 com contexto completo → Retorna top-5

⏱️ ~200ms | Precision@5: 95%

Resultado: Melhor dos dois mundos - velocidade do bi-encoder + precisão do cross-encoder

### Cohere Rerank API

Serviço managed de re-ranking. Envie query + top-100 docs, receba scores otimizados.

Custo: $2/1k searches

Latência: ~200-300ms

Suporte: 100+ idiomas

### Cross-Encoder Self-Hosted

Modelos open-source (HuggingFace): cross-encoder/ms-marco-MiniLM-L-6-v2

- Custo: Zero (GPU própria)
- Privacidade: Dados não saem do data center
- Manutenção: Precisa gerenciar infra

RAG Avançado

## HyDE

Hypothetical Document Embeddings: Gerando documentos sintéticos para melhorar a busca.

### A Ideia Central

Problema: A query do usuário é curta e pode não ter overlap semântico com os documentos.

Solução HyDE: Use o LLM para gerar uma resposta hipotética à query, então busque documentos similares a essa resposta (não à query original).

❌ Busca Tradicional

Query: "Quais as garantias?"

embed("Quais as garantias?") → Busca no DB

Poucas palavras-chave para match

✅ HyDE

Query: "Quais as garantias?"

LLM gera: "Alienação fiduciária de imóvel..." embed(resposta_hipotética) → Busca

Mais contexto semântico para match

### Pipeline HyDE

1. User Query

"Garantias do contrato?"

→

2. LLM Generation

Prompt: "Imagine uma resposta sobre garantias de contratos..." LLM: "A garantia típica é alienação fiduciária de imóvel comercial..."

3. Embedding

embed(resposta_hipotética) → [0.23, -0.45,..., 0.89]

→

4. Retrieval

Top-5 docs similares

### Vantagens

- Queries curtas viram documentos ricos em contexto
- Melhora recall quando vocabulário é diferente
- Funciona bem com domínios técnicos

### Trade-offs

- Adiciona latência (1 chamada extra ao LLM)
- Aumenta custo (~$0.002 por query)
- LLM pode "alucinar" na resposta hipotética

RAG Avançado

## Parent-Child Chunking

Busca em chunks pequenos, retorna contexto completo dos pais.

### O Dilema do Chunk Size

#### Chunks Pequenos (100 tokens)

- + Alta precisão na busca
- - Falta contexto (LLM não entende o parágrafo anterior)

#### Chunks Grandes (500 tokens)

- + Contexto completo para o LLM
- - Busca menos precisa (muito "ruído")

### Hierarquia Parent-Child

Parent Chunk (500 tokens)

"CLÁUSULA QUARTA - DAS GARANTIAS 4.1. Como garantia fiel do cumprimento das obrigações... 4.2. O imóvel deverá estar livre de ônus... 4.3. A MUTUÁRIA se compromete..."

ID: parent_123 | Armazenado mas NÃO indexado

↓ divide em ↓

Child 1 (100 tokens)

"4.1. Como garantia fiel..."

parent_id: parent_123

Child 2 (100 tokens)

"4.2. O imóvel deverá..."

parent_id: parent_123

Child 3 (100 tokens)

"4.3. A MUTUÁRIA se..."

parent_id: parent_123

Estratégia: Indexe apenas os children no vector DB. Quando encontrar match, retorne o parent completo para o LLM.

### Workflow na Prática

1

User query: "Quais garantias do contrato?"

2

Busca no ChromaDB encontra Child 1 (score: 0.92)

3

Sistema recupera parent_123 do armazenamento

4

Envia Parent Chunk completo (500 tokens) para o LLM

### Por que usar no Itaú?

#### Documentos Jurídicos

Contratos têm cláusulas numeradas. Busca precisa em 4.1, mas LLM precisa ver toda a CLÁUSULA QUARTA.

#### Manuais Técnicos

Procedimento tem 10 passos. Busca no passo 5, mas retorna seção completa para contexto.

RAG Avançado

## RAPTOR

Recursive Abstractive Processing for Tree-Organized Retrieval. Sumarizações hierárquicas para perguntas de alto nível.

### Limitação do RAG Tradicional

RAG padrão é excelente para perguntas específicas ("Qual a garantia da cláusula 4?"), mas falha em perguntas conceituais/abrangentes.

Exemplo de Falha:

User: "Qual o tema principal deste conjunto de 50 contratos?" RAG Tradicional: → Busca retorna 5 chunks aleatórios de contratos diferentes → LLM não consegue ver o "panorama geral" → Resposta é superficial ou incorreta

### Hierarquia RAPTOR

RAPTOR cria uma árvore de sumarizações em múltiplos níveis de abstração.

Level 0: Chunks Originais

C1

C2

C3

C4

C5

C6

C7

C8

↓ LLM sumariza clusters ↓

Level 1: Sumários Intermediários

S1

Resumo de C1-C2

S2

Resumo de C3-C4

S3

Resumo de C5-C6

S4

Resumo de C7-C8

↓ LLM sumariza novamente ↓

Level 2: Sumário Geral

SUMÁRIO FINAL

Visão panorâmica de todos os 8 chunks

### Como Funciona na Query?

Pergunta Específica:

"Qual o valor da multa na cláusula 5?"

→ Busca no Level 0 (chunks originais) → Retorna chunk específico com resposta precisa

Pergunta Intermediária:

"Quais os principais riscos deste contrato?"

→ Busca no Level 1 (sumários de seções) → Retorna sumários que consolidam múltiplas cláusulas

Pergunta Abrangente:

"Qual o padrão de risco em todos os contratos de 2024?"

→ Busca no Level 2 (sumário geral) → Retorna visão consolidada de alto nível

### Vantagens

- Responde perguntas conceituais/estratégicas
- Reduz informação irrelevante (foco nos sumários)
- Escalável para grandes corpora (milhares de docs)

### Trade-offs

- Setup complexo (gerar árvore de sumários)
- Custo alto (LLM sumariza cada cluster)
- Sumários podem perder detalhes importantes

Agentes LangChain

## ReAct Pattern

Reasoning + Acting: Agentes que pensam antes de agir.

### O que é ReAct?

ReAct = Rea soning + Act ion. É um padrão onde o agente alterna entre pensar (reasoning) e agir (tool calling) iterativamente até resolver o problema.

❌ Sem ReAct (Chain simples)

User: "Qual o câmbio e converta $100" LLM: "A taxa é aproximadamente 5.2..." ❌ Não chama API, alucina

✅ Com ReAct

Thought: "Preciso buscar taxa atual" Action: get_exchange_rate() Observation: 5.24 Thought: "Agora multiplico" Final Answer: R$ 524,00

### Loop Thought → Action → Observation

💭

Thought

LLM raciocina sobre o problema

"I need to find the customer's account balance first, then check if there are pending transactions."

↓

⚡

Action

Chama ferramenta específica

Action: get_account_balance Action Input: {"customer_id": "12345"}

↓

👁️

Observation

Resultado da ferramenta

Observation: Balance is R$ 5,420.30

↻ Repeat até ter resposta final

### Exemplo: Análise de Crédito

Thought 1: I need to get the customer's credit history first.

Action 1: get_credit_history(cpf="123.456.789-00")

Observation 1: Score: 720, No defaults in 5 years

Thought 2: Good score. Now check current income.

Action 2: get_income_data(cpf="123.456.789-00")

Observation 2: Monthly income: R$ 12,000

Thought 3: I have all needed info. Score is good and income is sufficient.

Final Answer: ✅ APROVADO - Limite sugerido: R$ 25,000

### Vantagens do ReAct

- LLM "explica" seu raciocínio (interpretável)
- Pode se auto-corrigir entre iterações
- Funciona com qualquer LLM (GPT-4, Claude)

### Desafios

- Pode entrar em loops infinitos (precisa max_iterations)
- Custo alto (múltiplas chamadas ao LLM)
- Latência variável (depende do número de steps)

Agentes LangChain

## Tool Calling & Function Calling

Integrando LLMs com APIs externas e sistemas bancários.

### O que são Tools?

Tools são funções Python que o agente pode chamar para realizar ações no mundo real: consultar APIs, ler bancos de dados, executar cálculos, etc.

🔍

#### Search Tools

Google, Wikipedia, ChromaDB

🗄️

#### Data Tools

SQL queries, REST APIs, GraphQL

⚙️

#### Action Tools

Email, Slack, criar ticket

### Anatomia de uma Tool

Uma tool em LangChain tem 3 componentes essenciais:

1. Name

"get_customer_balance"

Identificador único que o LLM usa para escolher

2. Description

"Useful for getting the current account balance of a customer. Input should be the customer CPF."

Instrução clara para o LLM saber QUANDO usar

3. Function

def get_customer_balance(cpf: str) -> float: # Chama API do Core Banking return balance

Implementação Python que executa a ação

### Tools para o Itaú

#### get_account_balance

Input: CPF

Output: Saldo atual (R$)

API: Core Banking REST

#### get_credit_score

Input: CPF

Output: Score (300-850)

API: Bureau de Crédito

#### search_contracts

Input: Customer ID

Output: Lista de contratos

Source: ChromaDB RAG

#### calculate_loan_eligibility

Input: Income, Score

Output: Limite aprovado

Logic: Regras de negócio

### Function Calling vs Tool Calling

| Aspecto | Function Calling (OpenAI) | Tool Calling (LangChain) |
| --- | --- | --- |
| Origem | Nativo do GPT-4 | Framework LangChain |
| Formato | JSON Schema | Python decorators |
| Execução | Manual (você executa) | Automática (agent executor) |
| Melhor para | Controle fino | Prototipagem rápida |

### Best Practices

- 1. Descriptions claras: Especifique exatamente quando usar a tool ❌ "Gets balance" ✅ "Use this when user asks about current account balance or available funds. Input is CPF."
- 2. Validação de inputs: Tools devem validar CPF, contas, etc.
- 3. Error handling: Retorne mensagens legíveis quando API falhar
- 4. Timeouts: APIs externas devem ter timeout de 5-10s

Agentes LangChain

## Planning & Multi-step Reasoning

Agentes que criam planos antes de executar, reduzindo erros e melhorando eficiência.

### Problema do ReAct Puro

ReAct é reativo: decide o próximo passo baseado apenas na observação anterior. Para tarefas complexas, isso leva a:

- • Ineficiência: Chama tools desnecessárias
- • Backtracking: Percebe erro tarde, precisa refazer steps
- • Loops: Fica preso em ciclos sem progresso

### Plan-and-Execute Pattern

Separa em 2 fases: Planning (criar plano completo) → Execution (executar steps sequencialmente).

#### Phase 1: Planning

1. LLM recebe task complexa

2. Gera plano com subtasks numeradas

3. Cada subtask tem dependências claras

#### Phase 2: Execution

1. Executor segue plano sequencialmente

2. Pode re-planejar se step falhar

3. Retorna resultado final

### Exemplo: Análise de Portfólio

User Query:

"Analise o portfólio do cliente 12345 e recomende realocação se necessário"

Generated Plan:

Step 1: Get customer risk profile (conservative/moderate/aggressive)

Step 2: Get current portfolio allocation (stocks/bonds/cash %)

Step 3: Compare allocation vs ideal for risk profile

Step 4: If deviation > 10%, generate rebalance recommendation

Execution Trace:

✓ Step 1: get_risk_profile(12345) → "moderate"

✓ Step 2: get_portfolio(12345) → 70% stocks, 20% bonds, 10% cash

✓ Step 3: Ideal for moderate: 60/30/10. Deviation: 10% stocks, -10% bonds

→ Step 4: Recommendation: Sell 10% stocks, buy bonds

### ReAct vs Plan-and-Execute

| Critério | ReAct | Plan-and-Execute |
| --- | --- | --- |
| Complexidade | Tarefas simples (1-3 steps) | Tarefas complexas (5+ steps) |
| Eficiência | Pode ser ineficiente | Otimizada (plano antecipado) |
| Adaptabilidade | Alta (reage a mudanças) | Média (precisa re-planejar) |
| Custo | Variável (loops) | Previsível |
| Quando usar | Exploração, incerteza | Workflows bem definidos |

Agentes LangChain

## Memory Systems

Dando contexto e histórico aos agentes para conversas naturais.

### Por que Memory?

LLMs são stateless: cada chamada é independente. Sem memória, o agente "esquece" a conversa anterior.

#### ❌ Sem Memory

User: "Meu saldo?"

Agent: "R$ 5,420"

User: "E o extrato?"

Agent: "De qual conta?"

❌ Esqueceu contexto

#### ✅ Com Memory

User: "Meu saldo?"

Agent: "R$ 5,420"

User: "E o extrato?"

Agent: "Aqui está o extrato da sua conta..."

✅ Lembra que já identificou o cliente

### Tipos de Memory

💬

Buffer Memory

Armazena as últimas N mensagens (ex: últimas 10).

messages = [msg1, msg2,..., msg10]

✅ Simples | ❌ Limita contexto longo

📝

Summary Memory

Sumariza conversas antigas em texto compacto.

summary = "Customer asked about balance, then requested loan info..."

✅ Contexto ilimitado | ❌ Pode perder detalhes

🏷️

Entity Memory

Extrai e rastreia entidades específicas (pessoas, contas, valores).

entities = { "customer_name": "João Silva", "account": "12345-6", "last_balance": 5420 }

✅ Dados estruturados | ❌ Setup complexo

🔍

Vector Memory

Armazena conversas em ChromaDB, busca mensagens relevantes semanticamente.

query: "loan discussion" retrieval: [msg_42, msg_89] (conversas sobre empréstimo)

✅ Contexto mais relevante | ❌ Adiciona latência

### Abordagem Híbrida (Recomendada)

Combine múltiplos tipos de memória para melhor desempenho:

Short-term

Buffer Memory (últimas 5 msgs)

Long-term

Summary Memory (resumo geral)

Structured

Entity Memory (dados do cliente)

### Implementação no Itaú

#### Chatbot de Atendimento

- • Buffer: últimas 10 mensagens da conversa
- • Entity: CPF, conta, saldo mencionados
- • Persiste no Redis com session_id

#### Assistente de Investimentos

- • Summary: conversas antigas sobre metas financeiras
- • Vector: busca discussões anteriores sobre fundos específicos
- • Persiste no PostgreSQL + ChromaDB

Agentes LangChain

## Agent Architectures

Padrões de orquestração: Router, Supervisor e Multi-Agent Systems.

### Router Agent

Classifica a intenção do usuário e roteia para o agente especializado correto.

User Query

→

ROUTER

Classifica intenção

→

Saldo Agent

Empréstimo Agent

Investimento Agent

Quando usar: Múltiplos domínios distintos (banking, investments, insurance) que não se comunicam entre si.

### Supervisor Agent

Orquestra múltiplos agentes subordinados, delegando subtarefas e agregando resultados.

SUPERVISOR

"Analisar crédito do cliente 12345"

↓ Delega subtarefas ↓

Credit Agent

Busca score

Income Agent

Verifica renda

Risk Agent

Calcula risco

↓ Agrega resultados ↓

SUPERVISOR

✅ APROVADO - Limite: R$ 25k

Quando usar: Tarefas complexas que requerem especialização (ex: análise de crédito com múltiplas fontes).

### Multi-Agent Collaboration

Agentes se comunicam entre si (peer-to-peer) sem hierarquia central.

Research Agent

Busca dados no ChromaDB

Writer Agent

Redige relatório com dados

Reviewer Agent

Revisa qualidade e compliance

Research ⟷ Writer ⟷ Reviewer

Quando usar: Workflows criativos onde agentes precisam iterar e refinar (ex: geração de relatórios).

### Comparativo

| Arquitetura | Comunicação | Complexidade | Melhor para |
| --- | --- | --- | --- |
| Router | 1:N (uma direção) | Baixa | Classificação simples |
| Supervisor | Hub-and-Spoke | Média | Orquestração hierárquica |
| Multi-Agent | Peer-to-Peer | Alta | Colaboração complexa |

Lab Prático

## Arquitetura do Projeto

Auditor de Contratos com RAG + Agente ReAct usando LangChain e ChromaDB.

### Objetivo do Projeto

Construir um agente que analisa contratos de mútuos bancários, extraindo metadados estruturados (garantias, taxas, riscos) usando RAG para contextualização.

📄

#### Input

PDFs de contratos de crédito

🤖

#### Processamento

RAG + Agent + Structured Output

📊

#### Output

JSON com metadados estruturados

### Arquitetura Completa

Layer 1: Document Ingestion

PyPDF

Extração de texto

RecursiveCharacterTextSplitter

Chunking semântico

OpenAI Embeddings

text-embedding-3-small

ChromaDB

Vector Store persistente

Layer 2: Retrieval

Query Embedding

Pergunta → vetor

Similarity Search

Top-3 chunks

Context Assembly

Monta prompt

Layer 3: ReAct Agent

Tools

search_contracts, extract_clause

GPT-4 Turbo

ReAct loop

Structured Output

Pydantic validation

Layer 4: Output

JSON Response

garantia_tipo, valor, prazo, risco_legal, compliance_status

### Stack Tecnológico

#### Core Libraries

langchain 0.1.0

chromadb 0.4.22

openai 1.10.0

pydantic 2.5.0

#### Utilities

pypdf2 3.0.1

python-dotenv 1.0.0

tiktoken 0.5.2

rich 13.7.0

Lab Prático

## Code Walkthrough

Implementação passo a passo do Auditor de Contratos com LangChain.

### 1. Setup & Imports

```
# auditor_contratos.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from pydantic import BaseModel, Field

# Carrega variáveis de ambiente
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

Crie um arquivo.env com sua chave: OPENAI_API_KEY=sk-...

### 2. Document Ingestion & Embedding

```
def ingest_contract(pdf_path: str, collection_name: str = "contratos"):
    """
    Carrega PDF, divide em chunks e indexa no ChromaDB.
    """
    # 1. Carregar PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # 2. Chunking (500 chars, overlap 50)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "]
    )
    chunks = text_splitter.split_documents(documents)
    
    # 3. Embedding + Indexing
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory="./chroma_db"
    )
    
    print(f"✅ Indexados {len(chunks)} chunks no ChromaDB")
    return vectorstore
```

### 3. Definição de Tools

```
def create_tools(vectorstore):
    """
    Cria tools para o agente usar.
    """
    
    def search_contract(query: str) -> str:
        """
        Busca chunks relevantes no contrato usando similaridade semântica.
        Input: pergunta sobre o contrato (ex: 'garantias', 'juros')
        """
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.get_relevant_documents(query)
        
        # Formata resultado
        context = "\n\n---\n\n".join([doc.page_content for doc in docs])
        return f"Chunks encontrados:\n{context}"
    
    def extract_clause(clause_number: str) -> str:
        """
        Extrai cláusula específica do contrato.
        Input: número da cláusula (ex: '4', '5.1')
        """
        query = f"CLÁUSULA {clause_number.upper()}"
        docs = vectorstore.similarity_search(query, k=1)
        
        if docs:
            return docs[0].page_content
        return f"Cláusula {clause_number} não encontrada."
    
    # Retorna lista de Tools
    return [
        Tool(
            name="search_contract",
            func=search_contract,
            description="Use this to search for information in the contract. Input should be a question or keyword."
        ),
        Tool(
            name="extract_clause",
            func=extract_clause,
            description="Use this to extract a specific clause number. Input should be the clause number like '4' or '5.1'."
        )
    ]
```

### 4. Structured Output Schema

```
class ContractMetadata(BaseModel):
    """
    Schema Pydantic para validar output estruturado.
    """
    garantia_tipo: str = Field(description="Tipo de garantia (ex: 'Alienação Fiduciária')")
    garantia_objeto: str = Field(description="Objeto dado em garantia (ex: 'Imóvel Matrícula 12345')")
    taxa_juros: float = Field(description="Taxa de juros mensal em %")
    prazo_meses: int = Field(description="Prazo do contrato em meses")
    valor_principal: float = Field(description="Valor principal do contrato em reais")
    risco_legal: str = Field(description="Classificação de risco: 'Baixo', 'Médio' ou 'Alto'")
    compliance_check: bool = Field(description="True se contrato está em compliance")
```

### 5. Criação do Agent ReAct

```
def create_auditor_agent(vectorstore):
    """
    Cria agente ReAct para auditar contratos.
    """
    # LLM
    llm = ChatOpenAI(
        model="gpt-4-turbo-preview",
        temperature=0,  # Determinístico para análise
        streaming=True
    )
    
    # Tools
    tools = create_tools(vectorstore)
    
    # Prompt Template ReAct
    prompt_template = """
    You are a legal contract auditor for Banco Itaú.
    Your task is to analyze contracts and extract structured metadata.
    
    You have access to the following tools:
    {tools}
    
    Use the following format:
    
    Thought: I need to find information about X
    Action: search_contract
    Action Input: "guarantees"
    Observation: [resultado da tool]
    ... (repeat Thought/Action/Observation as needed)
    Thought: I now have enough information
    Final Answer: [JSON with ContractMetadata schema]
    
    Question: {input}
    
    {agent_scratchpad}
    """
    
    # Cria Agent
    agent = create_react_agent(llm, tools, prompt_template)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )
    
    return agent_executor
```

### 6. Execução Principal

```
if __name__ == "__main__":
    # 1. Ingestão
    print("📄 Processando contrato...")
    vectorstore = ingest_contract("contrato_mutuo.pdf")
    
    # 2. Criar Agent
    print("🤖 Criando agente auditor...")
    agent = create_auditor_agent(vectorstore)
    
    # 3. Executar Análise
    print("🔍 Analisando contrato...\n")
    query = """
    Analyze this contract and extract:
    - Type and object of guarantee
    - Interest rate and term
    - Principal amount
    - Legal risk assessment
    - Compliance status
    
    Return as JSON following ContractMetadata schema.
    """
    
    result = agent.invoke({"input": query})
    
    # 4. Exibir Resultado
    print("\n✅ RESULTADO FINAL:")
    print(result["output"])
```

Para executar:

python auditor_contratos.py

Lab Prático

## Exercícios Práticos

Desafios hands-on para implementar durante a aula.

Básico

### Setup do Ambiente

Configure o ambiente Python com as dependências necessárias.

#### Tarefas:

#### Suas Anotações:

Salvo automaticamente no navegador

Básico

### Ingestão de Documento

Implemente a função de ingestão de PDFs no ChromaDB.

#### Tarefas:

#### Suas Anotações:

Salvo automaticamente no navegador

Intermediário

### Tool Customizada

Crie uma nova tool para calcular o custo total do contrato.

#### Tarefas:

#### Suas Anotações:

Salvo automaticamente no navegador

Intermediário

### Validação com Pydantic

Estenda o schema ContractMetadata com novos campos.

#### Tarefas:

#### Suas Anotações:

Salvo automaticamente no navegador

Avançado

### Hybrid Search

Implemente busca híbrida (dense + sparse) para melhorar retrieval.

#### Tarefas:

#### Suas Anotações:

Salvo automaticamente no navegador

Avançado

### Memory com ConversationBufferMemory

Adicione memória conversacional ao agente.

#### Tarefas:

#### Suas Anotações:

Salvo automaticamente no navegador

Avançado

### Multi-Document RAG

Indexe múltiplos contratos e implemente busca cross-document.

#### Tarefas:

#### Suas Anotações:

Salvo automaticamente no navegador

Expert

### Plan-and-Execute Agent

Substitua ReAct por Plan-and-Execute para tarefas complexas.

#### Tarefas:

#### Suas Anotações:

Salvo automaticamente no navegador

Lab Prático

## Lab: Hybrid Search

Construa o arquivo exemplo_hybrid_search.py passo a passo.

### Objetivo do Lab

Neste laboratório, você vai criar um arquivo Python que demonstra três formas de busca:

- BM25 Isolado: Busca por palavras-chave (sem API externa)
- Hybrid Search: Combina BM25 + busca semântica com RRF
- Comparação: Mostra as diferenças entre os métodos

### 1 Header e Imports Básicos

Linhas 1-19

Crie o arquivo exemplo_hybrid_search.py na raiz do projeto e adicione:

```
"""
Exemplo de uso do Hybrid Search
Auditor de Contratos - Bootcamp Itaú FIAP 2026

Demonstra:
1. BM25 isolado (sem API externa)
2. HybridSearchAdapter completo (requer OpenAI)
"""

import os
import sys
from dotenv import load_dotenv
from langchain.schema import Document

# Carrega variáveis de ambiente (override=True sobrescreve vars do sistema)
load_dotenv(override=True)

# Imports do projeto
from adapters.hybrid_search import BM25, HybridSearchAdapter, SearchResult
```

#### Explicação

- Docstring: Documenta o propósito do arquivo e o que será demonstrado
- load_dotenv(override=True): Carrega variáveis do.env e sobrescreve variáveis de ambiente do sistema
- Document: Classe do LangChain que encapsula texto + metadados
- BM25, HybridSearchAdapter: Componentes do nosso projeto para busca

### 2 Função BM25 - Documentos de Exemplo

Linhas 22-45

Inicie a função que demonstra o BM25 isoladamente (não precisa de API key):

```
def exemplo_bm25_isolado():
    """
    Exemplo 1: Usar BM25 isoladamente (sem OpenAI).
    
    Este exemplo NÃO precisa de API key - usa apenas o algoritmo BM25
    para busca por palavras-chave.
    """
    print("=" * 60)
    print("EXEMPLO 1: BM25 Isolado (sem API externa)")
    print("=" * 60)
    
    # Documentos de exemplo (simulando chunks de um contrato)
    docs = [
        Document(page_content="Contrato de mútuo com taxa de juros de 5% ao ano. "
                              "O mutuário compromete-se a pagar em parcelas mensais."),
        Document(page_content="Garantia hipotecária sobre imóvel residencial localizado "
                              "na Rua das Flores, 123, São Paulo/SP."),
        Document(page_content="Prazo de 36 meses com parcelas mensais fixas. "
                              "O vencimento ocorre todo dia 10 de cada mês."),
        Document(page_content="Cláusula penal prevê multa de 2% sobre valor devido "
                              "em caso de atraso no pagamento das parcelas."),
        Document(page_content="O mutuário declara ter recebido o valor de R$ 100.000,00 "
                              "(cem mil reais) na data de assinatura deste contrato."),
    ]
```

#### Explicação

- Document(page_content=...): Cria objetos Document do LangChain simulando chunks de contrato
- 5 documentos: Cada um representa um aspecto diferente do contrato (juros, garantia, prazo, multa, valor)
- Sem API: Este exemplo roda 100% local, sem precisar de OpenAI

### 3 BM25 - Indexação e Estatísticas

Linhas 47-54

Adicione a criação e treinamento do BM25 (ainda dentro da função):

```
    # Criar e treinar BM25
    print("\n📚 Indexando documentos...")
    bm25 = BM25(k1=1.5, b=0.75)
    bm25.fit(docs)
    
    print(f"   ✓ Corpus indexado: {bm25.corpus_size} documentos")
    print(f"   ✓ Vocabulário: {len(bm25.doc_freqs)} termos únicos")
    print(f"   ✓ Tamanho médio: {bm25.avg_doc_length:.1f} tokens/documento")
```

#### Explicação

- k1=1.5: Parâmetro de saturação de frequência de termo (valores típicos: 1.2-2.0)
- b=0.75: Parâmetro de normalização por tamanho de documento (0=sem normalização, 1=normalização total)
- fit(): Indexa os documentos, criando o vocabulário e calculando estatísticas
- doc_freqs: Dicionário com frequência de cada termo no corpus

Dica: O BM25 é o algoritmo por trás de motores de busca tradicionais como Elasticsearch e Lucene.

### 4 BM25 - Executando Buscas

Linhas 56-83

Complete a função com as buscas e fechamento:

```
    # Executar buscas
    queries = [
        "taxa de juros",
        "garantia imóvel hipoteca",
        "multa atraso pagamento",
        "valor recebido reais",
    ]
    
    print("\n🔍 Executando buscas BM25:")
    print("-" * 60)
    
    for query in queries:
        print(f"\n📝 Query: '{query}'")
        results = bm25.search(query, k=2)
        
        if not results:
            print("   Nenhum resultado encontrado.")
            continue
            
        for rank, (idx, score) in enumerate(results, 1):
            content = docs[idx].page_content
            # Truncar para exibição
            preview = content[:80] + "..." if len(content) > 80 else content
            print(f"   {rank}. [Score: {score:.4f}] {preview}")
    
    print("\n" + "=" * 60)
    print("✅ Exemplo BM25 concluído!")
    print("=" * 60)
```

#### Explicação

- search(query, k=2): Retorna os k documentos mais relevantes para a query
- Retorno: Lista de tuplas (índice_documento, score_bm25)
- Score BM25: Quanto maior, mais relevante o documento para a query
- Truncamento: Preview de 80 caracteres para exibição legível

### 5 Função Hybrid Search Completo

Linhas 86-191

Adicione a função que combina BM25 + busca semântica (requer OPENAI_API_KEY):

```
def exemplo_hybrid_search_completo():
    """
    Exemplo 2: HybridSearchAdapter completo (requer OpenAI).
    
    Combina BM25 (keyword) + busca semântica (embeddings) usando
    Reciprocal Rank Fusion (RRF) para melhor ranking.
    """
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Hybrid Search Completo")
    print("=" * 60)
    
    # Verificar API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n❌ OPENAI_API_KEY não configurada!")
        print("   Configure a variável de ambiente e tente novamente.")
        print("   Exemplo: export OPENAI_API_KEY='sua-chave-aqui'")
        return
    
    # Debug: mostrar qual key está sendo usada (mascarada)
    print(f"\n🔑 API Key carregada: {api_key[:8]}...{api_key[-4:]}")
    
    # Imports que dependem de config
    from adapters.openai_adapter import OpenAIAdapter
    from adapters.chromadb_adapter import ChromaDBAdapter
    from adapters.document_loader import DocumentLoader
    from core.config import Config
    
    try:
        # Carregar configuração
        print("\n⚙️  Carregando configuração...")
        config = Config.from_env()
        
        # Inicializar OpenAI adapter
        print("🔧 Inicializando OpenAI adapter...")
        openai_adapter = OpenAIAdapter(
            api_key=config.openai_api_key,
            embedding_model=config.embedding_model
        )
        
        # Inicializar ChromaDB adapter
        print("🔧 Inicializando ChromaDB adapter...")
        chromadb_adapter = ChromaDBAdapter(
            embeddings=openai_adapter.embeddings,
            collection_name="hybrid_search_demo",
            persist_directory="./chroma_demo"
        )
        
        # Carregar documento
        contract_path = "v1/contrato_mutuo_exemplo.txt"
        if not os.path.exists(contract_path):
            print(f"\n❌ Arquivo não encontrado: {contract_path}")
            return
        
        print(f"📄 Processando documento: {contract_path}")
        loader = DocumentLoader(chunk_size=500, chunk_overlap=50)
        chunks = loader.process_document(contract_path)
        print(f"   ✓ {len(chunks)} chunks criados")
        
        # Criar vectorstore
        print("📊 Criando vectorstore...")
        chromadb_adapter.create_from_documents(chunks)
        
        # Criar HybridSearchAdapter
        print("🔀 Inicializando Hybrid Search...")
        hybrid = HybridSearchAdapter(
            chromadb_adapter=chromadb_adapter,
            alpha=0.5,  # 50% semântico, 50% BM25
            rrf_k=60
        )
        hybrid.index_documents(chunks)
        print("   ✓ Hybrid Search pronto!")
```

#### Explicação

- Config.from_env(): Carrega configurações do arquivo.env
- OpenAIAdapter: Encapsula chamadas à API da OpenAI (embeddings e chat)
- ChromaDBAdapter: Interface com o banco vetorial ChromaDB
- alpha=0.5: Peso entre busca semântica e BM25 (0.5 = 50%/50%)
- rrf_k=60: Parâmetro do Reciprocal Rank Fusion (valor padrão comum)

### 5b Hybrid Search - Executando Buscas

Continuação

Continue a função com as buscas híbridas (ainda dentro do try):

```
        # Executar buscas
        queries = [
            "qual a taxa de juros do contrato?",
            "informações sobre a garantia",
            "prazo e valor das parcelas",
        ]
        
        print("\n🔍 Executando buscas híbridas:")
        print("-" * 60)
        
        for query in queries:
            print(f"\n📝 Query: '{query}'")
            results = hybrid.search(query, k=3)
            
            for r in results:
                content = r.document.page_content
                preview = content[:100] + "..." if len(content) > 100 else content
                
                print(f"\n   Rank {r.rank}:")
                print(f"   ├─ Score combinado: {r.combined_score:.4f}")
                print(f"   ├─ Score semântico: {r.semantic_score:.4f}")
                print(f"   ├─ Score keyword:   {r.keyword_score:.4f}")
                print(f"   └─ Conteúdo: {preview}")
        
        print("\n" + "=" * 60)
        print("✅ Exemplo Hybrid Search concluído!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
```

#### Explicação

- hybrid.search(): Retorna objetos SearchResult com múltiplos scores
- combined_score: Score final após fusão RRF
- semantic_score: Score da busca vetorial (similaridade de embeddings)
- keyword_score: Score do BM25 (match de palavras)

RRF (Reciprocal Rank Fusion): Combina rankings de diferentes métodos usando a fórmula: score = 1/(k + rank). Isso dá mais peso a resultados bem rankeados em ambos os métodos.

### 6 Função Comparação BM25 vs Semântico

Linhas 193-259

Adicione a função que compara os dois métodos lado a lado:

```
def comparar_bm25_vs_semantico():
    """
    Exemplo 3: Comparar resultados BM25 vs Semântico.
    
    Mostra as diferenças entre busca por palavras-chave e busca semântica.
    """
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Comparação BM25 vs Semântico")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ OPENAI_API_KEY não configurada!")
        return
    
    from adapters.openai_adapter import OpenAIAdapter
    from adapters.chromadb_adapter import ChromaDBAdapter
    from core.config import Config
    
    # Documentos com sinônimos e variações
    docs = [
        Document(page_content="O empréstimo tem taxa de juros de 1.5% ao mês."),
        Document(page_content="Os custos financeiros são de 18% ao ano."),  # Sinônimo
        Document(page_content="A garantia é um apartamento de 3 quartos."),
        Document(page_content="O imóvel dado em hipoteca está na Av. Paulista."),  # Relacionado
        Document(page_content="Prazo de pagamento: 48 parcelas mensais."),
    ]
    
    try:
        config = Config.from_env()
        
        openai_adapter = OpenAIAdapter(
            api_key=config.openai_api_key,
            embedding_model=config.embedding_model
        )
        
        chromadb_adapter = ChromaDBAdapter(
            embeddings=openai_adapter.embeddings,
            collection_name="comparacao_demo"
        )
        chromadb_adapter.create_from_documents(docs)
        
        # BM25
        bm25 = BM25()
        bm25.fit(docs)
        
        query = "juros do financiamento"
        print(f"\n📝 Query: '{query}'")
        
        # Resultado BM25
        print("\n🔤 Resultados BM25 (palavras-chave):")
        bm25_results = bm25.search(query, k=3)
        for rank, (idx, score) in enumerate(bm25_results, 1):
            print(f"   {rank}. [Score: {score:.4f}] {docs[idx].page_content}")
        
        # Resultado Semântico
        print("\n🧠 Resultados Semânticos (significado):")
        sem_results = chromadb_adapter.search_with_score(query, k=3)
        for rank, (doc, score) in enumerate(sem_results, 1):
            print(f"   {rank}. [Dist: {score:.4f}] {doc.page_content}")
        
        print("\n💡 Observação:")
        print("   - BM25 encontra matches exatos de palavras")
        print("   - Semântico encontra sinônimos e conceitos relacionados")
        print("   - Hybrid Search combina o melhor dos dois!")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
```

#### Explicação

- Documentos com sinônimos: "taxa de juros" vs "custos financeiros" - mesmo conceito, palavras diferentes
- Query "juros do financiamento": Não contém exatamente as palavras dos documentos
- BM25: Vai encontrar apenas documentos com a palavra "juros"
- Semântico: Pode encontrar "custos financeiros" por similaridade de significado

Insight: Este é o poder do Hybrid Search - combina precisão lexical (BM25) com compreensão semântica (embeddings).

### 7 Menu Principal e Execução

Linhas 262-294

Finalize o arquivo com o bloco de execução principal:

```
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║         DEMONSTRAÇÃO DO HYBRID SEARCH                                ║
║         Auditor de Contratos - Bootcamp FIAP 2026                    ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    print("Escolha um exemplo para executar:\n")
    print("1. BM25 Isolado (NÃO precisa de API key)")
    print("2. Hybrid Search Completo (precisa de OPENAI_API_KEY)")
    print("3. Comparação BM25 vs Semântico (precisa de OPENAI_API_KEY)")
    print("0. Executar TODOS os exemplos")
    
    choice = input("\nDigite o número do exemplo (ou Enter para sair): ").strip()
    
    if choice == "1":
        exemplo_bm25_isolado()
    elif choice == "2":
        exemplo_hybrid_search_completo()
    elif choice == "3":
        comparar_bm25_vs_semantico()
    elif choice == "0":
        exemplo_bm25_isolado()
        exemplo_hybrid_search_completo()
        comparar_bm25_vs_semantico()
    else:
        print("Saindo...")
    
    print("\n" + "=" * 60)
    print("🎉 Demonstração finalizada!")
    print("=" * 60)
```

#### Explicação

- if __name__ == "__main__": Garante que o código só executa quando o arquivo é rodado diretamente
- Menu interativo: Permite escolher qual exemplo executar
- Opção 0: Executa todos os exemplos em sequência
- Banner ASCII: Identificação visual do programa

### Como Executar

```
# Ativar ambiente virtual (se ainda não ativou)
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Executar o exemplo
python exemplo_hybrid_search.py

# Opção 1: BM25 (não precisa de API key)
# Opção 2 e 3: Precisam de OPENAI_API_KEY no .env
```

#### Opção 1

BM25 puro - funciona sem API key, demonstra busca por palavras-chave

#### Opção 2

Hybrid Search completo - requer OpenAI API para embeddings

#### Opção 3

Comparação visual entre BM25 vs Semântico

### Conceitos-Chave Aprendidos

#### BM25 (Best Match 25)

Algoritmo de ranking baseado em frequência de termos e IDF (Inverse Document Frequency). Excelente para matches exatos de palavras.

#### Busca Semântica

Usa embeddings (vetores) para encontrar documentos por similaridade de significado, não apenas palavras exatas.

#### Hybrid Search

Combina BM25 + Semântico para obter o melhor dos dois mundos: precisão lexical e compreensão de contexto.

#### RRF (Reciprocal Rank Fusion)

Técnica para combinar rankings de múltiplos métodos de busca em um ranking final unificado.
