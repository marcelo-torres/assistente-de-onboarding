"""Conversão dos HTMLs cujo conteúdo está em JavaScript.

Por que um parser comum falha nestes arquivos: o HTML entregue é só a casca
(menu, cabeçalho, um <div> vazio). O conteúdo de verdade mora num objeto JS
(ex.: `const MODULES = [...]`) ou em templates dentro de funções `render*`,
e só vira HTML quando o navegador executa o script. O BeautifulSoup lê o
arquivo sem executar nada, então enxerga de 137 a 747 caracteres de texto.

Por isso o Playwright abre a página num Chromium headless e:
- lê a variável de dados com `page.evaluate` e a transforma em markdown;
- avalia a função de template de cada seção e converte o HTML gerado; ou
- chama `router(rota)` para cada rota da página e converte o HTML renderizado.
"""

import html
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from playwright.sync_api import Page, sync_playwright

from texto_markdown import adicionar, tabela, texto_de_html

ConverterHtml = Callable[[str], str]


@dataclass(frozen=True)
class Variavel:
    """O conteúdo está numa variável global com os dados da página."""

    nome: str

    def extrair(self, pagina: Page, arquivo: Path, converter_html: ConverterHtml) -> str:
        dados = pagina.evaluate(f"JSON.parse(JSON.stringify({self.nome}))")
        return dados_para_markdown(pagina.title(), dados)


@dataclass(frozen=True)
class Template:
    """Uma expressão JS devolve o HTML de cada seção: dados + texto fixo do template."""

    expressao: str

    def extrair(self, pagina: Page, arquivo: Path, converter_html: ConverterHtml) -> str:
        return converter_html(_documento(pagina.title(), pagina.evaluate(self.expressao)))


@dataclass(frozen=True)
class Rotas:
    """O conteúdo é renderizado por `router(rota)` num contêiner; modais por `openModal`."""

    conteiner: str
    modais: tuple[str, ...] = ()

    def extrair(self, pagina: Page, arquivo: Path, converter_html: ConverterHtml) -> str:
        secoes = []
        for rota in _rotas(arquivo.read_text(encoding="utf-8")):
            pagina.evaluate("rota => router(rota)", rota)
            secoes.append(pagina.inner_html(self.conteiner))
        for modal in self.modais:
            pagina.evaluate("modal => openModal(modal)", modal)
            secoes.append(pagina.inner_html(f"#modal-{modal}"))
        return converter_html(_documento(pagina.title(), secoes))


# Mapeamento feito lendo o script de cada página.
PAGINAS_COM_JS = {
    "rag__agentic-retrieval-e-memoria.html": Variavel("MODULES"),
    "rag__masterclass-rag-e-memoria.html": Template(
        "courseData.modules.map(modulo => buildSectionHTML(modulo))"
    ),
    "rag__rag-avancado-e-agentes.html": Rotas("#app-content"),
    "memoria-agentes__the-memory-arquitetura-stateful.html": Rotas("#content-area"),
    "fundamentos-agentes__ecossistema-adk-e-economia-de-tokens.html": Rotas(
        "#main-content", modais=("setup", "vertexai")
    ),
}

# Chaves de apresentação (cor, layout, identificador), não conteúdo.
_IGNORAR = {"id", "kind", "cols", "icon", "color", "lang", "levelColor", "tone"}
_CORES = {
    "slate", "gray", "rose", "red", "amber", "yellow", "emerald", "green", "blue",
    "indigo", "violet", "purple", "pink", "orange", "teal", "cyan", "sky", "lime",
}
# Até este nível (###) um objeto com título vira heading; abaixo, item de lista.
_NIVEL_MAXIMO_HEADING = 3
# Acima disto (em caracteres) um texto é parágrafo, não item de lista.
_TEXTO_LONGO = 200


def converter_html_com_js(arquivo: Path, converter_html: ConverterHtml) -> str:
    """Abre a página no Chromium headless e extrai o conteúdo pela estratégia mapeada."""
    with sync_playwright() as playwright:
        navegador = playwright.chromium.launch()
        try:
            pagina = navegador.new_page()
            pagina.goto(arquivo.resolve().as_uri(), wait_until="load")
            return PAGINAS_COM_JS[arquivo.name].extrair(pagina, arquivo, converter_html)
        finally:
            navegador.close()


def _documento(titulo: str, secoes: list[str]) -> str:
    corpo = "".join(f"<section>{secao}</section>" for secao in secoes)
    return f"<html><head><title>{html.escape(titulo)}</title></head><body>{corpo}</body></html>"


