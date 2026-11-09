# Índices e Vector Stores — Do zero à referência

Arquivo dedicado · referência

## Índices, Vector Stores e busca aproximada

Você já sabe o que é um embedding: um endereço numérico de significado. Agora a pergunta muda: com milhões de endereços, como achar o vizinho certo em milissegundos — e onde guardar tudo isso?

Índices merecem arquivo próprio. Aqui vamos do ANN até Vector Stores reais, com fichas profundas de ChromaDB e do ecossistema Gemini Enterprise (File Search, Agent Search, Vertex AI Vector Search, RAG Engine).

Começar → ChromaDB Gemini Enterprise

Capítulo 1 O problema

## Por que o índice existe

Cada documento virou um ponto num mapa (isso o embedding já fez). Você quer a padaria mais perto da pergunta.

Opção A: visitar todas as casas do país. Sempre certa. Absurdamente lenta — custo O(N × d).

Opção B: usar atalhos (bairros, grafos, árvores). Pode errar 1–5%. Chega em milissegundos.

Embedding cria o mapa. Índice navega o mapa. Vector Store é o prédio onde mapa + documentos + etiquetas moram juntos.

Busca exata

Compara com todos. Recall 100%. Inviável acima de ~100 mil vetores em latência interativa.

ANN

Approximate Nearest Neighbor. O 1–5% perdido aqui o reranker/LLM nunca recuperam.

Capítulo 2 Conceito

## O que é um Vector Store

Uma lib ANN (Faiss, HNSWlib) só busca vizinhos. Um Vector Store é um sistema de dados: vetor + texto + metadata + IDs, com API, persistência e filtros.

Vetor

embedding

Documento

texto original

Metadata

tags filtráveis

ID

chave estável

| Camada | Exemplos | Entrega | Ops |
| --- | --- | --- | --- |
| Lib ANN | Faiss, HNSWlib | Só k-NN | Você monta tudo |
| Extensão SQL | pgvector, AlloyDB | Vetores + SQL | Baixa se já tem PG |
| Vector DB OSS | Chroma, Qdrant, Weaviate, Milvus | API + filtros | Self-host / cloud |
| Managed | Pinecone, Vertex AI Vector Search | Escala + SLA | Paga serviço |
| RAG managed | Gemini File Search, Vertex AI Search | Pipeline inteiro | Mínima · menos controle |

Capítulo 3 Siglas

## Famílias ANN — ficha de referência

| Sigla | Nome | Ideia | Use quando |
| --- | --- | --- | --- |
| Flat | Exact / Brute-force | Compara com todos | <100k · recall 100% |
| ANN | Approximate Nearest Neighbor | Categoria | Guarda-chuva |
| IVF | Inverted File Index | Bairros/células · nprobe | RAM apertada |
| PQ | Product Quantization | Comprime vetores | IVF-PQ |
| HNSW | Hierarchical Navigable Small World | Grafo em camadas | Padrão em RAM |
| DiskANN | Disk-based ANN | Grafo no SSD | Bilhões |
| Tree-AH | Shallow Tree + Asymmetric Hashing | Árvore + hashing (Google) | Vertex AI Vector Search |

Padrão de mercado

### HNSW — Hierarchical Navigable Small World

- Hierarchical — camadas (zoom de mapa).
- Navigable — caminha pelas arestas até a região certa.
- Small World — poucos saltos ligam pontos distantes.

Paper: Malkov & Yashunin, 2018. Analogia: avião → ônibus → a pé.

M

conexões/nó · ↑ recall ↑ RAM

efConstruction

qualidade na construção

efSearch

botão recall × latência

Usar: RAG com índice em RAM — Chroma, pgvector, Qdrant, Weaviate.

Evitar: bilhões sem RAM; deleções agressivas (tombstones).

Partição

### IVF / IVF-PQ

IVF (Inverted File): k-means cria nlist células; na query visita nprobe. PQ (Product Quantization): comprime vetores 10–50×. Dupla clássica Faiss/Milvus.

Usar: milhões de vetores, RAM cara, rescoring ok.

Evitar: corpus pequeno; nprobe sem medição.

Google

### Tree-AH — algoritmo do Vertex AI Vector Search

Padrão do Vertex AI Vector Search (ex-Matching Engine). Paper arXiv 1908.10396.

- Shallow tree — partição hierárquica rasa (ideia de “bairros”).
- Asymmetric Hashing — banco comprimido; query em precisão maior na comparação.

