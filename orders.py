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


def show_new_order() -> None:
    title("🛒 Novo Pedido")

    products = read_table(PRODUCTS_FILE)
    clients = read_table(CLIENTS_FILE)

    if "fornecedor" not in products.columns:
        products["fornecedor"] = ""

    if "carrinho" not in st.session_state:
        st.session_state.carrinho = []

    if len(products) == 0:
        st.warning("Nenhum produto cadastrado.")
        st.stop()

    c1, c2 = st.columns(2)

    with c1:
        client_list = (
            clients["cliente"].astype(str).tolist()
            if "cliente" in clients.columns and len(clients)
            else ["CLIENTE PADRÃO"]
        )
        client = st.selectbox("Cliente", client_list)

    with c2:
        seller = st.text_input("Vendedor", value=st.session_state.get("vendedor", ""))

    search = st.text_input("🔍 Buscar produto por código, nome ou fornecedor")

    if search:
        filtered = products[
            products["produto"].astype(str).str.contains(search, case=False, na=False)
            | products["codigo"].astype(str).str.contains(search, case=False, na=False)
            | products["fornecedor"].astype(str).str.contains(search, case=False, na=False)
        ]
    else:
        filtered = products.head(8)

    st.markdown("### Sugestões de produtos")

    for _, row in filtered.head(8).iterrows():
        col_info, col_qty, col_discount, col_button = st.columns([5, 1.2, 1.4, 1.8])

        codigo = str(row.get("codigo", ""))
        produto = str(row.get("produto", ""))
        fornecedor = str(row.get("fornecedor", ""))
        unidade = str(row.get("un", "UN"))

        try:
            preco = float(row.get("preco", 0))
        except Exception:
            preco = 0.0

        safe_key = f"{codigo}_{produto}".replace(" ", "_").replace("/", "_").replace(".", "_")

        with col_info:
            st.markdown(
                f"""
                <div class='sugestao'>
                    <span class='codigo'>{codigo}</span> - {produto} | {money(preco)}<br>
                    <small>Fornecedor: {fornecedor}</small>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_qty:
            quantity = st.number_input(
                "Qtd",
                min_value=1,
                value=1,
                step=1,
                key=f"qty_{safe_key}",
            )

        with col_discount:
            discount = st.number_input(
                "% Desc.",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key=f"disc_{safe_key}",
            )

        with col_button:
            st.write("")
            st.write("")

            flash_area = st.empty()

            if st.button("➕ Adicionar", key=f"add_{safe_key}"):
                subtotal = preco * quantity
                total = subtotal - (subtotal * discount / 100)

                st.session_state.carrinho.append({
                    "codigo": codigo,
                    "produto": produto,
                    "un": unidade,
                    "quantidade": quantity,
                    "preco": preco,
                    "desconto": discount,
                    "subtotal": subtotal,
                    "total": total,
                })

                flash_area.markdown(
                    """
                    <div style="
                        background:#16a34a;
                        color:white;
                        padding:12px;
                        border-radius:10px;
                        text-align:center;
                        font-weight:800;
                        animation: piscar 0.35s alternate 3;
                    ">
                        ✅ Adicionado
                    </div>

                    <style>
                    @keyframes piscar {
                        from { opacity: 0.35; }
                        to { opacity: 1; }
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                time.sleep(0.8)
                st.rerun()

    st.markdown("---")
    st.markdown(f"### Carrinho ({len(st.session_state.carrinho)} itens)")

    if len(st.session_state.carrinho):
        cart = pd.DataFrame(st.session_state.carrinho)
        st.dataframe(cart, use_container_width=True)

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

    f1, f2 = st.columns(2)

    with f1:
        if st.button("✅ FINALIZAR PEDIDO"):
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
                st.rerun()

    with f2:
        if st.button("🗑️ LIMPAR PEDIDO"):
            st.session_state.carrinho = []
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

    if is_admin():
        st.markdown("---")
        st.markdown("### 🗑️ Excluir Pedido")

        order_list = sorted(orders["pedido"].dropna().unique())
        selected = st.selectbox(
            "Selecione o número do pedido que deseja excluir",
            order_list
        )

        order_data = orders[orders["pedido"] == selected]

        if len(order_data):
            st.warning(
                f"Você está prestes a excluir o pedido nº {selected} "
                f"do cliente {order_data['cliente'].iloc[0]}, "
                f"total {money(order_data['total'].sum())}."
            )

        confirm = st.checkbox(
            f"Confirmo que desejo excluir o pedido nº {selected}"
        )

        if st.button("🗑️ EXCLUIR PEDIDO"):
            if not confirm:
                st.warning("Marque a confirmação antes de excluir.")
            else:
                orders = orders[orders["pedido"] != selected]
                save_table(orders, ORDERS_FILE)

                st.success(f"Pedido nº {selected} excluído com sucesso.")
                st.rerun()
