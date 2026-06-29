import streamlit as st


def cfg(blocos, nome):
    return blocos.get(nome, {"x": 1, "y": 1, "w": 1, "h": 1, "mostrar": True})


def mostrar(blocos, nome):
    return bool(cfg(blocos, nome).get("mostrar", True))


def bloco_ordem(blocos):
    return sorted(
        blocos.items(),
        key=lambda item: (
            float(item[1].get("y", 1)),
            float(item[1].get("x", 1))
        )
    )


def largura(blocos, nome, padrao=1):
    return float(cfg(blocos, nome).get("w", padrao))


def linha(blocos, nome, padrao=1):
    return int(float(cfg(blocos, nome).get("y", padrao)))


def coluna(blocos, nome, padrao=1):
    return int(float(cfg(blocos, nome).get("x", padrao)))


def renderizar_linha(blocos, componentes, linha_numero):
    """
    componentes = {
        "Fornecedor": funcao,
        "Produto": funcao,
        "Botão Adicionar": funcao,
    }
    """

    itens = []

    for nome, funcao in componentes.items():
        if not mostrar(blocos, nome):
            continue

        if linha(blocos, nome) == linha_numero:
            itens.append({
                "nome": nome,
                "funcao": funcao,
                "x": coluna(blocos, nome),
                "w": largura(blocos, nome),
            })

    if not itens:
        return

    itens = sorted(itens, key=lambda x: x["x"])

    colunas_config = []

    posicao_atual = 1

    for item in itens:
        espaco = item["x"] - posicao_atual

        if espaco > 0:
            colunas_config.append(float(espaco))

        colunas_config.append(float(item["w"]))
        posicao_atual = item["x"] + 1

    colunas_config.append(1.0)

    cols = st.columns(colunas_config)

    indice_coluna = 0
    posicao_atual = 1

    for item in itens:
        espaco = item["x"] - posicao_atual

        if espaco > 0:
            indice_coluna += 1

        with cols[indice_coluna]:
            item["funcao"]()

        indice_coluna += 1
        posicao_atual = item["x"] + 1
