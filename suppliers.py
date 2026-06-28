import pandas as pd
import streamlit as st

from database import SUPPLIERS_FILE, read_table, save_table
from ui import is_admin, title


def supplier_options() -> list[str]:
    suppliers = read_table(SUPPLIERS_FILE)
    if "fornecedor" not in suppliers.columns:
        return []
    return sorted([x for x in suppliers["fornecedor"].dropna().astype(str).tolist() if x.strip()])


def save_supplier(name: str, contato: str = "", telefone: str = "", email: str = "", cidade: str = "", estado: str = "", observacao: str = "") -> bool:
    suppliers = read_table(SUPPLIERS_FILE)
    if len(suppliers) == 0:
        suppliers = pd.DataFrame(columns=["fornecedor", "contato", "telefone", "email", "cidade", "estado", "observacao"])
    if not name.strip():
        return False
    new = pd.DataFrame([{
        "fornecedor": name.strip(),
        "contato": contato,
        "telefone": telefone,
        "email": email,
        "cidade": cidade,
        "estado": estado,
        "observacao": observacao,
    }])
    suppliers = pd.concat([suppliers, new], ignore_index=True)
    suppliers = suppliers.drop_duplicates(subset=["fornecedor"], keep="last")
    save_table(suppliers, SUPPLIERS_FILE)
    return True


def supplier_form_inline(prefix: str = "inline") -> None:
    if not is_admin():
        return
    with st.expander("➕ Novo Fornecedor"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Nome do fornecedor", key=f"{prefix}_supplier_name")
            contato = st.text_input("Contato", key=f"{prefix}_supplier_contact")
            telefone = st.text_input("Telefone", key=f"{prefix}_supplier_phone")
        with c2:
            email = st.text_input("E-mail", key=f"{prefix}_supplier_email")
            cidade = st.text_input("Cidade", key=f"{prefix}_supplier_city")
            estado = st.text_input("Estado", key=f"{prefix}_supplier_state")
        observacao = st.text_area("Observação", key=f"{prefix}_supplier_note")
        if st.button("💾 Salvar Fornecedor", key=f"{prefix}_save_supplier"):
            if save_supplier(name, contato, telefone, email, cidade, estado, observacao):
                st.success("Fornecedor cadastrado com sucesso.")
                st.rerun()
            else:
                st.warning("Informe o nome do fornecedor.")


def show_suppliers() -> None:
    if not is_admin():
        st.error("Acesso permitido somente para administrador.")
        st.stop()

    title("🏭 Fornecedores")
    supplier_form_inline("page")

    suppliers = read_table(SUPPLIERS_FILE)
    st.markdown("### 🔍 Consultar fornecedores")
    search = st.text_input("Buscar fornecedor")
    if search and len(suppliers):
        suppliers = suppliers[suppliers.astype(str).apply(lambda row: row.str.contains(search, case=False, na=False).any(), axis=1)]
    st.dataframe(suppliers, use_container_width=True)
