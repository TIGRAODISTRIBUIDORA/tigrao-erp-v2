import streamlit as st


def apply_style() -> None:
    st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg,#050505,#101820);
        color:white;
    }

    /* Sidebar */

    [data-testid="stSidebar"]{
        background:#060606;
        border-right:1px solid #252525;
    }

    /* Títulos */

    h1,h2,h3,label,p{
        color:white !important;
    }

    .titulo{
        font-size:38px;
        font-weight:900;
        color:white;
        margin-bottom:20px;
    }

    /* Menu lateral */

    section[data-testid="stSidebar"] label{
        font-size:20px !important;
        font-weight:700 !important;
    }

    section[data-testid="stSidebar"] .stRadio label{
        font-size:20px !important;
        font-weight:700 !important;
        padding-top:8px;
        padding-bottom:8px;
    }

    section[data-testid="stSidebar"] p{
        font-size:20px !important;
        font-weight:700 !important;
    }

    section[data-testid="stSidebar"] h2{
        font-size:28px !important;
        font-weight:900 !important;
    }

    /* Cards */

    .card{
        background:#111827;
        border:1px solid #263241;
        border-radius:18px;
        padding:18px;
        margin-bottom:16px;
    }

    .valor{
        color:#ff7a00;
        font-size:32px;
        font-weight:900;
    }

    /* Sugestões */

    .sugestao{
        background:#0b1118;
        border:1px solid #27313d;
        border-radius:14px;
        padding:14px;
        margin-bottom:8px;
        font-size:18px;
    }

    .codigo{
        color:#ff7a00;
        font-weight:900;
    }

    /* Botões */

    div.stButton>button{
        background:linear-gradient(90deg,#ff7a00,#ff4d00);
        color:white;
        border:none;
        border-radius:12px;
        min-height:50px;
        font-size:18px;
        font-weight:800;
    }

    div.stButton>button:hover{
        background:linear-gradient(90deg,#ff8c1a,#ff5a00);
        color:white;
    }

    </style>
    """, unsafe_allow_html=True)


def title(text: str) -> None:
    st.markdown(
        f"<div class='titulo'>{text}</div>",
        unsafe_allow_html=True
    )


def metric_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div class='card'>
            {label}
            <br>
            <div class='valor'>{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def is_admin() -> bool:
    return st.session_state.get("perfil") == "admin"
