import streamlit as st

from database import USERS_FILE, read_table


def login_screen() -> None:
    if "logado" not in st.session_state:
        st.session_state.logado = False
    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []
    if "produto_selecionado" not in st.session_state:
        st.session_state.produto_selecionado = None

    if st.session_state.logado:
        return

    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #111827 0%, #000000 45%, #f97316 100%) !important;
    }

    .block-container {
        max-width: 430px !important;
        padding: 35px 18px !important;
        margin: auto !important;
    }

    header, footer {
        display: none !important;
    }

    .login-logo {
        text-align: center;
        color: white !important;
        font-size: 34px;
        font-weight: 1000;
        line-height: 1.15;
        margin-bottom: 8px;
    }

    .login-sub {
        text-align: center;
        color: #ffedd5 !important;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 26px;
    }

    .login-card-title {
        text-align: center;
        background: white;
        color: #111827 !important;
        padding: 18px;
        border-radius: 22px;
        font-size: 22px;
        font-weight: 1000;
        margin-bottom: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,.25);
        border: 2px solid #fed7aa;
    }

    label {
        color: white !important;
        font-weight: 900 !important;
    }

    input {
        background: white !important;
        color: #111827 !important;
        border: 2px solid #fed7aa !important;
        border-radius: 16px !important;
        min-height: 52px !important;
        font-size: 16px !important;
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #f97316, #ea580c) !important;
        color: white !important;
        border-radius: 18px !important;
        min-height: 58px !important;
        font-size: 16px !important;
        font-weight: 1000 !important;
        border: none !important;
        box-shadow: 0 7px 18px rgba(249,115,22,.35);
        transition: all .12s ease-in-out !important;
    }

    div.stButton > button:hover {
        background: #ea580c !important;
        transform: translateY(-1px);
    }

    div.stButton > button:active {
        background: #22c55e !important;
        transform: scale(.96);
    }

    .stAlert {
        border-radius: 16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-logo">🐯 TIGRÃO<br>DISTRIBUIDORA</div>
    <div class="login-sub">Sistema profissional de pedidos</div>
    <div class="login-card-title">Acesso ao sistema</div>
    """, unsafe_allow_html=True)

    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("ENTRAR", use_container_width=True):
        users = read_table(USERS_FILE)
        users["usuario"] = users["usuario"].astype(str)

        match = users[
            (users["usuario"] == usuario) &
            (users["senha"].astype(str) == senha)
        ]

        if len(match):
            row = match.iloc[0]
            if str(row.get("ativo", "SIM")).upper() != "SIM":
                st.error("Usuário inativo.")
            else:
                st.session_state.logado = True
                st.session_state.usuario = str(row["usuario"])
                st.session_state.vendedor = str(row["nome"])
                st.session_state.perfil = str(row["perfil"])
                st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")

    st.stop()


def logout() -> None:
    st.session_state.logado = False
    st.session_state.carrinho = []
    st.session_state.produto_selecionado = None
    st.session_state.usuario = ""
    st.session_state.vendedor = ""
    st.session_state.perfil = ""

    if "menu_mobile" in st.session_state:
        st.session_state.menu_mobile = "Início"

    st.rerun()
