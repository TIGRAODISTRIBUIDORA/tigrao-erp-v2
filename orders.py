import os
import json
import uuid
import streamlit as st
import streamlit.components.v1 as components

from ui import is_admin, title

DATA_DIR = "dados"
LAYOUT_FILE = os.path.join(DATA_DIR, "visual_layout.json")

os.makedirs(DATA_DIR, exist_ok=True)


DEFAULT_LAYOUT = {
    "Dashboard": [
        {"id": "cards_dashboard", "label": "Cards Dashboard", "tipo": "Card", "x": 20, "y": 20, "w": 860, "h": 160, "font": 18, "show": True},
        {"id": "grafico_dashboard", "label": "Gráfico Dashboard", "tipo": "Gráfico", "x": 20, "y": 200, "w": 860, "h": 300, "font": 18, "show": True},
    ],

    "Novo Pedido": [
        {"id": "cliente", "label": "Cliente", "tipo": "Campo", "x": 20, "y": 20, "w": 260, "h": 70, "font": 18, "show": True},
        {"id": "fornecedor", "label": "Fornecedor", "tipo": "Campo", "x": 20, "y": 110, "w": 220, "h": 70, "font": 18, "show": True},
        {"id": "produto", "label": "Produto", "tipo": "Campo", "x": 260, "y": 110, "w": 420, "h": 70, "font": 18, "show": True},
        {"id": "adicionar", "label": "Botão Adicionar", "tipo": "Botão", "x": 700, "y": 110, "w": 180, "h": 70, "font": 18, "show": True},
        {"id": "produto_selecionado", "label": "Produto Selecionado", "tipo": "Card", "x": 20, "y": 200, "w": 600, "h": 90, "font": 18, "show": True},
        {"id": "quantidade", "label": "Quantidade", "tipo": "Campo", "x": 20, "y": 310, "w": 180, "h": 70, "font": 18, "show": True},
        {"id": "desconto", "label": "Desconto", "tipo": "Campo", "x": 220, "y": 310, "w": 180, "h": 70, "font": 18, "show": True},
        {"id": "total_item", "label": "Total do Item", "tipo": "Campo", "x": 420, "y": 310, "w": 220, "h": 70, "font": 18, "show": True},
        {"id": "carrinho", "label": "Carrinho", "tipo": "Tabela", "x": 20, "y": 400, "w": 860, "h": 220, "font": 18, "show": True},
        {"id": "finalizar", "label": "Finalizar Pedido", "tipo": "Botão", "x": 20, "y": 640, "w": 220, "h": 70, "font": 18, "show": True},
        {"id": "limpar", "label": "Limpar Pedido", "tipo": "Botão", "x": 260, "y": 640, "w": 220, "h": 70, "font": 18, "show": True},
    ],

    "Pedidos Lançados": [
        {"id": "tabela_pedidos", "label": "Tabela Pedidos", "tipo": "Tabela", "x": 20, "y": 20, "w": 860, "h": 300, "font": 18, "show": True},
        {"id": "baixar_excel", "label": "Baixar Excel", "tipo": "Botão", "x": 20, "y": 340, "w": 220, "h": 70, "font": 18, "show": True},
        {"id": "alterar_pedido", "label": "Alterar Pedido", "tipo": "Card", "x": 20, "y": 430, "w": 860, "h": 300, "font": 18, "show": True},
        {"id": "excluir_pedido", "label": "Excluir Pedido", "tipo": "Card", "x": 20, "y": 750, "w": 400, "h": 120, "font": 18, "show": True},
    ],

    "Clientes": [
        {"id": "cadastrar_cliente", "label": "Cadastrar Cliente", "tipo": "Card", "x": 20, "y": 20, "w": 600, "h": 220, "font": 18, "show": True},
        {"id": "buscar_cliente", "label": "Buscar Cliente", "tipo": "Campo", "x": 20, "y": 260, "w": 420, "h": 70, "font": 18, "show": True},
        {"id": "card_cliente", "label": "Card Cliente", "tipo": "Card", "x": 20, "y": 350, "w": 600, "h": 160, "font": 18, "show": True},
    ],

    "Produtos": [
        {"id": "cadastrar_produto", "label": "Cadastrar Produto", "tipo": "Card", "x": 20, "y": 20, "w": 600, "h": 240, "font": 18, "show": True},
        {"id": "exportar_produtos", "label": "Exportar Produtos", "tipo": "Botão", "x": 20, "y": 280, "w": 600, "h": 100, "font": 18, "show": True},
        {"id": "consultar_produto", "label": "Consultar Produto", "tipo": "Campo", "x": 20, "y": 400, "w": 420, "h": 70, "font": 18, "show": True},
        {"id": "botao_buscar", "label": "Botão Buscar", "tipo": "Botão", "x": 460, "y": 400, "w": 90, "h": 70, "font": 18, "show": True},
        {"id": "card_produto", "label": "Card Produto", "tipo": "Card", "x": 20, "y": 500, "w": 500, "h": 160, "font": 18, "show": True},
        {"id": "imagem_produto", "label": "Imagem Produto", "tipo": "Imagem", "x": 560, "y": 500, "w": 240, "h": 260, "font": 18, "show": True},
    ],

    "Fornecedores": [
        {"id": "cadastrar_fornecedor", "label": "Cadastrar Fornecedor", "tipo": "Card", "x": 20, "y": 20, "w": 600, "h": 220, "font": 18, "show": True},
        {"id": "lista_fornecedores", "label": "Lista Fornecedores", "tipo": "Tabela", "x": 20, "y": 260, "w": 860, "h": 300, "font": 18, "show": True},
    ],

    "Vendedores": [
        {"id": "cadastrar_vendedor", "label": "Cadastrar Vendedor", "tipo": "Card", "x": 20, "y": 20, "w": 600, "h": 220, "font": 18, "show": True},
        {"id": "lista_vendedores", "label": "Lista Vendedores", "tipo": "Tabela", "x": 20, "y": 260, "w": 860, "h": 300, "font": 18, "show": True},
    ],

    "Importar Produtos": [
        {"id": "modelo_importacao", "label": "Modelo Importação", "tipo": "Botão", "x": 20, "y": 20, "w": 500, "h": 100, "font": 18, "show": True},
        {"id": "upload_planilha", "label": "Upload Planilha", "tipo": "Campo", "x": 20, "y": 140, "w": 500, "h": 100, "font": 18, "show": True},
        {"id": "preview_importacao", "label": "Prévia Importação", "tipo": "Tabela", "x": 20, "y": 260, "w": 860, "h": 300, "font": 18, "show": True},
        {"id": "botao_importar", "label": "Botão Importar", "tipo": "Botão", "x": 20, "y": 580, "w": 260, "h": 70, "font": 18, "show": True},
    ],

    "Comissões": [
        {"id": "resumo_comissoes", "label": "Resumo Comissões", "tipo": "Card", "x": 20, "y": 20, "w": 600, "h": 160, "font": 18, "show": True},
        {"id": "tabela_comissoes", "label": "Tabela Comissões", "tipo": "Tabela", "x": 20, "y": 200, "w": 860, "h": 300, "font": 18, "show": True},
    ],
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
            layout[tela] = blocos

        for tela, blocos in DEFAULT_LAYOUT.items():
            if tela not in layout:
                layout[tela] = blocos

        return layout

    except Exception:
        return DEFAULT_LAYOUT.copy()


def get_visual_layout(tela):
    layout = load_layout()
    return layout.get(tela, [])


def show_visual_designer():
    if not is_admin():
        st.error("Acesso permitido somente para administrador.")
        st.stop()

    title("🎨 Designer Visual")

    layout = load_layout()

    tela = st.selectbox(
        "Tela para editar",
        list(layout.keys())
    )

    blocos = layout[tela]

    st.markdown("### ➕ Adicionar novo bloco")

    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:
        novo_nome = st.text_input(
            "Nome do novo bloco",
            placeholder="Ex: Botão Desconto"
        )

    with c2:
        novo_tipo = st.selectbox(
            "Tipo",
            ["Botão", "Campo", "Tabela", "Card", "Imagem", "Gráfico", "Texto"]
        )

    with c3:
        st.write("")
        st.write("")
        if st.button("➕ Adicionar", use_container_width=True):
            if novo_nome.strip():
                novo_id = str(uuid.uuid4())[:8]

                blocos.append({
                    "id": novo_id,
                    "label": novo_nome.strip(),
                    "tipo": novo_tipo,
                    "x": 40,
                    "y": 40,
                    "w": 220,
                    "h": 80,
                    "font": 18,
                    "show": True
                })

                layout[tela] = blocos
                save_layout(layout)

                st.success("Bloco adicionado.")
                st.rerun()
            else:
                st.warning("Digite o nome do bloco.")

    st.markdown("---")

    st.info(
        "Arraste os blocos, aumente ou diminua pelas bordas, altere fonte, "
        "oculte, duplique ou exclua. Depois clique em Copiar Layout e salve."
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <script src="https://cdn.jsdelivr.net/npm/interactjs/dist/interact.min.js"></script>

        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: white;
            }}

            .toolbar {{
                padding: 12px;
                background: #111827;
                border-radius: 10px;
                margin-bottom: 12px;
                display: flex;
                gap: 10px;
                align-items: center;
                flex-wrap: wrap;
            }}

            button {{
                background: #f97316;
                border: none;
                color: white;
                padding: 10px 14px;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
            }}

            button.red {{
                background: #dc2626;
            }}

            button.green {{
                background: #16a34a;
            }}

            button.gray {{
                background: #475569;
            }}

            input {{
                width: 70px;
                padding: 9px;
                border-radius: 8px;
                background: #020617;
                color: white;
                border: 1px solid #334155;
                font-weight: bold;
            }}

            textarea {{
                width: 100%;
                height: 160px;
                margin-top: 10px;
                background: #020617;
                color: #22c55e;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
            }}

            #canvas {{
                position: relative;
                width: 100%;
                height: 950px;
                background:
                    linear-gradient(rgba(255,255,255,.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,.05) 1px, transparent 1px);
                background-size: 20px 20px;
                border: 2px solid #334155;
                border-radius: 14px;
                overflow: hidden;
            }}

            .box {{
                position: absolute;
                background: #f97316;
                border: 2px solid #fb923c;
                border-radius: 12px;
                color: white;
                padding: 10px;
                box-sizing: border-box;
                cursor: move;
                user-select: none;
                font-weight: 800;
                box-shadow: 0 8px 20px rgba(0,0,0,.35);
                overflow: hidden;
            }}

            .box.selected {{
                outline: 4px solid #22c55e;
                z-index: 10;
            }}

            .box small {{
                display: block;
                margin-top: 8px;
                font-size: 11px;
                color: #fff7ed;
                line-height: 1.4;
            }}

            .hidden-box {{
                opacity: 0.35;
                background: #64748b;
                border-color: #94a3b8;
            }}
        </style>
    </head>

    <body>
        <div class="toolbar">
            <button onclick="copyLayout()">📋 Copiar Layout</button>
            <button class="gray" onclick="toggleSelected()">👁️ Mostrar/Ocultar</button>
            <button class="green" onclick="duplicateSelected()">📄 Duplicar</button>
            <button class="red" onclick="deleteSelected()">🗑️ Excluir</button>

            <span>Fonte:</span>
            <button onclick="changeFont(-1)">A-</button>
            <input id="fontInput" type="number" value="18" onchange="setFontFromInput()">
            <button onclick="changeFont(1)">A+</button>

            <span>Selecione um bloco e edite.</span>
        </div>

        <div id="canvas"></div>

        <textarea id="output" placeholder="O JSON do layout aparecerá aqui automaticamente..."></textarea>

        <script>
            let blocks = {json.dumps(blocos, ensure_ascii=False)};
            let selectedIndex = null;

            const canvas = document.getElementById("canvas");
            const output = document.getElementById("output");
            const fontInput = document.getElementById("fontInput");

            function normalizeBlock(b) {{
                if (b.x === undefined) b.x = 20;
                if (b.y === undefined) b.y = 20;
                if (b.w === undefined) b.w = 220;
                if (b.h === undefined) b.h = 80;
                if (b.font === undefined) b.font = 18;
                if (b.show === undefined) b.show = true;
                if (b.tipo === undefined) b.tipo = "Bloco";
                return b;
            }}

            function updateOutput() {{
                output.value = JSON.stringify(blocks, null, 4);
            }}

            function selectBlock(index) {{
                selectedIndex = index;
                fontInput.value = blocks[index].font || 18;
                draw();
            }}

            function deleteSelected() {{
                if (selectedIndex === null) {{
                    alert("Selecione um bloco primeiro.");
                    return;
                }}

                if (confirm("Excluir esse bloco do layout?")) {{
                    blocks.splice(selectedIndex, 1);
                    selectedIndex = null;
                    draw();
                    updateOutput();
                }}
            }}

            function duplicateSelected() {{
                if (selectedIndex === null) {{
                    alert("Selecione um bloco primeiro.");
                    return;
                }}

                let original = blocks[selectedIndex];
                let novo = JSON.parse(JSON.stringify(original));

                novo.id = Math.random().toString(36).substring(2, 10);
                novo.label = original.label + " Cópia";
                novo.x = original.x + 30;
                novo.y = original.y + 30;

                blocks.push(novo);
                selectedIndex = blocks.length - 1;

                draw();
                updateOutput();
            }}

            function toggleSelected() {{
                if (selectedIndex === null) {{
                    alert("Selecione um bloco primeiro.");
                    return;
                }}

                blocks[selectedIndex].show = !blocks[selectedIndex].show;
                draw();
                updateOutput();
            }}

            function changeFont(delta) {{
                if (selectedIndex === null) {{
                    alert("Selecione um bloco primeiro.");
                    return;
                }}

                blocks[selectedIndex].font = Math.max(8, (blocks[selectedIndex].font || 18) + delta);
                fontInput.value = blocks[selectedIndex].font;

                draw();
                updateOutput();
            }}

            function setFontFromInput() {{
                if (selectedIndex === null) {{
                    alert("Selecione um bloco primeiro.");
                    return;
                }}

                blocks[selectedIndex].font = Math.max(8, parseInt(fontInput.value || 18));
                draw();
                updateOutput();
            }}

            function draw() {{
                canvas.innerHTML = "";

                blocks.forEach((b, index) => {{
                    b = normalizeBlock(b);

                    const div = document.createElement("div");
                    div.className =
                        "box" +
                        (b.show ? "" : " hidden-box") +
                        (selectedIndex === index ? " selected" : "");

                    div.dataset.index = index;

                    div.style.left = b.x + "px";
                    div.style.top = b.y + "px";
                    div.style.width = b.w + "px";
                    div.style.height = b.h + "px";
                    div.style.fontSize = b.font + "px";

                    div.innerHTML =
                        b.label +
                        "<small>" +
                        "Tipo: " + b.tipo +
                        "<br>X: " + b.x +
                        " | Y: " + b.y +
                        " | W: " + b.w +
                        " | H: " + b.h +
                        " | Fonte: " + b.font +
                        "<br>" + (b.show ? "Visível" : "Oculto") +
                        "</small>";

                    div.onclick = function(e) {{
                        e.stopPropagation();
                        selectBlock(index);
                    }};

                    canvas.appendChild(div);
                }});

                interact(".box")
                    .draggable({{
                        listeners: {{
                            move(event) {{
                                const target = event.target;
                                const index = parseInt(target.dataset.index);

                                blocks[index].x = Math.round(blocks[index].x + event.dx);
                                blocks[index].y = Math.round(blocks[index].y + event.dy);

                                target.style.left = blocks[index].x + "px";
                                target.style.top = blocks[index].y + "px";

                                updateOutput();
                                draw();
                            }}
                        }}
                    }})
                    .resizable({{
                        edges: {{
                            left: true,
                            right: true,
                            bottom: true,
                            top: true
                        }},
                        listeners: {{
                            move(event) {{
                                const target = event.target;
                                const index = parseInt(target.dataset.index);

                                blocks[index].w = Math.max(40, Math.round(event.rect.width));
                                blocks[index].h = Math.max(35, Math.round(event.rect.height));
                                blocks[index].x = Math.round(blocks[index].x + event.deltaRect.left);
                                blocks[index].y = Math.round(blocks[index].y + event.deltaRect.top);

                                target.style.width = blocks[index].w + "px";
                                target.style.height = blocks[index].h + "px";
                                target.style.left = blocks[index].x + "px";
                                target.style.top = blocks[index].y + "px";

                                updateOutput();
                                draw();
                            }}
                        }}
                    }});
            }}

            function copyLayout() {{
                updateOutput();
                navigator.clipboard.writeText(JSON.stringify(blocks, null, 4));
                alert("Layout copiado. Agora cole no campo abaixo e clique em salvar.");
            }}

            canvas.onclick = function() {{
                selectedIndex = null;
                draw();
            }};

            blocks = blocks.map(normalizeBlock);
            draw();
            updateOutput();
        </script>
    </body>
    </html>
    """

    components.html(html, height=1160, scrolling=True)

    st.markdown("---")
    st.markdown("### 💾 Salvar layout atualizado")

    novo_json = st.text_area(
        "Cole aqui o layout copiado do Designer Visual",
        height=260,
        placeholder="Cole aqui o JSON copiado..."
    )

    c1, c2 = st.columns([1, 1])

    with c1:
        if st.button("💾 Salvar Layout Visual", use_container_width=True):
            try:
                novos_blocos = json.loads(novo_json)

                if not isinstance(novos_blocos, list):
                    st.error("O layout precisa ser uma lista JSON.")
                    return

                layout[tela] = novos_blocos
                save_layout(layout)

                st.success("Layout visual salvo com sucesso.")
                st.rerun()

            except Exception as e:
                st.error(f"Erro ao salvar layout: {e}")

    with c2:
        if st.button("🔄 Restaurar Padrão", use_container_width=True):
            save_layout(DEFAULT_LAYOUT.copy())
            st.success("Layout padrão restaurado.")
            st.rerun()def _renderizar_visual(blocos, componentes):
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
