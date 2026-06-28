import pandas as pd
import streamlit as st

from database import PRODUCTS_FILE, normalize_columns, read_table, save_table, to_excel_bytes
from suppliers import supplier_form_inline, supplier_options
from ui import is_admin, title


def show_products() -> None:
    title("📦 Produtos")
    products = read_table(PRODUCTS_FILE)
    if "fornecedor" not in products.columns:
        products["fornecedor"] = ""

    if is_admin():
        supplier_form_inline("products")

        with st.expander("Cadastrar produto manual"):
            suppliers = supplier_options()
            codigo = st.text_input("Código")
            produto = st.text_input("Produto")
            un = st.text_input("Unidade", value="UN")
            preco = st.number_input("Preço", min_value=0.0, step=0.10)
            fornecedor = st.selectbox("Fornecedor", suppliers) if suppliers else st.text_input("Fornecedor")
            if st.button("Salvar Produto"):
                new = pd.DataFrame([{"codigo": codigo, "produto": produto, "un": un, "preco": preco, "fornecedor": fornecedor}])
                products = pd.concat([products, new], ignore_index=True)
                products = products.drop_duplicates(subset=["codigo"], keep="last")
                save_table(products, PRODUCTS_FILE)
                st.success("Produto salvo.")
                st.rerun()

        st.markdown("### 📤 Exportar modelo / produtos")
        model = pd.DataFrame([{"codigo": "187", "produto": "37 ERVAS 500MG 100 CAPSULAS", "un": "UN", "preco": 20.77, "fornecedor": "Vitalab"}])
        st.download_button("⬇️ Baixar modelo de importação", to_excel_bytes(model), file_name="modelo_produtos_tigrao.xlsx")
        st.download_button("⬇️ Exportar produtos cadastrados", to_excel_bytes(products), file_name="produtos_tigrao.xlsx")

    st.markdown("---")
    st.markdown("### 🔍 Consultar produtos")
    suppliers = sorted(products["fornecedor"].fillna("").astype(str).unique().tolist()) if len(products) else []
    suppliers = [x for x in suppliers if x.strip()]
    suppliers = ["Todos"] + suppliers

    c1, c2 = st.columns(2)
    with c1:
        search = st.text_input("Buscar por código ou nome")
    with c2:
        supplier_filter = st.selectbox("Filtrar por fornecedor", suppliers)

    filtered = products.copy()
    if search and len(filtered):
        filtered = filtered[
            filtered["produto"].astype(str).str.contains(search, case=False, na=False) |
            filtered["codigo"].astype(str).str.contains(search, case=False, na=False)
        ]
    if supplier_filter != "Todos" and len(filtered):
        filtered = filtered[filtered["fornecedor"].astype(str) == supplier_filter]
    st.dataframe(filtered, use_container_width=True)


def show_import_products() -> None:
    if not is_admin():
        st.error("Acesso permitido somente para administrador.")
        st.stop()

    title("📥 Importar Produtos por Excel")
    st.info("A planilha precisa ter: código, produto, unidade, preço e fornecedor.")
    model = pd.DataFrame([{"codigo": "187", "produto": "37 ERVAS 500MG 100 CAPSULAS", "un": "UN", "preco": 20.77, "fornecedor": "Vitalab"}])
    st.download_button("⬇️ Baixar modelo de importação", to_excel_bytes(model), file_name="modelo_produtos_tigrao.xlsx")

    file = st.file_uploader("Escolha a planilha de produtos", type=["xlsx", "xls", "csv"])
    if not file:
        return

    df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
    df = normalize_columns(df)
    mapping = {}
    for col in df.columns:
        if col in ["codigo", "cod", "cod_produto", "id"]:
            mapping[col] = "codigo"
        elif col in ["produto", "descricao", "nome", "nome_produto"]:
            mapping[col] = "produto"
        elif col in ["un", "und", "unidade"]:
            mapping[col] = "un"
        elif col in ["preco", "preco_venda", "valor", "valor_venda"]:
            mapping[col] = "preco"
        elif col in ["fornecedor", "fabricante", "marca", "industria", "industria_fornecedor"]:
            mapping[col] = "fornecedor"
    df = df.rename(columns=mapping)

    required = ["codigo", "produto", "preco"]
    missing = [x for x in required if x not in df.columns]
    if missing:
        st.error(f"Faltam colunas obrigatórias: {missing}")
        st.stop()

    if "un" not in df.columns:
        df["un"] = "UN"
    if "fornecedor" not in df.columns:
        df["fornecedor"] = ""

    df = df[["codigo", "produto", "un", "preco", "fornecedor"]]
    df["codigo"] = df["codigo"].astype(str).str.strip()
    df["produto"] = df["produto"].astype(str).str.strip()
    df["un"] = df["un"].astype(str).str.strip()
    df["fornecedor"] = df["fornecedor"].astype(str).str.strip()
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce").fillna(0)
    df = df[df["produto"] != ""].drop_duplicates(subset=["codigo"], keep="last")

    st.markdown("### Pré-visualização")
    st.dataframe(df, use_container_width=True)

    if st.button("✅ IMPORTAR E ATUALIZAR PRODUTOS"):
        current = read_table(PRODUCTS_FILE)
        if "fornecedor" not in current.columns:
            current["fornecedor"] = ""
        current["codigo"] = current["codigo"].astype(str).str.strip() if len(current) else ""
        new_codes = set(df["codigo"].astype(str))
        final = pd.concat([current[~current["codigo"].astype(str).isin(new_codes)], df], ignore_index=True) if len(current) else df
        save_table(final, PRODUCTS_FILE)
        st.success("Produtos importados com sucesso.")
        st.rerun()
