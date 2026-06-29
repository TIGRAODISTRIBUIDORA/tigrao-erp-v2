import pandas as pd
import streamlit as st

from database import CLIENTS_FILE, read_table, save_table
from ui import is_admin, title


def show_clients() -> None:
    title("👥 Clientes")

    clients = read_table(CLIENTS_FILE)

    if "vendedor_login" not in clients.columns:
        clients["vendedor_login"] = ""

    if "vendedor_nome" not in clients.columns:
        clients["vendedor_nome"] = ""

    usuario_logado = st.session_state.get("usuario", "")
    vendedor_nome = st.session_state.get("vendedor", "")

    if not is_admin():
        clients = clients[clients["vendedor_login"].astype(str) == usuario_logado]

    with st.expander("Cadastrar cliente"):
        codigo = st.number_input("Código do cliente", min_value=1, step=1)
        nome = st.text_input("Nome")
        cnpj = st.text_input("CNPJ")
        telefone = st.text_input("Telefone")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")

        if st.button("Salvar Cliente"):
            all_clients = read_table(CLIENTS_FILE)

            if "vendedor_login" not in all_clients.columns:
                all_clients["vendedor_login"] = ""

            if "vendedor_nome" not in all_clients.columns:
                all_clients["vendedor_nome"] = ""

            new = pd.DataFrame([{
                "codigo": codigo,
                "cliente": nome,
                "cnpj": cnpj,
                "telefone": telefone,
                "cidade": cidade,
                "estado": estado,
                "vendedor_login": usuario_logado,
                "vendedor_nome": vendedor_nome
            }])

            all_clients = pd.concat([all_clients, new], ignore_index=True)
            all_clients = all_clients.drop_duplicates(subset=["codigo"], keep="last")

            save_table(all_clients, CLIENTS_FILE)

            st.success("Cliente salvo.")
            st.rerun()

    search = st.text_input("Buscar cliente")

    if search and len(clients):
        clients = clients[
            clients.astype(str).apply(
                lambda row: row.str.contains(search, case=False, na=False).any(),
                axis=1
            )
        ]

    st.dataframe(clients, use_container_width=True)
