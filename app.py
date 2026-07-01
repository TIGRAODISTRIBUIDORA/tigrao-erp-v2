import os
import time
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tigrão App",
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


# =========================
# BANCO
# =========================

def criar_banco():
    os.makedirs(PASTA_DADOS, exist_ok=True)

    if not os.path.exists(ARQ_USUARIOS):
        pd.DataFrame([
            {"usuario": "admin", "senha": "admin123", "nome": "Administrador", "perfil": "ADMIN", "comissao": 0.07},
            {"usuario": "vendedor", "senha": "123", "nome": "Vendedor", "perfil": "VENDEDOR", "comissao": 0.07},
        ]).to_excel(ARQ_USUARIOS, index=False)

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


def safe_float(valor):
    try:
        return float(valor)
    except Exception:
        return 0.0


def numero_pedido():
    pedidos = ler_excel(ARQ_PEDIDOS)

    if len(pedidos) == 0 or "pedido" not in pedidos.columns:
        return 1

    maior = pd.to_numeric(pedidos["pedido"], errors="coerce").max()

    return 1 if pd.isna(maior) else int(maior) + 1


def resumo_pedidos(pedidos):
    if len(pedidos) == 0 or "pedido" not in pedidos.columns:
        return pd.DataFrame(columns=["pedido", "data", "vendedor", "cliente", "total", "status"])

    pedidos = pedidos.copy()
    pedidos["total"] = pd.to_numeric(pedidos["total"], errors="coerce").fillna(0)

    return pedidos.groupby("pedido", as_index=False).agg({
        "data": "first",
        "vendedor": "first",
        "cliente": "first",
        "total": "sum",
        "status": "first",
    })


def filtrar_por_usuario(pedidos):
    if len(pedidos) == 0:
        return pedidos

    if st.session_state.get("perfil") != "ADMIN":
        vendedor = st.session_state.get("nome", "")
        pedidos = pedidos[pedidos["vendedor"].astype(str) == vendedor].copy()

    return pedidos


# =========================
# CSS LEVE / NATIVO
# =========================

