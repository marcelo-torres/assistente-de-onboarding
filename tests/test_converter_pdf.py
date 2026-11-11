from converter_base import converter_paginas_pdf


def test_um_heading_por_slide_com_letras_espacadas_corrigidas():
    paginas = [
        "A U L Ã O  B V\nGuardrails para Agentes de IA\nA Descida da Serra",
        "A T O  1  ·  A  I D E I A  Q U E  U M A  C R I A N Ç A  E N T E N D E\n"
        "Você ensina a criança\nENSINAR = PROMPT\nSystem instruction.",
    ]

    assert converter_paginas_pdf(paginas) == (
        "# Guardrails para Agentes de IA\n\n"
        "## Slide 1: Guardrails para Agentes de IA\n\n"
        "Aulão BV\nA Descida da Serra\n\n"
        "## Slide 2: Você ensina a criança\n\n"
        "Ato 1 · A ideia que uma criança entende\nENSINAR = PROMPT\nSystem instruction.\n"
    )


def test_remove_cabecalho_rodape_e_numeros_e_junta_linhas_quebradas():
    paginas = [
        "Deck RAG 1\nA Memória do Agente\nRodapé · Turma 1",
        "Deck RAG 2\n1\nO agente que esquecia \ntudo\nUm cliente negocia \nfinanciamento.\n2Rodapé · Turma",
        "Deck RAG 3\nAgenda\nRodapé · Turma 3",
    ]

    assert converter_paginas_pdf(paginas) == (
        "# A Memória do Agente\n\n"
        "## Slide 1: A Memória do Agente\n\n"
        "## Slide 2: O agente que esquecia tudo\n\n"
        "Um cliente negocia financiamento.\n\n"
        "## Slide 3: Agenda\n"
    )


def test_comentario_de_codigo_no_slide_nao_vira_heading():
    paginas = ["Input rail determinístico\n# src/guardrails/input_rail.py\ndef guard(): ..."]

    assert converter_paginas_pdf(paginas) == (
        "# Input rail determinístico\n\n"
        "## Slide 1: Input rail determinístico\n\n"
        "\\# src/guardrails/input_rail.py\ndef guard(): ...\n"
    )


def test_sobretitulo_espacado_vira_frase_mantendo_so_siglas_conhecidas():
    paginas = [
        "A T O  1  ·  O N D E  —  A S  S E T E  F A M Í L I A S  D E  R I S C O  N O  A D K\nRiscos"
    ]

    assert converter_paginas_pdf(paginas).endswith(
        "## Slide 1: Riscos\n\nAto 1 · Onde — as sete famílias de risco no ADK\n"
    )


def test_deck_curto_nao_perde_linhas_parecidas_nem_anos():
    paginas = ["Agenda\nPasso 1\n2024", "Agenda\nPasso 2\n7"]

    assert converter_paginas_pdf(paginas) == (
        "# Agenda\n\n## Slide 1: Agenda\n\nPasso 1\n2024\n\n## Slide 2: Agenda\n\nPasso 2\n"
    )


def test_codigo_nao_e_juntado_mas_bullet_quebrado_e():
    paginas = [
        "Comando\n• Um índice criado e \nconsultável\n# .env: PROJETO, \n"
        "#  REGIAO \npython -m src.indexing \\ \n  --push \nCom backend vertex."
    ]

    assert converter_paginas_pdf(paginas).endswith(
        "• Um índice criado e consultável\n\\# .env: PROJETO,\n\\#  REGIAO\n"
        "python -m src.indexing \\\n--push\nCom backend vertex.\n"
    )