Params: leaf_node_embedding_count, leaf_nodes_to_search_percent, approximate_neighbors_count. Alternativa no mesmo produto: BruteForce.

HNSW = grafo (OSS). Tree-AH = partição+hashing otimizado para serving distribuído Google. Ambos são ANN.

### Guia por tamanho

| < 100 mil | Força bruta |
| --- | --- |
| 10⁵–10⁷ em RAM | HNSW |
| Milhões · RAM cara | IVF-PQ |
| GCP · escala alta | Tree-AH |
| Bilhões | DiskANN / VS sharded |

Capítulo 4 Brinquedo

## Ache o vizinho — ao vivo

Clique no mapa (estrela = consulta). Compare força bruta × IVF × HNSW: quantas casas visitou e se achou o vizinho verdadeiro.

Comparações

—

Tempo

—

Achou?

—

Estratégia

—

Clique no mapa…

Capítulo 5 Métricas

## Recall × velocidade

Recall do ANN

Resultado aproximado vs busca exata. “O índice está calibrado?”

Recall do sistema

Recuperado vs o que um humano marcou como certo. Mede embedding + chunking + índice.

Índice com recall 0,99 sobre embeddings ruins = lixo rápido. As duas engrenagens precisam estar boas.

Capítulo 6 ChromaDB

## ChromaDB — referência completa

Antes do Chroma, o menu era: Faiss (só índice), Milvus/Weaviate (infra pesada) ou Pinecone (pago). Faltava o “Postgres do embedding” para quem quer pip install e já busca.

Fundado em 2022 por Jeff Huber e Anton Troynikov com tese clara: developer experience first. Defaults sensatos: HNSW + SQLite + embedding function embutida.

Analogia: um armário mágico. Cada pasta tem sensor de significado. Você descreve a ideia — o armário desliza as pastas mais parecidas. Por baixo: embeddings + HNSW + metadata.

### A unidade de dado: o trio

embedding

vetor denso (ex.: 384D MiniLM)

document

texto bruto devolvido na query

metadata

tags: status, produto, tenant…

Mais o id. Muitos bancos só guardam vetor+id; o Chroma colocaliza os três — um insert, uma query, tudo volta junto.

### Arquitetura interna (o que mora no disco)

Desde ~v1.0 o núcleo de performance (HNSW, segmentos, query) migrou para Rust. Separação chave:

SQLite — chroma.sqlite3

- Sysdb: tenants, databases, collections, segments
- Metadata segment: documentos + key-values
- FTS5 para where_document
- WAL para durabilidade

Pasta UUID por collection — HNSW

- header.bin — params/estrutura
- link_lists.bin — adjacências
- data_level0.bin — camada base + vetores
- index_metadata.pickle — mapa id ↔ label

Cada collection tem dois segments: metadata e vector. Query: embed → HNSW ANN → pós-filtro SQL → devolve docs.

### Quatro modos de deploy

Ephemeral

Só RAM. Some ao sair. Ideal para testes.

Persistent

Pasta no disco. Labs e apps locais.

HttpClient

Server separado. Time compartilhando índice.

Chroma Cloud

Gerenciado pelo vendor.

### Collection + parâmetros HNSW

```
import chromadb
client = chromadb.PersistentClient(path="./chroma_data")
collection = client.create_collection(
    name="politicas",
    metadata={
        "hnsw:space": "cosine",          # l2 | ip | cosine
        "hnsw:M": 16,                   # conexões por nó
        "hnsw:construction_ef": 100,  # qualidade do grafo
        "hnsw:search_ef": 100,         # recall × latência
    },
)
```

hnsw:space — métrica. Em RAG costuma ser cosine.

M — mais conexões = melhor recall, mais RAM.

construction_ef — pago na indexação; grafo mais cuidadoso.

search_ef — pago na query; aumente até o recall estabilizar.

### API essencial + o perigo do pós-filtro

```
collection.add(
    ids=["doc-1", "doc-2"],
    documents=["Carência de 45 dias…", "Seguro prestamista…"],
    metadatas=[{"status": "vigente", "produto": "credito"},
               {"status": "revogado", "produto": "credito"}],
)
results = collection.query(
    query_texts=["qual o prazo de carência?"],
    n_results=5,
    where={"status": "vigente", "produto": "credito"},
    where_document={"$contains": "dias"},
)
```

