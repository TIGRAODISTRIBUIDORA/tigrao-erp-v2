import os
import pandas as pd
import streamlit as st

DATA_DIR = "dados"
SUPPLIERS_FILE = os.path.join(DATA_DIR, "fornecedores.xlsx")

os.makedirs(DATA_DIR, exist_ok=True)

COLS = [
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


def load_suppliers():
    if not os.path.exists(SUPPLIERS_FILE):
        df = pd.DataFrame(columns=COLS)
        df.to_excel(SUPPLIERS_FILE, index=False)
        return df

    df = pd.read_excel(SUPPLIERS_FILE)

    for col in COLS:
        if col not in df.columns:
            df[col] = ""

    df = df[COLS]
    df = df.fillna("")
    return df


def save_suppliers(df):
    df = df[COLS].fillna("")
    df.to_excel(SUPPLIERS_FILE, index=False)


def supplier_options():
    df = load_suppliers()
    fornecedores = df["fornecedor"].dropna().astype(str).tolist()
    fornecedores = [f for f in fornecedores if f.strip() != ""]
    fornecedores = sorted(list(set(fornecedores)))
    return fornecedores if fornecedores else ["Não informado"]


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
                codigos = pd.to_numeric(df["codigo"], errors="coerce").fillna(0)
                novo_codigo = int(codigos.max()) + 1

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
    st.markdown("### ✏️ Editar fornecedor")

    fornecedores = load_suppliers()

    if len(fornecedores) > 0:
        lista = fornecedores["fornecedor"].astype(str).tolist()
        fornecedor_escolhido = st.selectbox("Selecione o fornecedor", lista)

        dados = fornecedores[fornecedores["fornecedor"].astype(str) == fornecedor_escolhido].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            novo_nome = st.text_input("Fornecedor", value=str(dados["fornecedor"]), key="edit_fornecedor")
            novo_cnpj = st.text_input("CNPJ", value=str(dados["cnpj"]), key="edit_cnpj")
            novo_ie = st.text_input("Inscrição Estadual", value=str(dados["ie"]), key="edit_ie")
            novo_telefone = st.text_input("Telefone", value=str(dados["telefone"]), key="edit_telefone")
            novo_whatsapp = st.text_input("WhatsApp", value=str(dados["whatsapp"]), key="edit_whatsapp")

        with col2:
            novo_email = st.text_input("E-mail", value=str(dados["email"]), key="edit_email")
            novo_contato = st.text_input("Contato", value=str(dados["contato"]), key="edit_contato")
            novo_cidade = st.text_input("Cidade", value=str(dados["cidade"]), key="edit_cidade")
            novo_estado = st.text_input("Estado / UF", value=str(dados["estado"]), key="edit_estado")
            novo_obs = st.text_area("Observação", value=str(dados["observacao"]), key="edit_obs")

        if st.button("💾 Atualizar fornecedor"):
            idx = fornecedores[fornecedores["fornecedor"].astype(str) == fornecedor_escolhido].index[0]

            fornecedores.loc[idx, "fornecedor"] = novo_nome.strip()
            fornecedores.loc[idx, "cnpj"] = novo_cnpj.strip()
            fornecedores.loc[idx, "ie"] = novo_ie.strip()
            fornecedores.loc[idx, "telefone"] = novo_telefone.strip()
            fornecedores.loc[idx, "whatsapp"] = novo_whatsapp.strip()
            fornecedores.loc[idx, "email"] = novo_email.strip()
            fornecedores.loc[idx, "contato"] = novo_contato.strip()
            fornecedores.loc[idx, "cidade"] = novo_cidade.strip()
            fornecedores.loc[idx, "estado"] = novo_estado.strip()
            fornecedores.loc[idx, "observacao"] = novo_obs.strip()

            save_suppliers(fornecedores)

            st.success("Fornecedor atualizado com sucesso!")
            st.rerun()

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
