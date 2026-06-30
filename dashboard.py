import streamlit as st

from database import COMMISSION_RATE, ORDERS_FILE, money, read_table


def show_dashboard() -> None:
    orders = read_table(ORDERS_FILE)

    total_sales = orders["total"].sum() if len(orders) and "total" in orders.columns else 0
    total_orders = orders["pedido"].nunique() if len(orders) and "pedido" in orders.columns else 0
    commission = total_sales * COMMISSION_RATE

    st.markdown("""
    <style>
    .dash-hero {
        background: linear-gradient(135deg, #111827 0%, #000000 45%, #f97316 100%);
        border-radius: 0 0 28px 28px;
        padding: 26px 22px 90px;
        margin: -10px -10px 0 -10px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,.22);
    }

    .dash-hero::after {
        content: "🐯";
        position: absolute;
        right: -20px;
        bottom: -40px;
        font-size: 150px;
        opacity: .18;
    }

    .dash-logo {
        color: white !important;
        font-size: 15px;
        font-weight: 900;
        margin-bottom: 28px;
    }

    .dash-title {
        color: white !important;
        font-size: 34px;
        font-weight: 1000;
        margin-bottom: 4px;
    }

    .dash-subtitle {
        color: #ffedd5 !important;
        font-size: 15px;
        font-weight: 800;
    }

    .dash-cards {
        margin: -60px 10px 24px 10px;
        display: grid;
        grid-template-columns: 1fr;
        gap: 14px;
        position: relative;
        z-index: 2;
    }

    .dash-card {
        background: white;
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 10px 26px rgba(15,23,42,.16);
        border: 1px solid #fed7aa;
        text-align: center;
    }

    .dash-icon {
        width: 64px;
        height: 64px;
        border-radius: 18px;
        background: #111827;
        color: #f97316 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 14px;
        font-size: 32px;
    }

    .dash-label {
        color: #6b7280 !important;
        font-size: 13px;
        font-weight: 1000;
        text-transform: uppercase;
    }

    .dash-value {
        color: #111827 !important;
        font-size: 30px;
        font-weight: 1000;
        margin-top: 8px;
    }

    .dash-desc {
        color: #f97316 !important;
        font-size: 14px;
        font-weight: 900;
        margin-top: 6px;
    }

    .orders-title {
        margin: 14px 12px 12px;
        font-size: 25px;
        font-weight: 1000;
        color: #111827 !important;
    }

    .orders-box {
        background: white;
        margin: 0 10px 20px 10px;
        border-radius: 22px;
        padding: 12px;
        box-shadow: 0 8px 24px rgba(15,23,42,.10);
        border: 1px solid #e5e7eb;
    }

    .order-row {
        border-bottom: 1px solid #e5e7eb;
        padding: 13px 4px;
    }

    .order-row:last-child {
        border-bottom: none;
    }

    .order-top {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        align-items: center;
    }

    .order-number {
        color: #f97316 !important;
        font-weight: 1000;
        font-size: 15px;
    }

    .order-total {
        color: #f97316 !important;
        font-weight: 1000;
        font-size: 16px;
    }

    .order-client {
        color: #111827 !important;
        font-weight: 900;
        font-size: 14px;
        margin-top: 4px;
    }

    .order-info {
        color: #6b7280 !important;
        font-weight: 700;
        font-size: 12px;
        margin-top: 3px;
    }

    @media (min-width: 700px) {
        .dash-cards {
            grid-template-columns: repeat(3, 1fr);
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dash-hero">
        <div class="dash-logo">🐯 TIGRÃO DISTRIBUIDORA</div>
        <div class="dash-title">Dashboard</div>
        <div class="dash-subtitle">Visão geral da operação</div>
    </div>
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
            <div class="dash-desc">Valor total de vendas</div>
        </div>

        <div class="dash-card">
            <div class="dash-icon">%</div>
            <div class="dash-label">Comissão 7%</div>
            <div class="dash-value">{money(commission)}</div>
            <div class="dash-desc">Valor da comissão</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="orders-title">🕘 Últimos pedidos</div>', unsafe_allow_html=True)

    if len(orders):
        ultimos = orders.tail(20).copy()

        st.markdown('<div class="orders-box">', unsafe_allow_html=True)

        for _, row in ultimos.iterrows():
            pedido = row.get("pedido", "")
            data = row.get("data", "")
            vendedor = row.get("vendedor", "")
            cliente = row.get("cliente", "")
            total = row.get("total", 0)

            st.markdown(f"""
            <div class="order-row">
                <div class="order-top">
                    <div class="order-number">Pedido #{pedido}</div>
                    <div class="order-total">{money(total)}</div>
                </div>
                <div class="order-client">{cliente}</div>
                <div class="order-info">{data} • {vendedor}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("Nenhum pedido lançado ainda.")import streamlit as st

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
