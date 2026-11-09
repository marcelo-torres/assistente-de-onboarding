"""Avalia a recuperação da base de conhecimento.

Uso: python scripts/avaliar_rag.py

Lê tests/avaliacao/perguntas.yaml e mede, para as perguntas da base:
- hit@3 pela tool (métrica principal): o alvo ou um arquivo aceito aparece entre
  os 3 primeiros trechos E com nota acima do limiar, ou seja, chega ao agente;
- hit@3 bruto: o mesmo, sem o limiar (mostra o que um limiar menor recuperaria);
- hit@3 estrito: só o `alvo` conta, sem os arquivos aceitos.
E, para as perguntas fora da base, os falsos positivos: algum trecho com nota
acima do limiar. No fim, mostra a margem entre os dois grupos.
"""

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
    carregar_env()
    perguntas = yaml.safe_load(ARQUIVO_PERGUNTAS.read_text(encoding="utf-8"))
    dentro = perguntas.get("dentro_da_base") or []
    fora = perguntas.get("fora_da_base") or []
    if not dentro:
        sys.exit(f"Nenhuma pergunta em dentro_da_base ({ARQUIVO_PERGUNTAS}).")

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


def _buscar_bruto(pergunta: str, k: int) -> list[dict]:
    resultados = buscar(pergunta, limiar=None, top_k=k)
    if isinstance(resultados, str):
        sys.exit(resultados)
    if not resultados:
        sys.exit("A coleção está vazia. Rode `python scripts/indexar_base.py`.")
    return resultados


if __name__ == "__main__":
    main()
