import streamlit as st
from html import escape

from database import COMMISSION_RATE, ORDERS_FILE, money, read_table


def show_dashboard() -> None:
    orders = read_table(ORDERS_FILE)

    total_sales = orders["total"].sum() if len(orders) and "total" in orders.columns else 0
    total_orders = orders["pedido"].nunique() if len(orders) and "pedido" in orders.columns else 0
    commission = total_sales * COMMISSION_RATE

    st.markdown("""
    <style>
    .dash-cards {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin: 0 0 22px 0;
    }

    .dash-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 14px 8px;
        text-align: center;
        box-shadow: 0 8px 22px rgba(15,23,42,.14);
        border: 1px solid #f3f4f6;
        min-height: 150px;
    }

    .dash-icon {
        width: 50px;
        height: 50px;
        border-radius: 15px;
        background: #111111;
        color: #f97316 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px;
        font-size: 26px;
        font-weight: 1000;
    }

    .dash-label {
        color: #6b7280 !important;
        font-size: 11px;
        font-weight: 1000;
        text-transform: uppercase;
    }

    .dash-value {
        color: #111111 !important;
        font-size: 19px;
        font-weight: 1000;
        margin-top: 8px;
        line-height: 1.1;
    }

    .dash-desc {
        color: #f97316 !important;
        font-size: 11px;
        font-weight: 900;
        margin-top: 8px;
    }

    .orders-title {
        margin: 8px 0 12px;
        font-size: 24px;
        font-weight: 1000;
        color: #111111 !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .orders-box {
        background: #ffffff;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 22px rgba(15,23,42,.12);
        border: 1px solid #e5e7eb;
        margin-bottom: 18px;
    }

    .orders-head {
        display: grid;
        grid-template-columns: .8fr 1.7fr 1.4fr 1.5fr;
        gap: 6px;
        background: #111111;
        padding: 14px 10px;
        font-size: 11px;
        font-weight: 1000;
        text-transform: uppercase;
    }

    .orders-head div {
        color: #f97316 !important;
    }

    .orders-row {
        display: grid;
        grid-template-columns: .8fr 1.7fr 1.4fr 1.5fr;
        gap: 6px;
        padding: 13px 10px;
        border-bottom: 1px solid #e5e7eb;
        font-size: 12px;
        align-items: center;
    }

    .orders-row:last-child {
        border-bottom: none;
    }

    .orders-row div {
        color: #111827 !important;
        font-weight: 700;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    .orders-total {
        color: #f97316 !important;
        font-weight: 1000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="dash-cards">
        <div class="dash-card">
            <div class="dash-icon">📋</div>
            <div class="dash-label">Pedidos</div>
            <div class="dash-value">{total_orders}</div>
            <div class="dash-desc">Total de pedidos</div>
        </div>

        <div class="dash-card">
            <div class="dash-icon">💰</div>
            <div class="dash-label">Vendas</div>
            <div class="dash-value">{money(total_sales)}</div>
            <div class="dash-desc">Valor total</div>
        </div>

        <div class="dash-card">
            <div class="dash-icon">%</div>
            <div class="dash-label">Comissão</div>
            <div class="dash-value">{money(commission)}</div>
            <div class="dash-desc">Comissão 7%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="orders-title">🕘 Últimos pedidos</div>', unsafe_allow_html=True)

    if len(orders):
        ultimos = orders.tail(10).copy()

        st.markdown("""
        <div class="orders-box">
            <div class="orders-head">
                <div>Pedido</div>
                <div>Data</div>
                <div>Cliente</div>
                <div>Total</div>
            </div>
        """, unsafe_allow_html=True)

        for _, row in ultimos.iterrows():
            pedido = escape(str(row.get("pedido", "")))
            data = escape(str(row.get("data", "")))
            cliente = escape(str(row.get("cliente", "")))
            total = escape(money(row.get("total", 0)))

            st.markdown(f"""
            <div class="orders-row">
                <div>{pedido}</div>
                <div>{data}</div>
                <div>{cliente}</div>
                <div class="orders-total">{total}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("Nenhum pedido lançado ainda.")
