# 01: RAG ponta a ponta com o arquivo markdown

**What to build:** o `agente_conhecimento` passa a responder perguntas com base na base de conhecimento, citando fonte e seção, usando por enquanto só o arquivo `rag__estrategias-de-chunking` (que já é markdown e não precisa de conversão). É o tracer bullet: cobre conversão (cópia simples), chunking, embedding, indexação no Chroma, tool de busca e prompt novo. As tarefas seguintes só acrescentam tipos de arquivo.

Decisões do plano (`docs/plano-rag-base-conhecimento.md`) que valem aqui:

- Chunking hierárquico por heading, medido em caracteres (1.200 a 3.200), seções grandes subdivididas por parágrafo, sem overlap.
- Cada trecho começa com o cabeçalho contextual `titulo > secao`; é esse texto que vai para o embedding.
- Metadados: `fonte`, `tema` (prefixo antes de `__`), `titulo`, `secao`, `indice_chunk`.
- Embedding `gemini-embedding-001`, dimensão padrão, `RETRIEVAL_DOCUMENT` na indexação e `RETRIEVAL_QUERY` na busca, reaproveitando a credencial do ADK.
- Chroma persistente fora do git, coleção `base_conhecimento`, distância de cosseno.
- Idempotência: por arquivo, apaga tudo da `fonte` e reinsere com ID `fonte::indice_chunk` (nunca `hash()` do Python). Trechos de arquivos removidos da pasta também são apagados.
- Tool `buscar_base_conhecimento(pergunta)` sem parâmetro de tema; devolve até `top_k` (5) itens `{texto, fonte, secao, score}` acima do limiar, com `score = 1 - distância`; lista vazia quando nada passa; mensagem de erro em texto (sem exceção) quando o índice não existe. Cliente do Chroma aberto uma vez, de forma lazy.
- Prompt novo: sempre chama a tool, responde só com base nos trechos, cita fonte e seção, diz "não encontrei" com lista vazia e não completa com conhecimento próprio, respostas concisas em português. O prompt atual (respostas inventadas, dinossauro) é removido. A `description` do agente não muda.
- `top_k` e limiar ficam na configuração do RAG; o limiar é provisório até a tarefa 05.

**Blocked by:** None (can start immediately)

**Status:** done

- [x] O markdown de `rag__estrategias-de-chunking` está na pasta de markdown revisado e é indexado pelo script de indexação
- [x] Rodar o script de indexação duas vezes imprime a mesma contagem de trechos
- [x] Remover um `.md` da pasta e reindexar apaga os trechos daquela fonte
- [x] Um teste `pytest` cobre o chunking: corte por heading, limite de tamanho e metadados
- [x] Sem índice criado, a tool devolve mensagem clara pedindo para rodar a indexação
- [x] No `adk web`, "o que é chunking pai-filho?" volta com resposta citando fonte e seção corretas
- [x] No `adk web`, uma pergunta fora da base volta com "não encontrei"
- [x] `requirements.txt` inclui `chromadb` e `pytest`; o diretório do índice está no `.gitignore`; o README documenta o passo de indexação antes do `adk web`
