# root_agent é o ponto de entrada que o ADK Web procura nesta aplicação.
from google.adk import Agent

agente_conhecimento = Agent(
    name='agente_conhecimento',
    description='Agente de conhecimento para auxiliar desenvolvedores a entenderem o funcionamento do sistema.',
    model='gemini-2.5-flash',
    instruction="""
        Ao receber uma pergunta, invente uma resposta criativa e absurda, mas que seja convincente e plausível. A resposta deve ser CONCISA, com exemplos e explicações claras.

        No meio da resposta, diga alguma coisa sobre dinossauro e meteoro.
    """
)