import time
import pandas as pd
import streamlit as st

from database import (
    CLIENTS_FILE,
    ORDERS_FILE,
    PRODUCTS_FILE,
    money,
    next_order_number,
    now_text,
    read_table,
    save_table,
    to_excel_bytes,
)
from ui import is_admin, metric_card, title


def _safe_float(value):
    try:
        return float(value)
    except Exception:
        return 0.0


def _prepare_products(products):
    if "codigo" not in products.columns:
        products["codigo"] = ""
    if "produto" not in products.columns:
        products["produto"] = ""
    if "un" not in products.columns:
        products["un"] = "UN"
    if "preco" not in products.columns:
        products["preco"] = 0
    if "fornecedor" not in products.columns:
        products["fornecedor"] = ""

    products["codigo"] = products["codigo"].astype(str).str.strip()
    products["produto"] = products["produto"].astype(str).str.strip()
    products["un"] = products["un"].astype(str).str.strip()
    products["fornecedor"] = products["fornecedor"].astype(str).str.strip()
    products["preco"] = pd.to_numeric(products["preco"], errors="coerce").fillna(0)

    products = products[products["produto"] != ""]
    products = products.drop_duplicates(
        subset=["codigo", "produto", "preco", "fornecedor"],
        keep="last"
    )

    return products.reset_index(drop=True)


def _supplier_options(products):
    fornecedores = []

    if len(products) and "fornecedor" in products.columns:
        fornecedores = sorted(
            products["fornecedor"]
            .fillna("")
            .astype(str)
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .unique()
            .tolist()
        )

    return ["Todos"] + fornecedores


def _filter_by_supplier(products, supplier):
    if supplier and supplier != "Todos":
        return products[
            products["fornecedor"].astype(str).str.strip() == supplier
        ].reset_index(drop=True)

    return products.reset_index(drop=True)


def _product_options(products):
    options = ["Selecione ou digite o produto"]

    for _, row in products.iterrows():
        options.append(
            f"{row.get('codigo', '')} - {row.get('produto', '')} | "
            f"{money(_safe_float(row.get('preco', 0)))} | {row.get('fornecedor', '')}"
        )

    return options


def _get_product_from_option(products, selected_text):
    options = _product_options(products)

    if selected_text == "Selecione ou digite o produto":
        return None

    if selected_text not in options:
        return None

    idx = options.index(selected_text) - 1

    if idx < 0:
        return None

    return products.iloc[idx].to_dict()


def _add_item_to_cart(product, quantity, discount):
    codigo = str(product.get("codigo", ""))
    produto = str(product.get("produto", ""))
    unidade = str(product.get("un", "UN"))
    price = _safe_float(product.get("preco", 0))

    subtotal = price * quantity
    total = subtotal - (subtotal * discount / 100)

    st.session_state.carrinho.append({
        "codigo": codigo,
        "produto": produto,
        "un": unidade,
        "quantidade": quantity,
        "preco": price,
        "desconto": discount,
        "subtotal": subtotal,
        "total": total,
    })


def _recalcular_item(index):
    item = st.session_state.carrinho[index]

    quantidade = int(item.get("quantidade", 0))
    preco = _safe_float(item.get("preco", 0))
    desconto = _safe_float(item.get("desconto", 0))

    subtotal = preco * quantidade
    total = subtotal - (subtotal * desconto / 100)

    st.session_state.carrinho[index]["subtotal"] = subtotal
    st.session_state.carrinho[index]["total"] = total


