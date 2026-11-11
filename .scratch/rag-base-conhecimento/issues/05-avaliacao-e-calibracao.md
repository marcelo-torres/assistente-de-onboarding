# 05: Avaliação e calibração

**What to build:** uma régua objetiva da recuperação, usada para calibrar o tamanho dos trechos e o limiar de similaridade com os 13 arquivos já indexados. Um arquivo de perguntas traz uma pergunta por arquivo da base (com o arquivo esperado) e 3 perguntas fora da base, próximas do domínio (assuntos de IA que a base não cobre, ex.: "como configurar o checkpointer do LangGraph?"). Um script roda cada pergunta pela tool de busca e mede hit@3 (o arquivo esperado aparece entre os 3 primeiros?) e, nas perguntas fora da base, se algum resultado passa do limiar.

**Blocked by:** 02 — HTMLs estáticos; 03 — PDFs; 04 — HTMLs com conteúdo em JS

**Status:** done

- [x] O arquivo de perguntas tem 13 perguntas da base (uma por arquivo) e 3 fora da base próximas do domínio
- [x] O script de avaliação imprime hit@3 e lista os falsos positivos
- [x] Tamanho dos trechos e limiar ajustados e registrados na configuração do RAG
- [x] hit@3 ≥ 85% nas perguntas da base e nenhum falso positivo fora dela (meta inicial, pode ser revista após a primeira rodada)
