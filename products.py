import os
import pandas as pd
import streamlit as st

from database import PRODUCTS_FILE, normalize_columns, read_table, save_table, to_excel_bytes
from suppliers import supplier_form_inline, supplier_options
from ui import is_admin, title


IMAGES_DIR = "assets/produtos"
os.makedirs(IMAGES_DIR, exist_ok=True)


def _prepare_products(df):
    if "fornecedor" not in df.columns:
        df["fornecedor"] = ""

    if "imagem" not in df.columns:
        df["imagem"] = ""

    return df


def _safe_filename(value):
    name = str(value).strip()
    name = name.replace("/", "_").replace("\\", "_").replace(" ", "_")
    name = name.replace(".", "_").replace(",", "_").replace(":", "_")
    return name if name else "produto"


def _save_uploaded_image(uploaded_file, codigo):
    if uploaded_file is None:
        return ""

    ext = uploaded_file.name.split(".")[-1].lower()
    filename = f"{_safe_filename(codigo)}.{ext}"
    path = os.path.join(IMAGES_DIR, filename)

    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return path


def show_products() -> None:
    title("📦 Produtos")

    products = read_table(PRODUCTS_FILE)
    products = _prepare_products(products)

    if is_admin():
        supplier_form_inline("products")

        with st.expander("Cadastrar produto manual"):
            suppliers = supplier_options()

            col1, col2 = st.columns(2)

            with col1:
                codigo = st.text_input("Código")
                produto = st.text_input("Produto")
                un = st.text_input("Unidade", value="UN")

            with col2:
                preco = st.number_input("Preço", min_value=0.0, step=0.10)
                fornecedor = st.selectbox("Fornecedor", suppliers) if suppliers else st.text_input("Fornecedor")
                imagem_link = st.text_input("Link da imagem do produto")
                imagem_upload = st.file_uploader(
                    "📷 Enviar imagem do produto",
                    type=["png", "jpg", "jpeg", "webp"],
                    key="upload_img_novo_produto"
                )

            if st.button("Salvar Produto"):
                imagem_final = imagem_link.strip()

                if imagem_upload is not None:
                    imagem_final = _save_uploaded_image(imagem_upload, codigo)

                new = pd.DataFrame([{
                    "codigo": codigo,
                    "produto": produto,
                    "un": un,
                    "preco": preco,
                    "fornecedor": fornecedor,
                    "imagem": imagem_final
                }])

                products = pd.concat([products, new], ignore_index=True)
                products = products.drop_duplicates(subset=["codigo"], keep="last")
                save_table(products, PRODUCTS_FILE)

                st.success("Produto salvo.")
                st.rerun()

        st.markdown("### 📤 Exportar modelo / produtos")

        model = pd.DataFrame([{
            "codigo": "187",
            "produto": "37 ERVAS 500MG 100 CAPSULAS",
            "un": "UN",
            "preco": 20.77,
            "fornecedor": "Vitalab",
            "imagem": "assets/produtos/187.jpg"
        }])

        st.download_button(
            "⬇️ Baixar modelo de importação",
            to_excel_bytes(model),
            file_name="modelo_produtos_tigrao.xlsx"
        )

        st.download_button(
            "⬇️ Exportar produtos cadastrados",
            to_excel_bytes(products),
            file_name="produtos_tigrao.xlsx"
        )

    st.markdown("---")
    st.markdown("### 🔍 Consultar produtos")

    suppliers = sorted(products["fornecedor"].fillna("").astype(str).unique().tolist()) if len(products) else []
    suppliers = [x for x in suppliers if x.strip()]
    suppliers = ["Todos"] + suppliers

    c1, c2 = st.columns([1.4, 1])

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

    st.markdown("---")
    st.markdown("### 🖼️ Visualizar / cadastrar imagem do produto")

    if len(filtered) == 0:
        st.info("Nenhum produto disponível para visualizar.")
        return

    opcoes = []

    for _, row in filtered.iterrows():
        opcoes.append(
            f"{row.get('codigo', '')} - {row.get('produto', '')}"
        )

    produto_escolhido = st.selectbox("Selecione um produto", opcoes)

    if produto_escolhido:
        idx = opcoes.index(produto_escolhido)
        row = filtered.iloc[idx]

        codigo = str(row.get("codigo", "")).strip()
        imagem = str(row.get("imagem", "")).strip()

        st.markdown(f"**Produto:** {row.get('produto', '')}")
        st.markdown(f"**Código:** {codigo}")
        st.markdown(f"**Fornecedor:** {row.get('fornecedor', '')}")

        if imagem:
            try:
                st.image(imagem, caption=str(row.get("produto", "")), width=350)
            except Exception:
                st.warning("A imagem cadastrada não pôde ser aberta.")
        else:
            st.warning("Esse produto ainda não tem imagem cadastrada.")

        if is_admin():
            st.markdown("### 📷 Cadastrar / trocar imagem deste produto")

            nova_imagem_link = st.text_input(
                "Link da imagem",
                value=imagem if imagem.startswith("http") else "",
                key=f"link_img_{codigo}"
            )

            nova_imagem_upload = st.file_uploader(
                "Enviar imagem do computador",
                type=["png", "jpg", "jpeg", "webp"],
                key=f"upload_img_{codigo}"
            )

            if st.button("💾 Salvar imagem do produto"):
                imagem_final = nova_imagem_link.strip()

                if nova_imagem_upload is not None:
                    imagem_final = _save_uploaded_image(nova_imagem_upload, codigo)

                all_products = read_table(PRODUCTS_FILE)
                all_products = _prepare_products(all_products)
                all_products["codigo"] = all_products["codigo"].astype(str).str.strip()

                all_products.loc[
                    all_products["codigo"] == codigo,
                    "imagem"
                ] = imagem_final

                save_table(all_products, PRODUCTS_FILE)

                st.success("Imagem do produto salva com sucesso.")
                st.rerun()


