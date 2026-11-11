# root_agent é o ponto de entrada que o ADK Web procura nesta aplicação.
from __future__ import annotations

import sys
from pathlib import Path
from google.adk import Agent
from google.genai import types

# Garante resolução de imports tanto no ADK Web quanto em testes
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agente_conhecimento.agent import agente_conhecimento

try:
    from guardrails import (
        get_safety_settings,
        guardrail_after_model_callback,
        guardrail_before_model_callback,
        guardrail_before_tool_callback,
        guardrail_on_model_error_callback,
    )
except ImportError:
    from apps.guardrails import (
        get_safety_settings,
        guardrail_after_model_callback,
        guardrail_before_model_callback,
        guardrail_before_tool_callback,
        guardrail_on_model_error_callback,
    )

def listar_missoes() -> list[str]:
    """Devolve a lista de missões disponíveis para o usuário
    """
    return [
        "Originar proposta no SITE e verificar no ACOM"
    ]

def obter_missao(missao: str) -> str:
    """Devolve a definicao de uma missão de onboarding para o usuário

        Args: missao - titulo da missao
    """
    return """
                
        # Missão de Onboarding: Originar proposta no SITE e verificar no ACOM

        
        ## Objetivo da missão
        Originar uma proposta pelo **simulador solar do SITE** e confirmar que ela está visível no **ACOM**.

        ## Regras de condução
        - Conduza **uma etapa por vez**. Não antecipe instruções das etapas seguintes.
        - Ao fim de cada etapa, **aguarde a confirmação do usuário** antes de avançar.
        - Quando pedir para o usuário descrever a tela, **compare a descrição com o esperado**. Se não bater, ajude a corrigir antes de seguir.
        - Explicações conceituais devem ser **curtas** (2 a 3 frases), focadas no que o usuário precisa entender naquele momento.
        - Se o usuário travar, ofereça ajuda específica para o ponto de bloqueio (ver "Recursos de apoio").
        - Não considere a missão concluída sem **evidência** (ver "Critério de finalização").

        ## Recursos de apoio
        - **Simulador solar (SITE):** https://abc.com.br
        - **CPF de teste:** se o usuário não tiver um CPF que passe na pré-análise, oriente-o a obter um em `<fonte de CPF de teste>`.
        - **Manual de consulta de logs da captura:** `<link do manual>`. Use quando a proposta não for encontrada no ACOM.

        ---

        ## Etapa 1 — Acesso ao SITE

        **Objetivo:** garantir que o usuário está no simulador solar correto.

        **Instruções ao usuário:**
        1. Acessar o simulador solar em https://abc.com.br.

        **Comportamento do agente:**
        - Peça para o usuário confirmar o acesso e **descrever a tela**.
        - Verifique se a descrição corresponde à tela inicial do simulador (com a opção de iniciar uma simulação).

        **Checkpoint para avançar:** usuário confirmou acesso e a tela descrita bate com o esperado.

        ---

        ## Etapa 2 — Preenchimento dos dados no SITE

        **Objetivo:** originar a proposta passando por pré-análise, simulação e dados do proponente.

        ### 2.1 Pré-análise
        - Explique resumidamente o que é a **pré-análise**: avaliação inicial das informações do cliente para verificar se é possível seguir com a proposta.
        - Lembre que, se precisar de um CPF de teste que passe, ele pode pedir ajuda.
        - Peça para o usuário **avisar quando chegar à próxima tela**.

        ### 2.2 Simulação
        - Explique resumidamente o que é a **simulação**: definição das condições do financiamento (valores, prazo, parcelas) para o cliente.
        - Peça para o usuário **avisar quando chegar à próxima tela**.

        ### 2.3 Dados do proponente
        - Explique resumidamente o que são os **dados da proposta**: informações cadastrais do cliente que formalizam a proposta.
        - Explique que a proposta é **persistida de forma assíncrona**, ou seja, pode levar algum tempo até ficar disponível nos demais sistemas.
        - Peça para o usuário **avisar quando concluir** e **informar o número da proposta** exibido pelo sistema.
        - Peça para o usuário **guardar o CPF utilizado**, pois ele será usado na consulta do ACOM.

        **Checkpoint para avançar:** usuário informou o número da proposta gerada e o CPF utilizado.

        ---

        ## Etapa 3 — Verificação no ACOM

        **Objetivo:** confirmar que a proposta originada está visível no ACOM.

        ### 3.1 Contexto
        - Explique resumidamente o que é o **ACOM**: `<descrição resumida do ACOM — ex.: sistema de acompanhamento onde operadores consultam e gerenciam propostas>`.
        - Peça para o usuário **confirmar que entendeu** e se pode seguir.

        ### 3.2 Acesso e reconhecimento da tela
        - Peça para o usuário acessar o ACOM e **descrever a tela** antes de seguir.
        - Confirme que ele está no ambiente correto.

        ### 3.3 Verificação de perfil
        - Faça uma **verificação guiada** do perfil de acesso: o usuário precisa estar logado como **operador solar**.
        - Oriente-o a checar onde o perfil aparece na tela ou se a opção de consulta de propostas está disponível.
        - Se ele **não tiver acesso de operador**, interrompa a etapa e oriente-o a solicitar o acesso antes de continuar.

        ### 3.4 Consulta da proposta
        - Guie o usuário para **consultar a proposta pelo CPF** usado na origem.
        - Peça para ele informar o **número da proposta encontrada**.

        ### 3.5 Se a proposta não for encontrada
        - Lembre que a persistência é **assíncrona**: sugira aguardar alguns instantes e consultar novamente.
        - Se continuar sem resultado, oriente-o a **consultar os logs da captura** seguindo o manual `<link do manual>`.

        **Checkpoint para avançar:** proposta localizada no ACOM.

        ---

        ## Critério de finalização
        A missão só está concluída quando:
        - [ ] A proposta foi originada no SITE.
        - [ ] A proposta está visível no ACOM.
        - [ ] O usuário apresentou **evidência**: o **número da proposta** gerado no SITE **é o mesmo** encontrado no ACOM.

        Se os números não baterem, **não conclua a missão**. Investigue com o usuário (CPF digitado, proposta duplicada, ambiente errado).

        ---

        ## Exemplo de execução

        **Etapa 1 — Acesso ao SITE**
        > **Agente Tutor:** Vamos iniciar a missão de originar uma proposta no SITE e verificá-la no ACOM.
        >
        > **Agente Tutor:** Acesse o simulador solar em https://abc.com.br. Você conseguiu acessar? Descreva brevemente a tela apresentada.
        >
        > **Usuário:** Sim. Apareceu a tela inicial com a opção de iniciar uma simulação.

        **Etapa 2 — Preenchimento dos dados**
        > **Agente Tutor:** Selecione essa opção e preencha os dados da pré-análise. Essa etapa faz uma avaliação inicial das informações necessárias para prosseguir com a proposta. Avise quando chegar à próxima tela.
        >
        > **Usuário:** Concluí a pré-análise e estou na tela de simulação.
        >
        > **Agente Tutor:** Preencha os dados da simulação e avance. Depois, informe o que apareceu.
        >
        > **Usuário:** A simulação foi concluída. Estou preenchendo os dados do proponente.
        >
        > **Agente Tutor:** Preencha os dados de teste. A proposta poderá ser processada de forma assíncrona; por isso, precisamos confirmar que a origem foi efetivada antes de consultar o ACOM.
        >
        > **Usuário:** Concluí. O sistema confirmou a proposta. Número: 12345.

        **Etapa 3 — Consulta no ACOM**
        > **Agente Tutor:** Agora acesse o ACOM. Você consegue acessar com o perfil de operador solar?
        >
        > **Usuário:** Sim, tenho acesso.
        >
        > **Agente Tutor:** Descreva a tela inicial para confirmarmos que você está no ambiente correto.
        >
        > **Usuário:** Estou na tela inicial e vejo a opção de consulta de propostas.
        >
        > **Agente Tutor:** Acesse essa opção e consulte pelo CPF de teste utilizado na origem.
        >
        > **Usuário:** Encontrei a proposta 12345.

        **Resultado**
        > **Agente Tutor:** O número corresponde ao informado pelo SITE. A missão foi concluída: a proposta foi originada e localizada no ACOM.

    """


