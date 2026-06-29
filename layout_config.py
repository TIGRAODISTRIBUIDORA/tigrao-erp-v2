import os
import pandas as pd
import streamlit as st

from ui import is_admin, title

DATA_DIR = "dados"
LAYOUT_FILE = os.path.join(DATA_DIR, "layout.xlsx")

os.makedirs(DATA_DIR, exist_ok=True)


# =========================
# LAYOUT PADRÃO
# =========================
DEFAULT_LAYOUT = {
    # NOVO PEDIDO
    "novo_pedido_fornecedor_linha": 1,
    "novo_pedido_fornecedor_coluna": 1,
    "novo_pedido_fornecedor_largura": 1.2,

    "novo_pedido_produto_linha": 1,
    "novo_pedido_produto_coluna": 2,
    "novo_pedido_produto_largura": 2.4,

    "novo_pedido_botao_adicionar_linha": 1,
    "novo_pedido_botao_adicionar_coluna": 3,
    "novo_pedido_botao_adicionar_largura": 1.0,

    "novo_pedido_quantidade_linha": 2,
    "novo_pedido_quantidade_coluna": 1,
    "novo_pedido_quantidade_largura": 1.0,

    "novo_pedido_desconto_linha": 2,
    "novo_pedido_desconto_coluna": 2,
    "novo_pedido_desconto_largura": 1.0,

    "novo_pedido_total_linha": 2,
    "novo_pedido_total_coluna": 3,
    "novo_pedido_total_largura": 1.2,

    # PRODUTOS
    "produtos_busca_linha": 1,
    "produtos_busca_coluna": 1,
    "produtos_busca_largura": 2.0,

    "produtos_botao_lupa_linha": 1,
    "produtos_botao_lupa_coluna": 2,
    "produtos_botao_lupa_largura": 0.5,

    "produtos_card_linha": 2,
    "produtos_card_coluna": 1,
    "produtos_card_largura": 2.0,

    "produtos_imagem_linha": 2,
    "produtos_imagem_coluna": 2,
    "produtos_imagem_largura": 1.0,

    # CLIENTES
    "clientes_busca_linha": 1,
    "clientes_busca_coluna": 1,
    "clientes_busca_largura": 2.0,

    "clientes_card_linha": 2,
    "clientes_card_coluna": 1,
    "clientes_card_largura": 2.0,

    # PEDIDOS LANÇADOS
    "pedidos_busca_linha": 1,
    "pedidos_busca_coluna": 1,
    "pedidos_busca_largura": 2.0,

    "pedidos_tabela_linha": 2,
    "pedidos_tabela_coluna": 1,
    "pedidos_tabela_largura": 3.0,

    # DASHBOARD
    "dashboard_cards_linha": 1,
    "dashboard_cards_coluna": 1,
    "dashboard_cards_largura": 3.0,

    # COMISSÕES
    "comissoes_busca_linha": 1,
    "comissoes_busca_coluna": 1,
    "comissoes_busca_largura": 2.0,

    # FORNECEDORES
    "fornecedores_busca_linha": 1,
    "fornecedores_busca_coluna": 1,
    "fornecedores_busca_largura": 2.0,

    # VENDEDORES
    "vendedores_busca_linha": 1,
    "vendedores_busca_coluna": 1,
    "vendedores_busca_largura": 2.0,
}


ABAS_SISTEMA = {
    "Novo Pedido": [
        ("Fornecedor", "novo_pedido_fornecedor"),
        ("Produto", "novo_pedido_produto"),
        ("Botão Adicionar", "novo_pedido_botao_adicionar"),
        ("Quantidade", "novo_pedido_quantidade"),
        ("Desconto", "novo_pedido_desconto"),
        ("Total do Item", "novo_pedido_total"),
    ],

    "Produtos": [
        ("Busca de Produto", "produtos_busca"),
        ("Botão Lupa", "produtos_botao_lupa"),
        ("Card do Produto", "produtos_card"),
        ("Imagem do Produto", "produtos_imagem"),
    ],

    "Clientes": [
        ("Busca de Cliente", "clientes_busca"),
        ("Card do Cliente", "clientes_card"),
    ],

    "Pedidos Lançados": [
        ("Busca de Pedido", "pedidos_busca"),
        ("Tabela / Lista de Pedidos", "pedidos_tabela"),
    ],

    "Dashboard": [
        ("Cards do Dashboard", "dashboard_cards"),
    ],

    "Comissões": [
        ("Busca de Comissão", "comissoes_busca"),
    ],

    "Fornecedores": [
        ("Busca de Fornecedor", "fornecedores_busca"),
    ],

    "Vendedores": [
        ("Busca de Vendedor", "vendedores_busca"),
    ],
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


def _editar_bloco(nome_bloco, layout, prefixo):
    st.markdown(f"### {nome_bloco}")

    c1, c2, c3 = st.columns(3)

    with c1:
        _numero("Linha", layout, f"{prefixo}_linha", 1.0)

    with c2:
        _numero("Coluna", layout, f"{prefixo}_coluna", 1.0)

    with c3:
        _numero("Largura", layout, f"{prefixo}_largura", 0.1)

    st.caption(
        "Linha = altura do bloco | Coluna = posição lateral | Largura = tamanho do bloco"
    )

    st.markdown("---")


def show_layout_config():
    if not is_admin():
        st.error("Acesso permitido somente para administrador.")
        st.stop()

    title("⚙️ Designer do Sistema")

    st.info(
        "Escolha a aba do sistema e ajuste os blocos dessa aba. "
        "Depois clique em Salvar Layout."
    )

    layout = load_layout()

    aba = st.selectbox(
        "Escolha a aba que deseja editar",
        list(ABAS_SISTEMA.keys())
    )

    st.markdown(f"## 🧩 Aba: {aba}")

    blocos = ABAS_SISTEMA.get(aba, [])

    for nome_bloco, prefixo in blocos:
        _editar_bloco(nome_bloco, layout, prefixo)

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
