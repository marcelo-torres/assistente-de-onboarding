# Estratégia de chunking — RAG da base de conhecimento

Data: 2026-11-09

Complementa a Fase 2 de [`plano-rag-base-conhecimento.md`](plano-rag-base-conhecimento.md). Este documento registra como a base é cortada em trechos e por que o corte é feito **sem overlap**.

## Estratégia adotada

- **Corte hierárquico por heading.** Cada seção do markdown vira um trecho, de 1.200 a 3.200 caracteres (cerca de 300 a 800 tokens, a ~4 caracteres por token, sem tokenizador).
- **Subdivisão por parágrafo.** Seções acima de 3.200 caracteres são divididas entre parágrafos, nunca no meio de uma frase.
- **Sem overlap.** Nenhum texto é repetido entre trechos vizinhos.
- **Cabeçalho contextual.** Cada trecho começa com `"{titulo} > {secao}"`, e esse é o texto embedado e guardado no Chroma.
- **Metadados:** `fonte`, `tema`, `titulo`, `secao` e `indice_chunk` (ver a tabela da Fase 2 no plano).

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
