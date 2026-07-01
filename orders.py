def show_new_order() -> None:
    _mobile_css_orders()

    products = read_table(PRODUCTS_FILE)
    products = _prepare_products(products)
    clients = read_table(CLIENTS_FILE)

    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    if "pedido_form_key" not in st.session_state:
        st.session_state.pedido_form_key = 0

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
        key=f"novo_pedido_fornecedor_mobile_{st.session_state.pedido_form_key}"
    )

    filtered_products = _filter_by_supplier(products, supplier)

    selected_text = st.selectbox(
        "Produto",
        _product_options(filtered_products),
        key=f"novo_pedido_produto_mobile_{supplier}_{st.session_state.pedido_form_key}",
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
        key=f"novo_pedido_quantidade_mobile_{st.session_state.pedido_form_key}"
    )

    discount = st.number_input(
        "% Desconto",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key=f"novo_pedido_desconto_mobile_{st.session_state.pedido_form_key}"
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

            st.session_state.pedido_form_key += 1

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

            st.markdown(
                "<hr style='margin:6px 0;border:0;border-top:1px solid #e5e7eb;'>",
                unsafe_allow_html=True
            )

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
            st.session_state.pedido_form_key += 1

            st.success(f"Pedido nº {number} salvo com sucesso!")
            time.sleep(0.8)
            st.rerun()

    if st.button("🗑️ LIMPAR PEDIDO", use_container_width=True):
        st.session_state.carrinho = []
        st.session_state.pedido_form_key += 1
        st.rerun()
