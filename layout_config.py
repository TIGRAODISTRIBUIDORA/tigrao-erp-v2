import os
import json
import streamlit as st

from ui import is_admin, title

DATA_DIR = "dados"
LAYOUT_FILE = os.path.join(DATA_DIR, "layout_builder.json")

os.makedirs(DATA_DIR, exist_ok=True)


DEFAULT_LAYOUT = {
    "Novo Pedido": {
        "Cliente": {"x": 1, "y": 1, "w": 2, "h": 1, "mostrar": True},
        "Fornecedor": {"x": 1, "y": 2, "w": 1.2, "h": 1, "mostrar": True},
        "Produto": {"x": 2, "y": 2, "w": 2.4, "h": 1, "mostrar": True},
        "Botão Adicionar": {"x": 3, "y": 2, "w": 1, "h": 1, "mostrar": True},
        "Produto Selecionado": {"x": 1, "y": 3, "w": 4, "h": 1, "mostrar": True},
        "Quantidade": {"x": 1, "y": 4, "w": 1, "h": 1, "mostrar": True},
        "Desconto": {"x": 2, "y": 4, "w": 1, "h": 1, "mostrar": True},
        "Total do Item": {"x": 3, "y": 4, "w": 1.2, "h": 1, "mostrar": True},
        "Carrinho": {"x": 1, "y": 5, "w": 5, "h": 2, "mostrar": True},
        "Finalizar Pedido": {"x": 1, "y": 6, "w": 1.2, "h": 1, "mostrar": True},
        "Limpar Pedido": {"x": 2, "y": 6, "w": 1.2, "h": 1, "mostrar": True},
    },
    "Produtos": {
        "Cadastrar Produto": {"x": 1, "y": 1, "w": 4, "h": 1, "mostrar": True},
        "Exportar Produtos": {"x": 1, "y": 2, "w": 4, "h": 1, "mostrar": True},
        "Consultar Produto": {"x": 1, "y": 3, "w": 2, "h": 1, "mostrar": True},
        "Botão Buscar": {"x": 2, "y": 3, "w": 0.5, "h": 1, "mostrar": True},
        "Card Produto": {"x": 1, "y": 4, "w": 2, "h": 1, "mostrar": True},
        "Imagem Produto": {"x": 2, "y": 4, "w": 1, "h": 1, "mostrar": True},
    },
    "Clientes": {
        "Cadastrar Cliente": {"x": 1, "y": 1, "w": 4, "h": 1, "mostrar": True},
        "Buscar Cliente": {"x": 1, "y": 2, "w": 2, "h": 1, "mostrar": True},
        "Card Cliente": {"x": 1, "y": 3, "w": 3, "h": 1, "mostrar": True},
    },
    "Pedidos Lançados": {
        "Tabela Pedidos": {"x": 1, "y": 1, "w": 5, "h": 1, "mostrar": True},
        "Baixar Excel": {"x": 1, "y": 2, "w": 1.5, "h": 1, "mostrar": True},
        "Alterar Pedido": {"x": 1, "y": 3, "w": 5, "h": 1, "mostrar": True},
        "Excluir Pedido": {"x": 1, "y": 4, "w": 3, "h": 1, "mostrar": True},
    },
    "Dashboard": {
        "Cards": {"x": 1, "y": 1, "w": 5, "h": 1, "mostrar": True},
        "Gráficos": {"x": 1, "y": 2, "w": 5, "h": 1, "mostrar": True},
    },
    "Comissões": {
        "Resumo": {"x": 1, "y": 1, "w": 4, "h": 1, "mostrar": True},
        "Tabela": {"x": 1, "y": 2, "w": 5, "h": 1, "mostrar": True},
    },
    "Fornecedores": {
        "Cadastrar Fornecedor": {"x": 1, "y": 1, "w": 4, "h": 1, "mostrar": True},
        "Lista Fornecedores": {"x": 1, "y": 2, "w": 5, "h": 1, "mostrar": True},
    },
    "Vendedores": {
        "Cadastrar Vendedor": {"x": 1, "y": 1, "w": 4, "h": 1, "mostrar": True},
        "Lista Vendedores": {"x": 1, "y": 2, "w": 5, "h": 1, "mostrar": True},
    },
}


def save_layout(layout):
    with open(LAYOUT_FILE, "w", encoding="utf-8") as f:
        json.dump(layout, f, ensure_ascii=False, indent=4)


def load_layout():
    if not os.path.exists(LAYOUT_FILE):
        save_layout(DEFAULT_LAYOUT)
        return DEFAULT_LAYOUT.copy()

    try:
        with open(LAYOUT_FILE, "r", encoding="utf-8") as f:
            saved = json.load(f)

        layout = DEFAULT_LAYOUT.copy()

        for tela, blocos in saved.items():
            if tela not in layout:
                layout[tela] = {}

            for bloco, config in blocos.items():
                layout[tela][bloco] = {
                    "x": config.get("x", config.get("coluna", 1)),
                    "y": config.get("y", config.get("linha", 1)),
                    "w": config.get("w", config.get("largura", 1)),
                    "h": config.get("h", 1),
                    "mostrar": config.get("mostrar", True),
                }

        return layout
    except Exception:
        return DEFAULT_LAYOUT.copy()