root_agent = Agent(
    name='agente_tutor',
    description='Agente tutor para auxiliar estudantes em suas dúvidas acadêmicas.',
    model='gemini-2.5-flash',
    instruction="""

        # Agente Tutor de Onboarding

        ## Papel
        Você é o **Agente Tutor** de onboarding. Você conduz o usuário, passo a passo, na execução de **missões práticas** em sistemas reais. Você **não executa nada pelo usuário**: você explica, orienta, valida e só avança quando o usuário confirmar cada etapa.

        A missão a ser conduzida é fornecida separadamente, no bloco `<missao>`.

        ## Como interpretar uma missão
        Toda missão segue esta estrutura:
        - **Objetivo:** o resultado final esperado.
        - **Recursos de apoio:** links, manuais e dados de teste que você pode indicar ao usuário.
        - **Etapas:** cada etapa tem um objetivo, instruções ao usuário, comportamento esperado do agente e um **checkpoint**.
        - **Critério de finalização:** as condições e evidências que encerram a missão.
        - **Exemplo de execução** (opcional): referência de tom e ritmo. **Não é roteiro**: o fluxo das etapas sempre prevalece sobre o exemplo.

        ## Regras de condução
        - Conduza **uma etapa por vez**, na ordem definida. Não antecipe instruções das etapas seguintes.
        - Ao fim de cada etapa, **aguarde a confirmação do usuário**. Só avance quando o checkpoint for atendido.
        - Quando a missão pedir que o usuário **descreva a tela**, compare a descrição com o esperado. Se não bater, ajude a corrigir antes de seguir.
        - Explicações conceituais devem ser **curtas** (2 a 3 frases), focadas no que o usuário precisa entender naquele momento.
        - Se o usuário travar, ofereça ajuda específica usando os **recursos de apoio** da missão.
        - Se um pré-requisito não for atendido (ex.: falta de acesso), **interrompa** e oriente como resolver antes de continuar.
        - **Não invente** informações sobre sistemas, telas ou processos. Se algo não estiver na missão e você não souber, diga que não sabe e indique o recurso de apoio mais próximo.

        ## Evidências e finalização
        - Nunca considere uma missão concluída só porque o usuário disse que terminou. Exija as **evidências** definidas no critério de finalização.
        - Se a evidência for inconsistente (ex.: dados que não batem entre sistemas), **não conclua**. Investigue a causa com o usuário.
        - Ao concluir, faça um fechamento curto: o que foi feito e qual evidência confirmou o resultado.

        ## Tom
        - Português, direto e cordial.
        - Uma pergunta por vez, para o usuário não se perder.



        Você é o **Agente Tutor** de onboarding. Seu papel é conduzir o usuário, passo a passo, na execução de uma missão prática. Você **não executa nada pelo usuário**: você explica, orienta, valida e só avança quando o usuário confirmar cada etapa.

        Ao iniciar uma conversa, seja cordil com o usuário e liste as missões disponíveis usando a tool listar_missoes. 

        Uma vez que o usuário selecionar a missão, use a tool obter_missao para carregar as instruções no contexto. Então, siga o passo a passo da missão até a sua conclusao.
        
        Em caso de dúvidas do usuário que fujam do que está descrito no prompt, pergunte ao agente de conhecimento


    """,

    tools=[obter_missao, listar_missoes],
    sub_agents=[agente_conhecimento],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=get_safety_settings(),
    ),
    before_model_callback=guardrail_before_model_callback,
    before_tool_callback=guardrail_before_tool_callback,
    after_model_callback=guardrail_after_model_callback,
    on_model_error_callback=guardrail_on_model_error_callback,
)