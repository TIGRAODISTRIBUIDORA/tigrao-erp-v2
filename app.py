import os
import time
from datetime import datetime

import pandas as pd
import streamlit as st

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


def criar_banco():
    os.makedirs(PASTA_DADOS, exist_ok=True)

    usuarios = pd.DataFrame([
        {"usuario": "admin", "senha": "admin123", "nome": "Administrador", "perfil": "ADMIN", "comissao": 0.07},
        {"usuario": "vendedor", "senha": "123", "nome": "Vendedor", "perfil": "VENDEDOR", "comissao": 0.07},
    ])
    usuarios.to_excel(ARQ_USUARIOS, index=False)

    if not os.path.exists(ARQ_CLIENTES):
        pd.DataFrame([
            {"codigo": 1, "cliente": "NELSON DAS GALAXIAS", "cnpj": "", "telefone": "", "cidade": ""},
            {"codigo": 2, "cliente": "DROGANNE MEDICAMENTOS E PERFUMARIA LTDA", "cnpj": "", "telefone": "", "cidade": ""},
            {"codigo": 3, "cliente": "NATURA TERRA COMERCIO E SERVICOS LTDA", "cnpj": "", "telefone": "", "cidade": ""},
        ]).to_excel(ARQ_CLIENTES, index=False)

    if not os.path.exists(ARQ_PRODUTOS):
        pd.DataFrame([
            {"codigo": "68.0", "produto": "BENETONICO 500M", "un": "UN", "preco": 10.21, "fornecedor": "ARTE NATIVA"},
            {"codigo": "103.0", "produto": "APIS FRESH SPRAY EXTRA FORTE 35ML", "un": "UN", "preco": 5.82, "fornecedor": "ARTE NATIVA"},
            {"codigo": "178.0", "produto": "BALDONI EXTRATO DE PROPOLIS VERDE 30ML", "un": "UN", "preco": 20.89, "fornecedor": "BALDONI"},
        ]).to_excel(ARQ_PRODUTOS, index=False)

    if not os.path.exists(ARQ_PEDIDOS):
        pd.DataFrame(columns=[
            "pedido", "data", "vendedor", "cliente", "codigo", "produto",
            "un", "quantidade", "preco", "desconto", "subtotal", "total", "status"
        ]).to_excel(ARQ_PEDIDOS, index=False)


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


