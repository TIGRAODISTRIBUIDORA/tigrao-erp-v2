import os
import pandas as pd
import streamlit as st

DATA_DIR = "dados"
SUPPLIERS_FILE = os.path.join(DATA_DIR, "fornecedores.xlsx")

os.makedirs(DATA_DIR, exist_ok=True)


def load_suppliers():
    if not os.path.exists(SUPPLIERS_FILE):
        df = pd.DataFrame(columns=[
            "codigo",
            "fornecedor",
            "cnpj",
            "ie",
            "telefone",
            "whatsapp",
            "email",
            "contato",
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
        "ie",
        "telefone",
        "whatsapp",
        "email",
        "contato",
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


def supplier_form_inline(prefix="suppliers"):
    with st.expander("➕ Novo fornecedor"):
        col1, col2 = st.columns(2)

        with col1:
            fornecedor = st.text_input("Nome do fornecedor", key=f"{prefix}_fornecedor")
            cnpj = st.text_input("CNPJ", key=f"{prefix}_cnpj")
            ie = st.text_input("Inscrição Estadual", key=f"{prefix}_ie")
            telefone = st.text_input("Telefone", key=f"{prefix}_telefone")
            whatsapp = st.text_input("WhatsApp", key=f"{prefix}_whatsapp")

        with col2:
            email = st.text_input("E-mail", key=f"{prefix}_email")
            contato = st.text_input("Contato", key=f"{prefix}_contato")
            cidade = st.text_input("Cidade", key=f"{prefix}_cidade")
            estado = st.text_input("Estado / UF", key=f"{prefix}_estado")
            observacao = st.text_area("Observação", key=f"{prefix}_observacao")

        if st.button("💾 Salvar fornecedor", key=f"{prefix}_salvar_fornecedor"):
            if fornecedor.strip() == "":
                st.warning("Informe o nome do fornecedor.")
                return

            df = load_suppliers()

            novo_codigo = 1
            if len(df) > 0:
                try:
                    novo_codigo = int(pd.to_numeric(df["codigo"], errors="coerce").max()) + 1
                except Exception:
                    novo_codigo = len(df) + 1

            novo = pd.DataFrame([{
                "codigo": novo_codigo,
                "fornecedor": fornecedor.strip(),
                "cnpj": cnpj.strip(),
                "ie": ie.strip(),
                "telefone": telefone.strip(),
                "whatsapp": whatsapp.strip(),
                "email": email.strip(),
                "contato": contato.strip(),
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

    supplier_form_inline("suppliers")

    st.markdown("---")
    st.markdown("### 🔍 Consultar fornecedores")

    fornecedores = load_suppliers()

    busca = st.text_input("Buscar por fornecedor, CNPJ, telefone, cidade ou contato")

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
