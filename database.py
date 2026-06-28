import os
from datetime import datetime
from io import BytesIO

import pandas as pd

DATA_DIR = "dados"
PRODUCTS_FILE = os.path.join(DATA_DIR, "produtos.xlsx")
CLIENTS_FILE = os.path.join(DATA_DIR, "clientes.xlsx")
SUPPLIERS_FILE = os.path.join(DATA_DIR, "fornecedores.xlsx")
ORDERS_FILE = os.path.join(DATA_DIR, "pedidos.xlsx")
USERS_FILE = os.path.join(DATA_DIR, "usuarios.xlsx")

COMMISSION_RATE = 0.07


def ensure_data_files() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(USERS_FILE):
        pd.DataFrame([
            {"usuario": "admin", "senha": "tigrao123", "nome": "Administrador", "perfil": "admin", "ativo": "SIM"},
            {"usuario": "vendedor", "senha": "123", "nome": "Vendedor", "perfil": "vendedor", "ativo": "SIM"},
        ]).to_excel(USERS_FILE, index=False)

    if not os.path.exists(SUPPLIERS_FILE):
        pd.DataFrame([
            {"fornecedor": "Vitalab", "contato": "", "telefone": "", "email": "", "cidade": "", "estado": "", "observacao": ""},
            {"fornecedor": "Mandiervas", "contato": "", "telefone": "", "email": "", "cidade": "", "estado": "", "observacao": ""},
        ]).to_excel(SUPPLIERS_FILE, index=False)

    if not os.path.exists(PRODUCTS_FILE):
        pd.DataFrame(columns=["codigo", "produto", "un", "preco", "fornecedor"]).to_excel(PRODUCTS_FILE, index=False)

    if not os.path.exists(CLIENTS_FILE):
        pd.DataFrame([{
            "codigo": 1,
            "cliente": "CLIENTE PADRÃO",
            "cnpj": "",
            "telefone": "",
            "cidade": "",
            "estado": ""
        }]).to_excel(CLIENTS_FILE, index=False)

    if not os.path.exists(ORDERS_FILE):
        pd.DataFrame(columns=[
            "pedido", "data", "vendedor", "cliente", "codigo", "produto", "un",
            "quantidade", "preco", "desconto", "subtotal", "total", "status"
        ]).to_excel(ORDERS_FILE, index=False)

    fix_columns()


def read_table(path: str) -> pd.DataFrame:
    try:
        return pd.read_excel(path)
    except Exception:
        return pd.DataFrame()


def save_table(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_excel(path, index=False)


def fix_columns() -> None:
    products = read_table(PRODUCTS_FILE)
    if "fornecedor" not in products.columns:
        products["fornecedor"] = ""
    for col in ["codigo", "produto", "un", "preco", "fornecedor"]:
        if col not in products.columns:
            products[col] = "" if col != "preco" else 0
    save_table(products[["codigo", "produto", "un", "preco", "fornecedor"]], PRODUCTS_FILE)

    suppliers = read_table(SUPPLIERS_FILE)
    for col in ["fornecedor", "contato", "telefone", "email", "cidade", "estado", "observacao"]:
        if col not in suppliers.columns:
            suppliers[col] = ""
    save_table(suppliers[["fornecedor", "contato", "telefone", "email", "cidade", "estado", "observacao"]], SUPPLIERS_FILE)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        str(c).strip().lower()
        .replace("ç", "c")
        .replace("ã", "a")
        .replace("á", "a")
        .replace("à", "a")
        .replace("â", "a")
        .replace("é", "e")
        .replace("ê", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ô", "o")
        .replace("ú", "u")
        for c in df.columns
    ]
    return df


def money(value) -> str:
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def to_excel_bytes(df: pd.DataFrame) -> BytesIO:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return output


def next_order_number() -> int:
    orders = read_table(ORDERS_FILE)
    if len(orders) == 0 or "pedido" not in orders.columns:
        return 1
    return int(pd.to_numeric(orders["pedido"], errors="coerce").fillna(0).max()) + 1


def now_text() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