def _rotas(html_da_pagina: str) -> list[str]:
    """Rotas chamadas pelo menu (router('x') ou router("x/y")), na ordem do menu."""
    return list(dict.fromkeys(re.findall(r"router\(['\"]([\w/-]+)['\"]\)", html_da_pagina)))


def dados_para_markdown(titulo: str, dados) -> str:
    """Converte o objeto de dados de uma página em markdown.

    Objetos com título viram headings nos dois primeiros níveis (módulo e
    bloco); objetos mais fundos viram itens de lista. Listas de strings viram
    bullets e o HTML dentro das strings é removido.
    """
    blocos = [f"# {titulo}"]
    _renderizar(dados, 2, blocos)
    return "\n\n".join(blocos) + "\n"


def _renderizar(valor, nivel: int, blocos: list[str]) -> None:
    if isinstance(valor, str):
        if texto := _limpar(valor):
            blocos.append(texto)
    elif isinstance(valor, list):
        if _so_textos(valor) and any(len(_limpar(item)) > _TEXTO_LONGO for item in valor):
            # Lista de textos longos é uma sequência de parágrafos, não bullets.
            for item in valor:
                _renderizar(item, nivel, blocos)
        elif nivel > _NIVEL_MAXIMO_HEADING or _so_textos(valor):
            adicionar(blocos, "\n".join(filter(None, map(_item_de_lista, valor))))
        else:
            for item in valor:
                _renderizar(item, nivel, blocos)
    elif isinstance(valor, dict):
        if nivel > _NIVEL_MAXIMO_HEADING:
            adicionar(blocos, _item_de_lista(valor))
        else:
            _renderizar_objeto(valor, nivel, blocos)


def _renderizar_objeto(objeto: dict, nivel: int, blocos: list[str]) -> None:
    titulo = _titulo(objeto)
    campos = _campos(objeto)
    if titulo:
        blocos.append(f"{'#' * nivel} {_limpar(titulo)}")
        nivel += 1
    if isinstance(campos.get("headers"), list) and isinstance(campos.get("rows"), list):
        linhas = [campos.pop("headers"), *campos.pop("rows")]
        blocos.append(tabela([[_limpar(str(celula)) for celula in linha] for linha in linhas]))
    if isinstance(campos.get("code"), str):
        blocos.append(f"```\n{campos.pop('code').strip(chr(10))}\n```")
    for valor in campos.values():
        _renderizar(valor, nivel, blocos)


def _item_de_lista(valor) -> str:
    """Um objeto fundo vira "- **título**: demais textos"; uma string, "- texto"."""
    if isinstance(valor, dict):
        titulo = _titulo(valor)
        textos = " — ".join(_textos(list(_campos(valor).values())))
        if titulo:
            return f"- **{_limpar(titulo)}**: {textos}" if textos else f"- **{_limpar(titulo)}**"
        return f"- {textos}" if textos else ""
    textos = " — ".join(_textos(valor))
    return f"- {textos}" if textos else ""


def _textos(valor) -> list[str]:
    """Todos os textos de um valor, achatados, na ordem em que aparecem."""
    if isinstance(valor, dict):
        valor = list(_campos(valor).values()) if not _titulo(valor) else [_titulo(valor), *_campos(valor).values()]
    if isinstance(valor, list):
        return [texto for item in valor for texto in _textos(item)]
    if isinstance(valor, (int, float)) and not isinstance(valor, bool):
        return [str(valor)]
    if isinstance(valor, str) and (texto := _limpar(valor)):
        return [texto]
    return []


_CHAVES_DE_TITULO = ("title", "q")


def _chave_do_titulo(objeto: dict) -> str | None:
    return next((c for c in _CHAVES_DE_TITULO if isinstance(objeto.get(c), str) and objeto[c]), None)


def _titulo(objeto: dict) -> str | None:
    chave = _chave_do_titulo(objeto)
    return objeto[chave] if chave else None


def _campos(objeto: dict) -> dict:
    """Campos de conteúdo: sem título e sem chaves de apresentação."""
    chave_do_titulo = _chave_do_titulo(objeto)
    return {
        chave: valor for chave, valor in objeto.items()
        if chave != chave_do_titulo and chave not in _IGNORAR
        and not chave.lower().endswith("accent") and not _cor(valor)
    }


def _so_textos(valor: list) -> bool:
    return bool(valor) and all(isinstance(item, str) for item in valor)


def _cor(valor) -> bool:
    return isinstance(valor, str) and valor in _CORES


def _limpar(texto: str) -> str:
    return texto_de_html(texto)