def get_screen_layout(tela):
    layout = load_layout()
    return layout.get(tela, {})


def _move(config, dx=0, dy=0):
    config["x"] = max(1, float(config.get("x", 1)) + dx)
    config["y"] = max(1, float(config.get("y", 1)) + dy)
    return config


def _resize(config, dw=0, dh=0):
    config["w"] = max(0.5, float(config.get("w", 1)) + dw)
    config["h"] = max(1, float(config.get("h", 1)) + dh)
    return config


def _preview_card(nome, cfg, selecionado=False):
    cor = "#ff7a00" if selecionado else "#111827"
    borda = "#ffb000" if selecionado else "#374151"
    display = "✅" if cfg.get("mostrar", True) else "🚫"

    st.markdown(
        f"""
        <div style="
            background:{cor};
            border:2px solid {borda};
            border-radius:12px;
            padding:14px;
            margin-bottom:8px;
            color:white;
            font-weight:800;
            font-size:16px;
        ">
            {display} {nome}<br>
            <span style="font-size:13px;">
                X: {cfg.get("x", 1)} | Y: {cfg.get("y", 1)} | Largura: {cfg.get("w", 1)} | Altura: {cfg.get("h", 1)}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_layout_config():
    if not is_admin():
        st.error("Acesso permitido somente para administrador.")
        st.stop()

    title("🎨 Criar Layout")

    st.info("Escolha uma aba, selecione um bloco e use os botões para mover, aumentar, diminuir ou ocultar.")

    layout = load_layout()

    tela = st.selectbox("Aba do sistema", list(layout.keys()))
    blocos = list(layout[tela].keys())
    bloco = st.selectbox("Bloco da aba", blocos)

    config = layout[tela][bloco]

    st.markdown(f"## Editando: {tela} → {bloco}")

    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown("### Mover bloco")

        b1, b2, b3 = st.columns(3)
        with b2:
            if st.button("⬆️", use_container_width=True):
                layout[tela][bloco] = _move(config, dy=-1)
                save_layout(layout)
                st.rerun()

        b4, b5, b6 = st.columns(3)
        with b4:
            if st.button("⬅️", use_container_width=True):
                layout[tela][bloco] = _move(config, dx=-1)
                save_layout(layout)
                st.rerun()
        with b5:
            st.markdown("<div style='text-align:center;font-weight:900;'>Mover</div>", unsafe_allow_html=True)
        with b6:
            if st.button("➡️", use_container_width=True):
                layout[tela][bloco] = _move(config, dx=1)
                save_layout(layout)
                st.rerun()

        b7, b8, b9 = st.columns(3)
        with b8:
            if st.button("⬇️", use_container_width=True):
                layout[tela][bloco] = _move(config, dy=1)
                save_layout(layout)
                st.rerun()

        st.markdown("---")
        st.markdown("### Tamanho")

        t1, t2 = st.columns(2)
        with t1:
            if st.button("➖ Largura", use_container_width=True):
                layout[tela][bloco] = _resize(config, dw=-0.5)
                save_layout(layout)
                st.rerun()
        with t2:
            if st.button("➕ Largura", use_container_width=True):
                layout[tela][bloco] = _resize(config, dw=0.5)
                save_layout(layout)
                st.rerun()

        a1, a2 = st.columns(2)
        with a1:
            if st.button("➖ Altura", use_container_width=True):
                layout[tela][bloco] = _resize(config, dh=-1)
                save_layout(layout)
                st.rerun()
        with a2:
            if st.button("➕ Altura", use_container_width=True):
                layout[tela][bloco] = _resize(config, dh=1)
                save_layout(layout)
                st.rerun()

        st.markdown("---")

        mostrar = st.checkbox("Mostrar bloco", value=bool(config.get("mostrar", True)))
        if mostrar != bool(config.get("mostrar", True)):
            config["mostrar"] = mostrar
            layout[tela][bloco] = config
            save_layout(layout)
            st.rerun()

        if st.button("🔄 Restaurar Layout Padrão", use_container_width=True):
            save_layout(DEFAULT_LAYOUT.copy())
            st.success("Layout padrão restaurado.")
            st.rerun()

    with c2:
        st.markdown("### Prévia dos blocos")

        blocos_ordenados = sorted(
            layout[tela].items(),
            key=lambda item: (float(item[1].get("y", 1)), float(item[1].get("x", 1)))
        )

        for nome, cfg in blocos_ordenados:
            _preview_card(nome, cfg, selecionado=(nome == bloco))
