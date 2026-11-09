# Assistente de Onboarding para Desenvolvedores

Este repositório contém a arquitetura e implementação dos agentes inteligentes de onboarding baseados em **Google ADK (Agent Development Kit)** e no protocolo **A2A (Agent-to-Agent)**.

## Módulos do Projeto

- **[agente-tutor](./agente-tutor)**: Subagente Tutor responsável por acolher o novo desenvolvedor, realizar a entrevista inicial de perfil, propor e gerenciar **missões guiadas de negócio e técnicas**, oferecer suporte em rounds e consultar a base corporativa via A2A.
- *(Subagente de Conhecimento - Fora do escopo atual, integrado via protocolo A2A)*



python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# (Só para reconverter os originais) Converter resources/base-conhecimento/ em markdown.
# Os HTMLs com conteúdo em JS são lidos num Chromium headless, que o Playwright precisa baixar:
playwright install chromium
python scripts/converter_base.py

# Indexar a base de conhecimento (antes do adk web; rodar de novo sempre que resources/base-conhecimento-md/ mudar)
python scripts/indexar_base.py

.venv\Scripts\adk.exe web ./apps --host 127.0.0.1 --port 8897