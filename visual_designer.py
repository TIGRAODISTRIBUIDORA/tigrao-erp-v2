import os
import json
import uuid
import copy
import streamlit as st
import streamlit.components.v1 as components

try:
    from ui import is_admin, title
except Exception:
    def is_admin():
        return True

    def title(txt):
        st.title(txt)


DATA_DIR = "dados"
LAYOUT_FILE = os.path.join(DATA_DIR, "visual_layout.json")
os.makedirs(DATA_DIR, exist_ok=True)


TELAS_DO_SISTEMA = [
    "Dashboard",
    "Novo Pedido",
    "Editar Pedido",
    "Pedidos Lançados",
    "Clientes",
    "Produtos",
    "Fornecedores",
    "Comissão",
    "Relatórios",
    "Banco de Dados",
    "Configurações",
]


def bloco(id_, label, tipo, x, y, w, h, show=True):
    return {
        "id": id_,
        "label": label,
        "tipo": tipo,
        "x": x,
        "y": y,
        "w": w,
        "h": h,
        "show": show,
    }


DEFAULT_LAYOUT = {tela: [] for tela in TELAS_DO_SISTEMA}

DEFAULT_LAYOUT["Dashboard"] = [
    bloco("vendas_mes", "Vendas do Mês", "Card", 30, 30, 260, 120),
    bloco("pedidos_abertos", "Pedidos Abertos", "Card", 310, 30, 260, 120),
    bloco("clientes_ativos", "Clientes Ativos", "Card", 590, 30, 260, 120),
    bloco("grafico_vendas", "Gráfico de Vendas", "Tabela", 30, 180, 820, 300),
]

DEFAULT_LAYOUT["Novo Pedido"] = [
    bloco("cliente", "Cliente", "Campo", 30, 30, 420, 80),
    bloco("vendedor", "Vendedor", "Campo", 470, 30, 250, 80),
    bloco("fornecedor", "Fornecedor", "Campo", 30, 140, 260, 80),
    bloco("produto", "Produto", "Campo", 310, 140, 420, 80),
    bloco("adicionar", "Adicionar Produto", "Botão", 750, 140, 190, 80),
    bloco("produto_selecionado", "Produto Selecionado", "Card", 30, 250, 600, 100),
    bloco("quantidade", "Quantidade", "Campo", 30, 380, 180, 80),
    bloco("desconto", "Desconto", "Campo", 230, 380, 180, 80),
    bloco("total_item", "Total do Item", "Card", 430, 380, 220, 80),
    bloco("carrinho", "Carrinho do Pedido", "Tabela", 30, 490, 910, 260),
    bloco("finalizar", "Finalizar Pedido", "Botão", 30, 780, 230, 80),
    bloco("limpar", "Limpar Pedido", "Botão", 280, 780, 230, 80),
]

DEFAULT_LAYOUT["Editar Pedido"] = [
    bloco("buscar_pedido", "Buscar Pedido", "Campo", 30, 30, 420, 80),
    bloco("botao_buscar", "Buscar", "Botão", 470, 30, 160, 80),
    bloco("dados_pedido", "Dados do Pedido", "Card", 30, 140, 600, 160),
    bloco("itens_pedido", "Itens do Pedido", "Tabela", 30, 330, 850, 300),
    bloco("salvar_alteracao", "Salvar Alteração", "Botão", 30, 660, 230, 80),
]

DEFAULT_LAYOUT["Pedidos Lançados"] = [
    bloco("filtro_cliente", "Filtro Cliente", "Campo", 30, 30, 300, 80),
    bloco("filtro_data", "Filtro Data", "Campo", 350, 30, 220, 80),
    bloco("lista_pedidos", "Lista de Pedidos", "Tabela", 30, 140, 900, 430),
    bloco("exportar", "Exportar Excel", "Botão", 30, 600, 220, 80),
]

DEFAULT_LAYOUT["Clientes"] = [
    bloco("buscar_cliente", "Buscar Cliente", "Campo", 30, 30, 420, 80),
    bloco("novo_cliente", "Novo Cliente", "Botão", 470, 30, 200, 80),
    bloco("dados_cliente", "Dados do Cliente", "Card", 30, 140, 640, 180),
    bloco("lista_clientes", "Lista de Clientes", "Tabela", 30, 350, 850, 320),
]

DEFAULT_LAYOUT["Produtos"] = [
    bloco("consultar_produto", "Consultar Produto", "Campo", 30, 30, 420, 80),
    bloco("botao_buscar", "Buscar", "Botão", 470, 30, 150, 80),
    bloco("card_produto", "Card Produto", "Card", 30, 140, 520, 180),
    bloco("imagem_produto", "Imagem Produto", "Imagem", 590, 140, 260, 280),
    bloco("lista_produtos", "Lista de Produtos", "Tabela", 30, 460, 820, 260),
]

