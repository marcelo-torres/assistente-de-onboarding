# Neural Architect: Masterclass em RAG e Memória

## 1. Fundamentos da Memória

A memória em agentes de IA transcende a simples retenção de dados. Em arquiteturas avançadas, distinguimos entre o estado paramétrico (pesos da rede) e o estado externalizado (memória episódica e semântica).

### Conceito Avançado: Memória Paramétrica vs. Externa

Tradicionalmente, a memória é o estado oculto (h_t) ou os pesos (θ). Em Transformers, a memória de curto prazo é limitada pela janela de contexto (O(N²)). A memória de longo prazo exige arquiteturas neuro-simbólicas.

Memória Semântica (Fatos Globais) vs. Memória Episódica (Transições de Estado MDP).

### Exemplo Prático

Agente de Suporte Técnico: Curto prazo retém os logs dos últimos 10 min. Longo prazo (episódica) lembra que o cliente teve falha de hardware há 6 meses, alterando a inferência causal.

Fonte: Park et al., 2023 (Generative Agents)

### Analogia Cognitiva

Memória de Trabalho

Context Window (RAM)

→

Memória Semântica

Vector Store (Hard Drive)

→

Memória Episódica

Logs de Sessão (Diário)

## 2. Arquitetura RAG

RAG (Retrieval-Augmented Generation) mitiga alucinações condicionando a geração probabilística a documentos recuperados (P(y|x, z)). É a injeção de memória não-paramétrica em tempo de inferência.

### Pipeline de Processamento

1

#### Ingestão

Coleta de dados (Scripts, Data Lakes, Eventos).

2

#### Indexação

Chunking → Embedding → Vector Store.

3

#### Retrieval

Busca Híbrida + Re-ranking.

4

#### Geração

Contexto montado + Query → LLM.

### Estratégias de Ingestão

| Arquitetura | Descrição & Aplicação |
| --- | --- |
| Simples (CLI) | Scripts Python para CSV/JSON estáticos. Execução via cron. |
| Enterprise (Dataflow) | Spark/Vertex Pipelines para Data Lakes. Processamento em batch (D+1). |
| Event-Driven (Real-time) | Workers (Celery/Kafka) processam uploads na sessão. Ingestão em segundos. |

## 3. Embeddings & Vetores

Embeddings são projeções topológicas f: X → R^d transformando tokens discretos em um espaço latente contínuo. A distância geométrica reflete a divergência semântica.

### Espaço Vetorial Latente

Visualização simplificada de como conceitos semânticos se agrupam em 3D. Observe como "Rei" e "Rainha" mantêm uma relação vetorial similar a "Homem" e "Mulher".

- Arquiteturas Bi-Encoder Redes siamesas (BERT) otimizadas com Contrastive Learning (InfoNCE loss) para aproximar pares positivos na hiperesfera.
- MRL (Matryoshka Learning) Concentra entropia nas primeiras dimensões, permitindo truncagem de vetores sem perda massiva de precisão.
- Métricas Cosseno vs. Produto Escalar (Dot Product). Se vetores normalizados (L2=1), são matematicamente idênticos.

Simulação Interativa Plotly.js

## 4. Engenharia de Chunking

A fragmentação é um problema de preservação entrópica. Chunking incorreto destrói correlações de dependência de longo alcance e dilui o sinal semântico no embedding.

### Estratégias

### Visualizador de Fragmentação

Passar o mouse sobre os blocos mostra os limites do chunk.

## 5. Vector Stores & ScaNN

Vector Stores resolvem o problema de Nearest Neighbor (ANN) em escala. O padrão HNSW usa grafos de mundo pequeno. O Google Vertex AI usa ScaNN.

### ScaNN vs HNSW

Quantização Vetorial Anisotrópica

ScaNN penaliza erros de quantização paralelos ao vetor original (que afetam o ranking) e tolera erros ortogonais. Resultado: Compressão massiva e maior QPS.

Impacto na Escala

Recall@10 ~98%

Compressão Alta

#### Comparativo de Latência (ms) em 1M Vetores

## 6. Recuperação Avançada

O Retrieval moderno é um pipeline de dois estágios: Busca Híbrida (Vetorial + BM25) seguida de Re-ranking (Cross-Encoders).

### Hybrid Search & Re-ranking

#### Hybrid Search

Fusão de pontuação densa (semântica) e esparsa (palavra-chave exata) via Reciprocal Rank Fusion (RRF).

#### Re-ranking

Cross-Encoders processam Query+Documento juntos (atenção total), refinando drasticamente a precisão do Top-K.

Exemplo: "Motor V8 da Ferrari 2023"

- Sparse (BM25): Pega "V8", "2023" (Exato).
- Dense (Vector): Pega "Motor", "Ferrari" (Semântico).
- Cross-Encoder: Reordena para remover tratores ou modelos V6.

Query do Usuário

↓

Vector Search (ANN)

Keyword Search (BM25)

↘ ↙

Reciprocal Rank Fusion (RRF)

↓

