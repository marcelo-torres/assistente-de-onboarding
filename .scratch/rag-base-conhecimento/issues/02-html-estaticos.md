# 02: HTMLs estáticos na base

**What to build:** os 5 HTMLs estáticos da base (`embeddings__embeddings-do-zero`, `vector-stores__indices-ann-e-vector-stores`, `vector-stores__anatomia-vertex-ai-vector-search`, `busca-hibrida__bm25-e-rrf`, `programa__jornada-agentes-ia-visao-geral`) passam a ser respondíveis pelo agente. O conversor ganha o tipo "HTML estático" com BeautifulSoup, descartando nav, sidebar e footer, gerando um H1 por arquivo, headings coerentes e nenhum HTML residual. O conversor e os originais ficam no repositório como material didático; o conversor sobrescreve os `.md` sem proteção (o git recupera).

**Blocked by:** 01 — RAG ponta a ponta com o arquivo markdown

**Status:** ready-for-agent

- [x] Os 5 `.md` existem na pasta de markdown revisado, nenhum vazio, só com menus ou com HTML residual
- [ ] O autor revisou cada `.md` lado a lado com o original
- [x] `beautifulsoup4` está no `requirements.txt`
- [x] Após reindexar, a coleção tem trechos dos 5 arquivos
- [x] No `adk web`, uma pergunta sobre BM25/RRF cita `busca-hibrida__bm25-e-rrf`
