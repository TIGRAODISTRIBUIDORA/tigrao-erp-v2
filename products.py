import os
import pandas as pd
import streamlit as st

from database import PRODUCTS_FILE, normalize_columns, read_table, save_table, to_excel_bytes
from suppliers import supplier_form_inline, supplier_options
from ui import is_admin, title


IMAGES_DIR = "assets/produtos"
os.makedirs(IMAGES_DIR, exist_ok=True)


def _prepare_products(df):
    if "codigo" not in df.columns:
        df["codigo"] = ""

    if "produto" not in df.columns:
        df["produto"] = ""

    if "un" not in df.columns:
        df["un"] = "UN"

    if "preco" not in df.columns:
        df["preco"] = 0

    if "fornecedor" not in df.columns:
        df["fornecedor"] = ""

    if "imagem" not in df.columns:
        df["imagem"] = ""

    df["codigo"] = df["codigo"].astype(str).str.strip()
    df["produto"] = df["produto"].astype(str).str.strip()
    df["un"] = df["un"].astype(str).str.strip()
    df["fornecedor"] = df["fornecedor"].astype(str).str.strip()
    df["imagem"] = df["imagem"].astype(str).str.strip()
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce").fillna(0)

    df = df[df["produto"] != ""]
    df = df.drop_duplicates(
        subset=["codigo", "produto", "preco", "fornecedor"],
        keep="last"
    )

    return df.reset_index(drop=True)


def _safe_float(value):
    try:
        return float(value)
    except Exception:
        return 0.0


def _money(value):
    return f"R$ {_safe_float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


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


def _product_options(products):
    options = ["Selecione ou digite o produto"]
    vistos = set()

    for idx, row in products.iterrows():
        codigo = str(row.get("codigo", "")).strip()
        produto = str(row.get("produto", "")).strip()
        preco = _money(row.get("preco", 0))
        fornecedor = str(row.get("fornecedor", "")).strip()

        chave = f"{codigo}|{produto}|{preco}|{fornecedor}"

        if chave in vistos:
            continue

        vistos.add(chave)

        options.append(
            f"{idx} | {codigo} - {produto} | {preco} | {fornecedor}"
        )

    return options


def _get_product_from_option(products, selected_text):
    if selected_text == "Selecione ou digite o produto":
        return None

    try:
        idx = int(str(selected_text).split("|")[0].strip())

        if idx not in products.index:
            return None

        return products.loc[idx]
    except Exception:
        return None


def show_products() -> None:
    title("📦 Produtos")

    products = read_table(PRODUCTS_FILE)
    products = _prepare_products(products)

    if "produto_busca_aplicada" not in st.session_state:
        st.session_state.produto_busca_aplicada = False

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
                products = _prepare_products(products)
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
    st.markdown("### 🔍 Consultar produto")

    col_busca, col_botao, col_vazio = st.columns([4, 0.7, 5.3])

    with col_busca:
        selected_text = st.selectbox(
            "Buscar produto por código ou nome",
            _product_options(products),
            key="consulta_produto_selectbox",
            label_visibility="collapsed",
        )

    with col_botao:
        st.write("")
        buscar = st.button("🔍", use_container_width=True)

    if buscar:
        st.session_state.produto_busca_aplicada = True

    if not st.session_state.produto_busca_aplicada:
        st.info("Selecione um produto e clique na lupa para visualizar.")
        return

    produto_selecionado = _get_product_from_option(products, selected_text)

    if produto_selecionado is None:
        st.info("Digite ou selecione um produto para visualizar.")
        return

    codigo = str(produto_selecionado.get("codigo", "")).strip()
    produto = str(produto_selecionado.get("produto", "")).strip()
    un = str(produto_selecionado.get("un", "UN")).strip()
    preco = _safe_float(produto_selecionado.get("preco", 0))
    fornecedor = str(produto_selecionado.get("fornecedor", "")).strip()
    imagem = str(produto_selecionado.get("imagem", "")).strip()

    st.markdown("---")
    st.markdown("### Produto selecionado")

    col_info, col_img = st.columns([2, 1])

    with col_info:
        st.markdown(
            f"""
            <div class='card'>
                <b>Código:</b> {codigo}<br>
                <b>Produto:</b> {produto}<br>
                <b>Unidade:</b> {un}<br>
                <b>Preço:</b> {_money(preco)}<br>
                <b>Fornecedor:</b> {fornecedor}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_img:
        if imagem:
            try:
                st.image(imagem, caption=produto, width=300)
            except Exception:
                st.warning("A imagem cadastrada não pôde ser aberta.")
        else:
            st.warning("Esse produto ainda não tem imagem cadastrada.")

    if is_admin():
        st.markdown("---")
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

    df = df[df["produto"] != ""]
    df = df.drop_duplicates(subset=["codigo"], keep="last")

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

        final = _prepare_products(final)
        final = final.drop_duplicates(subset=["codigo"], keep="last")

        save_table(final, PRODUCTS_FILE)

        st.success("Produtos importados com sucesso.")
        st.rerun()
