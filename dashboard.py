import streamlit as st

from database import COMMISSION_RATE, ORDERS_FILE, money, read_table
from ui import metric_card, title


def show_dashboard() -> None:
    title("📊 Dashboard")
    orders = read_table(ORDERS_FILE)

    total_sales = orders["total"].sum() if len(orders) and "total" in orders.columns else 0
    total_orders = orders["pedido"].nunique() if len(orders) and "pedido" in orders.columns else 0
    commission = total_sales * COMMISSION_RATE

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Pedidos", str(total_orders))
    with c2:
        metric_card("Vendas", money(total_sales))
    with c3:
        metric_card("Comissão 7%", money(commission))

    if len(orders):
        st.markdown("### Últimos pedidos")
        st.dataframe(orders.tail(20), use_container_width=True)
