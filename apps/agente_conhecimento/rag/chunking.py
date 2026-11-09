"""Corte hierárquico do markdown em trechos, por heading."""

import re
from collections.abc import Callable, Iterator
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
    """Corta o markdown em trechos pela hierarquia de headings.

    O título é o primeiro H1; a seção é o caminho de headings abaixo dele
    (ex.: "Solicitação > Aprovação"). Uma seção que cabe inteira no limite,
    junto com as subseções, vira um trecho só (subseções minúsculas sozinhas
    geram embeddings fracos). Senão, o corpo dela vira um trecho e cada
    subseção é avaliada do mesmo jeito. O texto começa com o cabeçalho
    contextual "titulo > secao" e tem no máximo `tamanho_maximo` caracteres:
    corpos maiores são subdivididos por parágrafo, sem overlap.
    """
    titulo = _titulo(markdown, fonte)
    tema = fonte.split("__", 1)[0] if "__" in fonte else ""

    def cabe(secao: str, corpo: str) -> bool:
        return len(_cabecalho(titulo, secao)) + 2 + len(corpo) <= tamanho_maximo

    trechos = []
    for secao, corpo in _agrupar(_secoes(markdown, titulo), cabe):
        cabecalho = _cabecalho(titulo, secao)
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


@dataclass(frozen=True)
class _Secao:
    nivel: int
    nome: str
    caminho: str
    corpo: str


# A introdução (texto antes do primeiro heading) não tem subseções.
_NIVEL_INTRODUCAO = 7


def _cabecalho(titulo: str, secao: str) -> str:
    return f"{titulo} > {secao}" if secao else titulo


def _secoes(markdown: str, titulo: str) -> list[_Secao]:
    """Todas as seções em ordem, inclusive as sem corpo (podem ter subseções)."""
    secoes: list[_Secao] = []
    caminho: list[tuple[int, str]] = []
    linhas: list[str] = []
    titulo_visto = False

    def fechar_secao():
        corpo = "\n".join(linhas).strip()
        if caminho:
            nivel, nome = caminho[-1]
            secoes.append(_Secao(nivel, nome, " > ".join(n for _, n in caminho), corpo))
        elif corpo:
            secoes.append(_Secao(_NIVEL_INTRODUCAO, "", "", corpo))
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


def _agrupar(secoes: list[_Secao], cabe: Callable[[str, str], bool]) -> list[tuple[str, str]]:
    """(caminho, corpo) dos trechos: seção + subseções juntas quando cabem."""
    grupos = []
    i = 0
    while i < len(secoes):
        secao = secoes[i]
        fim = i + 1
        while fim < len(secoes) and secoes[fim].nivel > secao.nivel:
            fim += 1
        if fim > i + 1:
            partes = [secao.corpo] + [
                f"{'#' * sub.nivel} {sub.nome}" + (f"\n\n{sub.corpo}" if sub.corpo else "")
                for sub in secoes[i + 1 : fim]
            ]
            corpo = "\n\n".join(parte for parte in partes if parte)
            if cabe(secao.caminho, corpo):
                grupos.append((secao.caminho, corpo))
                i = fim
                continue
        if secao.corpo:
            grupos.append((secao.caminho, secao.corpo))
        i += 1
    return grupos