Re-ranking (Cross-Encoder)

↓

Top-K Contexto

## 7. Montagem de Contexto

O fenômeno 'Lost in the Middle' mostra que LLMs ignoram informações no meio do prompt. A montagem de contexto é engenharia de estado.

### 7. Montagem de Contexto

O fenômeno 'Lost in the Middle' mostra que LLMs ignoram informações no meio do prompt. A montagem de contexto é engenharia de estado.

Estratégia: Reordenar chunks para colocar os mais relevantes no início e no fim do prompt, evitando o vale de atenção.

## 8. Memória vs. Knowledge Base

Stateful Memory (Sessão/Usuário) e Knowledge Base (RAG) têm propósitos epistemológicos distintos. Um atualiza o modelo de mundo mutável, o outro fornece fatos imutáveis.

### 8. Memória vs. Knowledge Base

Stateful Memory (Sessão/Usuário) e Knowledge Base (RAG) têm propósitos epistemológicos distintos. Um atualiza o modelo de mundo mutável, o outro fornece fatos imutáveis.

Exemplo Prático

RAG traz calorias da maçã (Fato). Memória traz alergia do usuário (Estado). Agente combina ambos.

## 9. Avaliação (RAGAS)

Métricas estáticas (BLEU, ROUGE) falham em RAG: medem overlap lexical, não fidelidade ao contexto nem utilidade da resposta. A avaliação moderna adota LLM-as-a-Judge — um modelo auxiliar pontua entradas/saídas — e o framework RAGAS padroniza esse processo.

### O que é o framework RAGAS?

RAGAS (Retrieval-Augmented Generation Assessment) é um framework open-source (Explodinggradients) que avalia pipelines RAG sem necessidade de respostas humanas de referência (ground truth). Ele usa o próprio LLM para extrair afirmações da resposta, compará-las ao contexto recuperado e à pergunta, produzindo scores reprodutíveis para Faithfulness, Answer Relevance, Context Precision e Context Recall.

### Por que não BLEU/ROUGE?

Métricas estáticas (BLEU, ROUGE) falham em RAG: medem overlap lexical, não fidelidade ao contexto nem utilidade da resposta. A avaliação moderna adota LLM-as-a-Judge — um modelo auxiliar pontua entradas/saídas — e o framework RAGAS padroniza esse processo.

#### Métricas RAGAS

Faithfulness

Mede se a resposta deriva apenas dos chunks recuperados (sem alucinação). O LLM extrai afirmações da resposta e verifica se cada uma é suportada pelo contexto. Score baixo indica que o modelo inventou informações.

Answer Relevance

Avalia se a resposta atende diretamente à query do usuário (relevância da resposta). Perguntas geradas a partir da resposta são comparadas à pergunta original; alta similaridade semântica indica boa relevância.

Context Precision

Verifica se o retrieval trouxe principalmente chunks úteis ou muito ruído. Chunks que não ajudam a responder penalizam o score; ideal para diagnosticar qualidade do índice e do ranking.

Context Recall

Mede se o contexto recuperado contém todos os fatos necessários para responder à pergunta (ground truth ou resposta de referência). Complementar à Precision: recall baixo indica que informações importantes ficaram de fora.

#### Radar de avaliação (exemplo)

## 10. Padrões Avançados

Além do RAG linear (uma query → retrieval → um contexto → uma resposta), existem padrões que lidam com síntese em larga escala e com raciocínio que exige múltiplos passos de busca e reflexão.

Além do RAG linear (uma query → retrieval → um contexto → uma resposta), existem padrões que lidam com síntese em larga escala e com raciocínio que exige múltiplos passos de busca e reflexão.

GraphRAG

GraphRAG (Microsoft) constrói um Knowledge Graph a partir dos documentos (entidades e relações extraídas por LLM) e agrupa nós em comunidades. Em vez de buscar apenas chunks similares à pergunta, o sistema faz sumarização hierárquica por comunidade e combina resumos. Ideal para perguntas de escopo amplo (ex.: 'Qual o tema principal do corpus?', 'Como X se relaciona com Y em todo o material?') que um RAG vetorial puro não responde bem.

Query: "Tema principal?" Graph: Detecta comunidades de nós -> Resumo Hierárquico.

Agentic RAG

Agentic RAG coloca um agente (ReAct, Plan-and-Execute, etc.) no centro: ele decide quando consultar a base, formula sub-perguntas, faz múltiplas buscas, reflete sobre os resultados e só então sintetiza a resposta. Essencial para perguntas multi-hop (ex.: 'Qual a política monetária do país do CEO da Apple?') que exigem encadear recuperação → inferência → nova recuperação.

Loop: Thought -> Act (Search) -> Obs -> Thought -> Act...

#### Exemplo Multi-Hop (CEO Apple)

Step 1 Quem é o CEO? → Tim Cook

Step 2 Onde nasceu/País sede? → EUA

Step 3 Política monetária EUA? → Taxas Fed Altas

Síntese: O aumento das taxas nos EUA impacta a importação...
