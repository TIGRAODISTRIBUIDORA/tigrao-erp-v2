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

    with st.expander("Cadastrar cliente", expanded=True):
        st.markdown("### Cadastro de Cliente")

        col1, col2 = st.columns(2)

        with col1:
            codigo = st.number_input("Código", min_value=1, step=1)
            cnpj = st.text_input("CNPJ")
            cidade = st.text_input("Cidade")

        with col2:
            nome = st.text_input("Nome do Cliente")
            telefone = st.text_input("Telefone")
            estado = st.text_input("Estado")

        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

        with col_btn1:
            salvar = st.button("💾 Salvar Cliente", use_container_width=True)

        if salvar:
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

    st.markdown("---")

    busca = st.text_input("🔍 Buscar cliente")

    if busca and len(clients):
        clients = clients[
            clients.astype(str).apply(
                lambda row: row.str.contains(busca, case=False, na=False).any(),
                axis=1
            )
        ]

    st.dataframe(clients, use_container_width=True)
