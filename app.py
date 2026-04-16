import streamlit as st

# 1. Configuração de Estética e Layout
st.set_page_config(
    page_title="ISOSED Cosmópolis - Portal de Gestão",
    page_icon="⛪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS para esconder a barra lateral e estilizar os botões centrais
st.markdown("""
    <style>
    /* Esconde a barra lateral e o botão de menu */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        display: none;
    }
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 5em;
        background-color: #1a1a1a;
        color: white;
        font-weight: bold;
        border: 2px solid #2e7bcf;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2e7bcf;
        border-color: white;
    }
    .login-header {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #1a1a1a 0%, #004a99 100%);
        border-radius: 15px;
        margin-bottom: 25px;
        color: white;
        border: 1px solid #2e7bcf;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Inicialização do Estado
if "logado" not in st.session_state:
    st.session_state.logado = False
if "perfil" not in st.session_state:
    st.session_state.perfil = None

USUARIOS = {
    "pastor": {"senha": "123", "perfil": "Pastores"},
    "secretaria": {"senha": "456", "perfil": "Secretária"},
    "comunicacao": {"senha": "789", "perfil": "Comunicação"}
}

def validar_login(usuario, senha):
    if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
        st.session_state.logado = True
        st.session_state.perfil = USUARIOS[usuario]["perfil"]
        return True
    return False

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.markdown("""
        <div class="login-header">
            <h1>INSTITUCIONAL ISOSED</h1>
            <p style="opacity: 0.8;">Sistema de Gestão Eclesiástica | Cosmópolis/SP</p>
        </div>
    """, unsafe_allow_html=True)

    left_co, cent_co, last_co = st.columns([0.5, 3, 0.5])
    with cent_co:
        with st.form("login_form"):
            usuario = st.text_input("Usuário", placeholder="Identificação")
            senha = st.text_input("Senha", type="password", placeholder="••••••••")
            if st.form_submit_button("ACESSAR PORTAL"):
                if validar_login(usuario, senha):
                    st.rerun()
                else:
                    st.error("Credenciais incorretas.")

# --- TELA INICIAL (MENU DE BOTÕES 2x2) ---
else:
    st.markdown(f"""
        <div class="login-header">
            <h2>Portal de Comando</h2>
            <p>Sessão ativa: {st.session_state.perfil}</p>
        </div>
    """, unsafe_allow_html=True)

    # Primeira Linha de Botões
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        if st.button("📝 NOVO CADASTRO"):
            st.switch_page("pages/1_📝_Cadastro.py")

    with row1_col2:
        if st.session_state.perfil in ["Pastores", "Secretária"]:
            if st.button("🔍 CONSULTAR MEMBRO"):
                st.switch_page("pages/3_🔍_Consulta.py")
        else:
            st.button("🔒 CONSULTA (RESTRITO)", disabled=True)

    # Espaçamento entre as linhas
    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

    # Segunda Linha de Botões
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        if st.session_state.perfil in ["Pastores", "Secretária"]:
            if st.button("📊 DASHBOARD"):
                st.switch_page("pages/2_📊_Dashboard.py")
        else:
            st.button("🔒 DASHBOARD (RESTRITO)", disabled=True)

    with row2_col2:
        if st.button("🚪 ENCERRAR SESSÃO"):
            st.session_state.logado = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("ISOSED Cosmópolis - Gestão Inteligente")

    st.caption("ISOSED Cosmópolis - Gestão Inteligente")