DEFAULT_LAYOUT["Fornecedores"] = [
    bloco("buscar_fornecedor", "Buscar Fornecedor", "Campo", 30, 30, 420, 80),
    bloco("novo_fornecedor", "Novo Fornecedor", "Botão", 470, 30, 220, 80),
    bloco("dados_fornecedor", "Dados do Fornecedor", "Card", 30, 140, 650, 180),
    bloco("lista_fornecedores", "Lista de Fornecedores", "Tabela", 30, 350, 850, 320),
]

DEFAULT_LAYOUT["Comissão"] = [
    bloco("filtro_vendedor", "Filtro Vendedor", "Campo", 30, 30, 350, 80),
    bloco("periodo", "Período", "Campo", 400, 30, 260, 80),
    bloco("total_vendas", "Total de Vendas", "Card", 30, 140, 260, 120),
    bloco("comissao_total", "Comissão Total", "Card", 310, 140, 260, 120),
    bloco("tabela_comissao", "Tabela de Comissão", "Tabela", 30, 300, 850, 330),
]

DEFAULT_LAYOUT["Relatórios"] = [
    bloco("relatorio_vendas", "Relatório de Vendas", "Card", 30, 30, 280, 120),
    bloco("relatorio_clientes", "Relatório de Clientes", "Card", 330, 30, 280, 120),
    bloco("relatorio_produtos", "Relatório de Produtos", "Card", 630, 30, 280, 120),
    bloco("grafico_relatorio", "Gráfico Relatório", "Tabela", 30, 190, 880, 360),
]

DEFAULT_LAYOUT["Banco de Dados"] = [
    bloco("importar_excel", "Importar Excel", "Botão", 30, 30, 220, 80),
    bloco("exportar_banco", "Exportar Banco", "Botão", 270, 30, 220, 80),
    bloco("status_banco", "Status do Banco", "Card", 30, 140, 520, 160),
    bloco("tabela_banco", "Tabela Banco de Dados", "Tabela", 30, 330, 850, 330),
]

DEFAULT_LAYOUT["Configurações"] = [
    bloco("usuarios", "Usuários", "Card", 30, 30, 300, 140),
    bloco("permissoes", "Permissões", "Card", 360, 30, 300, 140),
    bloco("config_sistema", "Configurações do Sistema", "Card", 30, 210, 630, 180),
]


def save_layout(layout):
    with open(LAYOUT_FILE, "w", encoding="utf-8") as f:
        json.dump(layout, f, ensure_ascii=False, indent=4)


def load_layout():
    padrao = copy.deepcopy(DEFAULT_LAYOUT)

    if not os.path.exists(LAYOUT_FILE):
        save_layout(padrao)
        return padrao

    try:
        with open(LAYOUT_FILE, "r", encoding="utf-8") as f:
            saved = json.load(f)

        for tela in TELAS_DO_SISTEMA:
            if tela not in saved:
                saved[tela] = padrao[tela]

        save_layout(saved)
        return saved

    except Exception:
        save_layout(padrao)
        return padrao


def get_visual_layout(tela):
    return load_layout().get(tela, [])


