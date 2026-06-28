import pandas as pd
import streamlit as st

from database import CLIENTS_FILE, read_table, save_table
from ui import is_admin, title


def show_clients() -> None:
    title("👥 Clientes")
    clients = read_table(CLIENTS_FILE)

    if is_admin():
        with st.expander("Cadastrar cliente"):
            codigo = st.number_input("Código do cliente", min_value=1, step=1)
            nome = st.text_input("Nome")
            cnpj = st.text_input("CNPJ")
            telefone = st.text_input("Telefone")
            cidade = st.text_input("Cidade")
            estado = st.text_input("Estado")
            if st.button("Salvar Cliente"):
                new = pd.DataFrame([{"codigo": codigo, "cliente": nome, "cnpj": cnpj, "telefone": telefone, "cidade": cidade, "estado": estado}])
                clients = pd.concat([clients, new], ignore_index=True)
                clients = clients.drop_duplicates(subset=["codigo"], keep="last")
                save_table(clients, CLIENTS_FILE)
                st.success("Cliente salvo.")
                st.rerun()

    search = st.text_input("Buscar cliente")
    if search and len(clients):
        clients = clients[clients.astype(str).apply(lambda row: row.str.contains(search, case=False, na=False).any(), axis=1)]
    st.dataframe(clients, use_container_width=True)
