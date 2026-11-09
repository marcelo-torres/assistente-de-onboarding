# Aula 4 — Anatomia do Vector Search

Turma 2 · agent-the-memory us-east1 Projeto spartan-setting-485114-e3 ADC · sem API Key

## Anatomia do Vector Search: o que é cada peça?

Clique em cada caixa do diagrama. O Vector Search não é um único botão: é um encadeamento de bucket, índice, endpoint e índice implantado. O agente só consulta quando as quatro peças estão no lugar e o índice tem vetores de 768 dimensões.

Tutoriais: 1 · Upload no GCS · 2 · Chroma e depois Vertex

Interativo

## Cinco peças. Clique para abrir.

Analogia rápida: o bucket é o depósito de papéis; o índice é o fichário numérico; o endpoint é o balcão; o índice implantado é o funcionário que liga o fichário ao balcão.

Convenção da turma

## Sua letra muda o nome de tudo

Sufixo 0 é o professor. Cada grupo usa uma letra. Nunca edite recursos grupo-0.

| Recurso | Nome na sua letra | Variável no.env |
| --- | --- | --- |
| Bucket |  | VECTOR_SEARCH_GCS_BUCKET |
| Índice |  | VECTOR_SEARCH_INDEX_ID (o número, não o nome) |
| Endpoint |  | VECTOR_SEARCH_ENDPOINT_ID (o número) |
| Deployed index |  | VECTOR_SEARCH_DEPLOYED_INDEX_ID |

Pasta de manuais: · JSONL gerado pelo pipeline:

Dois tempos

## Indexar não é consultar

Escolha o fluxo e avance passo a passo. São APIs diferentes, no código e no Console.

Armadilha

## O PDF no bucket não entra sozinho no índice

Marque verdadeiro ou falso. O gabarito aparece na hora.

Dimensões

## 384 no notebook, 768 na nuvem

O índice desta turma foi criado com 768 dimensões (modelo text-multilingual-embedding-002). O MiniLM local da Aula 1 gera 384. São mapas de tamanhos diferentes: um ponto de 384 coordenadas não cabe no fichário de 768.

Parte A · Chroma

embedding.backend: local vector_search.backend: chroma

Use na Parte A do Tutorial 2. Não aponte esse vetor para o índice Vertex.

Parte B · Vector Search

embedding.backend: vertex vector_search.backend: vertex

Indexação e query precisam do mesmo modelo. ADC, sem API Key.

Console

## O que a tela está tentando te dizer

| Você vê | Significa | Pode consultar? |
| --- | --- | --- |
| Índice Pronto, contagem densa -- | Estrutura criada, ainda sem vetores (ou UI não mostrou) | Ainda não de verdade |
| Link Implantar | Índice sem endpoint | Não |
| Implantando | Deploy em andamento (minutos a ~30 min) | Não ainda |
| Deployed index Pronto + JSONL enviado | Balcão aberto e fichário alimentado | Sim, depois do rebuild batch |

Região da lista: sempre us-east1. Lista vazia quase sempre é dropdown na região errada.

Glossário

## Termos do console, em português

Não use o menu Mecanismo RAG neste projeto. O código chama Vector Search (find_neighbors) e o CLI python -m src.indexing --push.
