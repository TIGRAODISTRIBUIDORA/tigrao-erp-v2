import streamlit as st

from clients import show_clients
from commissions import show_commissions
from dashboard import show_dashboard
from database import ensure_data_files
from login import login_screen, logout
from orders import show_new_order, show_orders
from products import show_import_products, show_products
from suppliers import show_suppliers
from users import show_users
from visual_designer import show_visual_designer
from ui import apply_style, is_admin

st.set_page_config(page_title="Tigrão App", page_icon="🐯", layout="centered")


def aplicar_app_mobile():
    st.markdown("""
    <style>
    header, footer {
        display: none !important;
    }

    [data-testid="stSidebar"] {
        display: none !important;
    }

    [data-testid="stAppViewContainer"] {
        background: #f2f4f7 !important;
    }

    .block-container {
        max-width: 430px !important;
        padding: 0 !important;
        margin: auto !important;
    }

    .app-phone {
        min-height: 100vh;
        background: #f2f4f7;
        font-family: Arial, sans-serif;
    }

    .app-top {
        background: linear-gradient(180deg, #0b8de3, #0671bb);
        color: white;
        padding: 18px 18px 14px;
        border-radius: 0 0 24px 24px;
        box-shadow: 0 6px 20px rgba(0,0,0,.22);
        margin-bottom: 14px;
    }

    .app-top-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 900;
        font-size: 15px;
    }

    .app-title {
        margin-top: 18px;
        font-size: 24px;
        font-weight: 900;
    }

    .app-subtitle {
        font-size: 13px;
        opacity: .9;
        margin-top: 4px;
    }

    .app-card {
        background: white;
        margin: 10px;
        padding: 14px;
        border-radius: 20px;
        box-shadow: 0 5px 18px rgba(0,0,0,.10);
        border: 1px solid #e5e7eb;
    }

    .menu-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 10px;
    }

    .menu-btn {
        background: white;
        border-radius: 20px;
        padding: 18px 12px;
        text-align: center;
        box-shadow: 0 5px 16px rgba(0,0,0,.10);
        border: 1px solid #e5e7eb;
        font-weight: 900;
        color: #111827;
        font-size: 14px;
    }

    .menu-btn span {
        display: block;
        font-size: 30px;
        margin-bottom: 8px;
    }

    div.stButton > button {
        width: 100%;
        min-height: 58px !important;
        border-radius: 18px !important;
        background: #0b8de3 !important;
        color: white !important;
        border: none !important;
        font-weight: 900 !important;
        font-size: 16px !important;
        box-shadow: 0 5px 14px rgba(11,141,227,.28);
    }

    input, textarea {
        border-radius: 16px !important;
        min-height: 50px !important;
        font-size: 16px !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 16px !important;
        min-height: 50px !important;
    }

    h1, h2, h3 {
        font-size: 22px !important;
        font-weight: 900 !important;
    }

    label {
        font-weight: 800 !important;
    }
    </style>
    """, unsafe_allow_html=True)


def topo_app(titulo, subtitulo=""):
    st.markdown(f"""
    <div class="app-top">
        <div class="app-top-row">
            <div>🐯 Tigrão</div>
            <div>{st.session_state.get("vendedor", "")}</div>
        </div>
        <div class="app-title">{titulo}</div>
        <div class="app-subtitle">{subtitulo}</div>
    </div>
    """, unsafe_allow_html=True)


def abrir_card():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)


def fechar_card():
    st.markdown('</div>', unsafe_allow_html=True)


ensure_data_files()
apply_style()
aplicar_app_mobile()
login_screen()

if "menu_mobile" not in st.session_state:
    st.session_state.menu_mobile = "Início"


def mudar_menu(nome):
    st.session_state.menu_mobile = nome
    st.rerun()


menu_admin = [
    ("Dashboard", "📊"),
    ("Novo Pedido", "🛒"),
    ("Pedidos Lançados", "📦"),
    ("Clientes", "👥"),
    ("Produtos", "🏷️"),
    ("Fornecedores", "🚚"),
    ("Vendedores", "👤"),
    ("Importar Produtos", "📥"),
    ("Comissões", "💰"),
    ("Designer Visual", "🎨"),
    ("Sair", "🚪"),
]

menu_vendedor = [
    ("Novo Pedido", "🛒"),
    ("Pedidos Lançados", "📦"),
    ("Clientes", "👥"),
    ("Produtos", "🏷️"),
    ("Comissões", "💰"),
    ("Sair", "🚪"),
]

opcoes = menu_admin if is_admin() else menu_vendedor
menu = st.session_state.menu_mobile


if menu == "Início":
    topo_app("Menu Principal", "Sistema de pedidos no formato aplicativo")

    st.markdown('<div class="menu-grid">', unsafe_allow_html=True)

    for nome, icone in opcoes:
        st.markdown(f"""
        <div class="menu-btn">
            <span>{icone}</span>
            {nome}
        </div>
        """, unsafe_allow_html=True)

        if st.button(nome, key=f"btn_{nome}"):
            mudar_menu(nome)

    st.markdown('</div>', unsafe_allow_html=True)


elif menu == "Sair":
    logout()


else:
    if st.button("← Voltar ao menu"):
        mudar_menu("Início")

    if menu == "Dashboard":
        topo_app("Dashboard", "Visão geral da operação")
        abrir_card()
        show_dashboard()
        fechar_card()

    elif menu == "Novo Pedido":
        topo_app("Novo Pedido", "Lançamento rápido de pedidos")
        abrir_card()
        show_new_order()
        fechar_card()

    elif menu == "Pedidos Lançados":
        topo_app("Pedidos", "Pedidos lançados pelos vendedores")
        abrir_card()
        show_orders()
        fechar_card()

    elif menu == "Clientes":
        topo_app("Clientes", "Consulta e cadastro de clientes")
        abrir_card()
        show_clients()
        fechar_card()

    elif menu == "Produtos":
        topo_app("Produtos", "Consulta de produtos e preços")
        abrir_card()
        show_products()
        fechar_card()

    elif menu == "Fornecedores":
        topo_app("Fornecedores", "Cadastro e consulta")
        abrir_card()
        show_suppliers()
        fechar_card()

    elif menu == "Vendedores":
        topo_app("Vendedores", "Equipe comercial")
        abrir_card()
        show_users()
        fechar_card()

    elif menu == "Importar Produtos":
        topo_app("Importar Produtos", "Atualizar base de produtos")
        abrir_card()
        show_import_products()
        fechar_card()

    elif menu == "Comissões":
        topo_app("Comissões", "Controle de vendas e comissão")
        abrir_card()
        show_commissions()
        fechar_card()

    elif menu == "Designer Visual":
        topo_app("Designer Visual", "Personalização das telas")
        abrir_card()
        show_visual_designer()
        fechar_card()
