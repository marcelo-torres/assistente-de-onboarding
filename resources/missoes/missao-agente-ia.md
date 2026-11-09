# Missão: Agente de IA

## Objetivo
Executar localmente um agente de IA, preparando o ambiente de desenvolvimento e validando seu funcionamento.

---

## Etapa 1 — Introdução ao desenvolvimento de agentes

**Objetivo:** Conhecer o nível de experiência do tutorado e apresentar os principais conceitos relacionados ao desenvolvimento de agentes de IA.

### 1.1 Entrevista
Pergunte ao tutorado:
1. Quantos anos de experiência você tem em desenvolvimento de software?
2. Quais linguagens de programação você conhece?
3. Você já desenvolveu algum agente de IA?

### 1.2 Fundamentos
Apresente, de acordo com a experiência do tutorado, os seguintes conceitos:
- Inteligência Artificial Generativa.
- Embeddings.
- Busca vetorial.
- RAG.
- Guardrails.

Utilize exemplos práticos e objetivos, seguindo uma linha de raciocínio. Consulte o agente de conhecimento para apoiar as explicações.

**Checkpoint:** O tutorado deve confirmar que compreendeu os conceitos e esclarecer eventuais dúvidas.

---

## Etapa 2 — Instalar o Python

**Objetivo:** Instalar e validar o Python 3.12 na máquina local.

### 2.1 Introdução
- Caso necessário, apresente brevemente a linguagem Python.
- Explique sua aplicação no desenvolvimento de agentes de IA.

### 2.2 Instalação
- Identifique o sistema operacional utilizado pelo tutorado.
- Oriente o download e a instalação pelo site oficial: https://www.python.org/

**Checkpoint:** Executar `python --version` e confirmar que a versão instalada é 3.12.

---

## Etapa 3 — Instalar o Google Cloud CLI

**Objetivo:** Preparar o ambiente local para autenticação e utilização das APIs do Google Cloud e Vertex AI.

### 3.1 Instalação
- Identificar o sistema operacional.
- Orientar o download e a instalação do Google Cloud CLI.

### 3.2 Configuração
- Realizar a autenticação na conta Google.
- Configurar o projeto e validar o acesso aos serviços necessários.

**Checkpoint:** Executar os comandos de validação e confirmar que o CLI está instalado, autenticado e configurado para o projeto correto.

---

## Etapa 4 — Clonar e configurar o repositório

**Objetivo:** Obter o código-fonte do projeto e preparar suas dependências e configurações locais.

### 4.1 Clonagem
- Repositório: https://github.com/Hcode-AI-Team/agent-the-memory
- Branch: `rag-turma-2`

### 4.2 Dependências e configurações
- Instalar as dependências utilizando `pip install`.
- Criar o arquivo `.env` com base no `.env.example`.
- Configurar o projeto GCP: `spartan-setting-485114-e3`.

**Checkpoint:** Confirmar que o repositório foi clonado, as dependências foram instaladas e as variáveis de ambiente foram configuradas.

---

## Etapa 5 — Executar e validar o agente

**Objetivo:** Executar o agente localmente e validar seu funcionamento.

### 5.1 Execução
- Seguir as instruções de execução do projeto.
- Inicializar o agente no ambiente local.

### 5.2 Validação
- Realizar uma interação com o agente.
- Verificar se o agente responde conforme o comportamento esperado.

**Checkpoint:** Apresentar uma evidência da execução local e de uma interação bem-sucedida com o agente.

---

## Conclusão da missão

**Evidência final:** Apresentar o agente em execução local, demonstrando uma interação funcional e confirmando que o ambiente foi configurado corretamente.