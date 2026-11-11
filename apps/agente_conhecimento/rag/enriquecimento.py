"""Enriquecimento opcional dos trechos com perguntas geradas por LLM.

Problema: a pergunta do usuário e o texto da base às vezes usam vocabulários
diferentes ("documento muito longo" x "RAPTOR, sumarização hierárquica"), e a
busca vetorial não os aproxima. Aqui, um LLM escreve, para cada trecho,
perguntas que ele responde no vocabulário de quem pergunta. As perguntas são
embedadas junto com o trecho; o texto guardado e entregue ao agente não muda.

Cuidados com tokens:
- desligado por padrão (ENRIQUECER_COM_PERGUNTAS em config.py ou --enriquecer);
- cache em JSON pela hash do texto do trecho: só trechos novos ou alterados
  chamam o LLM, e o cache pode ser versionado para não pagar de novo;
- vários trechos por chamada, e o cache é salvo depois de cada lote;
- `scripts/indexar_base.py --estimar` mostra o custo sem chamar API nenhuma.
"""

import hashlib
import json
import time
from collections.abc import Callable
from pathlib import Path

from .config import MODELO_PERGUNTAS, PERGUNTAS_POR_TRECHO

GerarPerguntas = Callable[[list[str]], list[list[str]]]

_ROTULO = "Perguntas que este trecho responde:"


def texto_para_embedding(texto: str, perguntas: list[str]) -> str:
    """Texto que vai para o embedding: o trecho seguido das perguntas que ele responde."""
    if not perguntas:
        return texto
    return f"{texto}\n\n{_ROTULO}\n" + "\n".join(f"- {pergunta}" for pergunta in perguntas)


class CachePerguntas:
    """Perguntas já geradas, por hash do texto do trecho, persistidas em JSON."""

    def __init__(self, arquivo: Path):
        self.arquivo = arquivo
        self._dados: dict[str, list[str]] = (
            json.loads(arquivo.read_text(encoding="utf-8")) if arquivo.exists() else {}
        )

    def get(self, texto: str) -> list[str] | None:
        return self._dados.get(_chave(texto))

    def guardar(self, texto: str, perguntas: list[str]) -> None:
        self._dados[_chave(texto)] = perguntas

    def salvar(self) -> None:
        self.arquivo.parent.mkdir(parents=True, exist_ok=True)
        conteudo = json.dumps(self._dados, ensure_ascii=False, indent=1, sort_keys=True)
        self.arquivo.write_text(conteudo + "\n", encoding="utf-8")


def faltando_no_cache(textos: list[str], cache: CachePerguntas) -> list[str]:
    """Textos distintos, na ordem, que ainda não têm perguntas no cache."""
    return [t for t in dict.fromkeys(textos) if cache.get(t) is None]


def perguntas_para(
    textos: list[str], cache: CachePerguntas, gerar: GerarPerguntas, tamanho_lote: int
) -> list[list[str]]:
    """Perguntas de cada texto: do cache quando houver; senão, geradas em lotes."""
    faltando = faltando_no_cache(textos, cache)
    for inicio in range(0, len(faltando), tamanho_lote):
        lote = faltando[inicio : inicio + tamanho_lote]
        for texto, perguntas in zip(lote, gerar(lote), strict=True):
            cache.guardar(texto, perguntas)
        # Salva a cada lote: uma falha no meio não desperdiça o que já foi pago.
        cache.salvar()
    return [cache.get(texto) for texto in textos]


def _chave(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


# --- Geração com o Gemini (não usada pelos testes) ---

_INSTRUCAO = """Você recebe trechos numerados de um material didático sobre agentes de IA e RAG.
Para cada trecho, escreva {n} perguntas em português que um desenvolvedor recém-chegado
faria e que o trecho responde. Use o vocabulário do dia a dia de quem ainda não conhece
os termos técnicos do trecho: descreva o problema ou a situação, em vez de repetir o
título. Responda só com um array JSON com um array de perguntas por trecho, na mesma
ordem e na mesma quantidade dos trechos."""

_ESPERAS_APOS_429 = (30, 60, 120)


def gerar_perguntas_gemini(textos: list[str]) -> list[list[str]]:
    """Perguntas para um lote de trechos pelo Gemini, dividindo o lote se a resposta vier inválida."""
    return dividir_se_invalida(_gerar_lote_gemini, textos)


def dividir_se_invalida(gerar: GerarPerguntas, textos: list[str]) -> list[list[str]]:
    """Chama `gerar` no lote; se a resposta for inválida, tenta cada metade do lote.

    Lotes grandes às vezes voltam com uma lista a mais ou a menos (o modelo junta ou
    separa trechos). Dividir resolve sem desperdiçar o lote inteiro: no pior caso,
    cada trecho vira uma chamada. Com um trecho só, o erro sobe.
    """
    try:
        return gerar(textos)
    except ValueError as erro:
        if len(textos) == 1:
            raise
        meio = len(textos) // 2
        print(f"  (resposta inválida para {len(textos)} trechos, dividindo o lote: {str(erro)[:80]})")
        return dividir_se_invalida(gerar, textos[:meio]) + dividir_se_invalida(gerar, textos[meio:])


def _gerar_lote_gemini(textos: list[str]) -> list[list[str]]:
    """Uma chamada ao Gemini para um lote de trechos; tenta de novo após 429."""
    from google.genai import types

    from .embeddings import _cliente_genai

    trechos = "\n\n".join(f"### Trecho {n}\n{texto}" for n, texto in enumerate(textos, 1))
    config = types.GenerateContentConfig(
        system_instruction=_INSTRUCAO.format(n=PERGUNTAS_POR_TRECHO),
        response_mime_type="application/json",
        # A quantidade de listas é fixada no schema: uma por trecho do lote.
        response_schema=types.Schema(
            type=types.Type.ARRAY,
            min_items=len(textos),
            max_items=len(textos),
            items=types.Schema(type=types.Type.ARRAY, items=types.Schema(type=types.Type.STRING)),
        ),
        temperature=0.2,
        # Sem raciocínio interno: tokens de "thinking" são cobrados e não ajudam aqui.
        thinking_config=types.ThinkingConfig(thinking_budget=0),
    )
    for espera in (*_ESPERAS_APOS_429, None):
        try:
            resposta = _cliente_genai().models.generate_content(
                model=MODELO_PERGUNTAS, contents=trechos, config=config
            )
            return interpretar_resposta(resposta.text, len(textos))
        except Exception as erro:
            if espera is None or "RESOURCE_EXHAUSTED" not in str(erro):
                raise
            print(f"  (cota do modelo esgotada; nova tentativa em {espera}s)")
            time.sleep(espera)
    raise AssertionError("inalcançável")


def interpretar_resposta(texto_json: str, quantidade: int) -> list[list[str]]:
    """Valida o JSON do modelo: uma lista de perguntas por trecho, na quantidade pedida."""
    dados = json.loads(texto_json)
    if not isinstance(dados, list) or len(dados) != quantidade:
        raise ValueError(f"Esperava {quantidade} listas de perguntas, recebi: {texto_json[:200]}")
    return [
        [p.strip() for p in perguntas if isinstance(p, str) and p.strip()][:PERGUNTAS_POR_TRECHO]
        for perguntas in dados
    ]