def _mobile_css_orders():
    st.markdown("""
    <style>
    .produto-card,
    .produto-card * {
        background: #ffffff !important;
        color: #111827 !important;
    }

    .produto-card {
        border: 2px solid #f97316 !important;
        border-radius: 18px !important;
        padding: 14px !important;
        margin: 12px 0 !important;
        box-shadow: 0 6px 16px rgba(15,23,42,.12) !important;
    }

    .produto-nome {
        font-size: 16px !important;
        font-weight: 1000 !important;
        color: #111827 !important;
        margin-bottom: 6px !important;
    }

    .produto-info {
        font-size: 13px !important;
        color: #475569 !important;
        font-weight: 800 !important;
        line-height: 1.5 !important;
    }

    div[data-baseweb="select"] span {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    .total-box {
        background: #0b8de3 !important;
        border-radius: 18px !important;
        padding: 16px !important;
        text-align: center !important;
        margin: 14px 0 !important;
        box-shadow: 0 6px 16px rgba(11,141,227,.25) !important;
    }

    .total-box div {
        color: white !important;
    }

    .total-label {
        font-size: 12px !important;
        font-weight: 900 !important;
        opacity: .9 !important;
    }

    .total-valor {
        font-size: 28px !important;
        font-weight: 1000 !important;
        margin-top: 4px !important;
    }

    .cart-table-box {
        background: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 18px !important;
        padding: 10px !important;
        margin: 12px 0 !important;
        box-shadow: 0 4px 14px rgba(15,23,42,.08) !important;
    }

    .cart-header {
        display: grid !important;
        grid-template-columns: 34px 1fr 42px 64px 64px 76px !important;
        gap: 5px !important;
        padding: 7px 2px !important;
        border-bottom: 2px solid #e5e7eb !important;
        font-size: 11px !important;
        font-weight: 1000 !important;
        color: #111827 !important;
        align-items: center !important;
        text-align: center !important;
    }

    .cart-header div:nth-child(2) {
        text-align: left !important;
    }

    .cart-product {
        color: #0b8de3 !important;
        font-weight: 1000 !important;
        line-height: 1.2 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        font-size: 14px !important;
        max-width: 100% !important;
    }

    .cart-code {
        font-size: 10px !important;
        color: #64748b !important;
        font-weight: 800 !important;
        margin-top: 2px !important;
    }

    .cart-value {
        font-weight: 900 !important;
        color: #111827 !important;
        text-align: center !important;
        font-size: 13px !important;
        padding-top: 9px !important;
    }

    .cart-total-value {
        font-weight: 1000 !important;
        color: #0b8de3 !important;
        text-align: right !important;
        font-size: 14px !important;
        padding-top: 9px !important;
    }

    div[data-testid="column"] div.stButton > button {
        min-height: 34px !important;
        height: 34px !important;
        padding: 0 !important;
        border-radius: 10px !important;
        font-size: 15px !important;
        box-shadow: none !important;
    }

    div[data-testid="stNumberInput"] input {
        min-height: 34px !important;
        height: 34px !important;
        padding: 3px 5px !important;
        text-align: center !important;
        font-size: 13px !important;
        font-weight: 900 !important;
        border-radius: 10px !important;
    }

    .resumo-pedido {
        background: #111827 !important;
        border-radius: 20px !important;
        padding: 16px !important;
        margin: 10px 0 !important;
    }

    .resumo-pedido span {
        color: white !important;
    }

    .resumo-linha {
        display: flex !important;
        justify-content: space-between !important;
        font-weight: 900 !important;
        margin-bottom: 8px !important;
    }

    .resumo-total {
        border-top: 1px solid rgba(255,255,255,.25) !important;
        padding-top: 10px !important;
        margin-top: 10px !important;
        font-size: 20px !important;
    }

    div.stButton > button {
        white-space: normal !important;
    }
    </style>
    """, unsafe_allow_html=True)


