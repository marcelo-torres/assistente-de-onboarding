from converter_base import converter_html_estatico


def test_descarta_navegacao_e_usa_o_title_como_unico_h1():
    html = """
    <html><head><title>Guia de Embeddings</title><style>.x{}</style></head>
    <body>
      <header><span>Logo</span> Menu</header>
      <aside id="sidebar"><nav><a href="#a">Capítulo 1</a></nav></aside>
      <main>
        <h1>O que é um embedding?</h1>
        <p>Um embedding   é um vetor
           de números.</p>
        <h2>Similaridade</h2>
        <h3>Cosseno</h3>
        <div>Mede o ângulo <b>entre</b> vetores.</div>
        <button>Tentar</button>
        <script>const x = 1;</script>
      </main>
      <footer>© 2026</footer>
    </body></html>
    """

    assert converter_html_estatico(html) == (
        "# Guia de Embeddings\n\n"
        "## O que é um embedding?\n\n"
        "Um embedding é um vetor de números.\n\n"
        "## Similaridade\n\n"
        "### Cosseno\n\n"
        "Mede o ângulo entre vetores.\n"
    )


def test_listas_tabelas_e_codigo_viram_markdown():
    html = """
    <html><head><title>Vector Stores</title></head><body>
      <ul><li>HNSW: <b>grafo</b> navegável</li><li>IVF</li></ul>
      <table>
        <thead><tr><th>Índice</th><th>Recall</th></tr></thead>
        <tbody><tr><td>HNSW</td><td>alto | rápido</td></tr></tbody>
      </table>
      <pre><code>col.query(
    n_results=5)</code></pre>
    </body></html>
    """

    assert converter_html_estatico(html) == (
        "# Vector Stores\n\n"
        "- HNSW: grafo navegável\n- IVF\n\n"
        "| Índice | Recall |\n| --- | --- |\n| HNSW | alto \\| rápido |\n\n"
        "```\ncol.query(\n    n_results=5)\n```\n"
    )


def test_header_com_o_h1_da_pagina_e_mantido():
    html = """
    <html><head><title>Aula 4</title></head><body>
      <header><h1>Anatomia do Vector Search</h1><p>Cinco peças do console.</p></header>
      <table></table>
    </body></html>
    """

    assert converter_html_estatico(html) == (
        "# Aula 4\n\n## Anatomia do Vector Search\n\nCinco peças do console.\n"
    )


def test_paragrafo_que_comeca_com_cerquilha_nao_vira_heading():
    html = "<html><head><title>BM25</title></head><body><p># Por que BM25?</p></body></html>"

    assert converter_html_estatico(html) == "# BM25\n\n\\# Por que BM25?\n"


def test_link_que_envolve_blocos_e_renderizado_como_blocos():
    html = """<html><head><title>Biblioteca</title></head><body>
      <a href="setup.html"><h4>Setup Guide</h4><div>setup.html</div></a>
    </body></html>"""

    assert converter_html_estatico(html) == "# Biblioteca\n\n#### Setup Guide\n\nsetup.html\n"


def test_texto_inline_mantem_paragrafo_e_separa_tags_irmas():
    html = """<html><head><title>T</title></head><body>
      <p>Veja <cite>o guia</cite> de <time>hoje</time>, ou <span>linha<br>nova</span>.</p>
      <div><span>Capítulo 1</span><span>O problema</span></div>
    </body></html>"""

    assert converter_html_estatico(html) == (
        "# T\n\nVeja o guia de hoje, ou linha nova.\n\nCapítulo 1 O problema\n"
    )


def test_sem_title_o_primeiro_h1_vira_o_titulo_sem_se_repetir():
    html = "<!DOCTYPE html><html><head><title> </title></head><body><h1>Guia</h1><p>Oi.</p></body></html>"

    assert converter_html_estatico(html) == "# Guia\n\nOi.\n"


def test_lista_numerada_ignora_itens_vazios_sem_pular_numero():
    html = "<html><head><title>T</title></head><body><ol><li>a</li><li> </li><li>c</li></ol></body></html>"

    assert converter_html_estatico(html) == "# T\n\n1. a\n2. c\n"


def test_header_com_heading_de_secao_e_mantido():
    html = """<html><head><title>T</title></head><body>
      <section><header><h2>O Paradoxo do Agente</h2><p>Intro da seção.</p></header><p>Corpo.</p></section>
    </body></html>"""

    assert converter_html_estatico(html) == (
        "# T\n\n## O Paradoxo do Agente\n\nIntro da seção.\n\nCorpo.\n"
    )
