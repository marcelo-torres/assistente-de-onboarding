# 03: PDFs na base

**What to build:** os 2 decks em PDF (`guardrails__deck-guardrails-descida-da-serra`, 29 páginas, e `rag__deck-rag-na-agent-platform`, 34 páginas) passam a ser respondíveis pelo agente. O conversor ganha o tipo "PDF" com `pypdf`: um bloco (heading) por slide e correção dos títulos com letras espaçadas (ex.: "A B E R T U R A" → "Abertura"), de preferência como regra no conversor e não como edição manual.

**Blocked by:** 01 — RAG ponta a ponta com o arquivo markdown

**Status:** ready-for-agent

- [ ] Os 2 `.md` existem na pasta de markdown revisado, com um heading por slide e sem títulos com letras espaçadas
- [ ] O autor revisou cada `.md` lado a lado com o original
- [ ] `pypdf` está no `requirements.txt`
- [ ] Após reindexar, a coleção tem trechos dos 2 arquivos
- [ ] No `adk web`, uma pergunta sobre guardrails cita o deck de guardrails
