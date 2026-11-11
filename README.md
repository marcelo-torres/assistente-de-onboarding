# Assistente de Onboarding para Desenvolvedores

Este repositório contém a arquitetura e implementação dos agentes inteligentes de onboarding baseados em **Google ADK (Agent Development Kit)**, `google-genai` e no protocolo **A2A (Agent-to-Agent)**.

## Módulos do Projeto

- **`agente_tutor` (`apps/agente_tutor`)**: Agente Tutor responsável por acolher o novo desenvolvedor, gerenciar **missões guiadas de negócio e técnicas** passo a passo, validar checkpoints (SITE, ACOM, logs de captura) e acionar o `agente_conhecimento` para aprofundamento técnico.
- **`agente_conhecimento` (`apps/agente_conhecimento`)**: Agente consultivo para dúvidas sobre desenvolvimento de agentes de IA, arquitetura RAG, estratégias de chunking, embeddings, memória (The Memory) e Google ADK. Opera em modo **estritamente somente-leitura**.
- **`guardrails` (`apps/guardrails`)**: Camada de Defesa em Profundidade (*Input, Scope, Execution e Output Rails*) cobrindo IA Responsável (RAI), controle de escopo e imutabilidade estrutural.

---

## Camada de Guardrails

A arquitetura implementa o princípio de que *"Prompt é pedido, Guardrail é parede"*:

1. **Prevenção de Palavras de Ódio e Conteúdo Nocivo (RAI):** Gemini Safety Settings nativas + varredura determinística rápida no `before_model_callback`.
2. **Controle de Tópico e Fuga de Escopo (Context Rail):** Garante foco estrito na missão para o Tutor e no ecossistema de IA para o Conhecimento, com recusa cordial e educativa.
3. **Imutabilidade e Restrição de Escrita (Execution Rail):** Bloqueio estrito (*Fail-Closed*) de qualquer ferramenta ou comando de alteração/exclusão na base de dados pelo `agente_conhecimento`.

---

## Configuração do Ambiente e Instalação

```bash
# 1. Criação e ativação do ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# 2. Instalação das dependências
pip install -r requirements.txt
```

---

## Execução dos Testes de Segurança (Red Teaming)

A suíte de testes cobre 30 cenários adversariais (`tests/guardrails/cenarios_adversariais.yaml`):

```bash
# Executar a bateria completa de testes de guardrails
pytest -v tests/guardrails
```

---

## Inicialização da Aplicação (ADK Web)

```bash
.venv\Scripts\adk.exe web ./apps --host 127.0.0.1 --port 8897
```