def show_new_order() -> None:
    _mobile_css_orders()

    products = read_table(PRODUCTS_FILE)
    products = _prepare_products(products)
    clients = read_table(CLIENTS_FILE)

    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    seller = st.session_state.get("vendedor", "")

    if len(products) == 0:
        st.warning("Nenhum produto cadastrado.")
        return

    st.markdown("## 🛒 Novo Pedido")

    client_list = (
        clients["cliente"].astype(str).tolist()
        if "cliente" in clients.columns and len(clients)
        else ["CLIENTE PADRÃO"]
    )

    client = st.selectbox("Cliente", client_list, key="novo_pedido_cliente_mobile")

    supplier = st.selectbox(
        "Fornecedor",
        _supplier_options(products),
        key="novo_pedido_fornecedor_mobile"
    )

    filtered_products = _filter_by_supplier(products, supplier)

    selected_text = st.selectbox(
        "Produto",
        _product_options(filtered_products),
        key=f"novo_pedido_produto_mobile_{supplier}",
    )

    product = _get_product_from_option(filtered_products, selected_text)

    if product:
        codigo = str(product.get("codigo", ""))
        produto = str(product.get("produto", ""))
        fornecedor = str(product.get("fornecedor", ""))
        price = _safe_float(product.get("preco", 0))

        st.markdown(f"""
        <div class="produto-card">
            <div class="produto-nome">{produto}</div>
            <div class="produto-info">
                Código: {codigo}<br>
                Fornecedor: {fornecedor}<br>
                Preço: <b>{money(price)}</b>
            </div>
        </div>
        """, unsafe_allow_html=True)

    quantity = st.number_input(
        "Quantidade",
        min_value=0,
        value=0,
        step=1,
        key="novo_pedido_quantidade_mobile"
    )

    discount = st.number_input(
        "% Desconto",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key="novo_pedido_desconto_mobile"
    )

    price = _safe_float(product.get("preco", 0)) if product else 0
    subtotal_item = price * quantity
    total_item = subtotal_item - (subtotal_item * discount / 100)

    st.markdown(f"""
    <div class="total-box">
        <div class="total-label">TOTAL DO ITEM</div>
        <div class="total-valor">{money(total_item)}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("➕ ADICIONAR PRODUTO AO PEDIDO", use_container_width=True):
        if not product:
            st.warning("Selecione um produto antes de adicionar.")
        elif quantity <= 0:
            st.warning("Informe a quantidade antes de adicionar.")
        else:
            _add_item_to_cart(product, quantity, discount)
            st.success("Produto adicionado ao carrinho.")
            time.sleep(0.3)
            st.rerun()

    st.markdown("## 📦 Carrinho")

    if len(st.session_state.carrinho) == 0:
        st.info("Nenhum produto adicionado ao pedido.")
        subtotal_general = 0
        total_general = 0
        discount_general = 0

    else:
        st.markdown("""
        <div class="cart-table-box">
            <div class="cart-header">
                <div>🗑</div>
                <div>Produto</div>
                <div>Qtd</div>
                <div>Unit.</div>
                <div>Desc.</div>
                <div>Total</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for i, item in enumerate(st.session_state.carrinho):
            codigo = str(item.get("codigo", ""))
            produto_nome = str(item.get("produto", ""))
            quantidade = int(item.get("quantidade", 0))
            preco = _safe_float(item.get("preco", 0))
            desconto = _safe_float(item.get("desconto", 0))
            total = _safe_float(item.get("total", 0))

            col_lixeira, col_produto, col_qtd, col_preco, col_desc, col_total = st.columns(
                [0.45, 3.8, 0.8, 1.2, 1.1, 1.4]
            )

            with col_lixeira:
                if st.button("🗑", key=f"remover_item_{i}", help="Remover produto"):
                    st.session_state.carrinho.pop(i)
                    st.rerun()

            with col_produto:
                st.markdown(
                    f"""
                    <div class="cart-product">{produto_nome}</div>
                    <div class="cart-code">Cód: {codigo}</div>
                    """,
                    unsafe_allow_html=True
                )

            with col_qtd:
                nova_qtd = st.number_input(
                    "Qtd",
                    min_value=0,
                    value=quantidade,
                    step=1,
                    key=f"cart_qtd_{i}",
                    label_visibility="collapsed"
                )

            with col_preco:
                st.markdown(
                    f"<div class='cart-value'>{money(preco)}</div>",
                    unsafe_allow_html=True
                )

            with col_desc:
                novo_desc = st.number_input(
                    "Desc",
                    min_value=0.0,
                    value=desconto,
                    step=1.0,
                    key=f"cart_desc_{i}",
                    label_visibility="collapsed"
                )

            with col_total:
                st.markdown(
                    f"<div class='cart-total-value'>{money(total)}</div>",
                    unsafe_allow_html=True
                )

            st.markdown("<hr style='margin:6px 0;border:0;border-top:1px solid #e5e7eb;'>", unsafe_allow_html=True)

            if nova_qtd != quantidade or novo_desc != desconto:
                st.session_state.carrinho[i]["quantidade"] = nova_qtd
                st.session_state.carrinho[i]["desconto"] = novo_desc
                _recalcular_item(i)
                st.rerun()

        cart = pd.DataFrame(st.session_state.carrinho)
        subtotal_general = cart["subtotal"].sum()
        total_general = cart["total"].sum()
        discount_general = subtotal_general - total_general

    st.markdown(f"""
    <div class="resumo-pedido">
        <div class="resumo-linha"><span>Subtotal</span><span>{money(subtotal_general)}</span></div>
        <div class="resumo-linha"><span>Desconto</span><span>{money(discount_general)}</span></div>
        <div class="resumo-linha resumo-total"><span>Total</span><span>{money(total_general)}</span></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✅ FINALIZAR PEDIDO", use_container_width=True):
        if len(st.session_state.carrinho) == 0:
            st.warning("Adicione pelo menos um produto.")
        else:
            orders = read_table(ORDERS_FILE)
            number = next_order_number()
            date = now_text()

            rows = []

            for item in st.session_state.carrinho:
                rows.append({
                    "pedido": number,
                    "data": date,
                    "vendedor": seller,
                    "cliente": client,
                    "codigo": item["codigo"],
                    "produto": item["produto"],
                    "un": item["un"],
                    "quantidade": item["quantidade"],
                    "preco": item["preco"],
                    "desconto": item["desconto"],
                    "subtotal": item["subtotal"],
                    "total": item["total"],
                    "status": "PENDENTE",
                })

            orders = pd.concat([orders, pd.DataFrame(rows)], ignore_index=True)
            save_table(orders, ORDERS_FILE)

            st.session_state.carrinho = []

            st.success(f"Pedido nº {number} salvo com sucesso!")
            time.sleep(0.8)
            st.rerun()

    if st.button("🗑️ LIMPAR PEDIDO", use_container_width=True):
        st.session_state.carrinho = []
        st.rerun()


def edit_order() -> None:
    st.markdown("---")
    st.markdown("## ✏️ Alterar Pedido")

    orders = read_table(ORDERS_FILE)
    products = read_table(PRODUCTS_FILE)
    products = _prepare_products(products)

    if len(orders) == 0:
        st.info("Nenhum pedido disponível para alteração.")
        return

    order_list = sorted(orders["pedido"].dropna().unique())
    selected_order = st.selectbox("Selecione o pedido para alterar", order_list)

    order_items = orders[orders["pedido"] == selected_order].copy()

    if len(order_items) == 0:
        st.warning("Pedido não encontrado.")
        return

    status = str(order_items["status"].iloc[0]) if "status" in order_items.columns else "PENDENTE"

    if status.upper() == "FATURADO" and not is_admin():
        st.error("Pedido faturado não pode ser alterado pelo vendedor.")
        return

    st.info(
        f"Pedido nº {selected_order} | Cliente: {order_items['cliente'].iloc[0]} | Status: {status}"
    )

    st.markdown("### Itens do pedido")

    updated_rows = []

    for idx, row in order_items.iterrows():
        st.markdown("---")
        st.markdown(f"**{row['codigo']} - {row['produto']}**")
        st.caption(f"Preço unitário: {money(_safe_float(row['preco']))}")

        new_qty = st.number_input(
            "Qtd",
            min_value=0,
            value=int(row["quantidade"]),
            step=1,
            key=f"edit_qty_{selected_order}_{idx}",
        )

        new_discount = st.number_input(
            "% Desc.",
            min_value=0.0,
            value=_safe_float(row["desconto"]),
            step=1.0,
            key=f"edit_desc_{selected_order}_{idx}",
        )

        price = _safe_float(row["preco"])
        subtotal = price * new_qty
        total = subtotal - (subtotal * new_discount / 100)

        st.write(f"Total: **{money(total)}**")

        remove = st.checkbox("Excluir este item", key=f"remove_{selected_order}_{idx}")

        if not remove and new_qty > 0:
            new_row = row.to_dict()
            new_row["quantidade"] = new_qty
            new_row["desconto"] = new_discount
            new_row["subtotal"] = subtotal
            new_row["total"] = total
            updated_rows.append(new_row)

    st.markdown("---")
    st.markdown("### ➕ Adicionar novo produto ao pedido")

    edit_supplier_filter = st.selectbox(
        "Fornecedor",
        _supplier_options(products),
        key="edit_order_fornecedor",
    )

    edit_filtered_products = _filter_by_supplier(products, edit_supplier_filter)

    selected_text = st.selectbox(
        "Buscar produto para adicionar",
        _product_options(edit_filtered_products),
        key=f"edit_order_product_selectbox_{edit_supplier_filter}",
    )

    product = _get_product_from_option(edit_filtered_products, selected_text)

    if product:
        price = _safe_float(product.get("preco", 0))

        st.markdown(f"**{product.get('codigo', '')} - {product.get('produto', '')}**")
        st.caption(f"Preço: {money(price)}")

        add_qty = st.number_input(
            "Qtd.",
            min_value=1,
            value=1,
            step=1,
            key="edit_add_qty",
        )

        add_discount = st.number_input(
            "% Desc.",
            min_value=0.0,
            value=0.0,
            step=1.0,
            key="edit_add_discount",
        )

        subtotal = price * add_qty
        total = subtotal - (subtotal * add_discount / 100)

        st.write(f"Total: **{money(total)}**")

        if st.button("➕ Adicionar produto ao pedido"):
            base = order_items.iloc[0].to_dict()

            new_item = {
                "pedido": selected_order,
                "data": base.get("data", now_text()),
                "vendedor": base.get("vendedor", ""),
                "cliente": base.get("cliente", ""),
                "codigo": product.get("codigo", ""),
                "produto": product.get("produto", ""),
                "un": product.get("un", "UN"),
                "quantidade": add_qty,
                "preco": price,
                "desconto": add_discount,
                "subtotal": subtotal,
                "total": total,
                "status": status,
            }

            updated_rows.append(new_item)
            st.success("Produto adicionado na alteração. Clique em Salvar Alterações.")
            time.sleep(0.5)

    st.markdown("---")

    if len(updated_rows):
        preview = pd.DataFrame(updated_rows)
        st.markdown("### Prévia do pedido alterado")
        st.dataframe(preview, use_container_width=True)

        total_order = preview["total"].sum()
        metric_card("Novo total do pedido", money(total_order))
    else:
        st.warning("O pedido ficará sem itens se salvar essa alteração.")

    if st.button("💾 SALVAR ALTERAÇÕES DO PEDIDO"):
        if len(updated_rows) == 0:
            st.warning("Não é possível salvar pedido sem itens.")
            return

        all_orders = read_table(ORDERS_FILE)
        all_orders = all_orders[all_orders["pedido"] != selected_order]

        updated_df = pd.DataFrame(updated_rows)
        all_orders = pd.concat([all_orders, updated_df], ignore_index=True)

        save_table(all_orders, ORDERS_FILE)

        st.success(f"Pedido nº {selected_order} atualizado com sucesso!")
        time.sleep(0.8)
        st.rerun()


def show_orders() -> None:
    title("📋 Pedidos Lançados")

    orders = read_table(ORDERS_FILE)

    if len(orders) == 0:
        st.info("Nenhum pedido lançado.")
        return

    st.dataframe(orders, use_container_width=True)

    st.download_button(
        "⬇️ Baixar pedidos em Excel",
        to_excel_bytes(orders),
        file_name="pedidos_tigrao.xlsx",
    )

    edit_order()

    if is_admin():
        st.markdown("---")
        st.markdown("### 🗑️ Excluir Pedido")

        order_list = sorted(orders["pedido"].dropna().unique())
        selected = st.selectbox("Selecione o número do pedido que deseja excluir", order_list)

        order_data = orders[orders["pedido"] == selected]

        if len(order_data):
            st.warning(
                f"Você está prestes a excluir o pedido nº {selected} "
                f"do cliente {order_data['cliente'].iloc[0]}, "
                f"total {money(order_data['total'].sum())}."
            )

        confirm = st.checkbox(f"Confirmo que desejo excluir o pedido nº {selected}")

        if st.button("🗑️ EXCLUIR PEDIDO"):
            if not confirm:
                st.warning("Marque a confirmação antes de excluir.")
            else:
                orders = orders[orders["pedido"] != selected]
                save_table(orders, ORDERS_FILE)

                st.success(f"Pedido nº {selected} excluído com sucesso.")
                st.rerun()
