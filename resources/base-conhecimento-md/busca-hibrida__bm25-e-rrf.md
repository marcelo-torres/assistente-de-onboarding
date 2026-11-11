# Masterclass: Arquitetura Hybrid Search | Auditor de Contratos

H

## Hybrid Search | Masterclass

Auditor de Contratos - Bootcamp Itaú FIAP 2026

Guia Interativo de Implementação

## A Miopia da Busca Semântica

Sistemas RAG puramente vetoriais são excelentes para conceitos, mas falham em termos exatos. No contexto de auditoria, confundir números de contrato é inaceitável.

### Busca Vetorial (Semântica)

Dense Retrieval

Query: "Contrato matrícula 12345 "

❌

Retorno: "Contrato matrícula 54321" Motivo: Semanticamente idêntico (ambos são contratos), mas número errado.

### Solução Híbrida

Dense + Sparse

Query: "Contrato matrícula 12345 "

✅

Retorno: "Contrato matrícula 12345" Motivo: BM25 captura o token exato "12345", corrigindo a alucinação semântica.

\# Por que precisamos do BM25?

class HybridSearchAdapter:

"""

Embeddings capturam significado.

BM25 captura tokens exatos (IDs, Datas, CPFs).

Juntos, eles cobrem as falhas um do outro.

"""

## Anatomia do BM25

O BM25 não é uma contagem linear. Ele usa uma curva de saturação. Se uma palavra aparece 100 vezes, ela não é 100x mais importante.

### Parâmetros de Ajuste

1.5

Controla quão rápido o score satura. Padrão: 1.2 - 2.0

0.75

Penaliza documentos longos. 1.0 = penalização total.

Score = IDF * (TF * (k1 + 1)) / (TF + k1 * (1 - b + b * L/avgL))

### Curva de Impacto da Frequência (TF)

Eixo X: Frequência do termo no doc | Eixo Y: Score BM25 Resultante

## Reciprocal Rank Fusion (RRF)

Como somar maçãs (distância vetorial) com laranjas (score BM25)? A resposta: ignoramos os valores e usamos apenas o Ranking.

### Calculadora RRF

RRF Score: 0.0317

Fórmula:

Score = (1 / (60 + rank_sem)) + (1 / (60 + rank_key))

A constante k=60 suaviza a curva, garantindo que o top 1 seja muito mais valioso que o top 10.

### Impacto da Posição no Score

## Simulador Hybrid

Ajuste o Alpha ($\alpha$) para balancear entre contexto e precisão exata.

0.5

Keyword (BM25) Semântico (Vector)

Modo Keyword Puro ($\alpha < 0.3$): Prioriza tokens exatos. Ideal para IDs, CPFs e Códigos.

Modo Híbrido ($\alpha \approx 0.5$): Equilíbrio perfeito. Usa contexto mas respeita termos técnicos.

Modo Semântico ($\alpha > 0.7$): Foca em intenção e sinônimos. Ignora erros de digitação.

### Resultados Re-rankeados

Query: "Contrato 12345 de Serviços TI"
