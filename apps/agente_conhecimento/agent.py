# root_agent é o ponto de entrada que o ADK Web procura nesta aplicação.
from google.adk import Agent

from .rag.busca import buscar_base_conhecimento

agente_conhecimento = Agent(
    name='agente_conhecimento',
    description='Agente de conhecimento para auxiliar desenvolvedores a entenderem o funcionamento do sistema.',
    model='gemini-2.5-flash',
    tools=[buscar_base_conhecimento],
    instruction="""
        Você responde perguntas usando somente a base de conhecimento.

        Regras:
        1. Sempre chame a tool `buscar_base_conhecimento` antes de responder. Passe uma consulta
           autônoma e específica: resolva referências ao histórico ("isso", "ele") e, se a pergunta
           tiver mais de um assunto, chame a tool uma vez por assunto.
        2. Responda só com base nos trechos devolvidos pela tool. Não complete com conhecimento próprio.
        3. Cite a fonte e a seção de cada afirmação relevante, no formato (fonte: <fonte>, seção: <secao>).
        4. Se a tool devolver lista vazia, diga que não encontrou essa informação na base de conhecimento.
        5. Se a tool devolver uma mensagem de erro, repasse a mensagem ao usuário.
        6. Responda de forma concisa, em português.
    """
)