def show_visual_designer():
    if not is_admin():
        st.error("Acesso permitido somente para administrador.")
        st.stop()

    st.set_page_config(page_title="Designer Visual Tigrão", page_icon="🐯", layout="wide")

    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #020617 0%, #111827 60%, #1f2937 100%);
    }
    .block-container {
        padding-top: 2rem;
    }
    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label {
        color: white !important;
        font-weight: 800;
    }
    .tigr-header {
        padding: 26px;
        border-radius: 24px;
        background: linear-gradient(135deg, #f97316, #ea580c, #7c2d12);
        color: white;
        box-shadow: 0 20px 50px rgba(0,0,0,.35);
        margin-bottom: 22px;
    }
    .tigr-header h1 {
        margin: 0;
        font-size: 34px;
        font-weight: 900;
    }
    .tigr-header p {
        margin: 8px 0 0 0;
        font-size: 16px;
        opacity: .95;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tigr-header">
        <h1>🐯 Tigrão Designer Visual Premium</h1>
        <p>Monte qualquer tela do sistema arrastando, redimensionando, ocultando e salvando os blocos.</p>
    </div>
    """, unsafe_allow_html=True)

    layout = load_layout()

    ctop1, ctop2 = st.columns([2, 1])

    with ctop1:
        tela = st.selectbox("Tela para editar", TELAS_DO_SISTEMA)

    with ctop2:
        st.write("")
        st.write("")
        if st.button("🔄 Recarregar Designer", use_container_width=True):
            st.rerun()

    blocos = layout.get(tela, [])

    st.markdown("### ➕ Adicionar novo bloco")

    c1, c2, c3 = st.columns([2, 1, 1])

    with c1:
        novo_nome = st.text_input("Nome do novo bloco", placeholder="Ex: Campo Frete, Botão Desconto, Total Final")

    with c2:
        novo_tipo = st.selectbox("Tipo", ["Botão", "Campo", "Tabela", "Card", "Imagem", "Texto"])

    with c3:
        st.write("")
        st.write("")
        if st.button("➕ Adicionar", use_container_width=True):
            if novo_nome.strip():
                novo_id = str(uuid.uuid4())[:8]
                blocos.append(bloco(novo_id, novo_nome.strip(), novo_tipo, 40, 40, 240, 90))
                layout[tela] = blocos
                save_layout(layout)
                st.success("Bloco adicionado.")
                st.rerun()
            else:
                st.warning("Digite o nome do bloco.")

    st.markdown("---")

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
                background: #020617;
                color: white;
            }}

            .designer {{
                background: linear-gradient(135deg, #020617, #0f172a, #111827);
                padding: 18px;
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,.12);
                box-shadow: 0 25px 60px rgba(0,0,0,.45);
            }}

            .toolbar {{
                padding: 14px;
                background: rgba(15, 23, 42, .95);
                border: 1px solid rgba(255,255,255,.12);
                border-radius: 18px;
                margin-bottom: 16px;
                display: flex;
                gap: 10px;
                align-items: center;
                flex-wrap: wrap;
            }}

            button {{
                border: none;
                color: white;
                padding: 11px 15px;
                border-radius: 12px;
                font-weight: 900;
                cursor: pointer;
                box-shadow: 0 8px 18px rgba(0,0,0,.25);
            }}

            .orange {{ background: linear-gradient(135deg, #f97316, #ea580c); }}
            .green {{ background: linear-gradient(135deg, #22c55e, #15803d); }}
            .red {{ background: linear-gradient(135deg, #ef4444, #991b1b); }}
            .gray {{ background: linear-gradient(135deg, #64748b, #334155); }}
            .blue {{ background: linear-gradient(135deg, #3b82f6, #1d4ed8); }}

            .hint {{
                font-size: 13px;
                color: #cbd5e1;
                font-weight: 700;
            }}

            #canvas {{
                position: relative;
                width: 100%;
                height: 920px;
                background:
                    radial-gradient(circle at top left, rgba(249,115,22,.20), transparent 28%),
                    radial-gradient(circle at bottom right, rgba(59,130,246,.18), transparent 30%),
                    linear-gradient(rgba(255,255,255,.055) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(255,255,255,.055) 1px, transparent 1px),
                    #020617;
                background-size: auto, auto, 20px 20px, 20px 20px, auto;
                border: 2px solid rgba(148,163,184,.35);
                border-radius: 24px;
                overflow: hidden;
            }}

            .box {{
                position: absolute;
                border-radius: 18px;
                color: white;
                padding: 13px;
                box-sizing: border-box;
                cursor: move;
                user-select: none;
                font-weight: 900;
                box-shadow: 0 14px 32px rgba(0,0,0,.38);
                backdrop-filter: blur(10px);
                overflow: hidden;
                border: 1px solid rgba(255,255,255,.22);
            }}

            .tipo-Card {{
                background: linear-gradient(135deg, rgba(249,115,22,.98), rgba(194,65,12,.95));
            }}

            .tipo-Campo {{
                background: linear-gradient(135deg, rgba(37,99,235,.96), rgba(30,64,175,.95));
            }}

            .tipo-Botão {{
                background: linear-gradient(135deg, rgba(34,197,94,.96), rgba(21,128,61,.95));
            }}

            .tipo-Tabela {{
                background: linear-gradient(135deg, rgba(124,58,237,.96), rgba(76,29,149,.95));
            }}

            .tipo-Imagem {{
                background: linear-gradient(135deg, rgba(236,72,153,.96), rgba(157,23,77,.95));
            }}

            .tipo-Texto {{
                background: linear-gradient(135deg, rgba(100,116,139,.96), rgba(51,65,85,.95));
            }}

            .box.selected {{
                outline: 5px solid #facc15;
                z-index: 99;
                transform: scale(1.015);
            }}

            .box small {{
                display: block;
                margin-top: 8px;
                font-size: 11px;
                color: rgba(255,255,255,.88);
                line-height: 1.45;
            }}

            .hidden-box {{
                opacity: .30;
                filter: grayscale(1);
            }}

            textarea {{
                width: 100%;
                height: 170px;
                margin-top: 14px;
                background: #020617;
                color: #22c55e;
                border: 1px solid #334155;
                border-radius: 14px;
                padding: 12px;
                font-size: 12px;
                box-sizing: border-box;
            }}
        </style>
    </head>

    <body>
        <div class="designer">
            <div class="toolbar">
                <button class="green" onclick="copyLayout()">📋 Copiar Layout</button>
                <button class="blue" onclick="duplicateSelected()">📑 Duplicar</button>
                <button class="gray" onclick="toggleSelected()">👁️ Mostrar/Ocultar</button>
                <button class="red" onclick="deleteSelected()">🗑️ Excluir</button>
                <span class="hint">Clique em um bloco, arraste, redimensione pelas bordas e depois copie o layout.</span>
            </div>

            <div id="canvas"></div>

            <textarea id="output" placeholder="O JSON do layout aparecerá aqui..."></textarea>
        </div>

        <script>
            let blocks = {json.dumps(blocos, ensure_ascii=False)};
            let selectedIndex = null;

            const canvas = document.getElementById("canvas");
            const output = document.getElementById("output");

            function normalizarBloco(b) {{
                if (b.show === undefined) b.show = true;
                if (!b.tipo) b.tipo = "Card";
                if (!b.w) b.w = 220;
                if (!b.h) b.h = 80;
                if (!b.x) b.x = 30;
                if (!b.y) b.y = 30;
                return b;
            }}

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

            function duplicateSelected() {{
                if (selectedIndex === null) {{
                    alert("Selecione um bloco primeiro.");
                    return;
                }}

                let b = JSON.parse(JSON.stringify(blocks[selectedIndex]));
                b.id = Math.random().toString(36).substring(2, 10);
                b.label = b.label + " Cópia";
                b.x = b.x + 30;
                b.y = b.y + 30;
                blocks.push(b);
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

            function boxHtml(b) {{
                return `
                    ${{b.label}}
                    <small>
                        Tipo: ${{b.tipo}}<br>
                        X: ${{b.x}} | Y: ${{b.y}} | W: ${{b.w}} | H: ${{b.h}}<br>
                        ${{b.show ? "Visível" : "Oculto"}}
                    </small>
                `;
            }}

            function draw() {{
                canvas.innerHTML = "";

                blocks.forEach((b, index) => {{
                    b = normalizarBloco(b);

                    const div = document.createElement("div");
                    div.className =
                        "box tipo-" + b.tipo +
                        (b.show ? "" : " hidden-box") +
                        (selectedIndex === index ? " selected" : "");

                    div.dataset.index = index;
                    div.style.left = b.x + "px";
                    div.style.top = b.y + "px";
                    div.style.width = b.w + "px";
                    div.style.height = b.h + "px";
                    div.innerHTML = boxHtml(b);

                    div.onclick = function(e) {{
                        e.stopPropagation();
                        selectBlock(index);
                    }};

                    canvas.appendChild(div);
                }});

                interact(".box")
                    .draggable({{
                        modifiers: [
                            interact.modifiers.restrictRect({{
                                restriction: "parent",
                                endOnly: false
                            }})
                        ],
                        listeners: {{
                            move(event) {{
                                const target = event.target;
                                const index = parseInt(target.dataset.index);

                                blocks[index].x = Math.round(blocks[index].x + event.dx);
                                blocks[index].y = Math.round(blocks[index].y + event.dy);

                                target.style.left = blocks[index].x + "px";
                                target.style.top = blocks[index].y + "px";
                                target.innerHTML = boxHtml(blocks[index]);

                                updateOutput();
                            }}
                        }}
                    }})
                    .resizable({{
                        edges: {{ left: true, right: true, bottom: true, top: true }},
                        modifiers: [
                            interact.modifiers.restrictSize({{
                                min: {{ width: 80, height: 50 }}
                            }})
                        ],
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
                                target.innerHTML = boxHtml(blocks[index]);

                                updateOutput();
                            }}
                        }}
                    }});
            }}

            function copyLayout() {{
                updateOutput();
                navigator.clipboard.writeText(JSON.stringify(blocks, null, 4));
                alert("Layout copiado. Cole no campo abaixo e clique em salvar.");
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

    components.html(html, height=1200, scrolling=True)

    st.markdown("---")
    st.markdown("### 💾 Salvar layout atualizado")

    novo_json = st.text_area(
        "Cole aqui o layout copiado do Designer Visual",
        height=260,
        placeholder="Cole aqui o JSON copiado no botão 📋 Copiar Layout..."
    )

    c1, c2, c3 = st.columns([1, 1, 1])

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
        if st.button("🔄 Restaurar Tela Atual", use_container_width=True):
            layout[tela] = copy.deepcopy(DEFAULT_LAYOUT[tela])
            save_layout(layout)
            st.success("Tela restaurada.")
            st.rerun()

    with c3:
        if st.button("⚠️ Restaurar Tudo", use_container_width=True):
            save_layout(copy.deepcopy(DEFAULT_LAYOUT))
            st.success("Todo o layout foi restaurado.")
            st.rerun()
