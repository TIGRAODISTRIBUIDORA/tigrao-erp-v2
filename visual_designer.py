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
    "Novo Pedido": [
        {"id": "cliente", "label": "Cliente", "x": 20, "y": 20, "w": 260, "h": 70, "show": True},
        {"id": "fornecedor", "label": "Fornecedor", "x": 20, "y": 110, "w": 220, "h": 70, "show": True},
        {"id": "produto", "label": "Produto", "x": 260, "y": 110, "w": 420, "h": 70, "show": True},
        {"id": "adicionar", "label": "Botão Adicionar", "x": 700, "y": 110, "w": 180, "h": 70, "show": True},
        {"id": "produto_selecionado", "label": "Produto Selecionado", "x": 20, "y": 200, "w": 600, "h": 90, "show": True},
        {"id": "quantidade", "label": "Quantidade", "x": 20, "y": 310, "w": 180, "h": 70, "show": True},
        {"id": "desconto", "label": "Desconto", "x": 220, "y": 310, "w": 180, "h": 70, "show": True},
        {"id": "total_item", "label": "Total do Item", "x": 420, "y": 310, "w": 220, "h": 70, "show": True},
        {"id": "carrinho", "label": "Carrinho", "x": 20, "y": 400, "w": 860, "h": 220, "show": True},
        {"id": "finalizar", "label": "Finalizar Pedido", "x": 20, "y": 640, "w": 220, "h": 70, "show": True},
        {"id": "limpar", "label": "Limpar Pedido", "x": 260, "y": 640, "w": 220, "h": 70, "show": True},
    ],
    "Produtos": [
        {"id": "consultar_produto", "label": "Consultar Produto", "x": 20, "y": 20, "w": 420, "h": 70, "show": True},
        {"id": "botao_buscar", "label": "Botão Buscar", "x": 460, "y": 20, "w": 90, "h": 70, "show": True},
        {"id": "card_produto", "label": "Card Produto", "x": 20, "y": 120, "w": 500, "h": 160, "show": True},
        {"id": "imagem_produto", "label": "Imagem Produto", "x": 560, "y": 120, "w": 240, "h": 260, "show": True},
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

    tela = st.selectbox("Tela para editar", list(layout.keys()))
    blocos = layout[tela]

    st.markdown("### ➕ Adicionar novo bloco")

    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:
        novo_nome = st.text_input("Nome do novo bloco", placeholder="Ex: Botão Desconto")

    with c2:
        novo_tipo = st.selectbox("Tipo", ["Botão", "Campo", "Tabela", "Card", "Imagem"])

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
                    "show": True
                })
                layout[tela] = blocos
                save_layout(layout)
                st.success("Bloco adicionado.")
                st.rerun()
            else:
                st.warning("Digite o nome do bloco.")

    st.markdown("---")
    st.info("Arraste os blocos, aumente/diminua pelas bordas e clique em 📋 Copiar Layout. Depois cole no campo de salvar.")

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

            button.gray {{
                background: #475569;
            }}

            select {{
                padding: 10px;
                border-radius: 8px;
                background: #020617;
                color: white;
                border: 1px solid #334155;
            }}

            textarea {{
                width: 100%;
                height: 140px;
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
                height: 850px;
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
            <button class="red" onclick="deleteSelected()">🗑️ Excluir Selecionado</button>
            <span>Selecione um bloco, arraste, redimensione e copie o layout.</span>
        </div>

        <div id="canvas"></div>

        <textarea id="output" placeholder="O JSON do layout aparecerá aqui automaticamente..."></textarea>

        <script>
            let blocks = {json.dumps(blocos, ensure_ascii=False)};
            let selectedIndex = null;

            const canvas = document.getElementById("canvas");
            const output = document.getElementById("output");

            function updateOutput() {{
                output.value = JSON.stringify(blocks, null, 4);
            }}

            function selectBlock(index) {{
                selectedIndex = index;
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

            function toggleSelected() {{
                if (selectedIndex === null) {{
                    alert("Selecione um bloco primeiro.");
                    return;
                }}

                blocks[selectedIndex].show = !blocks[selectedIndex].show;
                draw();
                updateOutput();
            }}

            function draw() {{
                canvas.innerHTML = "";

                blocks.forEach((b, index) => {{
                    if (b.show === undefined) b.show = true;

                    const div = document.createElement("div");
                    div.className = "box" + (b.show ? "" : " hidden-box") + (selectedIndex === index ? " selected" : "");
                    div.dataset.index = index;
                    div.style.left = b.x + "px";
                    div.style.top = b.y + "px";
                    div.style.width = b.w + "px";
                    div.style.height = b.h + "px";

                    div.innerHTML =
                        b.label +
                        "<small>X: " + b.x +
                        " | Y: " + b.y +
                        " | W: " + b.w +
                        " | H: " + b.h +
                        " | " + (b.show ? "Visível" : "Oculto") +
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

                                target.innerHTML =
                                    blocks[index].label +
                                    "<small>X: " + blocks[index].x +
                                    " | Y: " + blocks[index].y +
                                    " | W: " + blocks[index].w +
                                    " | H: " + blocks[index].h +
                                    " | " + (blocks[index].show ? "Visível" : "Oculto") +
                                    "</small>";

                                updateOutput();
                            }}
                        }}
                    }})
                    .resizable({{
                        edges: {{ left: true, right: true, bottom: true, top: true }},
                        listeners: {{
                            move(event) {{
                                const target = event.target;
                                const index = parseInt(target.dataset.index);

                                blocks[index].w = Math.round(event.rect.width);
                                blocks[index].h = Math.round(event.rect.height);
                                blocks[index].x = Math.round(blocks[index].x + event.deltaRect.left);
                                blocks[index].y = Math.round(blocks[index].y + event.deltaRect.top);

                                target.style.width = blocks[index].w + "px";
                                target.style.height = blocks[index].h + "px";
                                target.style.left = blocks[index].x + "px";
                                target.style.top = blocks[index].y + "px";

                                target.innerHTML =
                                    blocks[index].label +
                                    "<small>X: " + blocks[index].x +
                                    " | Y: " + blocks[index].y +
                                    " | W: " + blocks[index].w +
                                    " | H: " + blocks[index].h +
                                    " | " + (blocks[index].show ? "Visível" : "Oculto") +
                                    "</small>";

                                updateOutput();
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

            draw();
            updateOutput();
        </script>
    </body>
    </html>
    """

    components.html(html, height=1050, scrolling=True)

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
            st.rerun()
