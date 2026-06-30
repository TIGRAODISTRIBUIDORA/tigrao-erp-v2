def _renderizar_visual(blocos, componentes):
    st.markdown(
        """
        <style>
        .stButton button {
            min-height: 60px !important;
            font-size: 18px !important;
            font-weight: 800 !important;
        }

        div[data-baseweb="select"] {
            font-size: 18px !important;
        }

        div[data-baseweb="input"] input {
            font-size: 18px !important;
            min-height: 55px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    blocos_ordenados = sorted(
        blocos.items(),
        key=lambda item: (
            float(item[1].get("y", 0)),
            float(item[1].get("x", 0))
        )
    )

    linhas = {}

    for nome, cfg in blocos_ordenados:
        y = int(float(cfg.get("y", 0)) / 90)
        linhas.setdefault(y, []).append((nome, cfg))

    for _, itens in sorted(linhas.items()):
        itens = sorted(itens, key=lambda item: float(item[1].get("x", 0)))

        colunas = []
        pos_atual = 0

        for nome, cfg in itens:
            x = float(cfg.get("x", 0))
            w = float(cfg.get("w", 120))

            espaco = max(0.1, (x - pos_atual) / 100)
            largura = max(0.5, w / 80)

            if espaco > 0.1:
                colunas.append(espaco)

            colunas.append(largura)
            pos_atual = x + w

        colunas.append(1)

        cols = st.columns(colunas)

        idx_col = 0
        pos_atual = 0
        maior_altura = 70

        for nome, cfg in itens:
            x = float(cfg.get("x", 0))
            w = float(cfg.get("w", 120))
            h = float(cfg.get("h", 70))

            maior_altura = max(maior_altura, h)

            espaco = max(0.1, (x - pos_atual) / 100)

            if espaco > 0.1:
                idx_col += 1

            with cols[idx_col]:
                if nome in componentes:
                    componentes[nome]()

                sobra_altura = max(0, int((h - 70) / 20))
                for _ in range(sobra_altura):
                    st.write("")

            idx_col += 1
            pos_atual = x + w

        espaco_linha = max(0, int((maior_altura - 70) / 25))
        for _ in range(espaco_linha):
            st.write("")
