import pandas as pd
import streamlit as st

from database import USERS_FILE, read_table, save_table
from ui import is_admin, title


def show_users() -> None:
    title("👨‍💼 Vendedores / Usuários")

    if not is_admin():
        st.error("Acesso permitido somente para administrador.")
        return

    users = read_table(USERS_FILE)

    required_cols = ["usuario", "senha", "nome", "perfil", "ativo"]

    for col in required_cols:
        if col not in users.columns:
            users[col] = ""

    users = users[required_cols]

    with st.expander("➕ Cadastrar vendedor / usuário", expanded=True):
        usuario = st.text_input("Login do usuário")
        senha = st.text_input("Senha")
        nome = st.text_input("Nome do vendedor")
        perfil = st.selectbox("Perfil", ["vendedor", "admin"])
        ativo = st.selectbox("Ativo", ["SIM", "NÃO"])

        if st.button("💾 Salvar usuário"):
            if usuario.strip() == "" or senha.strip() == "" or nome.strip() == "":
                st.warning("Informe login, senha e nome.")
            else:
                novo = pd.DataFrame([{
                    "usuario": usuario.strip(),
                    "senha": senha.strip(),
                    "nome": nome.strip(),
                    "perfil": perfil,
                    "ativo": ativo
                }])

                users = pd.concat([users, novo], ignore_index=True)
                users = users.drop_duplicates(subset=["usuario"], keep="last")

                save_table(users, USERS_FILE)

                st.success("Usuário salvo com sucesso.")
                st.rerun()

    st.markdown("---")
    st.markdown("### 🔍 Usuários cadastrados")

    busca = st.text_input("Buscar usuário")

    if busca:
        filtrado = users[
            users.astype(str).apply(
                lambda row: row.str.contains(busca, case=False, na=False).any(),
                axis=1
            )
        ]
    else:
        filtrado = users

    st.dataframe(filtrado, use_container_width=True)
