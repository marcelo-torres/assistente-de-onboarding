"""Converte os originais da base de conhecimento em markdown revisável.

Uso: python scripts/converter_base.py

Lê `resources/base-conhecimento/` e grava um `.md` por arquivo em
`resources/base-conhecimento-md/`, sobrescrevendo sem proteção (o git recupera
correções manuais). O resultado é revisado à mão antes da indexação.

Conversores: markdown (cópia simples), HTML estático (BeautifulSoup), HTML
com conteúdo em JS (Playwright, ver converter_js.py) e PDF (pypdf, um heading
por slide). A conversão de HTML com JS exige `playwright install chromium`.
"""

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag
from bs4.element import PreformattedString
from pypdf import PdfReader

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "apps"))

from agente_conhecimento.rag.config import PASTA_MARKDOWN as DESTINO  # noqa: E402
from converter_js import PAGINAS_COM_JS, converter_html_com_js  # noqa: E402
from texto_markdown import adicionar, escapar_cerquilha, normalizar, tabela  # noqa: E402

ORIGINAIS = RAIZ / "resources" / "base-conhecimento"

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
        # Alguns headers são só a barra do topo; outros abrem a página ou a
        # seção com o heading dela.
        if not header.find(list(_HEADINGS)):
            header.decompose()

    blocos = [f"# {titulo}"]
    _renderizar(sopa.body or sopa, blocos)
    return "\n\n".join(blocos) + "\n"


def _renderizar(no: Tag, blocos: list[str]) -> None:
    inline: list[str] = []

    def fechar_paragrafo() -> None:
        texto = normalizar("".join(inline))
        if texto:
            blocos.append(escapar_cerquilha(texto))
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
            adicionar(blocos, f"{'#' * nivel} {_texto(filho)}" if _texto(filho) else "")
        elif filho.name in ("ul", "ol"):
            adicionar(blocos, _lista(filho))
        elif filho.name == "table":
            adicionar(blocos, _tabela(filho))
        elif filho.name == "pre":
            codigo = filho.get_text().strip("\n")
            adicionar(blocos, f"```\n{codigo}\n```" if codigo.strip() else "")
        else:
            _renderizar(filho, blocos)
    fechar_paragrafo()


def _lista(lista: Tag) -> str:
    itens = [texto for li in lista.find_all("li", recursive=False) if (texto := _texto(li))]
    if lista.name == "ol":
        return "\n".join(f"{n}. {item}" for n, item in enumerate(itens, 1))
    return "\n".join(f"- {item}" for item in itens)


def _tabela(elemento: Tag) -> str:
    return tabela([
        [_texto(celula) for celula in tr.find_all(["th", "td"])]
        for tr in elemento.find_all("tr")
    ])


def _texto(no) -> str:
    return normalizar(no.get_text(" ") if isinstance(no, Tag) else str(no))


def converter_paginas_pdf(paginas: list[str]) -> str:
    """Converte o texto das páginas de um deck em markdown, um heading por slide.

    O título de cada slide é a primeira linha com minúsculas; sobretítulos em
    maiúsculas ficam no corpo. O H1 do arquivo é o título do primeiro slide.
    """
    paginas_em_linhas = [_juntar_linhas_quebradas(pagina) for pagina in paginas]
    repetidas = _linhas_repetidas(paginas_em_linhas)

    slides = []
    for numero, linhas in enumerate(paginas_em_linhas, 1):
        linhas = [
            linha for linha in linhas
            if _sem_numeros(linha) not in repetidas and not _numero_de_pagina(linha)
        ]
        # Título: primeira linha com minúsculas que não é sobretítulo espaçado.
        indice_titulo = next(
            (i for i, linha in enumerate(linhas)
             if _tem_minuscula(linha) and not _letras_espacadas(linha)),
            None,
        )
        titulo = linhas[indice_titulo] if indice_titulo is not None else f"Slide {numero}"
        corpo = [
            escapar_cerquilha(_corrigir_letras_espacadas(linha))
            for i, linha in enumerate(linhas) if i != indice_titulo
        ]
        slides.append((numero, titulo, corpo))

    if not slides:
        return ""
    blocos = [f"# {slides[0][1]}"]
    for numero, titulo, corpo in slides:
        blocos.append(f"## Slide {numero}: {titulo}")
        adicionar(blocos, "\n".join(corpo))
    return "\n\n".join(blocos) + "\n"


