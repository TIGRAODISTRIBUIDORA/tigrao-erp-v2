import os
import json
import streamlit as st

from ui import is_admin, title

DATA_DIR = "dados"
LAYOUT_FILE = os.path.join(DATA_DIR, "layout_builder.json")

os.makedirs(DATA_DIR, exist_ok=True)


DEFAULT_LAYOUT = {
    "Novo Pedido": {
        "Cliente": {"linha": 1, "coluna": 1, "largura": 2, "mostrar": True},
        "Fornecedor": {"linha": 2, "coluna": 1, "largura": 1.2, "mostrar": True},
        "Produto": {"linha": 2, "coluna": 2, "largura": 2.4, "mostrar": True},
        "Botão Adicionar": {"linha": 2, "coluna": 3, "largura": 1.0, "mostrar": True},
        "Produto Selecionado": {"linha": 3, "coluna": 1, "largura": 4, "mostrar": True},
        "Quantidade": {"linha": 4, "coluna": 1, "largura": 1, "mostrar": True},
        "Desconto": {"linha": 4, "coluna": 2, "largura": 1, "mostrar": True},
        "Total do Item": {"linha": 4, "coluna": 3, "largura": 1.2, "mostrar": True},
        "Carrinho": {"linha": 5, "coluna": 1, "largura": 5, "mostrar": True},
        "Finalizar Pedido": {"linha": 6, "coluna": 1, "largura": 1.2, "mostrar": True},
        "Limpar Pedido": {"linha": 6, "coluna": 2, "largura": 1.2, "mostrar": True},
    },
    "Produtos": {
        "Cadastrar Produto": {"linha": 1, "coluna": 1, "largura": 4, "mostrar": True},
        "Exportar Produtos": {"linha": 2, "coluna": 1, "largura": 4, "mostrar": True},
        "Consultar Produto": {"linha": 3, "coluna": 1, "largura": 2, "mostrar": True},
        "Botão Buscar": {"linha": 3, "coluna": 2, "largura": 0.5, "mostrar": True},
        "Card Produto": {"linha": 4, "coluna": 1, "largura": 2, "mostrar": True},
        "Imagem Produto": {"linha": 4, "coluna": 2, "largura": 1, "mostrar": True},
    },
    "Clientes": {
        "Cadastrar Cliente": {"linha": 1, "coluna": 1, "largura": 4, "mostrar": True},
        "Buscar Cliente": {"linha": 2, "coluna": 1, "largura": 2, "mostrar": True},
        "Card Cliente": {"linha": 3, "coluna": 1, "largura": 3, "mostrar": True},
    },
    "Pedidos Lançados": {
        "Tabela Pedidos": {"linha": 1, "coluna": 1, "largura": 5, "mostrar": True},
        "Baixar Excel": {"linha": 2, "coluna": 1, "largura": 1.5, "mostrar": True},
        "Alterar Pedido": {"linha": 3, "coluna": 1, "largura": 5, "mostrar": True},
        "Excluir Pedido": {"linha": 4, "coluna": 1, "largura": 3, "mostrar": True},
    },
    "Dashboard": {
        "Cards": {"linha": 1, "coluna": 1, "largura": 5, "mostrar": True},
        "Gráficos": {"linha": 2, "coluna": 1, "largura": 5, "mostrar": True},
    },
    "Comissões": {
        "Resumo": {"linha": 1, "coluna": 1, "largura": 4, "mostrar": True},
        "Tabela": {"linha": 2, "coluna": 1, "largura": 5, "mostrar": True},
    },
    "Fornecedores": {
        "Cadastrar Fornecedor": {"linha": 1, "coluna": 1, "largura": 4, "mostrar": True},
        "Lista Fornecedores": {"linha": 2, "coluna": 1, "largura": 5, "mostrar": True},
    },
    "Vendedores": {
        "Cadastrar Vendedor": {"linha": 1, "coluna": 1, "largura": 4, "mostrar": True},
        "Lista Vendedores": {"linha": 2, "coluna": 1, "largura": 5, "mostrar": True},
    },
}


def load_layout():
    if not os.path.exists(LAYOUT_FILE):
        save_layout(DEFAULT_LAYOUT)
        return DEFAULT_LAYOUT.copy()

    try:
        with open(LAYOUT_FILE, "r", encoding="utf-8") as f:
            saved = json.load(f)

        layout = DEFAULT_LAYOUT.copy()

        for tela, blocos in saved.items():
            if tela not in layout:
                layout[tela] = {}

            for bloco, config in blocos.items():
                layout[tela][bloco] = config

        return layout
    except Exception:
        return DEFAULT_LAYOUT.copy()


def save_layout(layout):
    with open(LAYOUT_FILE, "w", encoding="utf-8") as f:
        json.dump(layout, f, ensure_ascii=False, indent=4)


def get_screen_layout(tela):
    layout = load_layout()
    return layout.get(tela, {})


def show_layout_config():
    if not is_admin():
        st.error("Acesso permitido somente para administrador.")
        st.stop()

    title("🎨 Criar Layout")

    st.info("Escolha a aba, selecione o bloco e defina onde ele deve aparecer.")

    layout = load_layout()

    tela = st.selectbox(
        "Aba do sistema",
        list(layout.keys())
    )

    blocos = list(layout[tela].keys())

    bloco = st.selectbox(
        "Bloco da aba",
        blocos
    )

    config = layout[tela][bloco]

    st.markdown(f"### Editando: {tela} → {bloco}")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        config["linha"] = st.number_input(
            "Linha",
            min_value=1,
            value=int(config.get("linha", 1)),
            step=1
        )

    with c2:
        config["coluna"] = st.number_input(
            "Coluna",
            min_value=1,
            value=int(config.get("coluna", 1)),
            step=1
        )

    with c3:
        config["largura"] = st.number_input(
            "Largura",
            min_value=0.1,
            value=float(config.get("largura", 1)),
            step=0.1
        )

    with c4:
        config["mostrar"] = st.checkbox(
            "Mostrar",
            value=bool(config.get("mostrar", True))
        )

    layout[tela][bloco] = config

    st.markdown("---")
    st.markdown("### Prévia simples da aba")

    preview = []

    for nome, cfg in layout[tela].items():
        if cfg.get("mostrar", True):
            preview.append({
                "Bloco": nome,
                "Linha": cfg.get("linha", 1),
                "Coluna": cfg.get("coluna", 1),
                "Largura": cfg.get("largura", 1),
                "Mostrar": cfg.get("mostrar", True),
            })

    preview = sorted(preview, key=lambda x: (x["Linha"], x["Coluna"]))
    st.dataframe(preview, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns([1, 1, 3])

    with col1:
        if st.button("💾 Salvar Layout", use_container_width=True):
            save_layout(layout)
            st.success("Layout salvo com sucesso.")
            st.rerun()

    with col2:
        if st.button("🔄 Restaurar Padrão", use_container_width=True):
            save_layout(DEFAULT_LAYOUT)
            st.success("Layout padrão restaurado.")
            st.rerun()