Atenção (pós-filtro): o Chroma tipicamente busca candidatos no HNSW e depois aplica o where no SQLite. Se o filtro for muito seletivo, pode voltar menos que n_results — ou quase nada. É o mesmo bug de família da “norma revogada” do módulo avançado: a ordem entre filtrar e ranquear importa. Em produção, meça recall com o filtro ligado.

Quando usar Chroma

- Aulas, labs, protótipos RAG
- Apps até alguns milhões de vetores
- Soberania de dados / on-prem / VPC
- Qualquer modelo de embedding (BYO)
- Time pequeno sem plataforma GCP

Quando NÃO usar

- Bilhões de vetores / multi-região gerenciada
- SLA enterprise sem equipe de ops
- Precisa de Tree-AH / serving Google nativo
- Quer pipeline “upload PDF → resposta” sem código

Manutenção do HNSW

Com o tempo o grafo fragmenta (deletes lógicos). Ferramentas do cookbook: hnsw info (fragmentação, WAL gap, orphan labels) e hnsw rebuild (reconstrói e permite mudar params de construção).

Capítulo 7 Gemini Enterprise

## Vector Stores no ecossistema Gemini Enterprise

No Google Cloud, “vector store” não é um único produto — é uma escada de controle. Em 2025–2026, Vertex AI e Agentspace convergem sob a marca Gemini Enterprise / Agent Platform. O que muda é o marketing; as peças de retrieval continuam distintas e você precisa escolher a camada certa.

Quanto mais gerenciado, menos você mexe em chunking/HNSW — e menos controle tem. Quanto mais “vector store de verdade”, mais ops e mais precisão de engenharia.

### Mapa mental — do mais gerenciado ao mais controle

1

Gemini File Search Store — upload → Google chunka, embeda, indexa, cita.

2

Agent Search / Vertex AI Search — busca enterprise + grounding “Your data”.

3

RAG Engine — pipeline managed; pode plugar Vector Search atrás.

4

Vertex AI Vector Search — índice ANN gerenciado (Tree-AH); você traz embeddings.

5

BYO — AlloyDB (pgvector+ScaNN), BigQuery vectors, Elasticsearch grounding.

Camada 1 · máximo managed

### Gemini File Search / File Search Store

Um File Search Store funciona como vector database gerenciado dentro da API Gemini. Você sobe arquivos; o Google cuida de OCR/chunking/embeddings/índice/retrieval e devolve respostas com citações. Suporta multimodal e filtros de metadata — sem você escolher HNSW vs IVF.

Usar: Q&A sobre docs em horas; POC; assistente interno simples; time sem infra de retrieval.

Evitar: precisa controlar chunk size/overlap; embedding custom; multi-cloud; auditoria fina do índice.

Trade-off central: velocidade de entrega × lock-in e opacidade do pipeline.

Camada 2 · busca enterprise

### Agent Search / Vertex AI Search (AI Applications)

Motor de busca gerenciado sobre data stores (sites ou documentos). É a peça de grounding “Your data” no Gemini Enterprise Agent Platform: o modelo consulta sua base e cita trechos. Dá para combinar com Google Search grounding. Limite típico: até ~10 fontes de dados no grounding.

Diferente do Vector Search “cru”: aqui você compra experiência de busca Google (ranking, permissões, conectores), não só k-NN de vetores.

Usar: assistente corporativo; intranet; docs com ACL; quando “search quality” > controle de embedding.

Evitar: precisa do seu modelo de embedding; lógica de retrieval muito custom; custo de grounding por query sem orçamento.

Camada 3 · pipeline

### RAG Engine

Pipeline managed: ingest → chunk → embed → retrieve. Meio-termo entre File Search (tudo opaco) e DIY total. Pode associar um índice de Vertex AI Vector Search (exige STREAM_UPDATE no índice compatível com o corpus).

Camada 4 · vector store de verdade no GCP

### Vertex AI Vector Search (ex-Matching Engine)

Aqui você gera embeddings e o Google serve o índice em nós. Custo típico: node-hour (máquina + réplicas), não “centavos por query” isolados.

Algoritmos

- Tree-AH — padrão produção (árvore rasa + hashing assimétrico).
- BruteForce — exato; baseline ou índices menores.

Atualização do índice (escolha imutável na criação)

BATCH_UPDATE

Delta via GCS; bom para jobs semanais/mensais.

