st.markdown("### Cadastro de Cliente")

col1, col2 = st.columns([1, 1])

with col1:
    codigo = st.number_input("Código", min_value=1, step=1)
    cnpj = st.text_input("CNPJ")
    cidade = st.text_input("Cidade")

with col2:
    nome = st.text_input("Nome do Cliente")
    telefone = st.text_input("Telefone")
    estado = st.text_input("Estado")

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

with col_btn1:
    if st.button("💾 Salvar Cliente", use_container_width=True):
        # mantém exatamente o código que você já tem para salvar
        pass

st.markdown("---")

busca = st.text_input("🔍 Buscar cliente")
