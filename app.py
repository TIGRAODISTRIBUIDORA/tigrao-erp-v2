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
    header, footer { display:none !important; }
    [data-testid="stSidebar"] { display:none !important; }

    [data-testid="stAppViewContainer"] {
        background:#f4f4f4 !important;
        color:#111827 !important;
    }

    .block-container {
        max-width:430px !important;
        padding:0 0 95px 0 !important;
        margin:auto !important;
        overflow:visible !important;
    }

    * {
        font-family: Arial, sans-serif;
        color:#111827 !important;
    }

    .tigrao-header {
        background:#111111;
        color:white !important;
        padding:18px 18px 0 18px;
        border-radius:0 0 28px 28px;
        overflow:hidden;
        position:relative;
        box-shadow:0 8px 24px rgba(0,0,0,.25);
    }

    .tigrao-header * {
        color:white !important;
    }

    .header-row {
        display:flex;
        align-items:center;
        justify-content:space-between;
        margin-bottom:14px;
    }

    .hamburger {
        color:#f97316 !important;
        font-size:28px;
        font-weight:1000;
    }

    .logo-area {
        text-align:center;
        font-weight:1000;
        font-size:27px;
        letter-spacing:1px;
        line-height:1;
    }

    .logo-sub {
        color:#f97316 !important;
        font-size:10px;
        letter-spacing:6px;
        margin-top:4px;
    }

    .admin-pill {
        border:2px solid #f97316;
        border-radius:24px;
        padding:7px 10px;
        font-size:13px;
        font-weight:1000;
        display:flex;
        gap:5px;
        align-items:center;
    }

    .orange-hero {
        background:linear-gradient(135deg,#ff8a00,#ff9f1c);
        margin:0 -18px;
        padding:28px 18px 78px 18px;
        border-radius:0 0 0 0;
        position:relative;
        overflow:hidden;
    }

    .orange-hero::after {
        content:"🐯";
        position:absolute;
        right:-22px;
        bottom:-40px;
        font-size:150px;
        opacity:.16;
    }

    .screen-title {
        color:#111111 !important;
        font-size:34px;
        font-weight:1000;
        margin:0;
        position:relative;
        z-index:2;
    }

    .screen-subtitle {
        color:#111111 !important;
        font-size:18px;
        font-weight:700;
        margin-top:8px;
        position:relative;
        z-index:2;
    }

    .page-content {
        margin-top:-58px;
        position:relative;
        z-index:5;
        padding:0 10px;
    }

    .app-card {
        background:white !important;
        margin:10px 0;
        padding:16px;
        border-radius:22px;
        box-shadow:0 8px 22px rgba(15,23,42,.12);
        border:1px solid #e5e7eb;
        overflow:visible !important;
    }

    .bottom-nav {
        position:fixed;
        left:50%;
        bottom:0;
        transform:translateX(-50%);
        width:100%;
        max-width:430px;
        background:#111111;
        padding:8px 8px 10px 8px;
        display:grid;
        grid-template-columns:repeat(6,1fr);
        gap:4px;
        z-index:999999;
        box-shadow:0 -8px 24px rgba(0,0,0,.28);
        border-radius:22px 22px 0 0;
    }

    .bottom-item {
        text-align:center;
        color:white !important;
        font-size:11px;
        font-weight:800;
        padding:7px 3px;
        border-radius:16px;
        min-height:50px;
    }

    .bottom-item span {
        display:block;
        color:white !important;
        font-size:21px;
        line-height:22px;
        margin-bottom:3px;
    }

    .bottom-active {
        border:2px solid #f97316;
        color:#f97316 !important;
    }

    .bottom-active span {
        color:#f97316 !important;
    }

    div.stButton > button {
        width:100%;
        min-height:52px !important;
        border-radius:16px !important;
        background:#0b8de3 !important;
        color:white !important;
        border:none !important;
        font-weight:900 !important;
        font-size:15px !important;
        box-shadow:0 5px 14px rgba(11,141,227,.28);
        white-space:normal !important;
    }

    div.stButton > button * {
        color:white !important;
    }

    div.stButton > button:active {
        background:#22c55e !important;
        transform:scale(.97);
    }

    input, textarea {
        background:white !important;
        color:#111827 !important;
        border:2px solid #cbd5e1 !important;
        border-radius:16px !important;
        min-height:50px !important;
        font-size:16px !important;
    }

    div[data-baseweb="select"] > div {
        background:white !important;
        color:#111827 !important;
        border:2px solid #cbd5e1 !important;
        border-radius:16px !important;
        min-height:50px !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color:#111827 !important;
    }

    div[data-baseweb="popover"] {
        z-index:9999999 !important;
    }

    label, p, span, h1, h2, h3, h4, h5, h6 {
        color:#111827 !important;
        font-weight:800;
    }

    [data-testid="stDataFrame"] {
        background:white !important;
        border-radius:18px;
        overflow:hidden;
    }
    </style>
    """, unsafe_allow_html=True)


def topo_app(titulo, subtitulo=""):
    perfil = st.session_state.get("perfil", "").upper() or "ADMIN"

    st.markdown(f"""
    <div class="tigrao-header">
        <div class="header-row">
            <div class="hamburger">☰</div>

            <div class="logo-area">
                🐯 TIGRÃO
                <div class="logo-sub">DISTRIBUIDORA</div>
            </div>

            <div class="admin-pill">👤 {perfil}</div>
        </div>

        <div class="orange-hero">
            <div class="screen-title">{titulo}</div>
            <div class="screen-subtitle">{subtitulo}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def abrir_conteudo():
    st.markdown('<div class="page-content">', unsafe_allow_html=True)


def fechar_conteudo():
    st.markdown('</div>', unsafe_allow_html=True)


def abrir_card():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)