def css():
    st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"] {
        display:none !important;
    }

    [data-testid="stAppViewContainer"] {
        background:#f4f5f7 !important;
    }

    .block-container {
        max-width:520px !important;
        padding-top:12px !important;
        padding-bottom:35px !important;
    }

    .stButton > button {
        border-radius:16px !important;
        min-height:46px !important;
        font-weight:800 !important;
        border:0 !important;
        background:#0b8de3 !important;
        color:white !important;
    }

    div[data-testid="stMetric"] {
        background:white;
        padding:14px;
        border-radius:18px;
        box-shadow:0 5px 16px rgba(0,0,0,.08);
    }

    div[data-testid="stMetricLabel"] {
        font-weight:900;
    }

    input, textarea {
        border-radius:14px !important;
        min-height:46px !important;
        font-weight:700 !important;
    }

    div[data-baseweb="select"] > div {
        border-radius:14px !important;
        min-height:46px !important;
    }

    .titulo-app {
        background:#111;
        border-radius:22px;
        padding:18px;
        color:white;
        text-align:center;
        margin-bottom:10px;
    }

    .titulo-app h1 {
        color:white !important;
        font-size:28px;
        margin:0;
        padding:0;
    }

    .titulo-app p {
        color:#ff8500 !important;
        font-weight:900;
        letter-spacing:3px;
        margin:4px 0 0 0;
    }

    .faixa {
        background:#ff8500;
        color:#111;
        border-radius:22px;
        padding:18px;
        margin-bottom:16px;
    }

    .faixa h2 {
        color:#111 !important;
        font-size:28px;
        margin:0 0 4px 0;
        padding:0;
    }

    .faixa p {
        color:#111 !important;
        font-weight:800;
        margin:0;
    }

    .card {
        background:white;
        border-radius:18px;
        padding:14px;
        box-shadow:0 5px 16px rgba(0,0,0,.08);
        margin-bottom:12px;
        border-left:5px solid #ff8500;
        color:#111;
    }

    .card b {
        color:#111 !important;
    }

    .valor {
        color:#ff8500 !important;
        font-weight:900;
        font-size:20px;
    }

    .resumo-box {
        background:#111827;
        border-radius:18px;
        padding:14px;
        color:white;
        margin-top:12px;
    }

    .resumo-box p {
        color:white !important;
        margin:5px 0;
        font-weight:800;
    }

    .subtitulo {
        font-size:24px;
        font-weight:900;
        margin:18px 0 8px 0;
        color:#111;
    }

    .linha-laranja {
        width:48px;
        height:4px;
        border-radius:4px;
        background:#ff8500;
        margin-bottom:12px;
    }
    </style>
    """, unsafe_allow_html=True)


# =========================
# SESSÃO / NAVEGAÇÃO
# =========================

def iniciar_sessao():
    if "logado" not in st.session_state:
        st.session_state.logado = False

    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []


def ir_para(page):
    st.session_state.page = page
    st.rerun()


def topo(titulo, subtitulo):
    perfil = st.session_state.get("perfil", "VENDEDOR")

    st.markdown("""
    <div class="titulo-app">
        <h1>🐯 TIGRÃO</h1>
        <p>DISTRIBUIDORA</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="faixa">
        <h2>{titulo}</h2>
        <p>{subtitulo} • {perfil}</p>
    </div>
    """, unsafe_allow_html=True)


def menu_nativo():
    st.divider()

    col1, col2, col3, col4, col5 = st.columns(5, gap="small")

    with col1:
        if st.button("🏠", key="nav_inicio", use_container_width=True):
            ir_para("dashboard")

    with col2:
        if st.button("🛒", key="nav_novo", use_container_width=True):
            ir_para("novo")

    with col3:
        if st.button("📋", key="nav_pedidos", use_container_width=True):
            ir_para("pedidos")

    with col4:
        if st.button("💰", key="nav_comissao", use_container_width=True):
            ir_para("comissao")

    with col5:
        if st.button("☰", key="nav_mais", use_container_width=True):
            ir_para("mais")


# =========================
# LOGIN
# =========================

def login():
    if st.session_state.logado:
        return

    st.markdown("""
    <div class="titulo-app">
        <h1>🐯 TIGRÃO</h1>
        <p>DISTRIBUIDORA</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Entrar no sistema")

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("ENTRAR", use_container_width=True):
        usuarios = ler_excel(ARQ_USUARIOS)

        if len(usuarios) == 0:
            st.error("Base de usuários não encontrada.")
            st.stop()

        usuarios["usuario"] = usuarios["usuario"].astype(str).str.strip().str.lower()
        usuarios["senha"] = usuarios["senha"].astype(str).str.strip()

        achou = usuarios[
            (usuarios["usuario"] == usuario.strip().lower()) &
            (usuarios["senha"] == senha.strip())
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
            st.session_state.page = "dashboard"
            st.session_state.carrinho = []
            st.rerun()

    st.info("Admin: admin / admin123  |  Vendedor: vendedor / 123")
    st.stop()


# =========================
# TELAS
# =========================

def dashboard():
    topo("Dashboard", "Resumo da operação")

    pedidos = filtrar_por_usuario(ler_excel(ARQ_PEDIDOS))

    if len(pedidos):
        pedidos["total"] = pd.to_numeric(pedidos["total"], errors="coerce").fillna(0)

    total_pedidos = pedidos["pedido"].nunique() if len(pedidos) else 0
    total_vendas = pedidos["total"].sum() if len(pedidos) else 0
    total_comissao = total_vendas * st.session_state.get("comissao", COMISSAO_PADRAO)

    c1, c2 = st.columns(2)
    c1.metric("Pedidos", total_pedidos)
    c2.metric("Comissão", dinheiro(total_comissao))

    st.metric("Vendas", dinheiro(total_vendas))

    st.markdown('<div class="subtitulo">🕘 Últimos pedidos</div><div class="linha-laranja"></div>', unsafe_allow_html=True)

    resumo = resumo_pedidos(pedidos).sort_values("pedido", ascending=False).head(5)

    if len(resumo) == 0:
        st.info("Nenhum pedido lançado.")
    else:
        for _, row in resumo.iterrows():
            st.markdown(f"""
            <div class="card">
                <b>Pedido #{row["pedido"]}</b><br>
                Cliente: {row["cliente"]}<br>
                Data: {row["data"]}<br>
                <span class="valor">{dinheiro(row["total"])}</span> — {row["status"]}
            </div>
            """, unsafe_allow_html=True)


def novo_pedido():
    topo("Novo Pedido", "Lançamento pelo celular")

    clientes = ler_excel(ARQ_CLIENTES)
    produtos = ler_excel(ARQ_PRODUTOS)

    busca_cliente = st.text_input("Buscar cliente", placeholder="Digite nome, código ou iniciais")

    clientes_filtrados = clientes.copy()
    if len(clientes_filtrados) and busca_cliente.strip():
        termo = busca_cliente.strip().lower()
        clientes_filtrados = clientes[
            clientes["cliente"].astype(str).str.lower().str.contains(termo, na=False) |
            clientes["codigo"].astype(str).str.lower().str.contains(termo, na=False) |
            clientes["cnpj"].astype(str).str.lower().str.contains(termo, na=False)
        ]

    lista_clientes = clientes_filtrados["cliente"].astype(str).tolist() if len(clientes_filtrados) else ["CLIENTE NÃO ENCONTRADO"]
    cliente = st.selectbox("Cliente", lista_clientes)

    busca_produto = st.text_input("Buscar produto", placeholder="Digite código ou nome do produto")

    produtos_filtrados = produtos.copy()
    if len(produtos_filtrados) and busca_produto.strip():
        termo = busca_produto.strip().lower()
        produtos_filtrados = produtos[
            produtos["produto"].astype(str).str.lower().str.contains(termo, na=False) |
            produtos["codigo"].astype(str).str.lower().str.contains(termo, na=False)
        ]

    opcoes = ["Selecione o produto"]

    for _, row in produtos_filtrados.iterrows():
        opcoes.append(f'{row["codigo"]} - {row["produto"]} | {dinheiro(row["preco"])}')

    produto_txt = st.selectbox("Produto", opcoes)

    produto = None
    if produto_txt != "Selecione o produto":
        idx = opcoes.index(produto_txt) - 1
        produto = produtos_filtrados.iloc[idx].to_dict()

    if produto:
        st.markdown(f"""
        <div class="card">
            <b>{produto["produto"]}</b><br>
            Código: {produto["codigo"]}<br>
            Fornecedor: {produto.get("fornecedor", "")}<br>
            Preço: <span class="valor">{dinheiro(produto["preco"])}</span>
        </div>
        """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    qtd = c1.number_input("Qtd", min_value=0, value=0, step=1)
    desc = c2.number_input("Desc. %", min_value=0.0, value=0.0, step=1.0)

    preco = safe_float(produto["preco"]) if produto else 0
    subtotal = preco * qtd
    total_item = subtotal - (subtotal * desc / 100)

    st.metric("Total do item", dinheiro(total_item))

    if st.button("➕ ADICIONAR AO CARRINHO", use_container_width=True):
        if not produto:
            st.warning("Selecione um produto.")
        elif qtd <= 0:
            st.warning("Informe a quantidade.")
        elif cliente == "CLIENTE NÃO ENCONTRADO":
            st.warning("Selecione um cliente válido.")
        else:
            st.session_state.carrinho.append({
                "codigo": produto["codigo"],
                "produto": produto["produto"],
                "un": produto.get("un", "UN"),
                "quantidade": qtd,
                "preco": preco,
                "desconto": desc,
                "subtotal": subtotal,
                "total": total_item,
            })
            st.success("Produto adicionado.")
            time.sleep(0.4)
            st.rerun()

    carrinho(cliente)


def carrinho(cliente):
    st.markdown('<div class="subtitulo">🛒 Carrinho</div><div class="linha-laranja"></div>', unsafe_allow_html=True)

    if len(st.session_state.carrinho) == 0:
        st.info("Nenhum produto adicionado.")
        return

    for i, item in enumerate(st.session_state.carrinho):
        st.markdown(f"""
        <div class="card">
            <b>{item["produto"]}</b><br>
            Qtd: {item["quantidade"]} | Unit: {dinheiro(item["preco"])}<br>
            Total: <span class="valor">{dinheiro(item["total"])}</span>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"🗑 Remover item {i+1}", key=f"del_{i}", use_container_width=True):
            st.session_state.carrinho.pop(i)
            st.rerun()

    subtotal = sum(safe_float(x["subtotal"]) for x in st.session_state.carrinho)
    total = sum(safe_float(x["total"]) for x in st.session_state.carrinho)
    desconto = subtotal - total

    st.markdown(f"""
    <div class="resumo-box">
        <p>Subtotal: {dinheiro(subtotal)}</p>
        <p>Desconto: {dinheiro(desconto)}</p>
        <p>Total: {dinheiro(total)}</p>
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
        st.success(f"Pedido nº {numero} salvo com sucesso!")
        time.sleep(1)
        ir_para("pedidos")

    if st.button("🧹 LIMPAR CARRINHO", use_container_width=True):
        st.session_state.carrinho = []
        st.rerun()


def pedidos_tela():
    topo("Pedidos", "Histórico de pedidos")

    pedidos = filtrar_por_usuario(ler_excel(ARQ_PEDIDOS))
    resumo = resumo_pedidos(pedidos).sort_values("pedido", ascending=False)

    if len(resumo) == 0:
        st.info("Nenhum pedido lançado.")
        return

    for _, row in resumo.iterrows():
        st.markdown(f"""
        <div class="card">
            <b>Pedido #{row["pedido"]}</b><br>
            Cliente: {row["cliente"]}<br>
            Vendedor: {row["vendedor"]}<br>
            Data: {row["data"]}<br>
            Total: <span class="valor">{dinheiro(row["total"])}</span><br>
            Status: <b>{row["status"]}</b>
        </div>
        """, unsafe_allow_html=True)

        if str(row["status"]).upper() == "PENDENTE":
            if st.button(f"✏️ Editar pedido {row['pedido']}", key=f"edit_{row['pedido']}", use_container_width=True):
                st.session_state.pedido_editando = int(row["pedido"])
                ir_para("editar")


def editar_pedido():
    topo("Editar Pedido", "Alterar pedido pendente")

    numero = st.session_state.get("pedido_editando")
    pedidos = ler_excel(ARQ_PEDIDOS)
    dados = pedidos[pedidos["pedido"] == numero].copy()

    if len(dados) == 0:
        st.error("Pedido não encontrado.")
        return

    status = str(dados["status"].iloc[0]).upper()

    if status == "FATURADO" and st.session_state.get("perfil") != "ADMIN":
        st.error("Pedido faturado não pode ser alterado pelo vendedor.")
        return

    st.info(f"Pedido #{numero} - {dados['cliente'].iloc[0]}")

    novos = []

    for idx, row in dados.iterrows():
        st.markdown(f"### {row['produto']}")

        c1, c2 = st.columns(2)
        qtd = c1.number_input("Qtd", min_value=0, value=int(row["quantidade"]), step=1, key=f"qtd_{idx}")
        desc = c2.number_input("Desc. %", min_value=0.0, value=safe_float(row["desconto"]), step=1.0, key=f"desc_{idx}")
        excluir = st.checkbox("Excluir item", key=f"exc_{idx}")

        preco = safe_float(row["preco"])
        subtotal = preco * qtd
        total = subtotal - (subtotal * desc / 100)

        st.write(f"Total: **{dinheiro(total)}**")

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
            st.warning("Pedido não pode ficar sem itens.")
        else:
            pedidos = pedidos[pedidos["pedido"] != numero]
            pedidos = pd.concat([pedidos, pd.DataFrame(novos)], ignore_index=True)
            salvar_excel(pedidos, ARQ_PEDIDOS)

            st.success("Pedido atualizado.")
            time.sleep(0.8)
            ir_para("pedidos")

    if st.button("⬅️ VOLTAR", use_container_width=True):
        ir_para("pedidos")


def comissao_tela():
    topo("Comissão", "Resumo da comissão")

    pedidos = filtrar_por_usuario(ler_excel(ARQ_PEDIDOS))

    if len(pedidos):
        pedidos["total"] = pd.to_numeric(pedidos["total"], errors="coerce").fillna(0)

    vendas = pedidos["total"].sum() if len(pedidos) else 0
    comissao = vendas * st.session_state.get("comissao", COMISSAO_PADRAO)

    st.metric("Vendas", dinheiro(vendas))
    st.metric("Comissão", dinheiro(comissao))


def admin_tela():
    topo("Administração", "Área do administrador")

    if st.session_state.get("perfil") != "ADMIN":
        st.error("Acesso permitido somente para administrador.")
        return

    if st.button("👥 Usuários", use_container_width=True):
        ir_para("admin_usuarios")

    if st.button("🏪 Clientes", use_container_width=True):
        ir_para("admin_clientes")

    if st.button("📦 Produtos", use_container_width=True):
        ir_para("admin_produtos")


def admin_usuarios():
    topo("Usuários", "Cadastro de vendedores")

    if st.session_state.get("perfil") != "ADMIN":
        st.error("Acesso negado.")
        return

    usuarios = ler_excel(ARQ_USUARIOS)

    with st.form("form_usuario"):
        nome = st.text_input("Nome")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha")
        perfil = st.selectbox("Perfil", ["VENDEDOR", "ADMIN"])
        comissao = st.number_input("Comissão", value=0.07, step=0.01)

        salvar = st.form_submit_button("💾 SALVAR", use_container_width=True)

    if salvar:
        if nome and usuario and senha:
            novo = pd.DataFrame([{
                "usuario": usuario.strip().lower(),
                "senha": senha.strip(),
                "nome": nome.strip(),
                "perfil": perfil,
                "comissao": comissao,
            }])
            usuarios = pd.concat([usuarios, novo], ignore_index=True)
            salvar_excel(usuarios, ARQ_USUARIOS)
            st.success("Usuário cadastrado.")
            time.sleep(0.5)
            st.rerun()
        else:
            st.warning("Preencha todos os campos.")

    st.dataframe(usuarios, use_container_width=True)

    if st.button("⬅️ VOLTAR", use_container_width=True):
        ir_para("admin")


def admin_clientes():
    topo("Clientes", "Cadastro de clientes")

    if st.session_state.get("perfil") != "ADMIN":
        st.error("Acesso negado.")
        return

    clientes = ler_excel(ARQ_CLIENTES)

    with st.form("form_cliente"):
        cliente = st.text_input("Cliente")
        cnpj = st.text_input("CNPJ")
        telefone = st.text_input("Telefone")
        cidade = st.text_input("Cidade")

        salvar = st.form_submit_button("💾 SALVAR", use_container_width=True)

    if salvar:
        if cliente:
            codigo = 1
            if len(clientes):
                maior = pd.to_numeric(clientes["codigo"], errors="coerce").max()
                codigo = 1 if pd.isna(maior) else int(maior) + 1

            novo = pd.DataFrame([{
                "codigo": codigo,
                "cliente": cliente.strip().upper(),
                "cnpj": cnpj.strip(),
                "telefone": telefone.strip(),
                "cidade": cidade.strip().upper(),
            }])

            clientes = pd.concat([clientes, novo], ignore_index=True)
            salvar_excel(clientes, ARQ_CLIENTES)
            st.success("Cliente cadastrado.")
            time.sleep(0.5)
            st.rerun()
        else:
            st.warning("Informe o nome do cliente.")

    st.dataframe(clientes, use_container_width=True)

    if st.button("⬅️ VOLTAR", use_container_width=True):
        ir_para("admin")


def admin_produtos():
    topo("Produtos", "Cadastro de produtos")

    if st.session_state.get("perfil") != "ADMIN":
        st.error("Acesso negado.")
        return

    produtos = ler_excel(ARQ_PRODUTOS)

    with st.form("form_produto"):
        codigo = st.text_input("Código")
        produto = st.text_input("Produto")
        un = st.text_input("Unidade", value="UN")
        preco = st.number_input("Preço", min_value=0.0, step=0.01)
        fornecedor = st.text_input("Fornecedor")

        salvar = st.form_submit_button("💾 SALVAR", use_container_width=True)

    if salvar:
        if codigo and produto:
            novo = pd.DataFrame([{
                "codigo": codigo.strip(),
                "produto": produto.strip().upper(),
                "un": un.strip().upper(),
                "preco": preco,
                "fornecedor": fornecedor.strip().upper(),
            }])
            produtos = pd.concat([produtos, novo], ignore_index=True)
            salvar_excel(produtos, ARQ_PRODUTOS)
            st.success("Produto cadastrado.")
            time.sleep(0.5)
            st.rerun()
        else:
            st.warning("Informe código e produto.")

    st.dataframe(produtos, use_container_width=True)

    if st.button("⬅️ VOLTAR", use_container_width=True):
        ir_para("admin")


def mais_tela():
    topo("Mais", "Opções do sistema")

    st.info(f"Usuário: {st.session_state.get('nome')} | Perfil: {st.session_state.get('perfil')}")

    if st.session_state.get("perfil") == "ADMIN":
        if st.button("⚙️ ADMINISTRAÇÃO", use_container_width=True):
            ir_para("admin")

    if st.button("🚪 SAIR", use_container_width=True):
        st.session_state.clear()
        st.rerun()


# =========================
# APP
# =========================

criar_banco()
css()
iniciar_sessao()
login()

page = st.session_state.page

if page == "dashboard":
    dashboard()
elif page == "novo":
    novo_pedido()
elif page == "pedidos":
    pedidos_tela()
elif page == "editar":
    editar_pedido()
elif page == "comissao":
    comissao_tela()
elif page == "admin":
    admin_tela()
elif page == "admin_usuarios":
    admin_usuarios()
elif page == "admin_clientes":
    admin_clientes()
elif page == "admin_produtos":
    admin_produtos()
elif page == "mais":
    mais_tela()
else:
    dashboard()

menu_nativo()