def show_import_products() -> None:
    if not is_admin():
        st.error("Acesso permitido somente para administrador.")
        st.stop()

    title("📥 Importar Produtos por Excel")

    st.info("A planilha precisa ter: código, produto, unidade, preço, fornecedor e imagem.")

    model = pd.DataFrame([{
        "codigo": "187",
        "produto": "37 ERVAS 500MG 100 CAPSULAS",
        "un": "UN",
        "preco": 20.77,
        "fornecedor": "Vitalab",
        "imagem": "assets/produtos/187.jpg"
    }])

    st.download_button(
        "⬇️ Baixar modelo de importação",
        to_excel_bytes(model),
        file_name="modelo_produtos_tigrao.xlsx"
    )

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
        elif col in ["imagem", "foto", "link_imagem", "url_imagem", "image"]:
            mapping[col] = "imagem"

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

    if "imagem" not in df.columns:
        df["imagem"] = ""

    df = df[["codigo", "produto", "un", "preco", "fornecedor", "imagem"]]

    df["codigo"] = df["codigo"].astype(str).str.strip()
    df["produto"] = df["produto"].astype(str).str.strip()
    df["un"] = df["un"].astype(str).str.strip()
    df["fornecedor"] = df["fornecedor"].astype(str).str.strip()
    df["imagem"] = df["imagem"].astype(str).str.strip()
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce").fillna(0)

    df = df[df["produto"] != ""].drop_duplicates(subset=["codigo"], keep="last")

    st.markdown("### Pré-visualização")
    st.dataframe(df, use_container_width=True)

    if st.button("✅ IMPORTAR E ATUALIZAR PRODUTOS"):
        current = read_table(PRODUCTS_FILE)
        current = _prepare_products(current)

        if len(current):
            current["codigo"] = current["codigo"].astype(str).str.strip()
            new_codes = set(df["codigo"].astype(str))

            final = pd.concat([
                current[~current["codigo"].astype(str).isin(new_codes)],
                df
            ], ignore_index=True)
        else:
            final = df

        save_table(final, PRODUCTS_FILE)

        st.success("Produtos importados com sucesso.")
        st.rerun()
