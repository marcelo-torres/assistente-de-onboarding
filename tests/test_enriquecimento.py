"""Enriquecimento dos trechos com perguntas geradas. Nenhum teste chama o Gemini."""

from agente_conhecimento.rag.enriquecimento import (
    CachePerguntas,
    perguntas_para,
    texto_para_embedding,
)


def test_texto_para_embedding_acrescenta_as_perguntas_ao_trecho():
    assert texto_para_embedding("Guia > RAPTOR\n\nSumários em árvore.", ["Como resumir um documento longo?"]) == (
        "Guia > RAPTOR\n\nSumários em árvore.\n\n"
        "Perguntas que este trecho responde:\n- Como resumir um documento longo?"
    )
    assert texto_para_embedding("Só o trecho.", []) == "Só o trecho."


def test_so_trechos_fora_do_cache_chamam_o_gerador_em_lotes_e_o_cache_e_salvo(tmp_path):
    arquivo = tmp_path / "perguntas.json"
    cache = CachePerguntas(arquivo)
    cache.guardar("A", ["pergunta de A"])
    chamadas = []

    def gerar(textos):
        chamadas.append(list(textos))
        return [[f"pergunta de {t}"] for t in textos]

    resultado = perguntas_para(["A", "B", "C", "B"], cache, gerar, tamanho_lote=1)

    assert resultado == [["pergunta de A"], ["pergunta de B"], ["pergunta de C"], ["pergunta de B"]]
    assert chamadas == [["B"], ["C"]]
    assert CachePerguntas(arquivo).get("C") == ["pergunta de C"]


def test_resposta_do_modelo_e_validada_antes_de_entrar_no_cache():
    import pytest

    from agente_conhecimento.rag.enriquecimento import interpretar_resposta

    assert interpretar_resposta('[[" a ", "", "b", "c", "d"], ["e"]]', 2) == [["a", "b", "c"], ["e"]]
    with pytest.raises(ValueError):
        interpretar_resposta('[["a"]]', 2)


def test_indexacao_enriquecida_embeda_as_perguntas_mas_guarda_o_trecho_original(tmp_path):
    from agente_conhecimento.rag.indice import abrir_ou_criar_colecao, sincronizar

    pasta = tmp_path / "md"
    pasta.mkdir()
    (pasta / "rag__raptor.md").write_text("# Guia\n\n## RAPTOR\n\nSumários em árvore.\n", encoding="utf-8")
    embedados = []

    def embedar(textos):
        embedados.extend(textos)
        return [[1.0, 0.0] for _ in textos]

    colecao = abrir_ou_criar_colecao(tmp_path / "chroma")
    sincronizar(colecao, pasta, embedar, perguntas=lambda textos: [["Como resumir um documento longo?"]] * len(textos))

    guardado = colecao.get(include=["documents", "metadatas"])
    assert guardado["documents"] == ["Guia > RAPTOR\n\nSumários em árvore."]
    assert guardado["metadatas"][0]["perguntas"] == "Como resumir um documento longo?"
    assert embedados == [
        "Guia > RAPTOR\n\nSumários em árvore.\n\n"
        "Perguntas que este trecho responde:\n- Como resumir um documento longo?"
    ]


def test_lote_com_resposta_invalida_e_dividido_ate_dar_certo():
    from agente_conhecimento.rag.enriquecimento import dividir_se_invalida

    chamadas = []

    def gerar(textos):
        chamadas.append(list(textos))
        if len(textos) > 2:
            raise ValueError("lista a mais")
        return [[f"pergunta de {t}"] for t in textos]

    assert dividir_se_invalida(gerar, ["A", "B", "C", "D", "E"]) == [
        ["pergunta de A"], ["pergunta de B"], ["pergunta de C"], ["pergunta de D"], ["pergunta de E"]
    ]
    assert chamadas == [["A", "B", "C", "D", "E"], ["A", "B"], ["C", "D", "E"], ["C"], ["D", "E"]]


def test_trecho_sozinho_com_resposta_invalida_propaga_o_erro():
    import pytest

    from agente_conhecimento.rag.enriquecimento import dividir_se_invalida

    def gerar(textos):
        raise ValueError("sempre inválida")

    with pytest.raises(ValueError):
        dividir_se_invalida(gerar, ["A", "B"])
