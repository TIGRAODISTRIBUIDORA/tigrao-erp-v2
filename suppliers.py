import streamlit as st
import pandas as pd
import os

DATA_DIR = "dados"
SUPPLIERS_FILE = os.path.join(DATA_DIR, "fornecedores.xlsx")

os.makedirs(DATA_DIR, exist_ok=True)


def load_suppliers():
    if not os.path.exists(SUPPLIERS_FILE):
        df = pd.DataFrame(columns=[
            "codigo", "fornecedor", "cnpj", "telefone",
            "email", "cidade", "estado", "observacao"
        ])
        df.to_excel(SUPPLIERS_FILE, index=False)
        return df

    df = pd.read_excel(SUPPLIERS_FILE)

    cols = [
        "codigo", "fornecedor", "cnpj", "telefone",
        "email", "cidade", "estado", "observacao"
    ]

    for col in cols:
        if col not in df.columns:
            df[col] = ""

    return df[cols]


def save_suppliers(df):
    df.to_excel(SUPPLIERS_FILE, index=False)


def supplier_options():
    df = load_suppliers()
    if len(df) == 0:
        return ["Não informado"]

    fornecedores = df["fornecedor"].dropna().astype(str).tolist()
    fornecedores = [f for f in fornecedores if f.strip() != ""]
    fornecedores = sorted(list(set(fornecedores)))

    if len(fornecedores) == 0:
        return ["Não informado"]

    return fornecedores


def supplier_form_inline():
    with st.expander("➕ Novo fornecedor"):
        fornecedor = st.text_input("Nome do fornecedor", key="forn_inline_nome")
        cnpj = st.text_input("CNPJ", key="forn_inline_cnpj")
        telefone = st.text_input("Telefone", key="forn_inline_tel")
        email = st.text_input("E-mail", key="forn_inline_email")
        cidade = st.text_input("Cidade", key="forn_inline_cidade")
        estado = st.text_input("Estado / UF", key="forn_inline_estado")
        observacao = st.text_area("Observação", key="forn_inline_obs")

        if st.button("💾 Salvar fornecedor", key="btn_salvar_fornecedor_inline"):
            if fornecedor.strip() == "":
                st.warning("Informe o nome do fornecedor.")
            else:
                df = load_suppliers()

                novo_codigo = 1
                if len(df) > 0:
                    try:
                        novo_codigo = int(pd.to_numeric(df["codigo"], errors="coerce").max()) + 1
                    except:
                        novo_codigo = len(df) + 1

                novo = pd.DataFrame([{
                    "codigo": novo_codigo,
                    "fornecedor": fornecedor.strip(),
                    "cnpj": cnpj.strip(),
                    "telefone": telefone.strip(),
                    "email": email.strip(),
                    "cidade": cidade.strip(),
                    "estado": estado.strip(),
                    "observacao": observacao.strip()
                }])

                df = pd.concat([df, novo], ignore_index=True)
                df = df.drop_duplicates(subset=["fornecedor"], keep="last")
                save_suppliers(df)

                st.success("Fornecedor cadastrado com sucesso!")
                st.rerun()


def render_suppliers():
    st.markdown("## 🏭 Fornecedores")

    supplier_form_inline()

    st.markdown("---")
    st.markdown("### 🔍 Consultar fornecedores")

    fornecedores = load_suppliers()

    busca = st.text_input("Buscar por nome, CNPJ, telefone ou cidade")

    if busca:
        filtrado = fornecedores[
            fornecedores.astype(str).apply(
                lambda linha: linha.str.contains(busca, case=False, na=False).any(),
                axis=1
            )
        ]
    else:
        filtrado = fornecedores

    st.dataframe(filtrado, use_container_width=True)


def show_suppliers():
    render_suppliers()


def suppliers_page():
    render_suppliers()
