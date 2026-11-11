"""Avalia a recuperação da base de conhecimento.

Uso:
  python scripts/avaliar_rag.py            busca com a pergunta crua do usuário
  python scripts/avaliar_rag.py --agente   roda o agente real em cada pergunta

Modo padrão (busca direta):

Lê tests/avaliacao/perguntas.yaml e mede, para as perguntas da base:
- hit@3 pela tool (métrica principal): o alvo ou um arquivo aceito aparece entre
  os 3 primeiros trechos E com nota acima do limiar, ou seja, chega ao agente;
- hit@3 bruto: o mesmo, sem o limiar (mostra o que um limiar menor recuperaria);
- hit@3 estrito: só o `alvo` conta, sem os arquivos aceitos.
E, para as perguntas fora da base, os falsos positivos: algum trecho com nota
acima do limiar. No fim, mostra a margem entre os dois grupos.

Modo --agente: em produção, quem chama a busca é o agente, com a consulta que
ele mesmo reescreve (às vezes mais de uma). Este modo mede o que chega de fato:
- dentro da base: o arquivo certo veio no top-3 de alguma chamada da tool? A
  resposta final disse "não encontrei"?
- fora da base: alguma chamada da tool devolveu trechos? A resposta final disse
  "não encontrei", como deveria?
O LLM não é determinístico: rodadas diferentes podem variar em uma ou duas perguntas.
"""

import argparse
import asyncio
import re
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "apps"))

from agente_conhecimento.rag.busca import buscar  # noqa: E402
from agente_conhecimento.rag.config import LIMIAR_SIMILARIDADE  # noqa: E402
from ambiente import carregar_env  # noqa: E402

ARQUIVO_PERGUNTAS = RAIZ / "tests" / "avaliacao" / "perguntas.yaml"
K = 3


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--agente", action="store_true", help="roda o agente real em cada pergunta")
    args = parser.parse_args()

    carregar_env()
    perguntas = yaml.safe_load(ARQUIVO_PERGUNTAS.read_text(encoding="utf-8"))
    dentro = perguntas.get("dentro_da_base") or []
    fora = perguntas.get("fora_da_base") or []
    if not dentro:
        sys.exit(f"Nenhuma pergunta em dentro_da_base ({ARQUIVO_PERGUNTAS}).")

    if args.agente:
        asyncio.run(avaliar_agente(dentro, fora))
    else:
        avaliar_busca(dentro, fora)


def avaliar_busca(dentro: list[dict], fora: list[dict]) -> None:
    print(f"Limiar atual: {LIMIAR_SIMILARIDADE}\n")
    print("== Dentro da base (hit@3) ==")
    pela_tool = brutos = estritos = 0
    notas_que_chegam = []
    for item in dentro:
        esperados = {item["alvo"], *item.get("aceitos", [])}
        resultados = _buscar_bruto(item["pergunta"], K)
        acerto = next((r for r in resultados if r["fonte"] in esperados), None)
        chega = acerto is not None and acerto["score"] >= LIMIAR_SIMILARIDADE
        brutos += acerto is not None
        pela_tool += chega
        estritos += any(r["fonte"] == item["alvo"] for r in resultados)
        if chega:
            notas_que_chegam.append(acerto["score"])

        marca = "OK  " if chega else ("ABAIXO DO LIMIAR" if acerto else "ERRO")
        nota = f"{acerto['score']:.3f}" if acerto else "  -  "
        print(f"{marca} {nota}  {item['pergunta']}")
        if not chega:
            for r in resultados:
                print(f"           {r['score']:.3f} {r['fonte']} | {r['secao'][:60]}")

    print("\n== Fora da base (falsos positivos) ==")
    notas_fora = []
    for item in fora:
        resultados = _buscar_bruto(item["pergunta"], 1)
        melhor = resultados[0]
        notas_fora.append(melhor["score"])
        marca = "FALSO POSITIVO" if melhor["score"] >= LIMIAR_SIMILARIDADE else "ok            "
        print(f"{marca} {melhor['score']:.3f}  {item['pergunta']}")
        print(f"               melhor trecho: {melhor['fonte']} | {melhor['secao'][:60]}")

    total = len(dentro)
    falsos = sum(nota >= LIMIAR_SIMILARIDADE for nota in notas_fora)
    print("\n== Resumo ==")
    print(f"hit@3 pela tool (acima do limiar): {pela_tool}/{total} = {pela_tool / total:.0%}")
    print(f"hit@3 bruto (sem limiar):          {brutos}/{total} = {brutos / total:.0%}")
    print(f"hit@3 estrito (só o alvo):         {estritos}/{total} = {estritos / total:.0%}")
    print(f"falsos positivos:                  {falsos}/{len(notas_fora)}")
    if notas_que_chegam and notas_fora:
        print(
            f"margem: acerto mais fraco que chega ao agente {min(notas_que_chegam):.3f}, "
            f"maior nota fora da base {max(notas_fora):.3f}"
        )


