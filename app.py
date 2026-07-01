import os
import time
from datetime import datetime

import pandas as pd
import streamlit as st

# =========================================================
# CONFIGURAÇÃO
# =========================================================

st.set_page_config(
    page_title="Tigrão V2",
    page_icon="🐯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

PASTA_DADOS = "dados"
ARQ_CLIENTES = f"{PASTA_DADOS}/clientes.xlsx"
ARQ_PRODUTOS = f"{PASTA_DADOS}/produtos.xlsx"
ARQ_PEDIDOS = f"{PASTA_DADOS}/pedidos.xlsx"
ARQ_USUARIOS = f"{PASTA_DADOS}/usuarios.xlsx"

COMISSAO_PADRAO = 0.07


# =========================================================
# BANCO DE DADOS
# =========================================================

def criar_banco():
    os.makedirs(PASTA_DADOS, exist_ok=True)

    # Recria usuários padrão para não dar erro de login.
    usuarios = pd.DataFrame([
        {
            "usuario": "admin",
            "senha": "admin123",
            "nome": "Administrador",
            "perfil": "ADMIN",
            "comissao": 0.07,
        },
        {
            "usuario": "vendedor",
            "senha": "123",
            "nome": "Vendedor",
            "perfil": "VENDEDOR",
            "comissao": 0.07,
        },
    ])
    usuarios.to_excel(ARQ_USUARIOS, index=False)

    if not os.path.exists(ARQ_CLIENTES):
        clientes = pd.DataFrame([
            {"codigo": 1, "cliente": "NELSON DAS GALAXIAS", "cnpj": "", "telefone": "", "cidade": ""},
            {"codigo": 2, "cliente": "DROGANNE MEDICAMENTOS E PERFUMARIA LTDA", "cnpj": "", "telefone": "", "cidade": ""},
            {"codigo": 3, "cliente": "NATURA TERRA COMERCIO E SERVICOS LTDA", "cnpj": "", "telefone": "", "cidade": ""},
            {"codigo": 4, "cliente": "TESTE DE GRAVIDEZ", "cnpj": "", "telefone": "", "cidade": ""},
        ])
        clientes.to_excel(ARQ_CLIENTES, index=False)

    if not os.path.exists(ARQ_PRODUTOS):
        produtos = pd.DataFrame([
            {"codigo": "68.0", "produto": "BENETONICO 500M", "un": "UN", "preco": 10.21, "fornecedor": "ARTE NATIVA", "imagem": ""},
            {"codigo": "103.0", "produto": "APIS FRESH SPRAY EXTRA FORTE 35ML", "un": "UN", "preco": 5.82, "fornecedor": "ARTE NATIVA", "imagem": ""},
            {"codigo": "126.0", "produto": "POTE DOCE BANANINHA ZERO AÇÚCAR", "un": "UN", "preco": 60.86, "fornecedor": "TIGRÃO", "imagem": ""},
            {"codigo": "94.0", "produto": "HALLS EXTRA FORTE 8 UN", "un": "UN", "preco": 12.17, "fornecedor": "MONDELEZ", "imagem": ""},
            {"codigo": "178.0", "produto": "BALDONI EXTRATO DE PROPOLIS VERDE 30ML", "un": "UN", "preco": 20.89, "fornecedor": "BALDONI", "imagem": ""},
        ])
        produtos.to_excel(ARQ_PRODUTOS, index=False)

    if not os.path.exists(ARQ_PEDIDOS):
        pedidos = pd.DataFrame(columns=[
            "pedido", "data", "vendedor", "cliente", "codigo", "produto", "un",
            "quantidade", "preco", "desconto", "subtotal", "total", "status"
        ])
        pedidos.to_excel(ARQ_PEDIDOS, index=False)


def ler_excel(caminho):
    try:
        return pd.read_excel(caminho)
    except Exception:
        return pd.DataFrame()


def salvar_excel(df, caminho):
    df.to_excel(caminho, index=False)


def dinheiro(valor):
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def numero_pedido():
    pedidos = ler_excel(ARQ_PEDIDOS)

    if len(pedidos) == 0 or "pedido" not in pedidos.columns:
        return 1

    maior = pd.to_numeric(pedidos["pedido"], errors="coerce").max()

    if pd.isna(maior):
        return 1

    return int(maior) + 1


def resumo_pedidos(pedidos):
    if len(pedidos) == 0 or "pedido" not in pedidos.columns:
        return pd.DataFrame(columns=["pedido", "data", "vendedor", "cliente", "total", "status"])

    return pedidos.groupby("pedido", as_index=False).agg({
        "data": "first",
        "vendedor": "first",
        "cliente": "first",
        "total": "sum",
        "status": "first",
    })


# =========================================================
# CSS / LAYOUT
# =========================================================

def css():
    st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"] {
        display:none !important;
    }

    [data-testid="stAppViewContainer"] {
        background:#f3f4f6 !important;
    }

    .block-container {
        max-width:1024px !important;
        padding:0 0 115px 0 !important;
    }

    * {
        font-family: Arial, sans-serif;
        box-sizing:border-box;
    }

    h1, h2, h3, p, label, span, div {
        color:#111827;
    }

    /* =========================
       LOGIN
    ========================= */

    .login-wrap {
        min-height:78vh;
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        padding:22px;
    }

    .login-logo {
        text-align:center;
        margin-bottom:34px;
    }

    .login-logo .tiger {
        font-size:70px;
        line-height:1;
        margin-bottom:12px;
    }

    .login-logo .name {
        font-size:54px;
        font-weight:1000;
        letter-spacing:2px;
        color:#111827;
    }

    .login-logo .sub {
        font-size:21px;
        color:#ff8500;
        letter-spacing:10px;
        font-weight:1000;
        margin-top:12px;
    }

    .login-box {
        width:100%;
        max-width:440px;
    }

    .login-box label {
        color:#111827 !important;
        font-weight:900 !important;
        font-size:15px !important;
    }

    .login-box input {
        background:white !important;
        border:2px solid #d1d5db !important;
        color:#111827 !important;
        height:56px !important;
        border-radius:18px !important;
        font-size:18px !important;
        font-weight:800 !important;
    }

    /* =========================
       TOPO
    ========================= */

    .topbar {
        background:#111;
        min-height:126px;
        padding:18px 40px;
        display:flex;
        align-items:center;
        justify-content:space-between;
        box-shadow:0 6px 22px rgba(0,0,0,.28);
    }

    .hamb {
        color:#ff8500 !important;
        font-size:40px;
        font-weight:1000;
        line-height:1;
    }

    .brand {
        display:flex;
        align-items:center;
        gap:14px;
        color:white !important;
    }

    .brand-icon {
        width:68px;
        height:68px;
        border:2px solid #fff;
        border-radius:50%;
        background:#111;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:42px;
    }

    .brand-name {
        color:white !important;
        font-size:42px;
        font-weight:1000;
        font-style:italic;
        letter-spacing:1px;
        line-height:1;
    }

    .brand-sub {
        color:#ff8500 !important;
        font-size:14px;
        font-weight:1000;
        letter-spacing:8px;
        margin-top:8px;
    }

    .perfil-pill {
        color:white !important;
        border:3px solid #ff8500;
        border-radius:35px;
        padding:12px 18px;
        font-size:18px;
        font-weight:1000;
        display:flex;
        align-items:center;
        gap:8px;
    }

    .hero {
        background:linear-gradient(135deg,#ff8500,#ff9d1c);
        padding:40px 40px 96px 40px;
        position:relative;
        overflow:hidden;
    }

    .hero::after {
        content:"🐯";
        position:absolute;
        right:62px;
        top:0px;
        font-size:185px;
        opacity:.14;
    }

    .hero h1 {
        margin:0;
        color:#111827 !important;
        font-size:46px;
        font-weight:1000;
        position:relative;
        z-index:2;
    }

    .hero p {
        color:#111827 !important;
        margin:12px 0 0 0;
        font-size:23px;
        font-weight:600;
        position:relative;
        z-index:2;
    }

    .conteudo {
        padding:0 28px;
        margin-top:-68px;
        position:relative;
        z-index:10;
    }

    .conteudo-normal {
        padding:32px 28px 0 28px;
        position:relative;
        z-index:10;
    }

    /* =========================
       CARDS
    ========================= */

    .cards {
        display:grid;
        grid-template-columns:repeat(3,1fr);
        gap:16px;
    }

    .metric-card {
        background:white;
        border-radius:24px;
        min-height:190px;
        padding:26px 16px;
        text-align:center;
        box-shadow:0 8px 24px rgba(15,23,42,.13);
    }

    .metric-icon {
        width:78px;
        height:78px;
        background:#111;
        border-radius:20px;
        color:#ff8500 !important;
        display:inline-flex;
        align-items:center;
        justify-content:center;
        font-size:40px;
        margin-bottom:14px;
    }

    .metric-title {
        color:#777 !important;
        font-size:17px;
        font-weight:1000;
    }

    .metric-value {
        color:#111827 !important;
        font-size:30px;
        font-weight:1000;
        margin-top:12px;
    }

    .metric-sub {
        color:#ff8500 !important;
        font-size:16px;
        font-weight:900;
        margin-top:12px;
    }

    .section-title {
        margin-top:34px;
        color:#111827 !important;
        font-size:32px;
        font-weight:1000;
        display:flex;
        align-items:center;
        gap:12px;
    }

    .section-line {
        width:80px;
        height:5px;
        border-radius:10px;
        background:#ff8500;
        margin:12px 0 24px 0;
    }

    .box {
        background:white;
        border-radius:24px;
        padding:22px;
        box-shadow:0 8px 24px rgba(15,23,42,.10);
        margin-bottom:18px;
        color:#111827 !important;
    }

    .box * {
        color:#111827 !important;
    }

    /* =========================
       TABELA DASHBOARD
    ========================= */

    .orders-table {
        background:white;
        border-radius:24px;
        padding:18px;
        box-shadow:0 8px 24px rgba(15,23,42,.10);
        overflow-x:auto;
    }

    .order-row {
        display:grid;
        grid-template-columns:90px 1.5fr 1.3fr 1.4fr 1fr;
        gap:12px;
        align-items:center;
        padding:16px 14px;
        border-bottom:1px solid #eee;
        font-size:16px;
    }

    .order-head {
        background:#111;
        color:#ff8500 !important;
        border-radius:16px 16px 0 0;
        font-weight:1000;
    }

    .order-head div {
        color:#ff8500 !important;
    }

    .money-orange {
        color:#ff8500 !important;
        font-weight:1000;
    }

    .status-pendente {
        background:#fff0bd;
        color:#9a6500 !important;
        padding:8px 10px;
        border-radius:10px;
        font-size:13px;
        font-weight:1000;
        text-align:center;
    }

    .status-faturado {
        background:#d8f7d1;
        color:#118022 !important;
        padding:8px 10px;
        border-radius:10px;
        font-size:13px;
        font-weight:1000;
        text-align:center;
    }

    /* =========================
       NOVO PEDIDO
    ========================= */

    .form-card {
        background:white;
        border-radius:24px;
        padding:22px;
        box-shadow:0 8px 24px rgba(15,23,42,.10);
        margin-bottom:22px;
    }

    .produto-preview {
        background:white;
        border:2px solid #ff8500;
        border-radius:18px;
        padding:14px;
        margin:14px 0;
        font-weight:800;
    }

    .produto-preview b {
        color:#0b8de3 !important;
    }

    .total-item {
        background:#0b8de3;
        border-radius:22px;
        padding:18px;
        text-align:center;
        margin:16px 0;
    }

    .total-item * {
        color:white !important;
    }

    .total-label {
        font-size:13px;
        font-weight:1000;
    }

    .total-value {
        font-size:36px;
        font-weight:1000;
        margin-top:8px;
    }

    /* =========================
       CARRINHO
    ========================= */

    .cart-client {
        background:white;
        border-radius:20px;
        padding:16px 22px;
        box-shadow:0 8px 22px rgba(15,23,42,.10);
        margin-bottom:20px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        font-size:23px;
        font-weight:800;
    }

    .cart-client b {
        color:#ff8500 !important;
        font-weight:1000;
    }

    .cart-panel {
        background:white;
        border-radius:24px;
        padding:24px 28px;
        box-shadow:0 8px 24px rgba(15,23,42,.13);
        margin-bottom:22px;
    }

    .cart-item {
        display:grid;
        grid-template-columns:135px 1fr;
        gap:22px;
        padding:18px 0;
        border-bottom:1px solid #e5e7eb;
    }

    .cart-item:last-child {
        border-bottom:none;
    }

    .cart-left {
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        gap:14px;
    }

    .product-img {
        width:95px;
        height:75px;
        border-radius:14px;
        background:#f3f4f6;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:52px;
        overflow:hidden;
    }

    .trash-red {
        width:60px;
        height:60px;
        border-radius:16px;
        background:linear-gradient(135deg,#ff3434,#df1f1f);
        color:white !important;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:30px;
        box-shadow:0 6px 14px rgba(239,68,68,.30);
    }

    .cart-name {
        color:#111827 !important;
        font-size:24px;
        font-weight:1000;
        line-height:1.15;
        margin-top:4px;
    }

    .cart-code {
        color:#6b7280 !important;
        font-size:19px;
        font-weight:700;
        margin-top:12px;
    }

    .cart-grid {
        display:grid;
        grid-template-columns:1fr 1fr 1fr;
        gap:18px;
        align-items:center;
        margin-top:26px;
    }

    .cart-label {
        color:#111827 !important;
        font-size:18px;
        font-weight:700;
        margin-bottom:10px;
    }

    .qty-box {
        display:flex;
        align-items:center;
        gap:18px;
    }

    .qty-btn {
        width:58px;
        height:58px;
        border-radius:14px;
        background:#f0f2f5;
        color:#2b7de9 !important;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:33px;
        font-weight:1000;
    }

    .qty-num {
        min-width:35px;
        text-align:center;
        color:#111827 !important;
        font-size:29px;
        font-weight:1000;
    }

    .cart-price {
        color:#111827 !important;
        font-size:26px;
        font-weight:1000;
    }

    .cart-total {
        color:#ff8500 !important;
        font-size:31px;
        font-weight:1000;
    }

    .resumo {
        background:linear-gradient(135deg,#111827,#10131a);
        border-radius:24px;
        padding:28px;
        box-shadow:0 8px 24px rgba(15,23,42,.16);
        margin-bottom:24px;
    }

    .resumo-row {
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:20px;
        font-size:28px;
        font-weight:1000;
    }

    .resumo-row span {
        color:white !important;
    }

    .resumo-row .orange-total {
        color:#ff8500 !important;
    }

    .resumo-line {
        height:1px;
        background:rgba(255,255,255,.22);
        margin:18px 0 24px 0;
    }

    .resumo-final {
        font-size:42px;
    }

    .btn-finalizar {
        background:linear-gradient(135deg,#2f8fe9,#2380d8);
        border-radius:18px;
        padding:22px;
        text-align:center;
        color:white !important;
        font-size:28px;
        font-weight:1000;
        margin-bottom:28px;
        box-shadow:0 7px 18px rgba(47,143,233,.28);
    }

    /* =========================
       BOTTOM NAV
    ========================= */

    .bottom-space {
        height:110px;
    }

    .bottom-nav {
        position:fixed;
        left:50%;
        bottom:0;
        transform:translateX(-50%);
        width:100%;
        max-width:1024px;
        background:#111;
        border-radius:28px 28px 0 0;
        padding:10px 18px 14px 18px;
        z-index:99999;
        box-shadow:0 -8px 24px rgba(0,0,0,.30);
    }

    .stButton > button {
        border-radius:16px !important;
        min-height:48px !important;
        font-weight:900 !important;
        border:none !important;
        background:#0b8de3 !important;
        color:white !important;
    }

    .bottom-nav .stButton > button {
        background:transparent !important;
        color:white !important;
        box-shadow:none !important;
        font-size:13px !important;
        padding:4px !important;
    }

    label {
        color:#111827 !important;
        font-weight:900 !important;
    }

    input, textarea {
        background:white !important;
        color:#111827 !important;
        border-radius:16px !important;
        min-height:50px !important;
        font-weight:800 !important;
    }

    div[data-baseweb="select"] > div {
        background:white !important;
        color:#111827 !important;
        border-radius:16px !important;
        min-height:50px !important;
    }

    div[data-baseweb="popover"] {
        z-index:9999999 !important;
    }

    div[data-baseweb="popover"] * {
        background:white !important;
        color:#111827 !important;
    }

    ul[role="listbox"] {
        background:white !important;
    }

    li[role="option"] {
        background:white !important;
        color:#111827 !important;
        font-weight:800 !important;
    }

    @media(max-width:720px) {
        .block-container {
            max-width:100% !important;
        }

        .topbar {
            min-height:105px;
            padding:16px 24px;
        }

        .hamb {
            font-size:34px;
        }

        .brand {
            gap:8px;
        }

        .brand-icon {
            width:48px;
            height:48px;
            font-size:30px;
        }

        .brand-name {
            font-size:31px;
        }

        .brand-sub {
            font-size:11px;
            letter-spacing:5px;
            margin-top:5px;
        }

        .perfil-pill {
            font-size:13px;
            padding:8px 12px;
        }

        .hero {
            padding:34px 32px 88px 32px;
        }

        .hero h1 {
            font-size:38px;
        }

        .hero p {
            font-size:18px;
        }

        .hero::after {
            right:15px;
            font-size:145px;
        }

        .conteudo {
            padding:0 18px;
            margin-top:-62px;
        }

        .conteudo-normal {
            padding:28px 18px 0 18px;
        }

        .cards {
            grid-template-columns:1fr;
        }

        .metric-card {
            min-height:145px;
        }

        .order-row {
            grid-template-columns:60px 1.2fr 1.2fr 1fr;
            font-size:13px;
        }

        .order-row div:nth-child(2) {
            display:none;
        }

        .section-title {
            font-size:34px;
        }

        .cart-client {
            font-size:18px;
            padding:14px 16px;
        }

        .cart-panel {
            padding:18px 16px;
        }

        .cart-item {
            grid-template-columns:82px 1fr;
            gap:14px;
            padding:18px 0;
        }

        .product-img {
            width:70px;
            height:58px;
            font-size:38px;
        }

        .trash-red {
            width:52px;
            height:52px;
            font-size:25px;
        }

        .cart-name {
            font-size:21px;
        }

        .cart-code {
            font-size:16px;
        }

        .cart-grid {
            grid-template-columns:1fr;
            gap:12px;
            margin-top:20px;
        }

        .cart-label {
            font-size:15px;
            margin-bottom:8px;
        }

        .qty-btn {
            width:46px;
            height:46px;
            font-size:28px;
        }

        .qty-num {
            font-size:25px;
        }

        .cart-price {
            font-size:24px;
        }

        .cart-total {
            font-size:27px;
        }

        .resumo-row {
            font-size:24px;
        }

        .resumo-final {
            font-size:35px;
        }

        .btn-finalizar {
            font-size:24px;
            padding:20px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# =========================================================
# LOGIN
# =========================================================

def login():
    if "logado" not in st.session_state:
        st.session_state.logado = False

    if st.session_state.logado:
        return

    st.markdown("""
    <div class="login-wrap">
        <div class="login-logo">
            <div class="tiger">🐯</div>
            <div class="name">TIGRÃO</div>
            <div class="sub">DISTRIBUIDORA</div>
        </div>
        <div class="login-box">
    """, unsafe_allow_html=True)

    usuario = st.text_input("Usuário", key="login_usuario")
    senha = st.text_input("Senha", type="password", key="login_senha")

    if st.button("ENTRAR", use_container_width=True):
        usuarios = ler_excel(ARQ_USUARIOS)

        usuarios["usuario"] = usuarios["usuario"].astype(str).str.strip().str.lower()
        usuarios["senha"] = usuarios["senha"].astype(str).str.strip()

        usuario_digitado = usuario.strip().lower()
        senha_digitada = senha.strip()

        achou = usuarios[
            (usuarios["usuario"] == usuario_digitado) &
            (usuarios["senha"] == senha_digitada)
        ]

        if len(achou) == 0:
            st.error("Usuário ou senha inválidos.")
        else:
            user = achou.iloc[0]
            st.session_state.logado = True
            st.session_state.usuario = str(user["usuario"])
            st.session_state.nome = str(user["nome"])
            st.session_state.perfil = str(user["perfil"]).upper()
            st.session_state.comissao = float(user.get("comissao", COMISSAO_PADRAO))
            st.session_state.menu = "Dashboard"
            st.session_state.carrinho = []
            st.session_state.form_key = 0
            st.rerun()

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# =========================================================
# UI
# =========================================================

def topo(titulo=None, subtitulo=None, mostrar_hero=True):
    perfil = st.session_state.get("perfil", "VENDEDOR")

    st.markdown(f"""
    <div class="topbar">
        <div class="hamb">☰</div>

        <div class="brand">
            <div class="brand-icon">🐯</div>
            <div>
                <div class="brand-name">TIGRÃO</div>
                <div class="brand-sub">DISTRIBUIDORA</div>
            </div>
        </div>

        <div class="perfil-pill">👤 {perfil}</div>
    </div>
    """, unsafe_allow_html=True)

    if mostrar_hero:
        st.markdown(f"""
        <div class="hero">
            <h1>{titulo}</h1>
            <p>{subtitulo}</p>
        </div>
        """, unsafe_allow_html=True)


def abrir(sobrepor=True):
    classe = "conteudo" if sobrepor else "conteudo-normal"
    st.markdown(f'<div class="{classe}">', unsafe_allow_html=True)


def fechar():
    st.markdown("</div>", unsafe_allow_html=True)


def mudar_menu(nome):
    st.session_state.menu = nome
    st.rerun()


def menu_inferior():
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)

    itens = [
        ("Dashboard", "📊 Dashboard"),
        ("Novo Pedido", "🛒 Novo Pedido"),
        ("Pedidos", "📋 Pedidos"),
        ("Comissão", "💰 Comissão"),
        ("Mais", "⋯ Mais"),
    ]

    cols = st.columns(len(itens))

    for col, (destino, texto) in zip(cols, itens):
        with col:
            if st.button(texto, key=f"nav_{destino}", use_container_width=True):
                mudar_menu(destino)

    st.markdown("</div>", unsafe_allow_html=True)


def produto_emoji(nome):
    nome = str(nome).upper()

    if "BANAN" in nome or "DOCE" in nome:
        return "🍯"
    if "HALLS" in nome or "MENTA" in nome or "BALAS" in nome:
        return "🍬"
    if "PROPOLIS" in nome or "SPRAY" in nome:
        return "🍶"
    if "CHA" in nome or "CHÁ" in nome:
        return "🍵"
    return "📦"


# =========================================================
# TELAS
# =========================================================

def dashboard():
    topo("Dashboard", "Visão geral da operação", mostrar_hero=True)
    abrir(sobrepor=True)

    pedidos = ler_excel(ARQ_PEDIDOS)
    vendedor = st.session_state.get("nome", "")
    perfil = st.session_state.get("perfil", "VENDEDOR")

    if len(pedidos) and perfil != "ADMIN":
        pedidos_view = pedidos[pedidos["vendedor"].astype(str) == vendedor].copy()
    else:
        pedidos_view = pedidos.copy()

    total_pedidos = pedidos_view["pedido"].nunique() if len(pedidos_view) else 0
    total_vendas = pedidos_view["total"].sum() if len(pedidos_view) else 0
    total_comissao = total_vendas * st.session_state.get("comissao", COMISSAO_PADRAO)

    st.markdown(f"""
    <div class="cards">
        <div class="metric-card">
            <div class="metric-icon">📋</div>
            <div class="metric-title">PEDIDOS</div>
            <div class="metric-value">{total_pedidos}</div>
            <div class="metric-sub">Total de pedidos</div>
        </div>

        <div class="metric-card">
            <div class="metric-icon">💲</div>
            <div class="metric-title">VENDAS</div>
            <div class="metric-value">{dinheiro(total_vendas)}</div>
            <div class="metric-sub">Valor total de vendas</div>
        </div>

        <div class="metric-card">
            <div class="metric-icon">%</div>
            <div class="metric-title">COMISSÃO 7%</div>
            <div class="metric-value">{dinheiro(total_comissao)}</div>
            <div class="metric-sub">Valor da comissão</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🕘 Últimos pedidos</div><div class="section-line"></div>', unsafe_allow_html=True)

    resumo = resumo_pedidos(pedidos_view).tail(6).sort_values("pedido", ascending=False)

    st.markdown('<div class="orders-table">', unsafe_allow_html=True)
    st.markdown("""
    <div class="order-row order-head">
        <div>PEDIDO</div>
        <div>DATA</div>
        <div>VENDEDOR</div>
        <div>CLIENTE</div>
        <div>TOTAL</div>
    </div>
    """, unsafe_allow_html=True)

    if len(resumo) == 0:
        st.info("Nenhum pedido lançado.")
    else:
        for _, row in resumo.iterrows():
            st.markdown(f"""
            <div class="order-row">
                <div>{row["pedido"]}</div>
                <div>{row["data"]}</div>
                <div>{row["vendedor"]}</div>
                <div>{row["cliente"]}</div>
                <div class="money-orange">{dinheiro(row["total"])}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    fechar()


def novo_pedido():
    topo("Novo Pedido", "Lançamento rápido de pedidos", mostrar_hero=True)
    abrir(sobrepor=True)

    clientes = ler_excel(ARQ_CLIENTES)
    produtos = ler_excel(ARQ_PRODUTOS)

    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    if "form_key" not in st.session_state:
        st.session_state.form_key = 0

    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    lista_clientes = clientes["cliente"].astype(str).tolist() if len(clientes) else ["CLIENTE PADRÃO"]

    cliente = st.selectbox("Cliente", lista_clientes, key="cliente_pedido")

    fornecedores = ["Todos"]

    if len(produtos) and "fornecedor" in produtos.columns:
        fornecedores += sorted(
            produtos["fornecedor"]
            .fillna("")
            .astype(str)
            .replace("", pd.NA)
            .dropna()
            .unique()
            .tolist()
        )

    fornecedor = st.selectbox("Fornecedor", fornecedores, key="fornecedor_pedido")

    if fornecedor != "Todos":
        produtos_filtrados = produtos[produtos["fornecedor"].astype(str) == fornecedor].copy()
    else:
        produtos_filtrados = produtos.copy()

    opcoes_produtos = ["Selecione o produto"]

    for _, row in produtos_filtrados.iterrows():
        opcoes_produtos.append(
            f'{row["codigo"]} - {row["produto"]} | {dinheiro(row["preco"])}'
        )

    produto_txt = st.selectbox(
        "Produto",
        opcoes_produtos,
        key=f"produto_pedido_{st.session_state.form_key}"
    )

    produto = None

    if produto_txt != "Selecione o produto":
        idx = opcoes_produtos.index(produto_txt) - 1
        produto = produtos_filtrados.iloc[idx].to_dict()

    if produto:
        st.markdown(f"""
        <div class="produto-preview">
            <b>{produto["produto"]}</b><br>
            Código: {produto["codigo"]}<br>
            Fornecedor: {produto["fornecedor"]}<br>
            Preço: <b>{dinheiro(produto["preco"])}</b>
        </div>
        """, unsafe_allow_html=True)

    qtd = st.number_input(
        "Quantidade",
        min_value=0,
        value=0,
        step=1,
        key=f"qtd_pedido_{st.session_state.form_key}"
    )

    desc = st.number_input(
        "% Desconto",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key=f"desc_pedido_{st.session_state.form_key}"
    )

    preco = float(produto["preco"]) if produto else 0
    subtotal = preco * qtd
    total = subtotal - (subtotal * desc / 100)

    st.markdown(f"""
    <div class="total-item">
        <div class="total-label">TOTAL DO ITEM</div>
        <div class="total-value">{dinheiro(total)}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("➕ ADICIONAR AO CARRINHO", use_container_width=True):
        if not produto:
            st.warning("Selecione um produto.")
        elif qtd <= 0:
            st.warning("Informe a quantidade.")
        else:
            st.session_state.carrinho.append({
                "codigo": produto["codigo"],
                "produto": produto["produto"],
                "un": produto.get("un", "UN"),
                "quantidade": qtd,
                "preco": preco,
                "desconto": desc,
                "subtotal": subtotal,
                "total": total,
            })

            st.session_state.form_key += 1
            st.success("Produto adicionado.")
            time.sleep(0.25)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    carrinho(cliente)
    fechar()


def carrinho(cliente):
    st.markdown('<div class="section-title">📦 Carrinho</div><div class="section-line"></div>', unsafe_allow_html=True)

    if len(st.session_state.carrinho) == 0:
        st.info("Nenhum produto adicionado.")
        return

    st.markdown(f"""
    <div class="cart-client">
        <div>👤 Cliente: <b>{cliente}</b></div>
        <div>⌄</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="cart-panel">', unsafe_allow_html=True)

    for i, item in enumerate(st.session_state.carrinho):
        nome = item["produto"]
        codigo = item["codigo"]
        qtd = int(item["quantidade"])
        preco = float(item["preco"])
        total = float(item["total"])
        emoji = produto_emoji(nome)

        st.markdown(f"""
        <div class="cart-item">
            <div class="cart-left">
                <div class="product-img">{emoji}</div>
                <div class="trash-red">🗑</div>
            </div>

            <div>
                <div class="cart-name">{nome}</div>
                <div class="cart-code">Cód: {codigo}</div>

                <div class="cart-grid">
                    <div>
                        <div class="cart-label">Quantidade</div>
                        <div class="qty-box">
                            <div class="qty-btn">−</div>
                            <div class="qty-num">{qtd}</div>
                            <div class="qty-btn">+</div>
                        </div>
                    </div>

                    <div>
                        <div class="cart-label">Preço unit.</div>
                        <div class="cart-price">{dinheiro(preco)}</div>
                    </div>

                    <div>
                        <div class="cart-label">Total</div>
                        <div class="cart-total">{dinheiro(total)}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Remover {nome}", key=f"remover_{i}", use_container_width=True):
            st.session_state.carrinho.pop(i)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    subtotal = sum(float(x["subtotal"]) for x in st.session_state.carrinho)
    total = sum(float(x["total"]) for x in st.session_state.carrinho)
    desconto = subtotal - total

    st.markdown(f"""
    <div class="resumo">
        <div class="resumo-row"><span>Subtotal</span><span>{dinheiro(subtotal)}</span></div>
        <div class="resumo-row"><span>Desconto</span><span class="orange-total">{dinheiro(desconto)}</span></div>
        <div class="resumo-line"></div>
        <div class="resumo-row resumo-final"><span>Total</span><span class="orange-total">{dinheiro(total)}</span></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✅ FINALIZAR PEDIDO", use_container_width=True):
        pedidos = ler_excel(ARQ_PEDIDOS)
        numero = numero_pedido()
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        vendedor = st.session_state.get("nome", "Vendedor")

        linhas = []

        for item in st.session_state.carrinho:
            linhas.append({
                "pedido": numero,
                "data": data,
                "vendedor": vendedor,
                "cliente": cliente,
                "codigo": item["codigo"],
                "produto": item["produto"],
                "un": item["un"],
                "quantidade": item["quantidade"],
                "preco": item["preco"],
                "desconto": item["desconto"],
                "subtotal": item["subtotal"],
                "total": item["total"],
                "status": "PENDENTE",
            })

        pedidos = pd.concat([pedidos, pd.DataFrame(linhas)], ignore_index=True)
        salvar_excel(pedidos, ARQ_PEDIDOS)

        st.session_state.carrinho = []
        st.session_state.form_key += 1

        st.success(f"Pedido nº {numero} salvo com sucesso!")
        time.sleep(0.8)
        st.rerun()

    if st.button("🧹 LIMPAR CARRINHO", use_container_width=True):
        st.session_state.carrinho = []
        st.session_state.form_key += 1
        st.rerun()


def pedidos_tela():
    topo("Pedidos", "Pedidos lançados", mostrar_hero=True)
    abrir(sobrepor=True)

    pedidos = ler_excel(ARQ_PEDIDOS)
    vendedor = st.session_state.get("nome", "")
    perfil = st.session_state.get("perfil", "VENDEDOR")

    if len(pedidos) and perfil != "ADMIN":
        pedidos = pedidos[pedidos["vendedor"].astype(str) == vendedor].copy()

    resumo = resumo_pedidos(pedidos).sort_values("pedido", ascending=False)

    if len(resumo) == 0:
        st.info("Nenhum pedido lançado.")
        fechar()
        return

    for _, row in resumo.iterrows():
        status = str(row["status"]).upper()

        st.markdown(f"""
        <div class="box">
            <b>Pedido #{row["pedido"]}</b><br>
            Cliente: {row["cliente"]}<br>
            Data: {row["data"]}<br>
            Total: <b style="color:#ff8500!important">{dinheiro(row["total"])}</b><br>
            Status: <b>{status}</b>
        </div>
        """, unsafe_allow_html=True)

        if status == "PENDENTE":
            if st.button(f"✏️ Editar pedido {row['pedido']}", key=f"edit_{row['pedido']}", use_container_width=True):
                st.session_state.pedido_editando = int(row["pedido"])
                st.session_state.menu = "Editar Pedido"
                st.rerun()

    fechar()


def editar_pedido():
    topo("Editar Pedido", "Alterar pedido pendente", mostrar_hero=True)
    abrir(sobrepor=True)

    numero = st.session_state.get("pedido_editando")
    pedidos = ler_excel(ARQ_PEDIDOS)
    dados = pedidos[pedidos["pedido"] == numero].copy()

    if len(dados) == 0:
        st.error("Pedido não encontrado.")
        fechar()
        return

    status = str(dados["status"].iloc[0]).upper()

    if status == "FATURADO" and st.session_state.get("perfil") != "ADMIN":
        st.error("Pedido faturado não pode ser alterado pelo vendedor.")
        fechar()
        return

    st.info(f"Pedido #{numero} - {dados['cliente'].iloc[0]}")

    novos = []

    for idx, row in dados.iterrows():
        st.markdown(f"### {row['produto']}")

        qtd = st.number_input(
            "Quantidade",
            min_value=0,
            value=int(row["quantidade"]),
            step=1,
            key=f"edit_qtd_{idx}"
        )

        desc = st.number_input(
            "% Desconto",
            min_value=0.0,
            value=float(row["desconto"]),
            step=1.0,
            key=f"edit_desc_{idx}"
        )

        preco = float(row["preco"])
        subtotal = preco * qtd
        total = subtotal - (subtotal * desc / 100)

        st.write(f"Total: **{dinheiro(total)}**")

        excluir = st.checkbox("Excluir item", key=f"excluir_{idx}")

        if not excluir and qtd > 0:
            item = row.to_dict()
            item["quantidade"] = qtd
            item["desconto"] = desc
            item["subtotal"] = subtotal
            item["total"] = total
            novos.append(item)

        st.divider()

    if st.button("💾 SALVAR ALTERAÇÕES", use_container_width=True):
        if len(novos) == 0:
            st.warning("Não é possível salvar pedido sem itens.")
            return

        pedidos = pedidos[pedidos["pedido"] != numero]
        pedidos = pd.concat([pedidos, pd.DataFrame(novos)], ignore_index=True)
        salvar_excel(pedidos, ARQ_PEDIDOS)

        st.success("Pedido atualizado.")
        time.sleep(0.8)
        st.session_state.menu = "Pedidos"
        st.rerun()

    if st.button("⬅️ VOLTAR", use_container_width=True):
        st.session_state.menu = "Pedidos"
        st.rerun()

    fechar()


def comissao_tela():
    topo("Comissão", "Resumo da comissão", mostrar_hero=True)
    abrir(sobrepor=True)

    pedidos = ler_excel(ARQ_PEDIDOS)
    vendedor = st.session_state.get("nome", "")

    if len(pedidos) and st.session_state.get("perfil") != "ADMIN":
        pedidos = pedidos[pedidos["vendedor"].astype(str) == vendedor].copy()

    vendas = pedidos["total"].sum() if len(pedidos) else 0
    comissao = vendas * st.session_state.get("comissao", COMISSAO_PADRAO)

    st.markdown(f"""
    <div class="cards">
        <div class="metric-card">
            <div class="metric-icon">💲</div>
            <div class="metric-title">VENDAS</div>
            <div class="metric-value">{dinheiro(vendas)}</div>
            <div class="metric-sub">Total vendido</div>
        </div>

        <div class="metric-card">
            <div class="metric-icon">%</div>
            <div class="metric-title">COMISSÃO</div>
            <div class="metric-value">{dinheiro(comissao)}</div>
            <div class="metric-sub">Comissão 7%</div>
        </div>

        <div class="metric-card">
            <div class="metric-icon">🎯</div>
            <div class="metric-title">META</div>
            <div class="metric-value">0%</div>
            <div class="metric-sub">Em breve</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fechar()


def mais_tela():
    topo("Mais", "Outras opções", mostrar_hero=True)
    abrir(sobrepor=True)

    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.write(f"**Usuário:** {st.session_state.get('nome')}")
    st.write(f"**Perfil:** {st.session_state.get('perfil')}")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚪 SAIR", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    fechar()


# =========================================================
# APP
# =========================================================

criar_banco()
css()
login()

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"

menu = st.session_state.menu

if menu == "Dashboard":
    dashboard()
elif menu == "Novo Pedido":
    novo_pedido()
elif menu == "Pedidos":
    pedidos_tela()
elif menu == "Editar Pedido":
    editar_pedido()
elif menu == "Comissão":
    comissao_tela()
elif menu == "Mais":
    mais_tela()

st.markdown('<div class="bottom-space"></div>', unsafe_allow_html=True)
menu_inferior()