def css():
    st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"] {display:none!important;}
    [data-testid="stAppViewContainer"] {background:#f4f5f7!important;}
    .block-container {max-width:1024px!important;padding:0 0 118px 0!important;}
    * {font-family:Arial, sans-serif;}

    .top-wrap {
        background:#111;
        border-radius:0 0 36px 36px;
        overflow:hidden;
        box-shadow:0 10px 28px rgba(0,0,0,.28);
    }

    .top-black {
        background:linear-gradient(180deg,#111,#1a1a1a);
        padding:22px 36px 10px 36px;
        position:relative;
    }

    .top-row {
        display:flex;
        justify-content:space-between;
        align-items:center;
        color:white;
    }

    .hamb {
        color:#ff8500;
        font-size:38px;
        font-weight:1000;
    }

    .brand {
        display:flex;
        align-items:center;
        gap:12px;
        justify-content:center;
        color:white;
        font-weight:1000;
        font-size:38px;
        letter-spacing:2px;
    }

    .brand .tiger {
        width:66px;
        height:66px;
        border:2px solid white;
        border-radius:50%;
        display:flex;
        align-items:center;
        justify-content:center;
        font-size:42px;
        background:#111;
    }

    .brand small {
        display:block;
        color:#ff8500;
        font-size:13px;
        letter-spacing:8px;
        margin-top:2px;
    }

    .perfil {
        border:3px solid #ff8500;
        border-radius:30px;
        color:white;
        padding:10px 17px;
        font-weight:1000;
        font-size:16px;
    }

    .orange {
        background:linear-gradient(135deg,#ff8500,#ff9d1c);
        padding:40px 40px 96px 40px;
        position:relative;
        overflow:hidden;
        border-radius:0 0 0 0;
    }

    .orange:before {
        content:"";
        position:absolute;
        top:-30px;
        left:0;
        width:100%;
        height:58px;
        background:#111;
        border-radius:0 0 50% 50%;
        z-index:1;
    }

    .orange:after {
        content:"🐯";
        position:absolute;
        right:70px;
        top:8px;
        font-size:180px;
        opacity:.13;
    }

    .orange h1 {
        margin:0;
        color:#111;
        font-size:46px;
        font-weight:1000;
        position:relative;
        z-index:2;
    }

    .orange p {
        margin:12px 0 0 0;
        color:#111;
        font-size:22px;
        font-weight:500;
        position:relative;
        z-index:2;
    }

    .conteudo {
        padding:0 28px;
        margin-top:-68px;
        position:relative;
        z-index:10;
    }

    .cards {
        display:grid;
        grid-template-columns:repeat(3,1fr);
        gap:16px;
    }

    .metric-card {
        background:white;
        border-radius:24px;
        padding:26px 16px;
        min-height:190px;
        text-align:center;
        box-shadow:0 8px 24px rgba(15,23,42,.13);
    }

    .metric-icon {
        width:78px;
        height:78px;
        background:#111;
        border-radius:20px;
        display:inline-flex;
        align-items:center;
        justify-content:center;
        color:#ff8500;
        font-size:40px;
        margin-bottom:14px;
    }

    .metric-title {
        color:#777;
        font-size:17px;
        font-weight:1000;
    }

    .metric-value {
        color:#111;
        font-size:30px;
        font-weight:1000;
        margin-top:12px;
    }

    .metric-sub {
        color:#ff8500;
        font-size:16px;
        font-weight:900;
        margin-top:12px;
    }

    .secao {
        margin-top:34px;
        color:#111;
        font-size:30px;
        font-weight:1000;
    }

    .linha-laranja {
        width:56px;
        height:4px;
        background:#ff8500;
        border-radius:8px;
        margin:8px 0 14px 0;
    }

    .box, .table-box {
        background:white;
        border-radius:24px;
        padding:18px;
        box-shadow:0 8px 24px rgba(15,23,42,.10);
        margin-bottom:18px;
        color:#111827!important;
    }

    .box * {color:#111827!important;}

    .order-grid {
        display:grid;
        grid-template-columns:80px 1.4fr 1.5fr 1fr 110px;
        gap:10px;
        align-items:center;
        padding:15px 12px;
        border-bottom:1px solid #eee;
        font-size:15px;
        color:#111;
    }

    .order-head {
        background:#111;
        color:#ff8500!important;
        border-radius:16px 16px 0 0;
        font-weight:1000;
    }

    .orange-money {
        color:#ff8500!important;
        font-weight:1000;
    }

    .pill-pendente {
        background:#fff0bd;
        color:#9a6500!important;
        padding:8px 10px;
        border-radius:10px;
        font-weight:1000;
        text-align:center;
        font-size:13px;
    }

    .pill-faturado {
        background:#d8f7d1;
        color:#118022!important;
        padding:8px 10px;
        border-radius:10px;
        font-weight:1000;
        text-align:center;
        font-size:13px;
    }

    .produto-card {
        border:2px solid #ff8500;
        border-radius:18px;
        padding:14px;
        margin:12px 0;
        background:white;
        color:#111827;
        font-weight:800;
    }

    .produto-card b {color:#0b8de3!important;}

    .total-item {
        background:#0b8de3;
        border-radius:22px;
        padding:18px;
        text-align:center;
        margin:14px 0;
    }

    .total-item * {color:white!important;}
    .total-label {font-size:13px;font-weight:1000;}
    .total-value {font-size:34px;font-weight:1000;margin-top:8px;}

    .resumo {
        background:#111827;
        border-radius:22px;
        padding:18px;
        margin-top:16px;
    }

    .resumo * {color:white!important;}
    .resumo-row {display:flex;justify-content:space-between;font-weight:1000;margin-bottom:10px;}
    .resumo-total {border-top:1px solid rgba(255,255,255,.25);padding-top:12px;font-size:22px;}

    .bottom-space {height:100px;}

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
        border-radius:16px!important;
        min-height:46px!important;
        font-weight:900!important;
        border:none!important;
        background:#0b8de3!important;
        color:white!important;
    }

    .bottom-nav .stButton > button {
        background:transparent!important;
        color:white!important;
        box-shadow:none!important;
        font-size:13px!important;
        padding:4px!important;
    }

    input, textarea {border-radius:16px!important;min-height:48px!important;font-weight:800!important;}
    div[data-baseweb="select"] > div {border-radius:16px!important;min-height:48px!important;}
    div[data-baseweb="popover"] {z-index:9999999!important;}
    div[data-baseweb="popover"] * {background:white!important;color:#111827!important;}
    ul[role="listbox"] {background:white!important;}
    li[role="option"] {background:white!important;color:#111827!important;font-weight:800!important;}

    @media(max-width:720px) {
        .block-container {max-width:100%!important;}
        .top-black {padding:20px 26px 8px 26px;}
        .hamb {font-size:32px;}
        .brand {font-size:30px;gap:8px;}
        .brand .tiger {width:46px;height:46px;font-size:30px;}
        .brand small {font-size:11px;letter-spacing:6px;}
        .perfil {font-size:13px;padding:8px 12px;}
        .orange {padding:34px 32px 86px 32px;}
        .orange h1 {font-size:36px;}
        .orange p {font-size:18px;}
        .orange:after {right:20px;font-size:150px;}
        .conteudo {padding:0 18px;margin-top:-62px;}
        .cards {grid-template-columns:1fr;}
        .metric-card {min-height:140px;}
        .order-grid {grid-template-columns:58px 1.2fr 1.4fr 1fr;font-size:13px;}
        .order-grid div:nth-child(2) {display:none;}
        .secao {font-size:28px;}
    }
    </style>
    """, unsafe_allow_html=True)


def login():
    if "logado" not in st.session_state:
        st.session_state.logado = False

    if st.session_state.logado:
        return

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;">
        <div style="font-size:70px;">🐯</div>
        <h1 style="margin-bottom:0;color:#111;">TIGRÃO</h1>
        <p style="color:#ff8500;font-weight:1000;letter-spacing:5px;">DISTRIBUIDORA</p>
    </div>
    """, unsafe_allow_html=True)

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

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

    st.stop()


def topo(titulo, subtitulo):
    perfil = st.session_state.get("perfil", "VENDEDOR")

    html = f"""
    <div class="top-wrap">
        <div class="top-black">
            <div class="top-row">
                <div class="hamb">☰</div>
                <div class="brand">
                    <div class="tiger">🐯</div>
                    <div>
                        TIGRÃO
                        <small>DISTRIBUIDORA</small>
                    </div>
                </div>
                <div class="perfil">👤 {perfil}</div>
            </div>
        </div>
        <div class="orange">
            <h1>{titulo}</h1>
            <p>{subtitulo}</p>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def abrir():
    st.markdown('<div class="conteudo">', unsafe_allow_html=True)


def fechar():
    st.markdown('</div>', unsafe_allow_html=True)


def mudar_menu(nome):
    st.session_state.menu = nome
    st.rerun()


def menu_inferior():
    st.markdown('<div class="bottom-nav">', unsafe_allow_html=True)

    itens = [
        ("Dashboard", "📊 Dashboard"),
        ("Novo Pedido", "🛒 Novo Pedido"),
        ("Pedidos", "📦 Pedidos"),
        ("Comissão", "💰 Comissão"),
        ("Mais", "⋯ Mais"),
    ]

    cols = st.columns(len(itens))
    for col, (destino, texto) in zip(cols, itens):
        with col:
            if st.button(texto, key=f"nav_{destino}", use_container_width=True):
                mudar_menu(destino)

    st.markdown("</div>", unsafe_allow_html=True)


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

    st.markdown('<div class="secao">🕘 Últimos pedidos</div><div class="linha-laranja"></div>', unsafe_allow_html=True)

    resumo = resumo_pedidos(pedidos_view).tail(6).sort_values("pedido", ascending=False)

    st.markdown('<div class="table-box">', unsafe_allow_html=True)
    st.markdown("""
    <div class="order-grid order-head">
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
            classe = "pill-faturado" if status == "FATURADO" else "pill-pendente"
            st.markdown(f"""
            <div class="order-grid">
                <div>{row["pedido"]}</div>
                <div>{row["data"]}</div>
                <div>{row["cliente"]}</div>
                <div class="orange-money">{dinheiro(row["total"])}</div>
                <div><span class="{classe}">{status}</span></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    fechar()


def novo_pedido():
    topo("Novo Pedido", "Lançamento rápido de pedidos")
    abrir()

    clientes = ler_excel(ARQ_CLIENTES)
    produtos = ler_excel(ARQ_PRODUTOS)

    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    if "form_key" not in st.session_state:
        st.session_state.form_key = 0

    st.markdown('<div class="box">', unsafe_allow_html=True)

    lista_clientes = clientes["cliente"].astype(str).tolist() if len(clientes) else ["CLIENTE PADRÃO"]
    cliente = st.selectbox("Cliente", lista_clientes, key="cliente_pedido")

    fornecedores = ["Todos"]
    if len(produtos) and "fornecedor" in produtos.columns:
        fornecedores += sorted(produtos["fornecedor"].fillna("").astype(str).replace("", pd.NA).dropna().unique().tolist())

    fornecedor = st.selectbox("Fornecedor", fornecedores, key="fornecedor_pedido")

    if fornecedor != "Todos":
        produtos_filtrados = produtos[produtos["fornecedor"].astype(str) == fornecedor].copy()
    else:
        produtos_filtrados = produtos.copy()

    opcoes_produtos = ["Selecione o produto"]
    for _, row in produtos_filtrados.iterrows():
        opcoes_produtos.append(f'{row["codigo"]} - {row["produto"]} | {dinheiro(row["preco"])}')

    produto_txt = st.selectbox("Produto", opcoes_produtos, key=f"produto_pedido_{st.session_state.form_key}")

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

    qtd = st.number_input("Quantidade", min_value=0, value=0, step=1, key=f"qtd_pedido_{st.session_state.form_key}")
    desc = st.number_input("% Desconto", min_value=0.0, value=0.0, step=1.0, key=f"desc_pedido_{st.session_state.form_key}")

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
            time.sleep(0.3)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    carrinho(cliente)
    fechar()


def carrinho(cliente):
    st.markdown('<div class="secao">📦 Carrinho</div><div class="linha-laranja"></div>', unsafe_allow_html=True)

    if len(st.session_state.carrinho) == 0:
        st.info("Nenhum produto adicionado.")
        return

    st.markdown('<div class="table-box">', unsafe_allow_html=True)
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

    st.markdown("</div>", unsafe_allow_html=True)

    subtotal = sum(x["subtotal"] for x in st.session_state.carrinho)
    total = sum(x["total"] for x in st.session_state.carrinho)
    desconto = subtotal - total

    st.markdown(f"""
    <div class="resumo">
        <div class="resumo-row"><span>Subtotal</span><span>{dinheiro(subtotal)}</span></div>
        <div class="resumo-row"><span>Desconto</span><span>{dinheiro(desconto)}</span></div>
        <div class="resumo-row resumo-total"><span>Total</span><span>{dinheiro(total)}</span></div>
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

        qtd = st.number_input("Quantidade", min_value=0, value=int(row["quantidade"]), step=1, key=f"edit_qtd_{idx}")
        desc = st.number_input("% Desconto", min_value=0.0, value=float(row["desconto"]), step=1.0, key=f"edit_desc_{idx}")

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
    topo("Comissão", "Resumo da comissão")
    abrir()

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
    topo("Mais", "Outras opções")
    abrir()

    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.write(f"**Usuário:** {st.session_state.get('nome')}")
    st.write(f"**Perfil:** {st.session_state.get('perfil')}")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚪 SAIR", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    fechar()


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