STREAM_UPDATE

upsert/delete quase real-time; obrigatório p/ RAG Engine.

Não dá para converter batch→stream: cria-se um índice novo. Streaming tem custo extra de update e compactação periódica.

Ciclo de vida

Index → IndexEndpoint → DeployedIndex (réplicas, machine type). Filtros: restricts / numeric restricts nos datapoints (o equivalente Google aos metadados filtráveis).

```
# Conceito — criar índice Tree-AH com streaming
index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    display_name="rag-credito",
    dimensions=768,
    approximate_neighbors_count=150,
    leaf_node_embedding_count=500,
    leaf_nodes_to_search_percent=7,
    distance_measure_type="DOT_PRODUCT_DISTANCE",
    index_update_method="STREAM_UPDATE",
)
```

Usar: dezenas de milhões de vetores; embedding custom; latência baixa; já está no GCP; RAG Engine com VS.

Evitar: lab de aula; orçamento sem nó dedicado; quer só “subir PDF”; multi-cloud portátil.

Camada 5 · BYO no GCP

### AlloyDB, BigQuery, Elasticsearch…

- AlloyDB AI — Postgres + pgvector + índice ScaNN do Google; vetores ao lado de dados operacionais.
- BigQuery vector search — vetores no warehouse; forte quando o dado já vive no BQ.
- Spanner / Firestore vectors — quando a distribuição global/documento manda.
- Grounding com Elasticsearch — reutiliza índice ES existente no Agent Platform (até 10 fontes).

| Preciso de… | Escolha no Gemini Enterprise |
| --- | --- |
| RAG em horas, zero infra | File Search Store |
| Busca enterprise + permissões + grounding | Agent Search / Vertex AI Search |
| Pipeline managed com VS atrás | RAG Engine + Vector Search |
| Controle de embeddings + escala | Vertex AI Vector Search (Tree-AH) |
| Vetores ao lado de SQL/analytics | AlloyDB / BigQuery |

Capítulo 8 Comparativo

## Chroma vs Gemini Enterprise — tabela honesta

| Critério | ChromaDB | File Search | Agent Search | Vertex Vector Search |
| --- | --- | --- | --- | --- |
| Soberania | Alta (seu disco/VPC) | Google | Google | Google (seu projeto) |
| Controle chunk/embed | Total | Mínimo | Baixo | Total (você embeda) |
| Ops | Baixa–média | Quase zero | Baixa | Média–alta (nós) |
| Escala confortável | Até ~10⁶–10⁷ | Docs de produto | Enterprise search | 10⁷–10⁹+ |
| Filtros | where (pós-filtro) | metadata | ACL + search | restricts |
| Tempo até 1ª demo | Minutos | Minutos | Horas | Dias (índice+endpoint) |

Aula FIAP / lab local

Chroma PersistentClient — você vê HNSW, metadata e o bug do pós-filtro com as próprias mãos.

Assistente no Workspace

Agent Search + grounding Gemini — permissões e conectores importam mais que tunar M.

50M vetores, embed custom

Vertex AI Vector Search Tree-AH + STREAM_UPDATE.

Weekend hack / PDF Q&A

Gemini File Search Store — zero índice para administrar.

Capítulo 9 Recap

## Recapitulando

Embedding

cria o endereço no mapa

Índice ANN

atalhos para achar vizinhos (HNSW, IVF, Tree-AH…)

Vector Store

guarda vetor+doc+metadata e serve a API

Retrieval → LLM

trechos vão ao modelo; o que o índice perdeu, ninguém recupera

### Glossário

ANN

Approximate Nearest Neighbor

HNSW

Grafo hierárquico navegável (Chroma default)

IVF / PQ

Células + compressão

Tree-AH

Algoritmo ANN do Vertex AI Vector Search

Collection

Namespace de vetores no Chroma

Restrict

Filtro nativo no Vector Search

File Search Store

Vector DB managed da API Gemini

Grounding

Ancorar a resposta do LLM em fontes

Pós-filtro

Filtra depois do ANN — risco de k incompleto

RAG Engine

Pipeline managed Google de retrieval

Base

Embeddings do Zero

O mapa, o cosseno, o buscador semântico.

Avançado

Masterclass · Índices

Filtros, freshness, código de produção.

Avançado

Masterclass · Embeddings

SPLADE, ColBERT, Matryoshka, quantização.
