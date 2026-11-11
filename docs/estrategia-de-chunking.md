# Estratégia de chunking — RAG da base de conhecimento

Data: 2026-11-09

Complementa a Fase 2 de [`plano-rag-base-conhecimento.md`](plano-rag-base-conhecimento.md). Este documento registra como a base é cortada em trechos e por que o corte é feito **sem overlap**.

## Estratégia adotada

- **Corte hierárquico por heading.** Trechos de até 2.000 caracteres, contando o cabeçalho contextual (cerca de 500 tokens, a ~4 caracteres por token, sem tokenizador).
- **Seção com subseções vira um trecho só quando cabe.** Se a seção, somada a todas as subseções, cabe no limite, vira um trecho com os subtítulos no texto e cita a seção pai. Se não cabe, o corpo próprio vira um trecho e cada subseção é avaliada do mesmo jeito. Seções vizinhas sem relação de pai e filho nunca são juntadas, então a citação continua apontando para um assunto só.
- **Subdivisão por parágrafo.** Um corpo acima do limite é dividido entre parágrafos, nunca no meio de uma frase.
- **Sem overlap.** Nenhum texto é repetido entre trechos vizinhos.
- **Cabeçalho contextual.** Cada trecho começa com `"{titulo} > {secao}"`, e esse é o texto embedado e guardado no Chroma.
- **Metadados:** `fonte`, `tema`, `titulo`, `secao` e `indice_chunk` (ver a tabela da Fase 2 no plano).

## Calibração (tarefa 05)

A primeira versão tinha só o limite máximo (3.200) e nenhuma junção, porque no primeiro arquivo da base as seções eram pequenas mas autossuficientes. Com os 13 arquivos, o `fundamentos-agentes__ecossistema-adk-e-economia-de-tokens` gerou centenas de seções minúsculas (ex.: "#### Orquestração" com três palavras), com embedding fraco: "quais são os níveis de agentes de IA?" não achava a seção "Níveis de Agentes".

Medição com `scripts/avaliar_rag.py` (13 perguntas da base e 3 de IA fora dela, em `tests/avaliacao/perguntas.yaml`):

| Configuração | Trechos | hit@3 pela tool (limiar 0,70) | hit@3 sem limiar | Falsos positivos | Pior acerto (sem limiar) | Maior nota fora da base |
| --- | --- | --- | --- | --- | --- | --- |
| Sem junção, até 3.200 | 1.077 | 85% | 92% | 1/3 | 0,665 | 0,703 |
| Com junção, até 3.200 | 569 | 85% | 92% | 0/3 | 0,626 | 0,692 |
| **Com junção, até 2.000** (adotada) | 644 | 85% | 92% | 0/3 | 0,665 | 0,692 |

"hit@3 pela tool" é o que chega ao agente: o arquivo certo entre os 3 primeiros e acima do limiar. Na configuração adotada, o hit@3 estrito (só o arquivo-alvo, sem os aceitos) também é 92%. Duas perguntas não chegam ao agente:

- **Documentos longos (RAPTOR):** erra nas três configurações; traz trechos sobre chunking e contexto longo de outros arquivos.
- **Comprovante repetido (memória do agente):** acha o arquivo certo, mas com nota 0,665, abaixo do limiar.

Cuidados ao ler estes números: tamanho e junção foram escolhidos com as mesmas 16 perguntas que os medem, e a margem do limiar é de 0,009 (acerto mais fraco que chega ao agente 0,701; maior nota fora da base 0,692), medida com só 3 perguntas negativas. Vale ampliar o conjunto de perguntas antes de confiar no limiar para novas fontes.

## Reavaliação: as falhas vêm do chunking?

Aplicando o critério de revisão (fim deste documento) às duas perguntas que não chegam ao agente:

| Pergunta | Trecho certo | Nota | Resposta dividida entre trechos? |
| --- | --- | --- | --- |
| Documento longo (RAPTOR) | `rag__rag-avancado-e-agentes.md::11`, seção RAPTOR inteira (1.831 caracteres) | 0,650 | Não |
| Comprovante pedido de novo | `memoria-agentes__...::3`, exemplo de diálogo inteiro (992 caracteres) | 0,665 | Não |

Hipóteses testadas embedando versões alternativas dos trechos com a mesma pergunta:

| Variação | Nota |
| --- | --- |
| RAPTOR sem o ruído do diagrama ("C1", "S1", "Resumo de C1-C2") | 0,645 (era 0,650) |
| Memória só com a parte relevante (RAG stateless) | 0,671 (era 0,665) |

