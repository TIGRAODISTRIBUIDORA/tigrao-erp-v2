import os
import pandas as pd
import streamlit as st

from ui import is_admin, title

DATA_DIR = "dados"
LAYOUT_FILE = os.path.join(DATA_DIR, "layout.xlsx")

os.makedirs(DATA_DIR, exist_ok=True)


DEFAULT_LAYOUT = {
    "novo_fornecedor": 1.2,
    "novo_produto": 2.4,
    "novo_botao": 1.0,
    "novo_espaco": 1.2,
    "item_quantidade": 1.0,
    "item_desconto": 1.0,
    "item_total": 1.2,
    "item_espaco": 1.8,
}


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


def save_layout(layout):
    df = pd.DataFrame([
        {"campo": campo, "valor": valor}
        for campo, valor in layout.items()
    ])
    df.to_excel(LAYOUT_FILE, index=False)


def show_layout_config():
    if not is_admin():
        st.error("Acesso permitido somente para administrador.")
        st.stop()

    title("⚙️ Layout do Sistema")

    st.info("Altere os números para mudar a largura dos campos na tela de Novo Pedido.")

    layout = load_layout()

    st.markdown("### 🛒 Novo Pedido - Busca de Produto")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        layout["novo_fornecedor"] = st.number_input("Fornecedor", value=float(layout["novo_fornecedor"]), step=0.1)

    with c2:
        layout["novo_produto"] = st.number_input("Produto", value=float(layout["novo_produto"]), step=0.1)

    with c3:
        layout["novo_botao"] = st.number_input("Botão Adicionar", value=float(layout["novo_botao"]), step=0.1)

    with c4:
        layout["novo_espaco"] = st.number_input("Espaço vazio", value=float(layout["novo_espaco"]), step=0.1)

    st.markdown("### 📦 Produto Selecionado")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        layout["item_quantidade"] = st.number_input("Quantidade", value=float(layout["item_quantidade"]), step=0.1)

    with q2:
        layout["item_desconto"] = st.number_input("Desconto", value=float(layout["item_desconto"]), step=0.1)

    with q3:
        layout["item_total"] = st.number_input("Total", value=float(layout["item_total"]), step=0.1)

    with q4:
        layout["item_espaco"] = st.number_input("Espaço vazio item", value=float(layout["item_espaco"]), step=0.1)

    if st.button("💾 Salvar Layout"):
        save_layout(layout)
        st.success("Layout salvo com sucesso.")
        st.rerun()
