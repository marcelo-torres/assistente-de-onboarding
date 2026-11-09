"""Corte hierárquico do markdown em trechos, por heading."""

import re
from collections.abc import Iterator
from dataclasses import dataclass

from .config import TAMANHO_MAXIMO_TRECHO

_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


@dataclass(frozen=True)
class Trecho:
    texto: str
    fonte: str
    tema: str
    titulo: str
    secao: str
    indice_chunk: int

    @property
    def id(self) -> str:
        return f"{self.fonte}::{self.indice_chunk}"

    def metadados(self) -> dict:
        return {
            "fonte": self.fonte,
            "tema": self.tema,
            "titulo": self.titulo,
            "secao": self.secao,
            "indice_chunk": self.indice_chunk,
        }


def cortar_em_trechos(
    markdown: str, fonte: str, tamanho_maximo: int = TAMANHO_MAXIMO_TRECHO
) -> list[Trecho]:
    """Corta o markdown em um trecho por seção.

    O título é o primeiro H1; a seção é o caminho de headings abaixo dele
    (ex.: "Solicitação > Aprovação"). O texto de cada trecho começa com o
    cabeçalho contextual "titulo > secao" e tem no máximo `tamanho_maximo`
    caracteres: seções maiores são subdivididas por parágrafo, sem overlap.
    """
    titulo = _titulo(markdown, fonte)
    tema = fonte.split("__", 1)[0] if "__" in fonte else ""

    secoes = _secoes(markdown, titulo)
    trechos = []
    for secao, corpo in secoes:
        cabecalho = f"{titulo} > {secao}" if secao else titulo
        espaco_para_corpo = tamanho_maximo - len(cabecalho) - 2
        if espaco_para_corpo <= 0:
            raise ValueError(f"Cabeçalho maior que o limite do trecho em {fonte}: {cabecalho!r}")
        for pedaco in _subdividir(corpo, espaco_para_corpo):
            trechos.append(
                Trecho(
                    texto=f"{cabecalho}\n\n{pedaco}",
                    fonte=fonte,
                    tema=tema,
                    titulo=titulo,
                    secao=secao,
                    indice_chunk=len(trechos),
                )
            )
    return trechos


def _subdividir(corpo: str, limite: int) -> list[str]:
    """Agrupa parágrafos inteiros em pedaços de até `limite` caracteres."""
    pedacos: list[str] = []
    atual = ""
    for paragrafo in re.split(r"\n\s*\n", corpo):
        for parte in _quebrar_paragrafo(paragrafo.strip(), limite):
            candidato = f"{atual}\n\n{parte}" if atual else parte
            if len(candidato) <= limite:
                atual = candidato
            else:
                pedacos.append(atual)
                atual = parte
    if atual:
        pedacos.append(atual)
    return pedacos


def _quebrar_paragrafo(paragrafo: str, limite: int) -> list[str]:
    """Último recurso para um parágrafo maior que o limite: corta no último espaço."""
    partes = []
    while len(paragrafo) > limite:
        corte = paragrafo.rfind(" ", 0, limite + 1)
        if corte <= 0:
            corte = limite
        partes.append(paragrafo[:corte].rstrip())
        paragrafo = paragrafo[corte:].lstrip()
    if paragrafo:
        partes.append(paragrafo)
    return partes


def _linhas(markdown: str) -> Iterator[tuple[str, re.Match | None]]:
    """Cada linha com seu casamento de heading; dentro de ``` nunca há heading."""
    em_codigo = False
    for linha in markdown.splitlines():
        if linha.lstrip().startswith("```"):
            em_codigo = not em_codigo
        yield linha, None if em_codigo else _HEADING.match(linha)


def _titulo(markdown: str, fonte: str) -> str:
    for _, casamento in _linhas(markdown):
        if casamento and len(casamento.group(1)) == 1:
            return casamento.group(2)
    return fonte.removesuffix(".md")


def _secoes(markdown: str, titulo: str) -> list[tuple[str, str]]:
    """Devolve (caminho da seção, corpo) para cada seção com conteúdo."""
    secoes = []
    caminho: list[tuple[int, str]] = []
    linhas: list[str] = []
    titulo_visto = False

    def fechar_secao():
        corpo = "\n".join(linhas).strip()
        if corpo:
            secoes.append((" > ".join(nome for _, nome in caminho), corpo))
        linhas.clear()

    for linha, casamento in _linhas(markdown):
        if not casamento:
            linhas.append(linha)
            continue
        fechar_secao()
        nivel, nome = len(casamento.group(1)), casamento.group(2)
        if nivel == 1 and nome == titulo and not titulo_visto:
            # O H1 do documento é o título, não entra no caminho da seção.
            titulo_visto = True
            caminho.clear()
            continue
        caminho = [(n, h) for n, h in caminho if n < nivel]
        caminho.append((nivel, nome))
    fechar_secao()
    return secoes