def fechar_card():
    st.markdown('</div>', unsafe_allow_html=True)


def mudar_menu(nome):
    st.session_state.menu_mobile = nome
    st.rerun()


def bottom_nav(menu_atual):
    itens = [
        ("Dashboard", "📊", "Dashboard"),
        ("Novo Pedido", "🛒", "Novo Pedido"),
        ("Pedidos Lançados", "📦", "Pedidos"),
        ("Clientes", "👥", "Clientes"),
        ("Produtos", "🏷️", "Produtos"),
        ("Mais", "⋯", "Mais"),
    ]

    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)

    for destino, icone, texto in itens:
        ativo = "bottom-active" if menu_atual == destino or (menu_atual in ["Fornecedores", "Vendedores", "Importar Produtos", "Comissões", "Designer Visual", "Sair"] and destino == "Mais") else ""

        st.markdown(f"""
        <div class="bottom-item {ativo}">
            <span>{icone}</span>
            {texto}
        </div>
        """, unsafe_allow_html=True)

        if st.button(texto, key=f"nav_{destino}"):
            mudar_menu(destino)

    st.markdown('</div>', unsafe_allow_html=True)


ensure_data_files()
apply_style()
aplicar_app_mobile()
login_screen()

if "menu_mobile" not in st.session_state:
    st.session_state.menu_mobile = "Dashboard"

menu = st.session_state.menu_mobile


if menu == "Sair":
    logout()


elif menu == "Dashboard":
    topo_app("Dashboard", "Visão geral da operação")
    abrir_conteudo()
    show_dashboard()
    fechar_conteudo()


elif menu == "Novo Pedido":
    topo_app("Novo Pedido", "Lançamento rápido de pedidos")
    abrir_conteudo()
    abrir_card()
    show_new_order()
    fechar_card()
    fechar_conteudo()


elif menu == "Pedidos Lançados":
    topo_app("Pedidos", "Pedidos lançados")
    abrir_conteudo()
    abrir_card()
    show_orders()
    fechar_card()
    fechar_conteudo()


elif menu == "Clientes":
    topo_app("Clientes", "Cadastro e consulta")
    abrir_conteudo()
    abrir_card()
    show_clients()
    fechar_card()
    fechar_conteudo()


elif menu == "Produtos":
    topo_app("Produtos", "Consulta de produtos")
    abrir_conteudo()
    abrir_card()
    show_products()
    fechar_card()
    fechar_conteudo()


elif menu == "Fornecedores":
    topo_app("Fornecedores", "Cadastro e consulta")
    abrir_conteudo()
    abrir_card()
    show_suppliers()
    fechar_card()
    fechar_conteudo()


elif menu == "Vendedores":
    topo_app("Vendedores", "Equipe comercial")
    abrir_conteudo()
    abrir_card()
    show_users()
    fechar_card()
    fechar_conteudo()


elif menu == "Importar Produtos":
    topo_app("Importar Produtos", "Atualizar base")
    abrir_conteudo()
    abrir_card()
    show_import_products()
    fechar_card()
    fechar_conteudo()


elif menu == "Comissões":
    topo_app("Comissões", "Controle de vendas")
    abrir_conteudo()
    abrir_card()
    show_commissions()
    fechar_card()
    fechar_conteudo()


elif menu == "Designer Visual":
    topo_app("Designer Visual", "Personalização")
    abrir_conteudo()
    abrir_card()
    show_visual_designer()
    fechar_card()
    fechar_conteudo()


elif menu == "Mais":
    topo_app("Mais", "Outras opções")
    abrir_conteudo()

    if is_admin():
        opcoes_mais = [
            ("Fornecedores", "🚚"),
            ("Vendedores", "👤"),
            ("Importar Produtos", "📥"),
            ("Comissões", "💰"),
            ("Designer Visual", "🎨"),
            ("Sair", "🚪"),
        ]
    else:
        opcoes_mais = [
            ("Comissões", "💰"),
            ("Sair", "🚪"),
        ]

    for nome, icone in opcoes_mais:
        if st.button(f"{icone} {nome}", key=f"mais_{nome}", use_container_width=True):
            mudar_menu(nome)

    fechar_conteudo()


bottom_nav(menu)
