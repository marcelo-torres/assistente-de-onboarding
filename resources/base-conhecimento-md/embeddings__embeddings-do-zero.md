# Embeddings do Zero — Uma jornada didática

Jornada interativa

## O que é um embedding?

Imagine que palavras fossem casas numa cidade enorme. Casas parecidas moram no mesmo bairro. Um embedding é o endereço secreto de cada casa — um conjunto de números que o computador usa para achar vizinhos.

Nesta página você vai construir, medir e buscar embeddings com as próprias mãos. Sem jargão antes da analogia. Sem magia preta.

Começar a jornada → Ir para índices e Vector Stores

Capítulo 1 O problema

## Computadores não entendem palavras

Você abre um texto e aperta Ctrl + F para achar a palavra “cão”. Mas o texto só escreveu “cachorro”. O computador responde: “não achei”. Ele é literal. Para ele, cão e cachorro são tão diferentes quanto cão e helicóptero.

O computador lê letras. Humanos leem significado. Embeddings existem para ensinar significado ao computador.

### Brinquedo: busca literal (Ctrl+F)

mexa aqui

Digite uma palavra e veja o que o computador encontra exatamente. Tente “cão”, depois “cachorro”, depois “animal”.

Meu cachorro late para o carteiro toda manhã. O animal é dócil com as crianças, mas late mesmo. Ontem ele viu um gato no quintal e correu atrás. Eu amo esse pet — ele é minha família de quatro patas.

Capítulo 2 A grande ideia

## Dar um endereço a cada palavra

Imagine uma cidade onde palavras moram. Palavras parecidas moram no mesmo bairro. “Cachorro” mora perto de “gato” e “animal”. “Pizza” mora perto de “hambúrguer”. “Triste” mora perto de “chorar”.

O endereço de cada palavra é uma lista de números — as coordenadas no mapa. Isso se chama embedding (do inglês to embed = encaixar, embutir).

### Brinquedo: mapa das palavras

clique numa palavra

Clique em qualquer bolinha. Vamos marcar os 3 vizinhos mais próximos e mostrar a distância. Perceba: palavras do mesmo bairro estão juntas.

Clique numa palavra para ver os vizinhos…

Capítulo 3 Construindo

## Faça um embedding com as próprias mãos

Em vez de deixar o computador inventar as dimensões, vamos inventar quatro perguntas humanas. Cada pergunta vira um número de 0 a 10. Juntas, formam o endereço (o vetor) da coisa.

Modelos reais fazem a mesma coisa — só que com 384, 768 ou 1536 perguntas secretas, aprendidas automaticamente a partir de bilhões de textos. Ninguém escolhe as perguntas à mão. O resultado é um endereço muito mais rico.

Capítulo 4 Medindo

## Como medir “parecença”?

Dois amigos apontam com o braço. Se apontam para o mesmo lado, estão alinhados. Se apontam para lados opostos, discordam. Em embeddings, medimos o ângulo entre dois endereços. O nome técnico dessa medida é similaridade de cosseno.

### A fórmula — pedaço por pedaço

cos(θ) = (A · B) / (|A| × |B|)

“Cosseno do ângulo entre A e B = produto escalar dividido pelos comprimentos”

A · B

Produto escalar (dot product)

Multiplique número com número na mesma posição e some tudo. Ex.: A=(3, 4) e B=(1, 2) → 3×1 + 4×2 = 11. Quanto mais “apontam juntos”, maior o resultado.

|A| e |B|

Comprimento (norma)

É o tamanho da seta: |A| = √(3² + 4²) = 5. Dividimos pelos comprimentos para ignorar o tamanho e olhar só a direção — textos longos não “ganham” só por serem longos.

cos(θ)

O resultado final

Sai um número entre −1 e +1. Perto de +1 = mesma direção (parecidos). Perto de 0 = perpendiculares (sem relação). Perto de −1 = opostos.

Exemplo completo com números de verdade

| Passo | Conta |
| --- | --- |
| 1. Vetores | A = (3, 4) B = (4, 3) |
| 2. A · B | 3×4 + 4×3 = 12 + 12 = 24 |
| 3. \|A\| | √(3²+4²) = √25 = 5 |
| 4. \|B\| | √(4²+3²) = √25 = 5 |
| 5. cos | 24 / (5×5) = 24/25 = 0,96 → quase iguais! |

Por que não usamos só a distância euclidiana (régua no mapa)? Porque dois textos sobre o mesmo assunto podem ter vetores de tamanhos diferentes. O cosseno pergunta: “apontam para o mesmo lado?” — e isso é o que importa para significado.

≈ 1

Mesma direção · textos parecidos

≈ 0

Ângulo reto · assuntos diferentes

≈ −1

Direções opostas · (raro em texto)

### Brinquedo: setas arrastáveis

arraste as pontas

Arraste as pontas das setas. Observe o ângulo, o cosseno e a conta ao vivo — é a mesma fórmula de cima, recalculada a cada movimento.

