import streamlit as st


def aplicar_tema_profissional():
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        background: #f3f7fb !important;
        font-family: Arial, sans-serif;
    }

    .block-container {
        max-width: 1200px !important;
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    header, footer {
        display: none !important;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0875bd, #064b7a) !important;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
        font-weight: 800 !important;
    }

    .topo-pro {
        background: linear-gradient(135deg, #0b84d8, #0865a8);
        color: white;
        padding: 22px;
        border-radius: 24px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,.18);
    }

    .topo-pro h1 {
        margin: 0;
        font-size: 30px;
        font-weight: 900;
    }

    .topo-pro p {
        margin: 6px 0 0;
        font-size: 15px;
        opacity: .95;
    }

    .card-pro {
        background: white;
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 8px 22px rgba(15,23,42,.10);
        border: 1px solid #e5e7eb;
        margin-bottom: 18px;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #0b84d8, #0865a8) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        min-height: 54px !important;
        font-size: 16px !important;
        font-weight: 900 !important;
        box-shadow: 0 6px 14px rgba(11,132,216,.25);
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #0865a8, #064b7a) !important;
        color: white !important;
        transform: translateY(-1px);
    }

    input, textarea {
        border-radius: 16px !important;
        min-height: 50px !important;
        font-size: 16px !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 16px !important;
        min-height: 50px !important;
        font-size: 16px !important;
    }

    [data-testid="stMetric"] {
        background: white;
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 8px 22px rgba(15,23,42,.10);
        border: 1px solid #e5e7eb;
    }

    [data-testid="stDataFrame"] {
        background: white;
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 8px 22px rgba(15,23,42,.08);
    }

    h1, h2, h3 {
        color: #0f172a;
        font-weight: 900;
    }

    label {
        font-weight: 800 !important;
        color: #0f172a !important;
    }

    @media (max-width: 700px) {
        .block-container {
            padding: .6rem !important;
        }

        .topo-pro {
            border-radius: 0 0 22px 22px;
            margin: -0.6rem -0.6rem 16px -0.6rem;
            padding: 20px;
        }

        .topo-pro h1 {
            font-size: 24px;
        }

        .card-pro {
            border-radius: 18px;
            padding: 16px;
        }

        div.stButton > button {
            width: 100%;
            min-height: 58px !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def topo_app(titulo="Tigrão Distribuidora", subtitulo="Sistema profissional de pedidos"):
    st.markdown(f"""
    <div class="topo-pro">
        <h1>🐯 {titulo}</h1>
        <p>{subtitulo}</p>
    </div>
    """, unsafe_allow_html=True)


def card_inicio():
    st.markdown('<div class="card-pro">', unsafe_allow_html=True)


def card_fim():
    st.markdown('</div>', unsafe_allow_html=True)