Conclusão: **as falhas não são de chunking.** Nem overlap, nem expansão de vizinhos, nem trechos menores ou mais limpos mudam a nota de forma relevante. A distância está entre o vocabulário da pergunta ("documento muito longo", "pede de novo um comprovante") e o do texto ("RAPTOR", "sumarização hierárquica", "RAG stateless"). A estratégia de chunking fica como está, sem overlap.

### Tentativa do lado da consulta: reescrita no prompt

Em produção, quem chama a busca é o agente, com a consulta que ele mesmo reescreve. Com o prompt original ("consulta autônoma e específica"), o LLM às vezes encurtava a pergunta: "agente de negociação pede comprovante novamente" não passava do limiar.

O prompt do `agente_conhecimento` passou a pedir:

- **Expandir, nunca encurtar:** manter todos os detalhes e acrescentar os termos técnicos do assunto.
- **Segunda tentativa:** com lista vazia, buscar mais uma vez com outra formulação.
- **Recusa mais ampla:** dizer "não encontrei" também quando os trechos não respondem à pergunta (para a segunda busca não puxar assunto vizinho).

Medição com o agente real (`python scripts/avaliar_rag.py --agente`, uma rodada de cada; o LLM não é determinístico):

| Métrica | Prompt original | Prompt novo |
| --- | --- | --- |
| Trecho certo no top-3 de alguma busca | 11/13 | 11/13 |
| Respondeu "não encontrei" para pergunta da base | 1/13 | 1/13 |
| Fora da base: a busca trouxe trechos | 2/3 | 2/3 |
| Fora da base: respondeu "não encontrei" | 3/3 | 3/3 |

Resultado: sem ganho e sem regressão. O agente passou a expandir as consultas, mas na direção errada nos dois casos que falham:

- **Comprovante:** expandiu como problema de processo de negócio ("falha no sistema de recebimento de documentos"), não de arquitetura de memória.
- **Documento longo:** expandiu para "documentos extensos com informações de múltiplas seções", sem chegar a "RAPTOR".

A reescrita só ajuda quando o LLM adivinha o conceito técnico, e HyDE ou multi-query dependem do mesmo palpite. O prompt novo foi mantido porque não encurta mais as consultas e a recusa continua firme fora da base (nas perguntas de vLLM e CrewAI, a segunda busca trouxe trechos vizinhos e o agente respondeu "não encontrei").

Caminhos que ainda podem fechar essa distância, sem testes até aqui:

- **Busca híbrida (BM25 + RRF):** não ajuda nestes dois casos, porque as palavras da pergunta não aparecem no texto.
- **Enriquecer os trechos na indexação:** gerar por LLM perguntas que cada trecho responde e embedar junto. Ataca o problema do lado do documento, no vocabulário do usuário, sem depender do palpite na hora da consulta. Implementado como opção; ver a próxima seção.

## Enriquecimento dos trechos com perguntas geradas

