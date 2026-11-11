from agente_conhecimento.rag.chunking import cortar_em_trechos

MARKDOWN = """# Guia de acessos

Introdução ao guia.

## Solicitação

Abra um chamado no portal.

### Aprovação

O gestor aprova em até dois dias.
"""


def test_cada_secao_vira_um_trecho_com_caminho_de_headings_e_metadados():
    # Limite em que "Solicitação" e "Aprovação" juntas não cabem num trecho só.
    trechos = cortar_em_trechos(MARKDOWN, fonte="acessos__guia.md", tamanho_maximo=90)

    assert [t.secao for t in trechos] == ["", "Solicitação", "Solicitação > Aprovação"]
    aprovacao = trechos[2]
    assert aprovacao.texto == "Guia de acessos > Solicitação > Aprovação\n\nO gestor aprova em até dois dias."
    assert aprovacao.metadados() == {
        "fonte": "acessos__guia.md",
        "tema": "acessos",
        "titulo": "Guia de acessos",
        "secao": "Solicitação > Aprovação",
        "indice_chunk": 2,
    }
    assert aprovacao.id == "acessos__guia.md::2"
    assert trechos[0].texto == "Guia de acessos\n\nIntrodução ao guia."


def test_secao_maior_que_o_limite_e_subdividida_por_paragrafo_sem_overlap():
    paragrafos = [f"Parágrafo {n}: " + "x" * 60 for n in range(1, 6)]
    markdown = "# Manual\n\n## Longa\n\n" + "\n\n".join(paragrafos) + "\n\n## Curta\n\nFim.\n"

    trechos = cortar_em_trechos(markdown, fonte="manual.md", tamanho_maximo=200)

    longos = [t for t in trechos if t.secao == "Longa"]
    assert len(longos) == 3
    assert all(len(t.texto) <= 200 for t in trechos)
    assert all(t.texto.startswith("Manual > Longa\n\n") for t in longos)
    corpos = [t.texto.removeprefix("Manual > Longa\n\n") for t in longos]
    assert "\n\n".join(corpos) == "\n\n".join(paragrafos)
    assert [t.indice_chunk for t in trechos] == [0, 1, 2, 3]
    assert trechos[3].secao == "Curta"


def test_cerquilha_dentro_de_bloco_de_codigo_nao_abre_secao():
    markdown = "# Manual\n\n## Exemplo\n\n```python\n# comentario\nx = 1\n```\n\n## Fim\n\nTchau.\n"

    trechos = cortar_em_trechos(markdown, fonte="manual.md")

    assert [t.secao for t in trechos] == ["Exemplo", "Fim"]
    assert "# comentario" in trechos[0].texto


def test_secao_com_subsecoes_que_cabem_no_limite_vira_um_trecho_so():
    markdown = (
        "# Agentes\n\nIntro.\n\n"
        "## Níveis\n\nDa simplicidade à complexidade.\n\n"
        "### Básico\n\nPrompt e resposta.\n\n"
        "#### Exemplo\n\nChatbot de FAQ.\n\n"
        "### Avançado\n\nMemória e ferramentas.\n\n"
        "## Custos\n\nTokens custam.\n"
    )

    trechos = cortar_em_trechos(markdown, fonte="agentes.md")

    assert [t.secao for t in trechos] == ["", "Níveis", "Custos"]
    assert trechos[1].texto == (
        "Agentes > Níveis\n\nDa simplicidade à complexidade.\n\n"
        "### Básico\n\nPrompt e resposta.\n\n#### Exemplo\n\nChatbot de FAQ.\n\n"
        "### Avançado\n\nMemória e ferramentas."
    )


def test_secao_que_nao_cabe_mantem_subsecoes_separadas():
    markdown = "# Doc\n\n## Grande\n\n" + "x" * 150 + "\n\n### Filha\n\n" + "y" * 100 + "\n"

    trechos = cortar_em_trechos(markdown, fonte="doc.md", tamanho_maximo=200)

    assert [t.secao for t in trechos] == ["Grande", "Grande > Filha"]
