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


def show_new_order() -> None:
    title("🛒 Novo Pedido")

    products = read_table(PRODUCTS_FILE)
    clients = read_table(CLIENTS_FILE)

    if "fornecedor" not in products.columns:
        products["fornecedor"] = ""

    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    if "selected_product" not in st.session_state:
        st.session_state.selected_product = None

    if "produto_adicionado" not in st.session_state:
        st.session_state.produto_adicionado = False

    seller = st.session_state.get("vendedor", "")

    if len(products) == 0:
        st.warning("Nenhum produto cadastrado.")
        st.stop()

    col_cliente, col_vazio = st.columns([2, 2])

    with col_cliente:
        client_list = (
            clients["cliente"].astype(str).tolist()
            if "cliente" in clients.columns and len(clients)
            else ["CLIENTE PADRÃO"]
        )
        client = st.selectbox("Cliente", client_list)

    st.markdown("---")

    search_col, button_col, empty_col = st.columns([2.4, 1, 1.2])

    with search_col:
        search = st.text_input("🔍 Buscar produto por código, nome ou fornecedor")

    with button_col:
        st.write("")
        st.write("")
        add_clicked = st.button("➕ ADICIONAR", use_container_width=True)

        if st.session_state.get("produto_adicionado"):
            st.markdown(
                """
                <div style="
                    background:#16a34a;
                    color:white;
                    padding:10px;
                    border-radius:8px;
                    text-align:center;
                    font-weight:800;
                    animation: blink 0.35s alternate 3;
                    margin-top:8px;
                ">
                    ✅ Produto adicionado
                </div>

                <style>
                @keyframes blink {
                    from { opacity: 0.35; }
                    to { opacity: 1; }
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            st.session_state.produto_adicionado = False

    if search.strip():
        filtered = products[
            products["produto"].astype(str).str.contains(search, case=False, na=False)
            | products["codigo"].astype(str).str.contains(search, case=False, na=False)
            | products["fornecedor"].astype(str).str.contains(search, case=False, na=False)
        ].head(8)

        if len(filtered):
            options = []
            for _, row in filtered.iterrows():
                options.append(
                    f"{row.get('codigo', '')} - {row.get('produto', '')} | "
                    f"{money(_safe_float(row.get('preco', 0)))} | {row.get('fornecedor', '')}"
                )

            selected_text = st.radio(
                "Sugestões de produtos",
                options,
                label_visibility="visible",
            )

            if selected_text:
                idx = options.index(selected_text)
                st.session_state.selected_product = filtered.iloc[idx].to_dict()
        else:
            st.info("Nenhum produto encontrado.")
    else:
        st.info("Digite para buscar produtos.")

    product = st.session_state.get("selected_product")

    if product:
        codigo = str(product.get("codigo", ""))
        produto = str(product.get("produto", ""))
        fornecedor = str(product.get("fornecedor", ""))
        unidade = str(product.get("un", "UN"))
        price = _safe_float(product.get("preco", 0))

        st.markdown("### Produto selecionado")

        st.markdown(
            f"""
            <div class='card' style="max-width:720px;">
                <b>{codigo} - {produto}</b><br>
                Preço: {money(price)}<br>
                Fornecedor: {fornecedor}
            </div>
            """,
            unsafe_allow_html=True,
        )

        q1, q2, q3, q4 = st.columns([1, 1, 1.2, 1.8])

        with q1:
            quantity = st.number_input(
                "Quantidade",
                min_value=0,
                value=0,
                step=1
            )

        with q2:
            discount = st.number_input(
                "% Desconto",
                min_value=0.0,
                value=0.0,
                step=1.0
            )

        subtotal = price * quantity
        total = subtotal - (subtotal * discount / 100)

        with q3:
            st.text_input(
                "Total do item",
                value=money(total),
                disabled=True
            )

        if add_clicked:
            if quantity <= 0:
                st.warning("Informe a quantidade antes de adicionar.")
            else:
                _add_item_to_cart(product, quantity, discount)
                st.session_state.selected_product = None
                st.session_state.produto_adicionado = True
                time.sleep(0.3)
                st.rerun()
    else:
        if add_clicked:
            st.warning("Selecione um produto antes de adicionar.")

    st.markdown("---")
    st.markdown(f"### Carrinho ({len(st.session_state.carrinho)} itens)")

    if len(st.session_state.carrinho):
        cart = pd.DataFrame(st.session_state.carrinho)
        st.dataframe(cart, use_container_width=True, height=320)

        subtotal_general = cart["subtotal"].sum()
        total_general = cart["total"].sum()
        discount_general = subtotal_general - total_general

        r1, r2, r3 = st.columns(3)

        with r1:
            metric_card("Subtotal", money(subtotal_general))
        with r2:
            metric_card("Desconto", money(discount_general))
        with r3:
            metric_card("Total", money(total_general))
    else:
        st.info("Nenhum produto adicionado ao pedido.")

    f1, f2, f3 = st.columns([1.2, 1.2, 2])

    with f1:
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
                st.session_state.selected_product = None

                st.success(f"Pedido nº {number} salvo com sucesso!")
                st.rerun()

    with f2:
        if st.button("🗑️ LIMPAR PEDIDO", use_container_width=True):
            st.session_state.carrinho = []
            st.session_state.selected_product = None
            st.rerun()


def edit_order() -> None:
    st.markdown("---")
    st.markdown("## ✏️ Alterar Pedido")

    orders = read_table(ORDERS_FILE)
    products = read_table(PRODUCTS_FILE)

    if len(orders) == 0:
        st.info("Nenhum pedido disponível para alteração.")
        return

    order_list = sorted(orders["pedido"].dropna().unique())

    col_pedido, col_vazio = st.columns([1.5, 2.5])

    with col_pedido:
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
        f"Pedido nº {selected_order} | Cliente: {order_items['cliente'].iloc[0]} | "
        f"Status: {status}"
    )

    st.markdown("### Itens do pedido")

    updated_rows = []

    for idx, row in order_items.iterrows():
        st.markdown("---")
        c1, c2, c3, c4, c5 = st.columns([4, 1, 1, 1, 1])

        with c1:
            st.markdown(f"**{row['codigo']} - {row['produto']}**")
            st.caption(f"Preço unitário: {money(_safe_float(row['preco']))}")

        with c2:
            new_qty = st.number_input(
                "Qtd",
                min_value=0,
                value=int(row["quantidade"]),
                step=1,
                key=f"edit_qty_{selected_order}_{idx}",
            )

        with c3:
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

        with c4:
            st.write("Total")
            st.write(money(total))

        with c5:
            remove = st.checkbox("Excluir", key=f"remove_{selected_order}_{idx}")

        if not remove and new_qty > 0:
            new_row = row.to_dict()
            new_row["quantidade"] = new_qty
            new_row["desconto"] = new_discount
            new_row["subtotal"] = subtotal
            new_row["total"] = total
            updated_rows.append(new_row)

    st.markdown("---")
    st.markdown("### ➕ Adicionar novo produto ao pedido")

    if "edit_selected_product" not in st.session_state:
        st.session_state.edit_selected_product = None

    col_busca, col_vazio = st.columns([2.4, 1.6])

    with col_busca:
        search = st.text_input("Buscar produto para adicionar", key="edit_order_search")

    if search.strip():
        if "fornecedor" not in products.columns:
            products["fornecedor"] = ""

        filtered = products[
            products["produto"].astype(str).str.contains(search, case=False, na=False)
            | products["codigo"].astype(str).str.contains(search, case=False, na=False)
            | products["fornecedor"].astype(str).str.contains(search, case=False, na=False)
        ].head(8)

        if len(filtered):
            options = []
            for _, product in filtered.iterrows():
                options.append(
                    f"{product.get('codigo', '')} - {product.get('produto', '')} | "
                    f"{money(_safe_float(product.get('preco', 0)))}"
                )

            selected_text = st.radio(
                "Sugestões",
                options,
                key="edit_order_product_radio",
            )

            if selected_text:
                idx = options.index(selected_text)
                st.session_state.edit_selected_product = filtered.iloc[idx].to_dict()
        else:
            st.info("Nenhum produto encontrado.")

    product = st.session_state.get("edit_selected_product")

    if product:
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])

        price = _safe_float(product.get("preco", 0))

        with c1:
            st.markdown(f"**{product.get('codigo', '')} - {product.get('produto', '')}**")
            st.caption(f"Preço: {money(price)}")

        with c2:
            add_qty = st.number_input(
                "Qtd.",
                min_value=1,
                value=1,
                step=1,
                key="edit_add_qty",
            )

        with c3:
            add_discount = st.number_input(
                "% Desc.",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key="edit_add_discount",
            )

        subtotal = price * add_qty
        total = subtotal - (subtotal * add_discount / 100)

        with c4:
            st.write("Total")
            st.write(money(total))

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
            st.session_state.edit_selected_product = None
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