**Status:** medido em 2026-11-11 e ligado por padrão (`ENRIQUECER_COM_PERGUNTAS = True`). O cache com as perguntas dos 643 trechos distintos está versionado em `resources/perguntas-geradas.json`. Resultados em [Medição](#medição-2026-11-11).

### Por quê

As duas perguntas que não chegam ao agente falham por vocabulário, não por chunking. Quem pergunta descreve o problema ("documento muito longo", "pede de novo um comprovante"); o trecho nomeia a solução ("RAPTOR", "RAG stateless"). Reescrever a consulta não resolveu, porque depende de o LLM adivinhar o conceito técnico na hora da pergunta, e nos dois casos ele errou a direção.

O enriquecimento ataca o mesmo problema do outro lado. Na indexação, com o trecho na frente, o LLM não precisa adivinhar nada: ele escreve perguntas que aquele trecho responde, no vocabulário de quem ainda não conhece os termos. Essas perguntas entram no embedding, e a pergunta real do usuário passa a ter algo parecido com ela para encontrar.

### Como funciona

- Para cada trecho, um LLM gera 3 perguntas no vocabulário de um desenvolvedor recém-chegado (`rag/enriquecimento.py`).
- O embedding é feito sobre o trecho seguido de "Perguntas que este trecho responde:" e da lista.
- O texto guardado no Chroma e entregue ao agente **não muda**: continua sendo só o trecho. As perguntas ficam no metadado `perguntas`, para inspeção.

### Como usar

```bash
python scripts/indexar_base.py --estimar               # custo, sem chamar API
python scripts/indexar_base.py --enriquecer --estimar  # custo com o enriquecimento
python scripts/indexar_base.py --enriquecer            # indexa com perguntas geradas
python scripts/avaliar_rag.py                           # mede o efeito
```

Também dá para ligar de vez com `ENRIQUECER_COM_PERGUNTAS = True` em `rag/config.py`.

### Cuidados com o consumo de tokens

| Medida | Efeito |
| --- | --- |
| Desligado por padrão | Nada é gerado sem pedir explicitamente |
| `--estimar` | Mostra trechos a gerar, chamadas e tokens previstos, sem credencial e sem API |
| Cache por hash do texto do trecho (`resources/perguntas-geradas.json`) | Reindexar não gera de novo; só trechos novos ou alterados chamam o LLM |
| Cache versionável no git | Quem clonar o repositório reaproveita as perguntas sem pagar de novo |
| Cache salvo a cada lote | Uma falha ou um 429 no meio não desperdiça o que já foi gerado |
| 10 trechos por chamada | Cerca de 65 chamadas para a base inteira, em vez de 644 (também reduz 429) |
| `gemini-2.5-flash-lite`, sem *thinking* | Modelo mais barato e sem tokens de raciocínio interno cobrados |
| Saída JSON validada antes de entrar no cache | Resposta malformada falha sem gravar lixo |

Um custo que continua existindo com ou sem enriquecimento: **toda indexação gera de novo o embedding de todos os trechos**, mesmo dos que não mudaram. O `--estimar` mostra esse número também.

### Medição (2026-11-11)

Roteiro seguido: estimar o custo, indexar com `--enriquecer`, rodar as duas avaliações, revisar uma amostra das perguntas geradas.

**Custo.** A estimativa previa 70 chamadas ao `gemini-2.5-flash-lite` (~137 mil tokens de entrada e ~48 mil de saída) e ~175 mil tokens de embedding. A geração rodou sem nenhum 429.

**Falha na primeira tentativa.** No primeiro lote, o modelo devolveu uma quantidade de listas de perguntas diferente da de trechos, e a validação barrou a resposta antes do cache, como previsto. O índice não foi afetado, porque a geração roda antes de apagar qualquer trecho. Correções:

- O schema de saída fixa a quantidade de listas (`min_items` = `max_items` = trechos do lote). Só isso já resolveu na segunda tentativa.
- Como garantia, `dividir_se_invalida` divide o lote ao meio e tenta cada metade se a resposta ainda vier inválida, até chegar a trechos individuais.

**Busca direta** (`python scripts/avaliar_rag.py`):

| Métrica | Sem enriquecimento | Com enriquecimento |
| --- | --- | --- |
| hit@3 pela tool (acima do limiar) | 11/13 = 85% | **12/13 = 92%** |
| hit@3 bruto / estrito | 92% / 92% | 92% / 92% |
| Falsos positivos | 0/3 | 0/3 |
| Acerto mais fraco que chega ao agente × maior nota fora da base | 0,701 × 0,692 | 0,701 × 0,693 |

**Agente real** (`python scripts/avaliar_rag.py --agente`, uma rodada de cada; o LLM não é determinístico):

| Métrica | Sem enriquecimento | Com enriquecimento |
| --- | --- | --- |
| Trecho certo no top-3 de alguma busca | 11/13 | **12/13** |
| Respondeu "não encontrei" para pergunta da base | 1/13 | **0/13** |
| Fora da base: a busca trouxe trechos | 2/3 | **3/3** (piorou) |
| Fora da base: respondeu "não encontrei" | 3/3 | 3/3 |

**As duas perguntas que falhavam:**

- **Comprovante pedido de novo:** passou a chegar ao agente (0,665 → 0,707 na busca direta; 0,78 pela consulta do agente). Uma das perguntas geradas para o trecho é quase a do usuário: "Por que o sistema de IA às vezes pede o comprovante de renda de novo, mesmo que eu já tenha enviado?".
- **Documento longo (RAPTOR):** continua falhando. As perguntas geradas falam em "resumir vários documentos" e "visão geral", não em "documento muito longo". A técnica aproxima vocabulários, mas não garante que o LLM preveja a pergunta exata.

**Efeito colateral: o limiar deixou de barrar as perguntas fora da base pelo agente.** Com as consultas expandidas pelo agente, as três perguntas fora da base (vLLM, RLHF, CrewAI/AutoGen) trouxeram trechos com notas de 0,70 a 0,73, no nível de acertos verdadeiros (o mais fraco pelo agente foi 0,71). Quem segurou foi a regra 5 do prompt: o agente disse "não encontrei" nas três. A proteção contra respostas fora da base passou de duas camadas (limiar e prompt) para uma (prompt).

**Revisão das perguntas geradas.** Uma amostra aleatória está no vocabulário pedido (descreve o problema, não repete o título), e só 1 trecho ficou com menos de 3 perguntas.

**Decisão.** Adotado: ganho em acerto pela tool e pelo agente, nenhuma recusa indevida e recusa correta fora da base. Pendências para recuperar a segunda camada:

1. Ampliar as perguntas fora da base de 3 para cerca de 10, com assuntos de IA próximos da base. O limiar está calibrado com pouquíssimos negativos.
2. Com esse conjunto, recalibrar o limiar. Subir para 0,72–0,73 pode barrar os negativos, mas o acerto mais fraco pela tool está em 0,701; a medição dirá se há espaço.

## O que é overlap

Overlap é repetir o final de um trecho no começo do seguinte. Com trechos de 2.000 caracteres e 10% de overlap, os últimos ~200 caracteres do trecho 4 também abrem o trecho 5.

## O que o overlap resolve

O problema é o corte no lugar errado. Quando uma ideia fica dividida entre dois trechos, nenhum dos dois a representa bem:

- O trecho 4 termina com "Para solicitar acesso ao sistema X, siga os passos abaixo:".
- O trecho 5 começa com "1. Abra um chamado... 2. Aguarde aprovação do gestor".

O trecho 4 tem a pergunta sem a resposta. O trecho 5 tem a resposta sem dizer do que se trata. O embedding de cada um fica fraco para a busca "como peço acesso ao sistema X". Com overlap, o trecho 5 carrega o enunciado junto e passa a ser encontrado.

## O que o overlap custa

| Custo | Impacto |
| --- | --- |
| Resultados quase duplicados | Trechos vizinhos compartilham texto e tendem a aparecer juntos no ranking. Com top-3, um deles pode ocupar a vaga de outro arquivo relevante. É o custo mais relevante neste projeto. |
| Contexto redundante para o LLM | O mesmo texto chega duas vezes ao prompt, gastando tokens sem trazer informação nova. |
| Citação e deduplicação mais confusas | Fica mais difícil dizer de onde veio um trecho, e às vezes é preciso deduplicar antes de responder. |
| Índice maior | 10 a 20% a mais de embeddings e armazenamento. Desprezível com 13 arquivos. |
| Mais um parâmetro para calibrar | Tamanho do overlap e se ele respeita frase ou parágrafo. |

## Por que não usar overlap aqui

O overlap foi pensado sobretudo para **chunking de tamanho fixo**, que corta no meio de frases e seções. A estratégia adotada já reduz esse problema de três formas:

1. **Corte por heading.** A maior parte dos trechos é uma seção inteira, sem corte interno. Entre seções diferentes, o overlap atrapalharia: misturaria o fim de um assunto no começo de outro.
2. **Subdivisão por parágrafo.** Nas seções longas, o corte cai entre parágrafos, não no meio de frases.
3. **Cabeçalho contextual.** No exemplo acima, o trecho 5 começaria com `"Guia de acessos > Solicitação de acesso"`, então o embedding já sabe do que se trata, mesmo sem o enunciado.

O único lugar onde o overlap faria diferença é a fronteira entre parágrafos de uma seção subdividida, e o cabeçalho contextual já cobre boa parte desse caso. Somado ao critério geral de **menor esforço**, o benefício não paga o custo.

## Alternativa, se for preciso: expandir vizinhos na busca

Em vez de duplicar texto no índice, a tool busca normalmente e, ao montar o resultado, traz também os trechos `indice_chunk - 1` e `indice_chunk + 1` da mesma `fonte` e `secao`, com um `collection.get(where=...)` a mais.

| | Overlap | Expansão de vizinhos |
| --- | --- | --- |
| Quando age | Na indexação | Na busca |
| Alcance | Todos os trechos | Só os trechos encontrados |
| Efeito no ranking | Gera quase duplicados | Ranking fica limpo |
| Mudança necessária | Reindexar | Só a tool de busca; metadados já existem |

É a mesma ideia dos chunks pai-filho listados nas evoluções pós-MVP, numa versão mais simples.

## Critério de revisão

Na avaliação da Fase 4 (16 perguntas, hit@3):

1. Para cada pergunta que falhar, verificar se a resposta estava dividida entre dois trechos da mesma seção subdividida.
2. Se esse padrão aparecer, adotar a expansão de vizinhos.
3. Só considerar overlap (10 a 20%, respeitando parágrafos e restrito às seções subdivididas) se a expansão de vizinhos não resolver.
