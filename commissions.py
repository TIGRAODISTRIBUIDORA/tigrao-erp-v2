import streamlit as st

from database import COMMISSION_RATE, ORDERS_FILE, read_table
from ui import title


def show_commissions() -> None:
    title("💰 Comissões")
    orders = read_table(ORDERS_FILE)
    if len(orders) == 0:
        st.info("Ainda não existem pedidos.")
        return
    summary = orders.groupby("vendedor")["total"].sum().reset_index()
    summary["comissao_7%"] = summary["total"] * COMMISSION_RATE
    st.dataframe(summary, use_container_width=True)
