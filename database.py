import os
from datetime import datetime
from io import BytesIO

import pandas as pd

DATA_DIR = "dados"

PRODUCTS_FILE = os.path.join(DATA_DIR, "produtos.xlsx")
CLIENTS_FILE = os.path.join(DATA_DIR, "clientes.xlsx")
ORDERS_FILE = os.path.join(DATA_DIR, "pedidos.xlsx")
SUPPLIERS_FILE = os.path.join(DATA_DIR, "fornecedores.xlsx")
USERS_FILE = os.path.join(DATA_DIR, "usuarios.xlsx")
CONFIG_FILE = os.path.join(DATA_DIR, "configuracoes.xlsx")

COMMISSION_RATE = 0.07

os.makedirs(DATA_DIR, exist_ok=True)


def normalize_columns(df):
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


def read_table(file_path):
    if not os.path.exists(file_path):
        return pd.DataFrame()

    try:
        return pd.read_excel(file_path)
    except Exception:
        return pd.DataFrame()


def save_table(df, file_path):
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_excel(file_path, index=False)


def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(PRODUCTS_FILE):
        pd.DataFrame(columns=["codigo", "produto", "un", "preco", "fornecedor"]).to_excel(PRODUCTS_FILE, index=False)

    if not os.path.exists(CLIENTS_FILE):
        pd.DataFrame([{
            "codigo": 1,
            "cliente": "CLIENTE PADRÃO",
            "cnpj": "",
            "telefone": "",
            "cidade": ""
        }]).to_excel(CLIENTS_FILE, index=False)

    if not os.path.exists(ORDERS_FILE):
        pd.DataFrame(columns=[
            "pedido", "data", "vendedor", "cliente", "codigo",
            "produto", "un", "quantidade", "preco", "desconto",
            "subtotal", "total", "status"
        ]).to_excel(ORDERS_FILE, index=False)

    if not os.path.exists(SUPPLIERS_FILE):
        pd.DataFrame(columns=[
            "codigo", "fornecedor", "cnpj", "ie", "telefone",
            "whatsapp", "email", "contato", "cidade", "estado",
            "observacao"
        ]).to_excel(SUPPLIERS_FILE, index=False)

    if not os.path.exists(USERS_FILE):
        pd.DataFrame([
            {
                "usuario": "admin",
                "senha": "tigrao123",
                "nome": "Administrador",
                "perfil": "admin",
                "ativo": "SIM"
            },
            {
                "usuario": "vendedor",
                "senha": "123",
                "nome": "Vendedor",
                "perfil": "vendedor",
                "ativo": "SIM"
            }
        ]).to_excel(USERS_FILE, index=False)

    if not os.path.exists(CONFIG_FILE):
        pd.DataFrame([{
            "chave": "ultimo_pedido",
            "valor": 0
        }]).to_excel(CONFIG_FILE, index=False)


def now_text():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def money(value):
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def to_excel_bytes(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()


def _load_config():
    ensure_data_files()
    config = read_table(CONFIG_FILE)

    if len(config) == 0 or "chave" not in config.columns or "valor" not in config.columns:
        config = pd.DataFrame([{
            "chave": "ultimo_pedido",
            "valor": 0
        }])
        save_table(config, CONFIG_FILE)

    return config


def _save_config_value(chave, valor):
    config = _load_config()

    if chave in config["chave"].astype(str).tolist():
        config.loc[config["chave"].astype(str) == chave, "valor"] = valor
    else:
        novo = pd.DataFrame([{
            "chave": chave,
            "valor": valor
        }])
        config = pd.concat([config, novo], ignore_index=True)

    save_table(config, CONFIG_FILE)


def _get_config_value(chave, default=0):
    config = _load_config()
    linha = config[config["chave"].astype(str) == chave]

    if len(linha) == 0:
        return default

    try:
        return int(float(linha["valor"].iloc[0]))
    except Exception:
        return default


def next_order_number():
    ensure_data_files()

    orders = read_table(ORDERS_FILE)
    maior_pedido_existente = 0

    if len(orders) > 0 and "pedido" in orders.columns:
        try:
            maior_pedido_existente = int(pd.to_numeric(orders["pedido"], errors="coerce").max())
        except Exception:
            maior_pedido_existente = 0

    ultimo_pedido_config = _get_config_value("ultimo_pedido", 0)
    proximo = max(maior_pedido_existente, ultimo_pedido_config) + 1

    _save_config_value("ultimo_pedido", proximo)

    return proximo


def format_order_number(number):
    try:
        return f"{int(number):06d}"
    except Exception:
        return str(number)
