import os
import pandas as pd
import streamlit as st

from ui import is_admin, title

DATA_DIR = "dados"
LAYOUT_FILE = os.path.join(DATA_DIR, "layout.xlsx")

os.makedirs(DATA_DIR, exist_ok=True)

DEFAULT_LAYOUT = {
    "novo_fornecedor_linha": 1,
    "novo_fornecedor_coluna": 1,
    "novo_fornecedor_largura": 1.2,

    "novo_produto_linha": 1,
    "novo_produto_coluna": 2,
    "novo_produto_largura": 2.4,

    "novo_botao_linha": 1,
    "novo_botao_coluna": 3,
    "novo_botao_largura": 1.0,

    "novo_espaco_linha": 1,
    "novo_espaco_coluna": 4,
    "novo_espaco_largura": 1.2,

    "item_quantidade_linha": 2,
    "item_quantidade_coluna": 1,
    "item_quantidade_largura": 1.0,

    "item_desconto_linha": 2,
    "item_desconto_coluna": 2,
    "item_desconto_largura": 1.0,

    "item_total_linha": 2,
    "item_total_coluna": 3,
    "item_total_largura": 1.2,

    "item_espaco_linha": 2,
    "item_espaco_coluna": 4,
    "item_espaco_largura": 1.8,
}


def save_layout(layout):
    df = pd.DataFrame([
        {"campo": campo, "valor": valor}
        for campo, valor in layout.items()
    ])
    df.to_excel(LAYOUT_FILE, index=False)


def load_layout():
    if not os.path.exists(LAYOUT_FILE):
        save_layout(DEFAULT_LAYOUT)
        return DEFAULT_LAYOUT.copy()

    try:
        df = pd.read_excel(LAYOUT_FILE)
        layout = DEFAULT_LAYOUT.copy()

        for _, row in df.iterrows():
            layout[str(row["campo"])] = float(row["valor"])

        return layout
    except Exception:
        return DEFAULT_LAYOUT.copy()


def _numero(label, layout, campo, min_value=0.0):
    layout[campo] = st.number_input(
        label,
        min_value=min_value,
        value=float(layout.get(campo, DEFAULT_LAYOUT.get(campo, 1))),
        step=0.1,
        key=campo
    )


def _componente(nome, layout, prefixo):
    st.markdown(f"### {nome}")

    c1, c2, c3 = st.columns(3)

    with c1:
        _numero("Linha", layout, f"{prefixo}_linha", 1.0)

    with c2:
        _numero("Coluna", layout, f"{prefixo}_coluna", 1.0)

    with c3:
        _numero("Largura", layout, f"{prefixo}_largura", 0.1)

    st.markdown("---")


def show_layout_config():
    if not is_admin():
        st.error("Acesso permitido somente para administrador.")
        st.stop()

    title("⚙️ Designer do Sistema")

    st.info(
        "Aqui você define onde cada campo vai aparecer. "
        "Linha muda a altura. Coluna muda a posição lateral. "
        "Largura muda o tamanho do campo."
    )

    layout = load_layout()

    tela = st.selectbox(
        "Escolha a tela para editar",
        [
            "Novo Pedido",
            "Produtos",
            "Clientes",
            "Pedidos Lançados",
            "Dashboard",
            "Comissões",
            "Fornecedores",
            "Vendedores",
        ]
    )

    if tela == "Novo Pedido":
        st.markdown("## 🛒 Novo Pedido")

        _componente("Fornecedor", layout, "novo_fornecedor")
        _componente("Produto", layout, "novo_produto")
        _componente("Botão Adicionar", layout, "novo_botao")
        _componente("Espaço vazio", layout, "novo_espaco")
        _componente("Quantidade", layout, "item_quantidade")
        _componente("Desconto", layout, "item_desconto")
        _componente("Total", layout, "item_total")
        _componente("Espaço vazio do item", layout, "item_espaco")

    else:
        st.warning(
            "Essa tela ainda não foi ligada ao Designer. "
            "Primeiro vamos finalizar o Novo Pedido, depois ligamos as outras."
        )

    col1, col2, col3 = st.columns([1, 1, 3])

    with col1:
        if st.button("💾 Salvar Layout", use_container_width=True):
            save_layout(layout)
            st.success("Layout salvo com sucesso.")
            st.rerun()

    with col2:
        if st.button("🔄 Restaurar Padrão", use_container_width=True):
            save_layout(DEFAULT_LAYOUT.copy())
            st.success("Layout padrão restaurado.")
            st.rerun()