_NAO_ENCONTREI = re.compile(r"não encontrei", re.IGNORECASE)


async def avaliar_agente(dentro: list[dict], fora: list[dict]) -> None:
    from google.adk.runners import InMemoryRunner

    from agente_conhecimento.agent import agente_conhecimento

    runner = InMemoryRunner(agent=agente_conhecimento, app_name="avaliacao")

    print("== Dentro da base, via agente ==")
    acertos = recusas_indevidas = 0
    for item in dentro:
        esperados = {item["alvo"], *item.get("aceitos", [])}
        chamadas, resposta = await _perguntar_ao_agente(runner, item["pergunta"])
        acerto = any(
            isinstance(trechos, list) and any(t["fonte"] in esperados for t in trechos[:K])
            for _, trechos in chamadas
        )
        recusou = bool(_NAO_ENCONTREI.search(resposta))
        acertos += acerto
        recusas_indevidas += recusou
        marca = "OK  " if acerto else "ERRO"
        print(f"{marca}{' (respondeu não encontrei)' if recusou else ''}  {item['pergunta']}")
        _imprimir_chamadas(chamadas)

    print("\n== Fora da base, via agente ==")
    com_trechos = respostas_certas = 0
    for item in fora:
        chamadas, resposta = await _perguntar_ao_agente(runner, item["pergunta"])
        trouxe = any(isinstance(trechos, list) and trechos for _, trechos in chamadas)
        recusou = bool(_NAO_ENCONTREI.search(resposta))
        com_trechos += trouxe
        respostas_certas += recusou
        marca = "ok " if recusou else "RESPONDEU"
        print(f"{marca}{' (a busca trouxe trechos)' if trouxe else ''}  {item['pergunta']}")
        _imprimir_chamadas(chamadas)
        if not recusou:
            print(f"      resposta: {resposta[:200]}")

    total = len(dentro)
    print("\n== Resumo (via agente) ==")
    print(f"hit@3 em alguma chamada da tool:    {acertos}/{total} = {acertos / total:.0%}")
    print(f"respondeu 'não encontrei' na base: {recusas_indevidas}/{total}")
    print(f"fora da base, busca trouxe trechos: {com_trechos}/{len(fora)}")
    print(f"fora da base, disse 'não encontrei': {respostas_certas}/{len(fora)}")


# Cada pergunta faz várias chamadas ao modelo; em sequência rápida, a cota do
# Vertex devolve 429 RESOURCE_EXHAUSTED. Pausa entre perguntas e novas tentativas.
_PAUSA_ENTRE_PERGUNTAS = 5
_ESPERAS_APOS_429 = (30, 60, 120)


async def _perguntar_ao_agente(runner, pergunta: str) -> tuple[list[tuple[str, object]], str]:
    """Roda uma pergunta numa sessão nova; devolve [(consulta, resultado da tool)] e a resposta."""
    await asyncio.sleep(_PAUSA_ENTRE_PERGUNTAS)
    for espera in (*_ESPERAS_APOS_429, None):
        try:
            return await _rodar_sessao(runner, pergunta)
        except Exception as erro:  # o ADK embrulha o 429 em exceções diferentes
            if espera is None or "RESOURCE_EXHAUSTED" not in str(erro):
                raise
            print(f"      (cota do modelo esgotada; nova tentativa em {espera}s)")
            await asyncio.sleep(espera)


async def _rodar_sessao(runner, pergunta: str) -> tuple[list[tuple[str, object]], str]:
    from google.genai import types

    sessao = await runner.session_service.create_session(app_name="avaliacao", user_id="avaliacao")
    mensagem = types.Content(role="user", parts=[types.Part(text=pergunta)])
    consultas, resultados, textos = [], [], []
    async for evento in runner.run_async(
        user_id="avaliacao", session_id=sessao.id, new_message=mensagem
    ):
        for parte in (evento.content.parts if evento.content else None) or []:
            if parte.function_call:
                consultas.append(parte.function_call.args.get("pergunta", ""))
            if parte.function_response:
                resultados.append(parte.function_response.response.get("result"))
            if parte.text:
                textos.append(parte.text)
    return list(zip(consultas, resultados)), "".join(textos)


def _imprimir_chamadas(chamadas: list[tuple[str, object]]) -> None:
    for consulta, trechos in chamadas:
        resumo = (
            ", ".join(f"{t['fonte'].removesuffix('.md')[:30]}:{t['score']:.2f}" for t in trechos[:K])
            if isinstance(trechos, list) else str(trechos)[:60]
        )
        print(f"      consulta: {consulta!r} -> [{resumo or 'vazio'}]")


def _buscar_bruto(pergunta: str, k: int) -> list[dict]:
    resultados = buscar(pergunta, limiar=None, top_k=k)
    if isinstance(resultados, str):
        sys.exit(resultados)
    if not resultados:
        sys.exit("A coleção está vazia. Rode `python scripts/indexar_base.py`.")
    return resultados


if __name__ == "__main__":
    main()
