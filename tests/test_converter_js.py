from converter_js import dados_para_markdown


def test_modulos_e_blocos_com_titulo_viram_headings():
    dados = [
        {
            "id": "prologo",
            "title": "O agente amnésico",
            "subtitle": "Por que o modelo <b>esquece</b>?",
            "keywords": ["motivação", "alucinação"],
            "blocks": [
                {"kind": "lead", "text": "Um LLM é um compressor."},
                {"kind": "callout", "tone": "danger", "title": "A armadilha", "text": "Contexto longo custa."},
            ],
        }
    ]

    assert dados_para_markdown("Masterclass", dados) == (
        "# Masterclass\n\n"
        "## O agente amnésico\n\n"
        "Por que o modelo esquece?\n\n"
        "- motivação\n- alucinação\n\n"
        "Um LLM é um compressor.\n\n"
        "### A armadilha\n\n"
        "Contexto longo custa.\n"
    )


def test_objetos_fundos_viram_lista_e_tabela_e_codigo_sao_preservados():
    dados = [
        {
            "title": "Busca",
            "blocks": [
                {"kind": "cards", "title": "Limites", "items": [
                    {"title": "Congelamento", "accent": "rose", "desc": "O peso foi fixado.", "bullets": ["Retreinar é caro"]},
                    {"q": "Top-k maior resolve?", "a": ["Quase sempre piora."]},
                ]},
                {"kind": "table", "title": "Comparativo", "headers": ["Abordagem", "Custo"],
                 "rows": [["RAG", "baixo | médio"]], "note": "Valores ilustrativos."},
                {"kind": "code", "title": "ingestao.py", "lang": "python", "code": "def ingest():\n    return 1"},
            ],
        }
    ]

    assert dados_para_markdown("T", dados) == (
        "# T\n\n## Busca\n\n"
        "### Limites\n\n"
        "- **Congelamento**: O peso foi fixado. — Retreinar é caro\n"
        "- **Top-k maior resolve?**: Quase sempre piora.\n\n"
        "### Comparativo\n\n"
        "| Abordagem | Custo |\n| --- | --- |\n| RAG | baixo \\| médio |\n\n"
        "Valores ilustrativos.\n\n"
        "### ingestao.py\n\n"
        "```\ndef ingest():\n    return 1\n```\n"
    )


def test_lista_de_textos_longos_vira_paragrafos():
    longo = "Marcos abre o app e conversa com a Íris. " * 6
    dados = [{"title": "História", "paragraphs": [longo, "Curto, mas da mesma lista."]}]

    assert dados_para_markdown("T", dados) == (
        f"# T\n\n## História\n\n{longo.strip()}\n\nCurto, mas da mesma lista.\n"
    )


def test_html_dentro_dos_textos_nao_cola_palavras():
    dados = [{"title": "Notas", "text": "Linha um<br>linha dois com <b>negrito</b>."}]

    assert dados_para_markdown("T", dados) == (
        "# T\n\n## Notas\n\nLinha um linha dois com negrito.\n"
    )
