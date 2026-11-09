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
- **Enriquecer os trechos na indexação:** gerar por LLM perguntas que cada trecho responde e embedar junto. Ataca o problema do lado do documento, no vocabulário do usuário, sem depender do palpite na hora da consulta.

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
