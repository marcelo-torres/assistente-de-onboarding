# Assistente de Onboarding para Desenvolvedores

Este repositório contém a arquitetura e implementação dos agentes inteligentes de onboarding baseados em **Google ADK (Agent Development Kit)**.

## Módulos do Projeto

- **[agente_tutor](./apps/agente_tutor)**: agente principal. Acolhe o novo desenvolvedor, lista as missões disponíveis, carrega a escolhida e conduz cada etapa até o checkpoint, exigindo as evidências de conclusão. Dúvidas conceituais são transferidas ao agente de conhecimento.
- **[agente_conhecimento](./apps/agente_conhecimento)**: subagente do tutor (`sub_agents` do ADK, no mesmo processo). Responde só com base na base de conhecimento, via RAG com ChromaDB, e cita as fontes. A integração via protocolo **A2A** faz parte da arquitetura futura.

As missões ficam em `resources/missoes/` e o prompt do tutor em `resources/prompt-tutor.md`.

Decisões e histórico em `docs/`: [plano do RAG](docs/plano-rag-base-conhecimento.md), [estratégia de chunking e avaliação](docs/estrategia-de-chunking.md) e [melhorias de baixo risco](docs/melhorias-baixo-risco.md).

## Como rodar

```bash
# Ambiente (macOS/Linux)
python -m venv .venv
source .venv/bin/activate
# No Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Credenciais: copie .exemplo.env para .env e preencha o projeto do Google Cloud

# (Só para reconverter os originais) Converter resources/base-conhecimento/ em markdown.
# Os HTMLs com conteúdo em JS são lidos num Chromium headless, que o Playwright precisa baixar:
playwright install chromium
python scripts/converter_base.py

# Indexar a base de conhecimento (antes do adk web; rodar de novo sempre que resources/base-conhecimento-md/ mudar)
python scripts/indexar_base.py
# Opcional (consome tokens do Gemini): enriquecer os trechos com perguntas geradas.
# Veja o custo antes com --estimar, que não chama nenhuma API.
python scripts/indexar_base.py --enriquecer --estimar
python scripts/indexar_base.py --enriquecer

# Avaliar a recuperação com as perguntas de tests/avaliacao/perguntas.yaml
python scripts/avaliar_rag.py            # busca direta com a pergunta do usuário
python scripts/avaliar_rag.py --agente   # agente real (usa o LLM; mais lento)

# Testes
pytest

# Subir a interface (com o ambiente ativado; acesse http://127.0.0.1:8897)
adk web ./apps --host 127.0.0.1 --port 8897
```
