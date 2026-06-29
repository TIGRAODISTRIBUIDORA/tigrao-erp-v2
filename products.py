import os
import pandas as pd
import streamlit as st

from database import PRODUCTS_FILE, normalize_columns, read_table, save_table, to_excel_bytes
from suppliers import supplier_form_inline, supplier_options
from ui import is_admin, title


IMAGES_DIR = "assets/produtos"
os.makedirs(IMAGES_DIR, exist_ok=True)


def _prepare_products(df):
    for col, default in {
        "codigo": "",
        "produto": "",
        "un": "UN",
        "preco": 0,
        "fornecedor": "",
        "imagem": "",
    }.items():
        if col not in df.columns:
            df[col] = default

    df["codigo"] = df["codigo"].replace("nan", "").fillna("").astype(str).str.strip()
    df["produto"] = df["produto"].replace("nan", "").fillna("").astype(str).str.strip()
    df["un"] = df["un"].replace("nan", "UN").fillna("UN").astype(str).str.strip()
    df["fornecedor"] = df["fornecedor"].replace("nan", "").fillna("").astype(str).str.strip()
    df["imagem"] = df["imagem"].replace("nan", "").fillna("").astype(str).str.strip()
    df["preco"] = pd.to_numeric(df["preco"], errors="coerce").fillna(0)

    df = df[df["produto"] != ""]
    df = df.drop_duplicates(subset=["codigo"], keep="last")

    return df.reset_index(drop=True)


def _safe_float(value):
    try:
        return float(value)
    except Exception:
        return 0.0


def _money(value):
    return f"R$ {_safe_float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _safe_text(value):
    if pd.isna(value):
        return ""
    text = str(value).strip()
    if text.lower() == "nan":
        return ""
    return text


def _safe_filename(value):
    name = _safe_text(value)
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


def _filter_products(products, search):
    search = str(search).strip().lower()

    if not search:
        return pd.DataFrame()

    filtered = products[
        products["codigo"].astype(str).str.lower().str.contains(search, na=False) |
        products["produto"].astype(str).str.lower().str.contains(search, na=False) |
        products["fornecedor"].astype(str).str.lower().str.contains(search, na=False)
    ]

    filtered = filtered.drop_duplicates(subset=["codigo"], keep="last")

    return filtered.head(10).reset_index(drop=True)


def _resultado_button_html(texto):
    return f"""
    <div style="
        background:#f97316;
        color:white;
        padding:18px 22px;
        margin-bottom:12px;
        border-radius:12px;
        font-size:20px;
        font-weight:800;
        text-align:center;
        border:1px solid #fb923c;
        box-shadow:0 2px 6px rgba(0,0,0,0.25);
    ">
        {texto}
    </div>
    """


def show_products() -> None:
    title("📦 Produtos")

    products = read_table(PRODUCTS_FILE)
    products = _prepare_products(products)

    if "produto_consulta_codigo" not in st.session_state:
        st.session_state.produto_consulta_codigo = ""

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

    search = st.text_input(
        "Buscar produto por código, nome ou fornecedor",
        label_visibility="collapsed",
        placeholder="Digite código, nome ou fornecedor"
    )

    filtered = _filter_products(products, search)

    if search and len(filtered) == 0:
        st.warning("Nenhum produto encontrado.")

    if len(filtered):
        st.markdown("### Resultado da busca")

        st.markdown("""
        <style>
        div.stButton > button {
            font-size: 20px !important;
            font-weight: 900 !important;
            min-height: 68px !important;
            border-radius: 12px !important;
            padding: 14px 18px !important;
            text-align: center !important;
            white-space: normal !important;
        }
        </style>
        """, unsafe_allow_html=True)

        for i, row in filtered.iterrows():
            codigo = _safe_text(row.get("codigo", ""))
            produto = _safe_text(row.get("produto", ""))
            fornecedor = _safe_text(row.get("fornecedor", ""))
            preco = _money(row.get("preco", 0))

            texto = f"{codigo} - {produto} | {preco} | {fornecedor}"

            if st.button(texto, key=f"selecionar_produto_{i}", use_container_width=True):
                st.session_state.produto_consulta_codigo = codigo
                st.rerun()

    produto_selecionado = None

    if st.session_state.produto_consulta_codigo:
        encontrado = products[
            products["codigo"].astype(str) == str(st.session_state.produto_consulta_codigo)
        ]

        if len(encontrado):
            produto_selecionado = encontrado.iloc[0]

    if produto_selecionado is None:
        st.info("Digite e selecione um produto para visualizar.")
        return

    codigo = _safe_text(produto_selecionado.get("codigo", ""))
    produto = _safe_text(produto_selecionado.get("produto", ""))
    un = _safe_text(produto_selecionado.get("un", "UN"))
    preco = _safe_float(produto_selecionado.get("preco", 0))
    fornecedor = _safe_text(produto_selecionado.get("fornecedor", ""))
    imagem = _safe_text(produto_selecionado.get("imagem", ""))

    st.markdown("---")
    st.markdown("### Produto selecionado")

    col_info, col_img = st.columns([2, 1])

    with col_info:
        st.markdown(
            f"""
            <div style="
                background:#111827;
                border-radius:16px;
                padding:26px;
                border:1px solid #374151;
                line-height:1.8;
                color:white;
            ">
                <div style="font-size:32px;font-weight:900;margin-bottom:14px;">
                    {produto}
                </div>

                <div style="font-size:22px;">
                    <b>Código:</b> {codigo}
                </div>

                <div style="font-size:22px;">
                    <b>Unidade:</b> {un}
                </div>

                <div style="font-size:22px;">
                    <b>Fornecedor:</b> {fornecedor}
                </div>

                <div style="font-size:24px;margin-top:8px;">
                    <b>Preço:</b>
                    <span style="color:#22c55e;font-size:30px;font-weight:900;">
                        {_money(preco)}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_img:
        if imagem:
            try:
                st.image(imagem, caption=produto, width=420)
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

    df["codigo"] = df["codigo"].replace("nan", "").fillna("").astype(str).str.strip()
    df["produto"] = df["produto"].replace("nan", "").fillna("").astype(str).str.strip()
    df["un"] = df["un"].replace("nan", "UN").fillna("UN").astype(str).str.strip()
    df["fornecedor"] = df["fornecedor"].replace("nan", "").fillna("").astype(str).str.strip()
    df["imagem"] = df["imagem"].replace("nan", "").fillna("").astype(str).str.strip()
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
