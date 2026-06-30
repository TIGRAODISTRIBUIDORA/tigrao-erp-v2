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

st.set_page_config(page_title="Tigrão ERP", page_icon="🐯", layout="wide")


def aplicar_layout_app():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: #f3f7fb;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        max-width: 1300px !important;
    }

    header, footer {
        display: none !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0284c7 0%, #075985 55%, #0f172a 100%) !important;
        border-right: 1px solid rgba(255,255,255,.12);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
        font-weight: 800 !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label {
        background: rgba(255,255,255,.10);
        border-radius: 14px;
        padding: 10px 12px;
        margin-bottom: 8px;
        border: 1px solid rgba(255,255,255,.10);
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(255,255,255,.20);
    }

    .topo-app {
        background: linear-gradient(135deg, #0284c7, #075985);
        color: white;
        padding: 24px;
        border-radius: 26px;
        margin-bottom: 22px;
        box-shadow: 0 14px 32px rgba(2,132,199,.25);
    }

    .topo-app h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 900;
        color: white !important;
    }

    .topo-app p {
        margin: 7px 0 0;
        font-size: 15px;
        opacity: .95;
    }

    .app-card {
        background: white;
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 10px 28px rgba(15,23,42,.08);
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #0284c7, #075985) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        min-height: 54px !important;
        font-size: 16px !important;
        font-weight: 900 !important;
        box-shadow: 0 7px 16px rgba(2,132,199,.25);
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #0369a1, #0f172a) !important;
        transform: translateY(-1px);
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

    [data-testid="stMetric"] {
        background: white;
        border-radius: 22px;
        padding: 18px;
        box-shadow: 0 8px 22px rgba(15,23,42,.08);
        border: 1px solid #e5e7eb;
    }

    [data-testid="stDataFrame"] {
        background: white;
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 8px 22px rgba(15,23,42,.08);
    }

    h1, h2, h3 {
        color: #0f172a;
        font-weight: 900;
    }

    label {
        font-weight: 800 !important;
        color: #0f172a !important;
    }

    @media (max-width: 700px) {
        .block-container {
            padding: .6rem !important;
        }

        .topo-app {
            border-radius: 0 0 24px 24px;
            margin: -0.6rem -0.6rem 16px -0.6rem;
            padding: 20px;
        }

        .topo-app h1 {
            font-size: 24px;
        }

        .app-card {
            padding: 15px;
            border-radius: 18px;
        }

        div.stButton > button {
            width: 100%;
            min-height: 58px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def topo(titulo, subtitulo):
    st.markdown(f"""
    <div class="topo-app">
        <h1>🐯 {titulo}</h1>
        <p>{subtitulo}</p>
    </div>
    """, unsafe_allow_html=True)


def abrir_card():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)


def fechar_card():
    st.markdown('</div>', unsafe_allow_html=True)


ensure_data_files()
apply_style()
aplicar_layout_app()
login_screen()

st.sidebar.markdown("## 🐯 TIGRÃO")
st.sidebar.markdown(f"### {st.session_state.get('vendedor', '')}")
st.sidebar.markdown(f"Perfil: **{st.session_state.get('perfil', '').upper()}**")

if is_admin():
    menu_options = [
        "Dashboard",
        "Novo Pedido",
        "Pedidos Lançados",
        "Clientes",
        "Produtos",
        "Fornecedores",
        "Vendedores",
        "Importar Produtos",
        "Comissões",
        "🎨 Designer Visual",
        "Sair",
    ]
else:
    menu_options = [
        "Novo Pedido",
        "Pedidos Lançados",
        "Clientes",
        "Produtos",
        "Comissões",
        "Sair",
    ]

menu = st.sidebar.radio("Menu", menu_options)

if menu == "Sair":
    logout()

elif menu == "Dashboard":
    topo("Dashboard", "Visão geral da operação")
    abrir_card()
    show_dashboard()
    fechar_card()

elif menu == "Novo Pedido":
    topo("Novo Pedido", "Lançamento rápido de pedidos")
    abrir_card()
    show_new_order()
    fechar_card()

elif menu == "Pedidos Lançados":
    topo("Pedidos Lançados", "Consulta e acompanhamento dos pedidos")
    abrir_card()
    show_orders()
    fechar_card()

elif menu == "Clientes":
    topo("Clientes", "Cadastro, consulta e edição de clientes")
    abrir_card()
    show_clients()
    fechar_card()

elif menu == "Produtos":
    topo("Produtos", "Consulta e gestão de produtos")
    abrir_card()
    show_products()
    fechar_card()

elif menu == "Fornecedores":
    topo("Fornecedores", "Consulta e cadastro de fornecedores")
    abrir_card()
    show_suppliers()
    fechar_card()

elif menu == "Vendedores":
    topo("Vendedores", "Cadastro e controle da equipe")
    abrir_card()
    show_users()
    fechar_card()

elif menu == "Importar Produtos":
    topo("Importar Produtos", "Atualização da base de produtos")
    abrir_card()
    show_import_products()
    fechar_card()

elif menu == "Comissões":
    topo("Comissões", "Controle de vendas e comissões")
    abrir_card()
    show_commissions()
    fechar_card()

elif menu == "🎨 Designer Visual":
    topo("Designer Visual", "Personalização das telas do sistema")
    show_visual_designer()