def _juntar_linhas_quebradas(pagina: str) -> list[str]:
    """O pypdf marca a quebra de linha visual com um espaço no fim da linha.

    Código também sai com espaço no fim, então linhas de código (comentário,
    flag, continuação com barra) e início de bullet ou de linha indentada
    nunca são juntados.
    """
    linhas: list[str] = []
    continua = False
    for linha in pagina.splitlines():
        if continua and linhas and not linha.startswith(("•", "#", "-", " ")):
            linhas[-1] += " " + linha.strip()
        else:
            linhas.append(linha.strip())
        atual = linhas[-1] if linhas else ""
        continua = (
            linha.endswith(" ")
            and not atual.startswith(("#", "-"))
            and not atual.endswith("\\")
        )
    return [linha for linha in linhas if linha]


def _sem_numeros(linha: str) -> str:
    return re.sub(r"\d+", "", linha).strip()


def _linhas_repetidas(paginas: list[list[str]]) -> set[str]:
    """Cabeçalhos e rodapés: mesmo texto (sem números) em mais da metade das páginas.

    Com menos de 3 páginas não dá para distinguir rodapé de conteúdo.
    """
    if len(paginas) < 3:
        return set()
    contagem: dict[str, int] = {}
    for linhas in paginas:
        for chave in {_sem_numeros(linha) for linha in linhas}:
            contagem[chave] = contagem.get(chave, 0) + 1
    return {chave for chave, n in contagem.items() if chave and n > len(paginas) / 2}


def _numero_de_pagina(linha: str) -> bool:
    return re.fullmatch(r"\d{1,2}", linha) is not None


def _tem_minuscula(texto: str) -> bool:
    return any(c.islower() for c in texto)


def _corrigir_letras_espacadas(linha: str) -> str:
    """'A T O  1  ·  A  I D E I A' -> 'Ato 1 · A ideia'.

    Títulos de slide com espaçamento entre letras saem do PDF com um espaço
    entre letras e dois entre palavras.
    """
    if not _letras_espacadas(linha):
        return linha
    palavras = [p.replace(" ", "") for p in re.split(r"\s{2,}", linha)]
    frase = re.sub(r"\s*—\s*", " — ", " ".join(palavras))
    segmentos = frase.split(" · ")
    return " · ".join(_capitalizar_frase(segmento) for segmento in segmentos)


def _letras_espacadas(linha: str) -> bool:
    tokens = linha.split()
    return len(tokens) >= 4 and sum(len(t) == 1 for t in tokens) >= 0.8 * len(tokens)


# Siglas que aparecem nos sobretítulos espaçados dos decks; o resto vira minúscula.
_SIGLAS = {"ADK": "ADK", "BV": "BV", "NEMO": "NeMo"}


def _capitalizar_frase(texto: str) -> str:
    """'ATO 1 · A IDEIA NO ADK' -> 'Ato 1 · A ideia no ADK'."""
    palavras = [_SIGLAS.get(palavra, palavra.lower()) for palavra in texto.split(" ")]
    if palavras and palavras[0] not in _SIGLAS.values():
        palavras[0] = palavras[0].capitalize()
    return " ".join(palavras)


def converter_html(arquivo: Path) -> str:
    if arquivo.name in PAGINAS_COM_JS:
        return converter_html_com_js(arquivo, converter_html_estatico)
    return converter_html_estatico(arquivo.read_text(encoding="utf-8"))


def converter_pdf(arquivo: Path) -> str:
    return converter_paginas_pdf([pagina.extract_text() for pagina in PdfReader(arquivo).pages])


CONVERSORES = {
    ".md": converter_markdown,
    ".html": converter_html,
    ".pdf": converter_pdf,
}


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    for arquivo in sorted(ORIGINAIS.iterdir()):
        conversor = CONVERSORES.get(arquivo.suffix.lower())
        if conversor is None:
            print(f"Ignorado (tipo ainda não suportado): {arquivo.name}")
            continue
        markdown = conversor(arquivo)
        destino = DESTINO / f"{arquivo.stem}.md"
        destino.write_text(markdown, encoding="utf-8")
        print(f"Convertido: {arquivo.name} -> {destino.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
