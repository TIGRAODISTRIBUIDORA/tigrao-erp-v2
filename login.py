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
    .login-bg {
        min-height: 100vh;
        background: linear-gradient(180deg, #111827 0%, #000000 45%, #f97316 100%);
        margin: -10px;
        padding: 38px 18px;
        position: relative;
        overflow: hidden;
    }

    .login-bg::after {
        content: "🐯";
        position: absolute;
        right: -35px;
        bottom: -50px;
        font-size: 190px;
        opacity: .14;
    }

    .login-logo {
        text-align: center;
        color: white !important;
        font-size: 34px;
        font-weight: 1000;
        line-height: 1.15;
        margin-top: 20px;
    }

    .login-sub {
        text-align: center;
        color: #ffedd5 !important;
        font-size: 16px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 28px;
    }

    .login-card {
        background: white;
        border-radius: 26px;
        padding: 24px;
        box-shadow: 0 14px 34px rgba(0,0,0,.30);
        border: 2px solid #fed7aa;
        max-width: 380px;
        margin: 0 auto;
        position: relative;
        z-index: 2;
    }

    .login-title {
        color: #111827 !important;
        font-size: 22px;
        font-weight: 1000;
        text-align: center;
        margin-bottom: 18px;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #f97316, #ea580c) !important;
        color: white !important;
        border-radius: 18px !important;
        min-height: 58px !important;
        font-size: 16px !important;
        font-weight: 1000 !important;
        border: none !important;
        box-shadow: 0 7px 18px rgba(249,115,22,.35);
    }

    div.stButton > button:active {
        background: #22c55e !important;
        transform: scale(.96);
    }

    input {
        background: white !important;
        color: #111827 !important;
        border: 2px solid #fed7aa !important;
        border-radius: 16px !important;
        min-height: 52px !important;
        font-size: 16px !important;
    }

    label {
        color: #111827 !important;
        font-weight: 900 !important;
    }

    .login-card * {
        color: #111827 !important;
    }
    </style>

    <div class="login-bg">
        <div class="login-logo">🐯 TIGRÃO<br>DISTRIBUIDORA</div>
        <div class="login-sub">Sistema profissional de pedidos</div>
        <div class="login-card">
            <div class="login-title">Acesso ao sistema</div>
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

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

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
