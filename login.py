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

    st.markdown("<h1 style='text-align:center;'>🐯 TIGRÃO DISTRIBUIDORA</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>Sistema de Pedidos</h3>", unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.2, 1])
    with center:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")

        if st.button("ENTRAR"):
            users = read_table(USERS_FILE)
            users["usuario"] = users["usuario"].astype(str)
            match = users[(users["usuario"] == usuario) & (users["senha"].astype(str) == senha)]
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
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


def logout() -> None:
    st.session_state.logado = False
    st.session_state.carrinho = []
    st.session_state.produto_selecionado = None
    st.session_state.usuario = ""
    st.session_state.vendedor = ""
    st.session_state.perfil = ""
    st.rerun()