Ângulo θ

0°

cos(θ)

1.00

Veredito

Quase iguais

Conta ao vivo (mesma fórmula)

Capítulo 5 Na prática

## Um buscador semântico de verdade

Agora juntamos tudo: cada frase do FAQ ganha um endereço. Sua pergunta também. Achamos as frases com endereço mais perto. Compare lado a lado com a busca antiga (só palavras iguais).

Léxico (Ctrl+F)

Embedding (semântico)

Capítulo 6 Dimensões

## De 2 para 1536 dimensões

Até agora usamos mapas chatos (2D) ou 4 perguntas. Modelos reais usam centenas ou milhares de números. Mais dimensões = mais nuances (“é sobre seguro?”, “é jurídico?”, “é vigente?”, “é sobre carro ou sobre crédito?”).

Abaixo: um pedacinho do “espaço” de um banco fictício, projetado em 3D. Arraste para girar. A query do cliente fica no meio — e o vizinho amarelo é a armadilha lexical (parece, mas não serve).

Similaridade semântica ≠ relevância. O blog de 2019 sobre “seguro do carro” fica perto da pergunta sobre seguro prestamista — mas não responde nada útil. Por isso existe o reranker (um juiz que lê os dois textos juntos).

384

dimensões pequenas

Rápido, barato, bom para começar

768–1536

padrão de mercado

Equilíbrio entre qualidade e custo de RAM

3072+

máxima precisão

Índice pesado — use Matryoshka/quantização

Capítulo 7 Ponte

## E quando são milhões de pontos?

Até aqui o embedding criou o mapa: cada texto tem um endereço. Comparar a pergunta com 20 frases é fácil. Com milhões de vetores, visitar todos é inviável.

A solução da indústria é a busca aproximada — ANN (Approximate Nearest Neighbor) — e os Vector Stores que guardam vetor + documento + metadata.

Índices, ChromaDB e o ecossistema Gemini Enterprise merecem um arquivo próprio: profundidade de referência, sem misturar com a jornada do embedding.

Força bruta

Visita todos · recall 100% · só para corpora pequenos

IVF / HNSW / Tree-AH

Atalhos (bairros ou grafos) · milissegundos · 95–99% de acerto

Vector Store

Chroma, Vertex AI Vector Search, File Search…

Arquivo dedicado

Continuar em Índices e Vector Stores →

Fichas de HNSW, IVF, Tree-AH · brinquedo ANN · ChromaDB completo (arquitetura, HNSW params, pós-filtro) · Gemini Enterprise (File Search, Agent Search, Vertex AI Vector Search, RAG Engine, AlloyDB/BigQuery) · comparativo honesto.

Abrir vector-stores__indices-ann-e-vector-stores.html

Capítulo 9 Recap

## Recapitulando a jornada

Texto

Computador só vê letras. Ctrl+F falha em sinônimos.

Números

Cada texto vira um endereço (vetor) — o embedding.

Mapa

Coisas parecidas moram perto. Cosseno mede a parecença.

Vizinhos

Busca semântica = achar endereços próximos da pergunta.

Índice

Com milhões de pontos, usamos atalhos (ANN): IVF, HNSW…

### Quiz rápido (5 perguntas)

0 / 5

### Glossário ilustrado

Embedding

O endereço secreto de um texto — uma lista de números que captura significado.

Vetor

A lista de números em si. Em 2D: (x, y). Em 1536D: 1536 números.

Dimensão

Uma “pergunta” do endereço. Mais dimensões = mais nuances.

Cosseno

Medida de alinhamento entre dois vetores. 1 = mesma direção, 0 = ortogonais, −1 = opostos.

ANN

Approximate Nearest Neighbor — busca aproximada do vizinho mais próximo (família: IVF, HNSW, DiskANN…).

IVF

Inverted File Index — divide o espaço em “bairros” (células) e só visita os mais próximos (nprobe).

PQ

Product Quantization — comprime vetores em códigos curtos; com IVF vira IVF-PQ (economiza muita RAM).

Recall

Dos vizinhos certos, quantos realmente foram encontrados.

Índice

Estrutura que organiza os embeddings para busca rápida (grafo, células…).

HNSW

Hierarchical Navigable Small World — grafo em camadas com atalhos (avião → ônibus → a pé); padrão de mercado.

DiskANN

ANN com grafo no SSD — para bilhões de vetores quando a RAM não basta.

### Quer ir mais fundo?

Didático + referência

Índices e Vector Stores

ANN, ChromaDB completo e Gemini Enterprise (File Search, Vector Search, RAG Engine).

Abrir jornada →

Avançado

Embeddings além do cosseno

Bi-encoder, SPLADE, ColBERT, Matryoshka, quantização.

Abrir módulo →

Avançado

Masterclass · Índices

Filtros, freshness e código de produção da Íris.

Abrir módulo →
