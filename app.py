import os
import time
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tigrão V2",
    page_icon="🐯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

PASTA_DADOS = "dados"
ARQ_CLIENTES = f"{PASTA_DADOS}/clientes.xlsx"
ARQ_PRODUTOS = f"{PASTA_DADOS}/produtos.xlsx"
ARQ_PEDIDOS = f"{PASTA_DADOS}/pedidos.xlsx"
ARQ_USUARIOS = f"{PASTA_DADOS}/usuarios.xlsx"

COMISSAO_PADRAO = 0.07


# =========================
# BANCO DE DADOS
# =========================

def criar_banco():
    os.makedirs(PASTA_DADOS, exist_ok=True)

    if not os.path.exists(ARQ_USUARIOS):
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
        ])
        clientes.to_excel(ARQ_CLIENTES, index=False)

    if not os.path.exists(ARQ_PRODUTOS):
        produtos = pd.DataFrame([
            {"codigo": "68.0", "produto": "BENETONICO 500M", "un": "UN", "preco": 10.21, "fornecedor": "ARTE NATIVA"},
            {"codigo": "103.0", "produto": "APIS FRESH SPRAY EXTRA FORTE 35ML", "un": "UN", "preco": 5.82, "fornecedor": "ARTE NATIVA"},
            {"codigo": "178.0", "produto": "BALDONI EXTRATO DE PROPOLIS VERDE 30ML", "un": "UN", "preco": 20.89, "fornecedor": "BALDONI"},
        ])
        produtos.to_excel(ARQ_PRODUTOS, index=False)

    if not os.path.exists(ARQ_PEDIDOS):
        pedidos = pd.DataFrame(columns=[
            "pedido", "data", "vendedor", "cliente", "codigo", "produto",
            "un", "quantidade", "preco", "desconto", "subtotal", "total", "status"
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
    try:
        return int(pd.to_numeric(pedidos["pedido"], errors="coerce").max()) + 1
    except Exception:
        return 1


# =========================
# ESTILO
# =========================

def css():
    st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"] {
        display:none !important;
    }

    .block-container {
        max-width: 980px !important;
        padding: 0 0 110px 0 !important;
    }

    [data-testid="stAppViewContainer"] {
        background: #f4f5f7 !important;
    }

    * {
        font-family: Arial, sans-serif;
    }

    .topo {
        background: linear-gradient(180deg, #111 0%, #191919 100%);
        padding: 24px 28px 0 28px;
        border-radius: 0 0 36px 36px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,.25);
    }

    .topo-linha {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: white;
    }

    .hamb {
        color: #ff8500;
        font-size: 34px;
        font-weight: 900;
    }

    .logo {
        text-align: center;
        color: white;
        font-size: 34px;
        font-weight: 1000;
        letter-spacing: 1px;
    }

    .logo small {
        display: block;
        color: #ff8500;
        font-size: 14px;
        letter-spacing: 7px;
        margin-top: 2px;
    }

    .perfil {
        border: 3px solid #ff8500;
        border-radius: 28px;
        color: white;
        padding: 10px 16px;
        font-weight: 900;
        font-size: 16px;
    }

    .hero {
        margin: 22px -28px 0 -28px;
        padding: 42px 38px 96px 38px;
        background: linear-gradient(135deg, #ff8500, #ff9d1c);
        position: relative;
        overflow: hidden;
    }

    .hero:after {
        content: "🐯";
        position: absolute;
        right: 25px;
        top: 12px;
        font-size: 180px;
        opacity: .14;
    }

    .hero h1 {
        margin: 0;
        color: #111;
        font-size: 46px;
        font-weight: 1000;
    }

    .hero p {
        color: #111;
        font-size: 22px;
        margin: 12px 0 0 0;
        font-weight: 500;
    }

    .conteudo {
        padding: 0 26px;
        margin-top: -64px;
        position: relative;
        z-index: 5;
    }

    .cards {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
    }

    .card-metrica {
        background: white;
        border-radius: 24px;
        padding: 24px 16px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(15,23,42,.12);
        min-height: 190px;
    }

    .icone {
        width: 78px;
        height: 78px;
        background: #111;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        color: #ff8500;
        font-size: 40px;
        margin-bottom: 14px;
    }

    .card-metrica .titulo {
        color: #777;
        font-size: 17px;
        font-weight: 900;
    }

    .card-metrica .valor {
        color: #111;
        font-size: 30px;
        font-weight: 1000;
        margin-top: 12px;
    }

    .card-metrica .sub {
        color: #ff8500;
        font-size: 16px;
        font-weight: 900;
        margin-top: 12px;
    }

    .secao {
        margin-top: 34px;
        color: #111;
        font-size: 30px;
        font-weight: 1000;
    }

    .linha-laranja {
        width: 56px;
        height: 4px;
        background: #ff8500;
        border-radius: 8px;
        margin-top: 8px;
        margin-bottom: 14px;
    }

    .tabela-box {
        background: white;
        border-radius: 22px;
        padding: 16px;
        box-shadow: 0 8px 24px rgba(15,23,42,.10);
        overflow-x: auto;
    }

    .linha-pedido {
        display: grid;
        grid-template-columns: 70px 1.4fr 1.7fr 1fr 120px;
        gap: 10px;
        align-items: center;
        padding: 15px 8px;
        border-bottom: 1px solid #eee;
        font-size: 15px;
    }

    .cabecalho {
        background: #111;
        color: #ff8500;
        border-radius: 14px 14px 0 0;
        font-weight: 1000;
    }

    .valor-laranja {
        color: #ff8500;
        font-weight: 1000;
    }

    .status-pendente {
        background: #fff0bd;
        color: #b07600;
        padding: 8px 10px;
        border-radius: 10px;
        font-weight: 900;
        text-align: center;
        font-size: 13px;
    }

    .status-faturado {
        background: #d8f7d1;
        color: #118022;
        padding: 8px 10px;
        border-radius: 10px;
        font-weight: 900;
        text-align: center;
        font-size: 13px;
    }

    .box {
        background: white;
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 8px 24px rgba(15,23,42,.10);
        margin-bottom: 18px;
    }

    .produto-card {
        border: 2px solid #ff8500;
        border-radius: 18px;
        padding: 14px;
        margin: 12px 0;
        background: white;
    }

    .produto-card b {
        color: #0b8de3;
    }

    .total-item {
        background: #0b8de3;
        color: white;
        border-radius: 22px;
        padding: 18px;
        text-align: center;
        margin: 14px 0;
    }

    .total-item .label {
        font-size: 13px;
        font-weight: 900;
    }

    .total-item .valor {
        font-size: 34px;
        font-weight: 1000;
        margin-top: 8px;
    }

    .resumo {
        background: #111827;
        color: white;
        border-radius: 22px;
        padding: 18px;
        margin-top: 16px;
    }

    .resumo-linha {
        display: flex;
        justify-content: space-between;
        font-weight: 900;
        margin-bottom: 10px;
    }

    .resumo-total {
        border-top: 1px solid rgba(255,255,255,.25);
        padding-top: 12px;
        font-size: 22px;
    }

    .bottom-space {
        height: 95px;
    }

    .bottom-nav {
        position: fixed;
        left: 50%;
        bottom: 0;
        transform: translateX(-50%);
        width: 100%;
        max-width: 980px;
        background: #111;
        border-radius: 28px 28px 0 0;
        padding: 10px 18px 14px 18px;
        z-index: 99999;
        box-shadow: 0 -8px 24px rgba(0,0,0,.28);
    }

    .stButton > button {
        border-radius: 16px !important;
        min-height: 46px !important;
        font-weight: 900 !important;
        border: none !important;
        background: #0b8de3 !important;
        color: white !important;
    }

    .bottom-nav .stButton > button {
        background: transparent !important;
        color: white !important;
        box-shadow: none !important;
        font-size: 13px !important;
    }

    input, textarea {
        border-radius: 16px !important;
        min-height: 48px !important;
        font-weight: 800 !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 16px !important;
        min-height: 48px !important;
    }

    div[data-baseweb="popover"] {
        z-index: 9999999 !important;
    }

    div[data-baseweb="popover"] * {
        background: white !important;
        color: #111827 !important;
    }

    ul[role="listbox"] {
        background: white !important;
    }

    li[role="option"] {
        background: white !important;
        color: #111827 !important;
        font-weight: 800 !important;
    }

    @media(max-width: 720px) {
        .block-container {
            max-width: 100% !important;
        }

        .topo {
            border-radius: 0 0 30px 30px;
            padding: 20px 18px 0 18px;
        }

        .logo {
            font-size: 24px;
        }

        .logo small {
            font-size: 10px;
            letter-spacing: 5px;
        }

        .perfil {
            font-size: 13px;
            padding: 8px 10px;
        }

        .hero {
            padding: 34px 26px 86px 26px;
        }

        .hero h1 {
            font-size: 36px;
        }

        .hero p {
            font-size: 18px;
        }

        .conteudo {
            padding: 0 18px;
        }

        .cards {
            grid-template-columns: 1fr;
        }

        .card-metrica {
            min-height: 140px;
        }

        .linha-pedido {
            grid-template-columns: 58px 1.2fr 1.4fr 1fr;
            font-size: 13px;
        }

        .linha-pedido div:nth-child(2) {
            display:none;
        }

        .secao {
            font-size: 28px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# =========================
# LOGIN
# =========================

def login():
    if "logado" not in st.session_state:
        st.session_state.logado = False

    if st.session_state.logado:
        return

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;">
        <div style="font-size:60px;">🐯</div>
        <h1 style="margin-bottom:0;">TIGRÃO</h1>
        <p style="color:#ff8500;font-weight:900;letter-spacing:5px;">DISTRIBUIDORA</p>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("ENTRAR", use_container_width=True):
            usuarios = ler_excel(ARQ_USUARIOS)

            achou = usuarios[
                (usuarios["usuario"].astype(str) == usuario) &
                (usuarios["senha"].astype(str) == senha)
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

    st.stop()


# =========================
# UI
# =========================

def topo(titulo, subtitulo):
    perfil = st.session_state.get("perfil", "VENDEDOR")

    st.markdown(f"""
    <div class="topo">
        <div class="topo-linha">
            <div class="hamb">☰</div>
            <div class="logo">
                🐯 TIGRÃO
                <small>DISTRIBUIDORA</small>
            </div>
            <div class="perfil">👤 {perfil}</div>
        </div>

        <div class="hero">
            <h1>{titulo}</h1>
            <p>{subtitulo}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def abrir():
    st.markdown('<div class="conteudo">', unsafe_allow_html=True)


def fechar():
    st.markdown('</div>', unsafe_allow_html=True)


def mudar_menu(nome):
    st.session_state.menu = nome
    st.rerun()


def menu_inferior():
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)

    if st.session_state.get("perfil") == "ADMIN":
        itens = [
            ("Dashboard", "🏠 Dashboard"),
            ("Novo Pedido", "🛒 Novo"),
            ("Pedidos", "📋 Pedidos"),
            ("Comissão", "💰 Comissão"),
            ("Mais", "⋯ Mais"),
        ]
    else:
        itens = [
            ("Dashboard", "🏠 Dashboard"),
            ("Novo Pedido", "🛒 Novo"),
            ("Pedidos", "📋 Pedidos"),
            ("Comissão", "💰 Comissão"),
            ("Mais", "⋯ Mais"),
        ]

    cols = st.columns(len(itens))

    for col, (destino, texto) in zip(cols, itens):
        with col:
            if st.button(texto, key=f"nav_{destino}", use_container_width=True):
                mudar_menu(destino)

    st.markdown('</div>', unsafe_allow_html=True)


# =========================
# TELAS
# =========================

def dashboard():
    topo("Dashboard", "Visão geral da operação")
    abrir()

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
        <div class="card-metrica">
            <div class="icone">📋</div>
            <div class="titulo">PEDIDOS</div>
            <div class="valor">{total_pedidos}</div>
            <div class="sub">Total de pedidos</div>
        </div>

        <div class="card-metrica">
            <div class="icone">💲</div>
            <div class="titulo">VENDAS</div>
            <div class="valor">{dinheiro(total_vendas)}</div>
            <div class="sub">Valor total de vendas</div>
        </div>

        <div class="card-metrica">
            <div class="icone">%</div>
            <div class="titulo">COMISSÃO 7%</div>
            <div class="valor">{dinheiro(total_comissao)}</div>
            <div class="sub">Valor da comissão</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="secao">🕘 Últimos pedidos</div><div class="linha-laranja"></div>', unsafe_allow_html=True)

    resumo = resumo_pedidos(pedidos_view).tail(6).sort_values("pedido", ascending=False)

    st.markdown('<div class="tabela-box">', unsafe_allow_html=True)
    st.markdown("""
    <div class="linha-pedido cabecalho">
        <div>PEDIDO</div>
        <div>DATA</div>
        <div>CLIENTE</div>
        <div>TOTAL</div>
        <div>STATUS</div>
    </div>
    """, unsafe_allow_html=True)

    if len(resumo) == 0:
        st.info("Nenhum pedido lançado.")
    else:
        for _, row in resumo.iterrows():
            status = str(row["status"]).upper()
            classe = "status-faturado" if status == "FATURADO" else "status-pendente"

            st.markdown(f"""
            <div class="linha-pedido">
                <div>{row["pedido"]}</div>
                <div>{row["data"]}</div>
                <div>{row["cliente"]}</div>
                <div class="valor-laranja">{dinheiro(row["total"])}</div>
                <div><span class="{classe}">{status}</span></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    fechar()


def resumo_pedidos(pedidos):
    if len(pedidos) == 0:
        return pd.DataFrame(columns=["pedido", "data", "vendedor", "cliente", "total", "status"])

    agrupado = pedidos.groupby("pedido", as_index=False).agg({
        "data": "first",
        "vendedor": "first",
        "cliente": "first",
        "total": "sum",
        "status": "first",
    })

    return agrupado


def novo_pedido():
    topo("Novo Pedido", "Lançamento rápido de pedidos")
    abrir()

    clientes = ler_excel(ARQ_CLIENTES)
    produtos = ler_excel(ARQ_PRODUTOS)

    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    if "form_key" not in st.session_state:
        st.session_state.form_key = 0

    with st.container():
        st.markdown('<div class="box">', unsafe_allow_html=True)

        lista_clientes = clientes["cliente"].astype(str).tolist() if len(clientes) else ["CLIENTE PADRÃO"]

        cliente = st.selectbox(
            "Cliente",
            lista_clientes,
            key="cliente_pedido"
        )

        fornecedores = ["Todos"] + sorted(
            produtos["fornecedor"].fillna("").astype(str).replace("", pd.NA).dropna().unique().tolist()
        )

        fornecedor = st.selectbox(
            "Fornecedor",
            fornecedores,
            key="fornecedor_pedido"
        )

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
            <div class="produto-card">
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
            <div class="label">TOTAL DO ITEM</div>
            <div class="valor">{dinheiro(total)}</div>
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
                time.sleep(0.3)
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    carrinho(cliente)

    fechar()


def carrinho(cliente):
    st.markdown('<div class="secao">📦 Carrinho</div><div class="linha-laranja"></div>', unsafe_allow_html=True)

    if len(st.session_state.carrinho) == 0:
        st.info("Nenhum produto adicionado.")
        return

    st.markdown('<div class="tabela-box">', unsafe_allow_html=True)

    st.markdown("""
    <div class="linha-pedido cabecalho" style="grid-template-columns:40px 1.8fr 70px 90px 90px;">
        <div>🗑</div>
        <div>PRODUTO</div>
        <div>QTD</div>
        <div>UNIT.</div>
        <div>TOTAL</div>
    </div>
    """, unsafe_allow_html=True)

    for i, item in enumerate(st.session_state.carrinho):
        col1, col2, col3, col4, col5 = st.columns([0.4, 2.4, 0.7, 1, 1])

        with col1:
            if st.button("🗑", key=f"del_{i}"):
                st.session_state.carrinho.pop(i)
                st.rerun()

        with col2:
            st.markdown(f"**{item['produto']}**  \n<small>Cód: {item['codigo']}</small>", unsafe_allow_html=True)

        with col3:
            st.write(int(item["quantidade"]))

        with col4:
            st.write(dinheiro(item["preco"]))

        with col5:
            st.markdown(f"<b style='color:#ff8500'>{dinheiro(item['total'])}</b>", unsafe_allow_html=True)

        st.divider()

    st.markdown('</div>', unsafe_allow_html=True)

    subtotal = sum([x["subtotal"] for x in st.session_state.carrinho])
    total = sum([x["total"] for x in st.session_state.carrinho])
    desconto = subtotal - total

    st.markdown(f"""
    <div class="resumo">
        <div class="resumo-linha"><span>Subtotal</span><span>{dinheiro(subtotal)}</span></div>
        <div class="resumo-linha"><span>Desconto</span><span>{dinheiro(desconto)}</span></div>
        <div class="resumo-linha resumo-total"><span>Total</span><span>{dinheiro(total)}</span></div>
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
    topo("Pedidos", "Pedidos lançados")
    abrir()

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

        with st.container():
            st.markdown(f"""
            <div class="box">
                <b>Pedido #{row["pedido"]}</b><br>
                Cliente: {row["cliente"]}<br>
                Data: {row["data"]}<br>
                Total: <b style="color:#ff8500">{dinheiro(row["total"])}</b><br>
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
    topo("Editar Pedido", "Alterar pedido pendente")
    abrir()

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
    topo("Comissão", "Resumo da comissão")
    abrir()

    pedidos = ler_excel(ARQ_PEDIDOS)
    vendedor = st.session_state.get("nome", "")

    if len(pedidos):
        pedidos = pedidos[pedidos["vendedor"].astype(str) == vendedor].copy()

    vendas = pedidos["total"].sum() if len(pedidos) else 0
    comissao = vendas * st.session_state.get("comissao", COMISSAO_PADRAO)

    st.markdown(f"""
    <div class="cards">
        <div class="card-metrica">
            <div class="icone">💲</div>
            <div class="titulo">VENDAS</div>
            <div class="valor">{dinheiro(vendas)}</div>
            <div class="sub">Total vendido</div>
        </div>

        <div class="card-metrica">
            <div class="icone">%</div>
            <div class="titulo">COMISSÃO</div>
            <div class="valor">{dinheiro(comissao)}</div>
            <div class="sub">Comissão 7%</div>
        </div>

        <div class="card-metrica">
            <div class="icone">🎯</div>
            <div class="titulo">META</div>
            <div class="valor">0%</div>
            <div class="sub">Em breve</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fechar()


def mais_tela():
    topo("Mais", "Outras opções")
    abrir()

    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.write(f"**Usuário:** {st.session_state.get('nome')}")
    st.write(f"**Perfil:** {st.session_state.get('perfil')}")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚪 SAIR", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    fechar()


# =========================
# APP
# =========================

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
