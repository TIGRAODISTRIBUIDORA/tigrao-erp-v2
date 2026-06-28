import streamlit as st
import pandas as pd
import os

DATA_DIR = "dados"
SUPPLIERS_FILE = os.path.join(DATA_DIR, "fornecedores.xlsx")

os.makedirs(DATA_DIR, exist_ok=True)


def load_suppliers():
    if not os.path.exists(SUPPLIERS_FILE):
        df = pd.DataFrame(columns=[
            "codigo",
            "fornecedor",
            "cnpj",
            "telefone",
            "email",
            "cidade",
            "estado",
            "observacao"
        ])
        df.to_excel(SUPPLIERS_FILE, index=False)
        return df

    df = pd.read_excel(SUPPLIERS_FILE)

    required_cols = [
        "codigo",
        "fornecedor",
        "cnpj",
        "telefone",
        "email",
        "cidade",
        "estado",
        "observacao"
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    return df[required_cols]


def save_suppliers(df):
    df.to_excel(SUPPLIERS_FILE, index=False)


def render_suppliers():
    st.markdown("## 🏭 Fornecedores")

    fornecedores = load_suppliers()

    st.markdown("### ➕ Cadastrar fornecedor")

    with st.expander("Novo fornecedor", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            fornecedor = st.text_input("Nome do fornecedor")
            cnpj = st.text_input("CNPJ")
            telefone = st.text_input("Telefone")
            email = st.text_input("E-mail")

        with col2:
            cidade = st.text_input("Cidade")
            estado = st.text_input("Estado / UF")
            observacao = st.text_area("Observação")

        if st.button("💾 Salvar fornecedor"):
            if fornecedor.strip() == "":
                st.warning("Informe o nome do fornecedor.")
            else:
                novo_codigo = 1
                if len(fornecedores) > 0:
                    try:
                        novo_codigo = int(fornecedores["codigo"].max()) + 1
                    except:
                        novo_codigo = len(fornecedores) + 1

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

                fornecedores = pd.concat([fornecedores, novo], ignore_index=True)
                fornecedores = fornecedores.drop_duplicates(subset=["fornecedor"], keep="last")

                save_suppliers(fornecedores)

                st.success("Fornecedor cadastrado com sucesso!")
                st.rerun()

    st.markdown("---")
    st.markdown("### 🔍 Consultar fornecedores")

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

    st.markdown("---")
    st.markdown("### ⬇️ Exportar fornecedores")

    fornecedores.to_excel("fornecedores_tigrao.xlsx", index=False)

    with open("fornecedores_tigrao.xlsx", "rb") as f:
        st.download_button(
            "Baixar fornecedores em Excel",
            f,
            file_name="fornecedores_tigrao.xlsx"
        )


def show_suppliers():
    render_suppliers()


def suppliers_page():
    render_suppliers()
