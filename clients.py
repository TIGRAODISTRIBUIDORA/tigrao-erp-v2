import re
import requests
import pandas as pd
import streamlit as st

from database import CLIENTS_FILE, read_table, save_table
from ui import is_admin, title


def limpar_cnpj(cnpj):
    return re.sub(r"\D", "", str(cnpj))


def buscar_cnpj_brasilapi(cnpj):
    cnpj_limpo = limpar_cnpj(cnpj)

    if len(cnpj_limpo) != 14:
        return None, "CNPJ inválido. Digite 14 números."

    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"

    try:
        resposta = requests.get(url, timeout=10)

        if resposta.status_code == 200:
            return resposta.json(), None

        if resposta.status_code == 404:
            return None, "CNPJ não encontrado."

        return None, f"Erro ao consultar CNPJ. Código: {resposta.status_code}"

    except Exception as e:
        return None, f"Erro de conexão: {e}"


def inicializar_campos_cliente():
    campos = {
        "cliente_cnpj": "",
        "cliente_ie": "",
        "cliente_nome": "",
        "cliente_fantasia": "",
        "cliente_telefone": "",
        "cliente_email": "",
        "cliente_cidade": "",
        "cliente_estado": "",
        "cliente_endereco": "",
        "cliente_numero": "",
        "cliente_bairro": "",
        "cliente_cep": "",
        "cliente_situacao": "",
    }

    for key, valor in campos.items():
        if key not in st.session_state:
            st.session_state[key] = valor


def limpar_campos_cliente():
    for key in [
        "cliente_cnpj",
        "cliente_ie",
        "cliente_nome",
        "cliente_fantasia",
        "cliente_telefone",
        "cliente_email",
        "cliente_cidade",
        "cliente_estado",
        "cliente_endereco",
        "cliente_numero",
        "cliente_bairro",
        "cliente_cep",
        "cliente_situacao",
    ]:
        if key in st.session_state:
            del st.session_state[key]


def show_clients() -> None:
    title("👥 Clientes")

    inicializar_campos_cliente()

    clients = read_table(CLIENTS_FILE)

    colunas_obrigatorias = [
        "codigo",
        "cliente",
        "cnpj",
        "inscricao_estadual",
        "telefone",
        "cidade",
        "estado",
        "endereco",
        "numero",
        "bairro",
        "cep",
        "email",
        "nome_fantasia",
        "situacao",
        "vendedor_login",
        "vendedor_nome",
    ]

    for col in colunas_obrigatorias:
        if col not in clients.columns:
            clients[col] = ""

    usuario_logado = st.session_state.get("usuario", "")
    vendedor_nome = st.session_state.get("vendedor", "")

    if not is_admin():
        clients = clients[clients["vendedor_login"].astype(str) == usuario_logado]

    with st.expander("Cadastrar cliente", expanded=True):
        st.markdown("### Cadastro de Cliente")

        cnpj = st.text_input("CNPJ", key="cliente_cnpj")

        if st.button("🔎 Buscar CNPJ", use_container_width=True):
            dados, erro = buscar_cnpj_brasilapi(cnpj)

            if erro:
                st.warning(erro)
            else:
                st.session_state.cliente_nome = dados.get("razao_social", "") or ""
                st.session_state.cliente_fantasia = dados.get("nome_fantasia", "") or ""
                st.session_state.cliente_telefone = dados.get("ddd_telefone_1", "") or ""
                st.session_state.cliente_email = dados.get("email", "") or ""
                st.session_state.cliente_cidade = dados.get("municipio", "") or ""
                st.session_state.cliente_estado = dados.get("uf", "") or ""
                st.session_state.cliente_endereco = dados.get("logradouro", "") or ""
                st.session_state.cliente_numero = dados.get("numero", "") or ""
                st.session_state.cliente_bairro = dados.get("bairro", "") or ""
                st.session_state.cliente_cep = dados.get("cep", "") or ""
                st.session_state.cliente_situacao = dados.get("descricao_situacao_cadastral", "") or ""

                st.success("Dados encontrados e preenchidos automaticamente.")
                st.rerun()

        nome = st.text_input("Nome do Cliente / Razão Social", key="cliente_nome")
        nome_fantasia = st.text_input("Nome Fantasia", key="cliente_fantasia")
        inscricao_estadual = st.text_input("Inscrição Estadual", key="cliente_ie")
        telefone = st.text_input("Telefone", key="cliente_telefone")
        email = st.text_input("E-mail", key="cliente_email")
        endereco = st.text_input("Endereço", key="cliente_endereco")
        numero = st.text_input("Número", key="cliente_numero")
        bairro = st.text_input("Bairro", key="cliente_bairro")
        cidade = st.text_input("Cidade", key="cliente_cidade")
        estado = st.text_input("Estado", key="cliente_estado")
        cep = st.text_input("CEP", key="cliente_cep")
        situacao = st.text_input("Situação Cadastral", key="cliente_situacao")

        salvar = st.button("💾 Salvar Cliente", use_container_width=True)

        if salvar:
            all_clients = read_table(CLIENTS_FILE)

            for col in colunas_obrigatorias:
                if col not in all_clients.columns:
                    all_clients[col] = ""

            if not nome.strip():
                st.warning("Informe o nome do cliente.")
                return

            cnpj_limpo = limpar_cnpj(cnpj)

            if cnpj_limpo and len(cnpj_limpo) != 14:
                st.warning("CNPJ inválido.")
                return

            if cnpj_limpo and len(all_clients):
                cnpj_existente = all_clients["cnpj"].astype(str).apply(limpar_cnpj)

                if cnpj_limpo in cnpj_existente.values:
                    st.warning("Esse CNPJ já está cadastrado.")
                    return

            if len(all_clients) == 0:
                novo_codigo = 1
            else:
                codigos = pd.to_numeric(
                    all_clients["codigo"],
                    errors="coerce"
                ).fillna(0)

                novo_codigo = int(codigos.max()) + 1

            new = pd.DataFrame([{
                "codigo": novo_codigo,
                "cliente": nome,
                "cnpj": cnpj,
                "inscricao_estadual": inscricao_estadual,
                "telefone": telefone,
                "cidade": cidade,
                "estado": estado,
                "endereco": endereco,
                "numero": numero,
                "bairro": bairro,
                "cep": cep,
                "email": email,
                "nome_fantasia": nome_fantasia,
                "situacao": situacao,
                "vendedor_login": usuario_logado,
                "vendedor_nome": vendedor_nome,
            }])

            all_clients = pd.concat([all_clients, new], ignore_index=True)
            all_clients = all_clients.drop_duplicates(
                subset=["codigo"],
                keep="last"
            )

            save_table(all_clients, CLIENTS_FILE)

            st.success("Cliente salvo com sucesso!")
            limpar_campos_cliente()
            st.rerun()

    st.markdown("---")

    busca = st.text_input("🔍 Buscar cliente")

    if busca and len(clients):
        clients = clients[
            clients.astype(str).apply(
                lambda row: row.str.contains(
                    busca,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ]

    st.dataframe(clients, use_container_width=True)
