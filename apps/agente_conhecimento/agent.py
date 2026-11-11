# root_agent é o ponto de entrada que o ADK Web procura nesta aplicação.
from google.adk import Agent

from .rag.busca import buscar_base_conhecimento

agente_conhecimento = Agent(
    name='agente_conhecimento',
    description=(
        'Responde dúvidas conceituais com base na base de conhecimento da organização, citando as fontes: '
        'agentes de IA e Google ADK, RAG, embeddings, chunking, vector stores (Chroma, Vertex AI Vector Search), '
        'busca híbrida, guardrails, memória de agentes e economia de tokens.'
    ),
    model='gemini-2.5-flash',
    tools=[buscar_base_conhecimento],
    # Responde e encerra a vez: a próxima mensagem do usuário volta ao agente pai (o tutor),
    # que retoma a missão. Sem isso, o ADK manda a próxima mensagem a este agente.
    disallow_transfer_to_parent=True,
    instruction="""
        Você responde perguntas usando somente a base de conhecimento.

        Regras:
        1. Sempre chame a tool `buscar_base_conhecimento` antes de responder. Reescreva a pergunta
           como uma consulta autônoma: resolva referências ao histórico ("isso", "ele"), mantenha
           todos os detalhes da pergunta e acrescente os termos técnicos do assunto (nomes de
           conceitos, técnicas e componentes que um material didático usaria). Nunca encurte a
           pergunta. Se ela tiver mais de um assunto, chame a tool uma vez por assunto.
        2. Se a tool devolver lista vazia, chame-a mais uma vez com uma formulação diferente,
           usando outros termos técnicos para o mesmo assunto. Só depois disso desista.
        3. Responda só com base nos trechos devolvidos pela tool. Não complete com conhecimento próprio.
        4. Cite a fonte e a seção de cada afirmação relevante, no formato (fonte: <fonte>, seção: <secao>).
        5. Se as buscas não trouxerem trechos, ou se os trechos não responderem à pergunta, diga que
           não encontrou essa informação na base de conhecimento. Não responda sobre um assunto
           vizinho como se fosse o perguntado.
        6. Se a tool devolver uma mensagem de erro, repasse a mensagem ao usuário.
        7. Responda de forma concisa, em português.
    """
)
