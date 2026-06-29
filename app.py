import streamlit as st

from clients import show_clients
from commissions import show_commissions
from dashboard import show_dashboard
from database import ensure_data_files
from login import login_screen, logout
from orders import show_new_order, show_orders
from products import show_import_products, show_products
from suppliers import show_suppliers
from users import show_users
from layout_config import show_layout_config
from ui import apply_style, is_admin

st.set_page_config(page_title="Tigrão ERP", page_icon="🐯", layout="wide")

ensure_data_files()
apply_style()
login_screen()

st.sidebar.markdown("## 🐯 TIGRÃO")
st.sidebar.markdown(f"### {st.session_state.get('vendedor', '')}")
st.sidebar.markdown(f"Perfil: **{st.session_state.get('perfil', '').upper()}**")

if is_admin():
    menu_options = [
        "Dashboard",
        "Novo Pedido",
        "Pedidos Lançados",
        "Clientes",
        "Produtos",
        "Fornecedores",
        "Vendedores",
        "Importar Produtos",
        "Comissões",
        "Layout do Sistema",
        "Sair",
    ]
else:
    menu_options = [
        "Novo Pedido",
        "Pedidos Lançados",
        "Clientes",
        "Produtos",
        "Comissões",
        "Sair",
    ]

menu = st.sidebar.radio("Menu", menu_options)

if menu == "Sair":
    logout()

elif menu == "Dashboard":
    show_dashboard()

elif menu == "Novo Pedido":
    show_new_order()

elif menu == "Pedidos Lançados":
    show_orders()

elif menu == "Clientes":
    show_clients()

elif menu == "Produtos":
    show_products()

elif menu == "Fornecedores":
    show_suppliers()

elif menu == "Vendedores":
    show_users()

elif menu == "Importar Produtos":
    show_import_products()

elif menu == "Comissões":
    show_commissions()

elif menu == "Layout do Sistema":
    show_layout_config()
