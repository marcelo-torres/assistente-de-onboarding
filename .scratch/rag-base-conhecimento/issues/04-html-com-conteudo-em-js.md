# 04: HTMLs com conteúdo em JS na base

**What to build:** os 5 HTMLs cujo conteúdo está em objetos JavaScript (`rag__agentic-retrieval-e-memoria`, `rag__masterclass-rag-e-memoria`, `rag__rag-avancado-e-agentes`, `memoria-agentes__the-memory-arquitetura-stateful`, `fundamentos-agentes__ecossistema-adk-e-economia-de-tokens`) passam a ser respondíveis pelo agente. Um parser comum extrai só 137 a 747 caracteres desses arquivos. O conversor ganha o tipo "HTML com JS": abre o arquivo no Playwright headless, lê a variável de dados (`MODULES` e equivalentes) com `page.evaluate` e a transforma em markdown com headings (módulo, bloco, capítulo). Vale deixar no conversor um comentário explicando por que o parser comum falha (valor didático).

Risco: se cada arquivo usar uma estrutura diferente, dividir esta tarefa em duas.

**Blocked by:** 01 — RAG ponta a ponta com o arquivo markdown

**Status:** ready-for-agent

- [ ] A variável de dados de cada um dos 5 arquivos foi mapeada
- [ ] Os 5 `.md` existem na pasta de markdown revisado, com headings coerentes e sem resíduos de JS/HTML
- [ ] O autor revisou cada `.md` lado a lado com o original
- [ ] `playwright` está no `requirements.txt` e o README menciona `playwright install chromium` para a conversão
- [ ] Após reindexar, a coleção tem trechos dos 5 arquivos
- [ ] No `adk web`, uma pergunta sobre agentic retrieval cita um dos arquivos `rag__`
