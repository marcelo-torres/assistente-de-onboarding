"""Converte os originais da base de conhecimento em markdown revisável.

Uso: python scripts/converter_base.py

Lê `resources/base-conhecimento/` e grava um `.md` por arquivo em
`resources/base-conhecimento-md/`, sobrescrevendo sem proteção (o git recupera
correções manuais). O resultado é revisado à mão antes da indexação.

Conversores: markdown (cópia simples) e HTML estático (BeautifulSoup). PDF e
HTML com conteúdo em JS entram nas tarefas seguintes e, até lá, são ignorados.
"""

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from bs4.element import PreformattedString

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "apps"))

from agente_conhecimento.rag.config import PASTA_MARKDOWN as DESTINO  # noqa: E402

ORIGINAIS = RAIZ / "resources" / "base-conhecimento"

# Estes HTMLs guardam o conteúdo em objetos JavaScript: um parser comum só vê
# a casca da página. Ficam para o conversor com Playwright (tarefa 04).
HTML_COM_CONTEUDO_EM_JS = {
    "rag__agentic-retrieval-e-memoria.html",
    "rag__masterclass-rag-e-memoria.html",
    "rag__rag-avancado-e-agentes.html",
    "memoria-agentes__the-memory-arquitetura-stateful.html",
    "fundamentos-agentes__ecossistema-adk-e-economia-de-tokens.html",
}

# Navegação, rodapé e elementos interativos não são conteúdo.
_DESCARTAR = [
    "script", "style", "noscript", "nav", "aside", "footer",
    "button", "input", "label", "select", "textarea", "canvas", "svg",
]
_HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
# Tags de bloco quebram parágrafo; qualquer outra tag é texto inline. Um inline
# que envolve um bloco (ex.: <a> com <h4> e <div>) também é tratado como bloco.
_BLOCOS = [
    *_HEADINGS, "html", "body", "main", "header", "section", "article", "div", "p",
    "blockquote", "figure", "figcaption", "details", "summary", "form",
    "ul", "ol", "li", "dl", "dt", "dd", "table", "pre",
]


def converter_markdown(arquivo: Path) -> str:
    return arquivo.read_text(encoding="utf-8")


def converter_html_estatico(html: str) -> str:
    """Converte um HTML estático em markdown com um único H1.

    O H1 vem do <title> (ou do primeiro <h1>). Os <h1> e <h2> do corpo viram
    H2, e os demais headings mantêm o nível, então o título é o único H1.
    """
    sopa = BeautifulSoup(html, "html.parser")
    titulo = _texto(sopa.title) if sopa.title else ""
    if not titulo and (primeiro_h1 := sopa.find("h1")):
        titulo = _texto(primeiro_h1)
        primeiro_h1.decompose()

    for tag in sopa.find_all(_DESCARTAR):
        tag.decompose()
    for header in sopa.find_all("header"):
        # Alguns headers são só a barra do topo; outros trazem o H1 da página.
        if not header.find("h1"):
            header.decompose()

    blocos = [f"# {titulo}"]
    _renderizar(sopa.body or sopa, blocos)
    return "\n\n".join(blocos) + "\n"


def _renderizar(no: Tag, blocos: list[str]) -> None:
    inline: list[str] = []

    def fechar_paragrafo() -> None:
        texto = _normalizar("".join(inline))
        if texto:
            # Texto que começa com "#" (ex.: comentário de código) não é heading.
            blocos.append(re.sub(r"^#", r"\\#", texto))
        inline.clear()

    for filho in no.children:
        if isinstance(filho, PreformattedString):
            continue  # comentário, doctype, CDATA
        if isinstance(filho, NavigableString):
            inline.append(str(filho))
            continue
        if filho.name not in _BLOCOS and not filho.find(_BLOCOS):
            # Espaços em volta: nestes HTMLs, tags inline irmãs vêm coladas
            # (<span>Capítulo 1</span><span>O problema</span>).
            inline.append(f" {filho.get_text(' ')} ")
            continue
        fechar_paragrafo()
        if filho.name in _HEADINGS:
            nivel = max(2, int(filho.name[1]))
            _adicionar(blocos, f"{'#' * nivel} {_texto(filho)}" if _texto(filho) else "")
        elif filho.name in ("ul", "ol"):
            _adicionar(blocos, _lista(filho))
        elif filho.name == "table":
            _adicionar(blocos, _tabela(filho))
        elif filho.name == "pre":
            codigo = filho.get_text().strip("\n")
            _adicionar(blocos, f"```\n{codigo}\n```" if codigo.strip() else "")
        else:
            _renderizar(filho, blocos)
    fechar_paragrafo()


def _adicionar(blocos: list[str], bloco: str) -> None:
    if bloco:
        blocos.append(bloco)


def _lista(lista: Tag) -> str:
    itens = [texto for li in lista.find_all("li", recursive=False) if (texto := _texto(li))]
    if lista.name == "ol":
        return "\n".join(f"{n}. {item}" for n, item in enumerate(itens, 1))
    return "\n".join(f"- {item}" for item in itens)


def _tabela(tabela: Tag) -> str:
    linhas = [
        [_texto(celula).replace("|", "\\|") for celula in tr.find_all(["th", "td"])]
        for tr in tabela.find_all("tr")
    ]
    linhas = [linha for linha in linhas if any(linha)]
    if not linhas:
        return ""
    largura = max(len(linha) for linha in linhas)
    linhas = [linha + [""] * (largura - len(linha)) for linha in linhas]
    cabecalho, *corpo = linhas
    saida = [cabecalho, ["---"] * largura, *corpo]
    return "\n".join(f"| {' | '.join(linha)} |" for linha in saida)


def _texto(no) -> str:
    return _normalizar(no.get_text(" ") if isinstance(no, Tag) else str(no))


def _normalizar(texto: str) -> str:
    texto = re.sub(r"\s+", " ", texto)
    # Os espaços em volta de tags inline não podem ficar antes de pontuação.
    texto = re.sub(r" ([.,;:!?)\]])", r"\1", texto)
    return re.sub(r"([(\[]) ", r"\1", texto).strip()


def converter_html(arquivo: Path) -> str | None:
    if arquivo.name in HTML_COM_CONTEUDO_EM_JS:
        return None
    return converter_html_estatico(arquivo.read_text(encoding="utf-8"))


CONVERSORES = {
    ".md": converter_markdown,
    ".html": converter_html,
}


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    for arquivo in sorted(ORIGINAIS.iterdir()):
        conversor = CONVERSORES.get(arquivo.suffix.lower())
        if conversor is None:
            print(f"Ignorado (tipo ainda não suportado): {arquivo.name}")
            continue
        markdown = conversor(arquivo)
        if markdown is None:
            print(f"Ignorado (conteúdo em JS, tarefa 04): {arquivo.name}")
            continue
        destino = DESTINO / f"{arquivo.stem}.md"
        destino.write_text(markdown, encoding="utf-8")
        print(f"Convertido: {arquivo.name} -> {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
