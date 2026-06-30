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


def aplicar_layout_tigrao():
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #fff7ed 0%, #f8fafc 100%) !important;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        max-width: 1320px !important;
    }

    header, footer {
        display: none !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #000000 55%, #7c2d12 100%) !important;
        border-right: 3px solid #f97316;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
        font-weight: 900 !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label {
        background: rgba(249,115,22,.18);
        border-radius: 15px;
        padding: 11px 13px;
        margin-bottom: 8px;
        border: 1px solid rgba(249,115,22,.35);
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: #f97316 !important;
        color: white !important;
    }

    .topo-app {
        background: linear-gradient(135deg, #000000 0%, #7c2d12 45%, #f97316 100%);
        color: white;
        padding: 26px;
        border-radius: 26px;
        margin-bottom: 22px;
        box-shadow: 0 14px 34px rgba(124,45,18,.35);
        border: 2px solid #fb923c;
    }

    .topo-app h1 {
        margin: 0;
        font-size: 34px;
        font-weight: 1000;
        color: white !important;
        letter-spacing: .3px;
    }

    .topo-app p {
        margin: 7px 0 0;
        font-size: 16px;
        opacity: .96;
        color: #ffedd5;
    }

    .app-card {
        background: #ffffff;
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 10px 28px rgba(15,23,42,.10);
        border: 2px solid #fed7aa;
        margin-bottom: 20px;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #f97316, #ea580c) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        min-height: 55px !important;
        font-size: 16px !important;
        font-weight: 1000 !important;
        box-shadow: 0 8px 18px rgba(249,115,22,.35);
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #ea580c, #9a3412) !important;
        color: white !important;
        transform: translateY(-1px);
    }

    input, textarea {
        border-radius: 16px !important;
        min-height: 52px !important;
        font-size: 16px !important;
        border: 2px solid #fed7aa !important;
        background: white !important;
        color: #111827 !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 16px !important;
        min-height: 52px !important;
        border: 2px solid #fed7aa !important;
        background: white !important;
        color: #111827 !important;
    }

    [data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 22px;
        padding: 18px;
        box-shadow: 0 8px 22px rgba(15,23,42,.10);
        border: 2px solid #fdba74;
    }

    [data-testid="stMetric"] label {
        color: #9a3412 !important;
        font-weight: 900 !important;
    }

    [data-testid="stDataFrame"] {
        background: white;
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 8px 22px rgba(15,23,42,.08);
        border: 2px solid #fed7aa;
    }

    h1, h2, h3 {
        color: #111827 !important;
        font-weight: 1000 !important;
    }

    label {
        font-weight: 900 !important;
        color: #111827 !important;
    }

    .stAlert {
        border-radius: 18px !important;
    }

    @media (max-width: 700px) {
        .block-container {
            padding: .6rem !important;
        }

        .topo-app {
            border-radius: 0 0 24px 24px;
            margin: -0.6rem -0.6rem 16px -0.6rem;
            padding: 22px;
        }

        .topo-app h1 {
            font-size: 25px;
        }

        .app-card {
            padding: 16px;
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
aplicar_layout_tigrao()
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
