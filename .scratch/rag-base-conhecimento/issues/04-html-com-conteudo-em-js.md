# 04: HTMLs com conteúdo em JS na base

**What to build:** os 5 HTMLs cujo conteúdo está em objetos JavaScript (`rag__agentic-retrieval-e-memoria`, `rag__masterclass-rag-e-memoria`, `rag__rag-avancado-e-agentes`, `memoria-agentes__the-memory-arquitetura-stateful`, `fundamentos-agentes__ecossistema-adk-e-economia-de-tokens`) passam a ser respondíveis pelo agente. Um parser comum extrai só 137 a 747 caracteres desses arquivos. O conversor ganha o tipo "HTML com JS": abre o arquivo no Playwright headless, lê a variável de dados (`MODULES` e equivalentes) com `page.evaluate` e a transforma em markdown com headings (módulo, bloco, capítulo). Vale deixar no conversor um comentário explicando por que o parser comum falha (valor didático).

Risco: se cada arquivo usar uma estrutura diferente, dividir esta tarefa em duas.

**Blocked by:** 01 — RAG ponta a ponta com o arquivo markdown

**Status:** ready-for-agent

- [x] A variável de dados de cada um dos 5 arquivos foi mapeada
- [x] Os 5 `.md` existem na pasta de markdown revisado, com headings coerentes e sem resíduos de JS/HTML
- [ ] O autor revisou cada `.md` lado a lado com o original
- [x] `playwright` está no `requirements.txt` e o README menciona `playwright install chromium` para a conversão
- [x] Após reindexar, a coleção tem trechos dos 5 arquivos
- [x] No `adk web`, uma pergunta sobre agentic retrieval cita um dos arquivos `rag__`

## Nota de implementação

O risco se confirmou: só 2 dos 5 arquivos guardam o conteúdo numa variável de dados. A tarefa não foi dividida; o conversor (`scripts/converter_js.py`) ganhou uma estratégia por formato, registrada em `PAGINAS_COM_JS`:

| Arquivo | Estratégia |
| --- | --- |
| `rag__agentic-retrieval-e-memoria` | `Variavel("MODULES")`: o objeto vira markdown (módulo `##`, bloco `###`) |
| `rag__masterclass-rag-e-memoria` | `Template`: `buildSectionHTML(modulo)` para cada item de `courseData.modules`, porque parte do texto só existe no template |
| `rag__rag-avancado-e-agentes` | `Rotas("#app-content")`: `router(rota)` para cada rota do menu |
| `memoria-agentes__the-memory-arquitetura-stateful` | `Rotas("#content-area")` |
| `fundamentos-agentes__ecossistema-adk-e-economia-de-tokens` | `Rotas("#main-content")` + modais `setup` e `vertexai` |

O HTML renderizado pelas estratégias `Template` e `Rotas` passa pelo mesmo conversor de HTML estático da tarefa 02.

Pendente para a tarefa 05: o `fundamentos` gera centenas de seções minúsculas (ex.: "#### Orquestração" com três palavras), que viram trechos com embedding fraco. A pergunta "quais são os níveis de agentes de IA?" não encontra a seção "Níveis de Agentes". Juntar seções pequenas com as subseções delas é calibração de chunking.
