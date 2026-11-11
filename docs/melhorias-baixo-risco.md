# Melhorias de baixo risco nos agentes

Data: 2026-11-11 · Branch: `melhorias-baixo-risco`

Ajustes nos dois agentes e no repositório, levantados na análise do projeto para a apresentação. Nenhum deles muda o RAG: chunking, embeddings, limiar, top-k e o prompt do `agente_conhecimento` continuam iguais, então a avaliação em [`estrategia-de-chunking.md`](estrategia-de-chunking.md) segue válida.

## Resumo

| # | Melhoria | Arquivo | Problema anterior |
| --- | --- | --- | --- |
| 1 | `description` do tutor | `apps/agente_tutor/agent.py` | Dizia "auxiliar estudantes em suas dúvidas acadêmicas", o que não combina com o projeto |
| 2 | `description` do agente de conhecimento | `apps/agente_conhecimento/agent.py` | Genérica ("funcionamento do sistema"); não dizia o que há na base |
| 3 | Prompt do tutor num arquivo só | `resources/prompt-tutor.md`, `apps/agente_tutor/agent.py` | Prompt colado no código, com o papel duplicado, um erro de digitação e referência a um bloco `<missao>` inexistente |
| 4 | Agente de conhecimento devolve a conversa ao tutor | `apps/agente_conhecimento/agent.py` | A mensagem seguinte do usuário ia para o especialista, não para o tutor |
| 5 | `session.db` fora do git | `apps/agente_tutor/.adk/session.db` | Conversas locais versionadas, apesar de `.adk` já estar no `.gitignore` |
| 6 | `.DS_Store` ignorado | `.gitignore` | Arquivo do macOS aparecia como não rastreado |
| 7 | README atualizado | `README.md` | Só comandos de Windows; apresentava o A2A como já integrado |
| 8 | Testes das tools do tutor | `tests/test_tutor_tools.py` | `listar_missoes` e `obter_missao` não tinham testes |

## Detalhes

### 1 e 2. Descrições dos agentes

No ADK, a `description` de um agente é lida pelo agente pai para decidir a delegação (`transfer_to_agent`). Uma descrição que lista os temas da base (ADK, RAG, embeddings, chunking, vector stores, busca híbrida, guardrails, memória, economia de tokens) ajuda o tutor a reconhecer quando uma dúvida deve ir para o especialista.

### 3. Prompt único do tutor

O `agent.py` agora lê `resources/prompt-tutor.md`, do mesmo jeito que as missões são lidas de `resources/missoes/`. Ajustar o comportamento do tutor passa a ser editar um Markdown, sem tocar no código.

Mudanças no conteúdo:

- Saiu a referência ao bloco `<missao>`: a missão chega pela tool `obter_missao`.
- Entrou a seção **Início da conversa**: cumprimentar, listar com `listar_missoes` e carregar a escolhida com `obter_missao`.
- Entrou a seção **Dúvidas fora da missão**: transferir dúvidas conceituais ao `agente_conhecimento` e, depois, retomar a missão na etapa em que o usuário estava.
- Saíram a duplicação do papel e o erro "cordil".

Cuidado: o ADK trata `{nome}` na instrução como variável de estado da sessão. O prompt não pode ter chaves, e há um teste que garante isso.

### 4. Volta da conversa ao tutor

**Causa.** Para escolher quem responde a próxima mensagem, o ADK (`google/adk/agents/_agent_router.py`) usa o último agente que respondeu, desde que ele possa transferir para o pai. Por padrão, o subagente pode. Então, depois de responder uma dúvida, o `agente_conhecimento` recebia também a mensagem seguinte, mesmo que fosse sobre a missão. Ele só voltava ao tutor se o LLM decidisse chamar `transfer_to_agent`.

**Correção.** `disallow_transfer_to_parent=True` no `agente_conhecimento`. Ele responde e encerra a vez, e o roteador volta ao agente raiz, o tutor. O agente rodando sozinho, como no `scripts/avaliar_rag.py --agente`, não é afetado: lá ele não tem pai.

**Antes e depois**, na mesma conversa pelo ADK Web ("O que é RAG?" e, em seguida, "Entendi, obrigado. Podemos seguir?"):

| Mensagem | Antes | Depois |
| --- | --- | --- |
| "O que é RAG?" | tutor transfere; conhecimento busca e responde com fonte | igual |
| "Podemos seguir?" | **conhecimento** recebe e chama `transfer_to_agent` para voltar ao tutor | **tutor** recebe direto e continua a Etapa 1 |

Ganho: uma chamada ao modelo a menos por dúvida, e a volta à missão deixa de depender de uma decisão do LLM.

Efeito colateral: se o usuário fizer uma segunda pergunta conceitual seguida, ela passa pelo tutor, que delega de novo.

### 5 e 6. Repositório

- `git rm --cached apps/agente_tutor/.adk/session.db`: o arquivo sai do git e continua no disco de quem já o tem.
- `.DS_Store` entrou no `.gitignore`.

### 7. README

- Descreve os dois agentes como estão hoje: o de conhecimento é subagente do tutor (`sub_agents`), no mesmo processo. O A2A aparece como arquitetura futura.
- Comandos de ambiente para macOS/Linux e Windows, passo de credenciais (`.exemplo.env`), `pytest` e `adk web`.

### 8. Testes

`tests/test_tutor_tools.py`, 9 testes, sem chamar APIs:

- `listar_missoes` devolve só `.md`, em ordem.
- `obter_missao` aceita o nome com ou sem extensão e devolve mensagem para missão inexistente.
- `obter_missao` não lê arquivos fora de `resources/missoes` nem de outro tipo: `../segredo.md`, `../segredo`, `/etc/passwd`, `rascunho.txt`.
- O prompt do tutor vem do arquivo e não tem chaves.
- O agente de conhecimento é subagente do tutor e tem `disallow_transfer_to_parent` ligado.

## Verificação

- `pytest`: 37 testes passando (28 anteriores e 9 novos).
- Conversa real pelo ADK Web (tabela do item 4): o tutor lista as missões, carrega a escolhida, delega a dúvida, o especialista cita a fonte e a mensagem seguinte volta ao tutor.

## Pontos observados, não tratados aqui

- **Tutor anuncia as tools.** Na conversa de verificação, o tutor passou a escrever "Estou carregando a missão… aguarde" antes de chamar a tool. Pode ser variação do modelo ou efeito do prompt reorganizado. Se incomodar, uma regra no prompt ("chame as tools sem anunciar") resolve.
- **App `agente_conhecimento` no ADK Web.** Ele aparece na lista de apps, mas não define `root_agent` (o comentário na primeira linha de `agent.py` diz o contrário). Provavelmente falha se for escolhido direto na interface. Não foi testado.
- **Modelo fixo em dois lugares.** `gemini-2.5-flash` está repetido nos dois agentes; uma constante comum evitaria que eles ficassem diferentes.
- **Poucas perguntas negativas na avaliação.** O limiar de 0,70 tem margem de 0,009, medida com só 3 perguntas fora da base. Ampliar `tests/avaliacao/perguntas.yaml` daria mais confiança ao número.
