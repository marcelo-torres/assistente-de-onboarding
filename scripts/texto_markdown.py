"""Funções de texto e markdown compartilhadas pelos conversores."""

import re

from bs4 import BeautifulSoup


def normalizar(texto: str) -> str:
    """Colapsa espaços e tira os que sobram antes de pontuação e depois de parênteses."""
    texto = re.sub(r"\s+", " ", texto)
    texto = re.sub(r" ([.,;:!?)\]])", r"\1", texto)
    return re.sub(r"([(\[]) ", r"\1", texto).strip()


def texto_de_html(html: str) -> str:
    """Texto de um trecho de HTML, com tags separadas por espaço (<br>, <b>...)."""
    return normalizar(BeautifulSoup(html, "html.parser").get_text(" "))


def escapar_cerquilha(texto: str) -> str:
    """Texto que começa com "#" (ex.: comentário de código) não é heading."""
    return re.sub(r"^#", r"\\#", texto)


def adicionar(blocos: list[str], bloco: str) -> None:
    if bloco:
        blocos.append(bloco)


def tabela(linhas: list[list[str]]) -> str:
    """Tabela markdown; a primeira linha é o cabeçalho e linhas vazias são ignoradas."""
    linhas = [[celula.replace("|", "\\|") for celula in linha] for linha in linhas]
    linhas = [linha for linha in linhas if any(linha)]
    if not linhas:
        return ""
    largura = max(len(linha) for linha in linhas)
    linhas = [linha + [""] * (largura - len(linha)) for linha in linhas]
    cabecalho, *corpo = linhas
    saida = [cabecalho, ["---"] * largura, *corpo]
    return "\n".join(f"| {' | '.join(linha)} |" for linha in saida)
