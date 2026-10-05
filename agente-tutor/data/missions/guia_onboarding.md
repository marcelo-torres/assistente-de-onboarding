# Guia Oficial de Onboarding do Desenvolvedor

Bem-vindo ao time de engenharia de software! Este guia orienta a jornada inicial de novos desenvolvedores, combinando aprendizado prático de **negócio** e **técnico**.

---

## 1. Visão Geral da Jornada de Onboarding

O onboarding é dividido em dois eixos complementares:
1. **Missões de Negócio**: Permitem entender o valor que nossos sistemas geram para os usuários e clientes finais, o domínio de faturamento, gestão de documentos e regras de conformidade.
2. **Missões Técnicas**: Guiam você pela arquitetura de microsserviços, repositórios de código no GitHub, motores de banco de dados, esteiras de CI/CD e práticas de testes da empresa.

---

## 2. Mapa de Missões Disponíveis

### Missões de Negócio
- **`biz-01` - Emissão de Documento no Ambiente de Homologação**:
  - *Objetivo*: Criar uma minuta de documento no portal de homologação e acompanhar o fluxo de aprovação e auditoria.
  - *Público*: Todos os desenvolvedores (Frontend, Backend, Fullstack).
- **`biz-02` - Fluxo de Cadastro e Onboarding de Novo Parceiro Comercial**:
  - *Objetivo*: Entender o fluxo de KYC, análise de compliance e eventos de webhook gerados.
  - *Público*: Todos os desenvolvedores.

### Missões Técnicas
- **`tech-01` - Investigação Arquitetural do Microsserviço de Documentos**:
  - *Objetivo*: Clonar o repositório `ms-documento-api`, inspecionar o arquivo docker-compose e identificar o motor de armazenamento de metadados e arquivos (PostgreSQL + MinIO/S3).
  - *Público*: Backend e Fullstack (Java, Python, Node).
- **`tech-02` - Configuração e Execução do Frontend do Portal Web**:
  - *Objetivo*: Rodar a aplicação Angular do portal localmente, configurando o proxy de homologação.
  - *Público*: Frontend e Fullstack (Angular, TypeScript).
- **`tech-03` - Padrões de Mensageria e Event-Driven Architecture**:
  - *Objetivo*: Mapear os eventos publicados no Kafka/RabbitMQ quando documentos sofrem mutações.
  - *Público*: Desenvolvedores Pleno e Sênior.

---

## 3. Como Funciona a Interação com o Agente Tutor

O **Agente Tutor** atua como seu par de programação e mentor durante todo o processo:
- **Entrevista Inicial**: O tutor identifica sua área (`backend`, `frontend`, `fullstack`), sua stack principal (`Java`, `Angular`, `Python`, etc.) e seu nível de experiência.
- **Rounds de Aprendizado**: A cada etapa da missão, você pode tirar dúvidas pontuais ou executar a tarefa prática e avançar.
- **Base de Conhecimento Corporativa (A2A)**: Caso tenha dúvidas sobre regras de negócio corporativas, repositórios ou processos internos, o tutor consulta automaticamente o **Subagente de Conhecimento** via A2A para lhe trazer respostas precisas e referenciadas.
