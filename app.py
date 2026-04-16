import streamlit as st

# 1. Configuração de Estética e Layout
st.set_page_config(
    page_title="ISOSED Cosmópolis - Portal de Gestão",
    page_icon="⛪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS para o visual profissional Dark/Blue
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #2e7bcf;
        color: white;
        font-weight: bold;
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
    h1 {
        font-family: 'Trebuchet MS', sans-serif;
        letter-spacing: 2px;
    }
    </style>
    """, unsafe_allow_html=True) # CORRIGIDO: O nome correto é unsafe_allow_html

# 2. Inicialização do Estado de Sessão
if "logado" not in st.session_state:
    st.session_state.logado = False
if "perfil" not in st.session_state:
    st.session_state.perfil = None

# Base de Dados de Usuários
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

# --- TELA DE LOGIN ESTILIZADA ---
if not st.session_state.logado:
    st.markdown("""
        <div class="login-header">
            <h1>INSTITUCIONAL ISOSED</h1>
            <p style="opacity: 0.8;">Sistema de Gestão Eclesiástica | Cosmópolis/SP</p>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        # Centralizando o formulário
        left_co, cent_co, last_co = st.columns([0.5, 3, 0.5])
        with cent_co:
            with st.form("login_form"):
                usuario = st.text_input("Usuário", placeholder="Identificação")
                senha = st.text_input("Senha", type="password", placeholder="••••••••")
                botao = st.form_submit_button("ACESSAR PORTAL")
                
                if botao:
                    if validar_login(usuario, senha):
                        st.rerun()
                    else:
                        st.error("Credenciais incorretas.")

# --- APÓS O LOGIN ---
else:
    st.sidebar.title(f"⛪ ISOSED")
    st.sidebar.info(f"Conectado: {st.session_state.perfil}")
    
    if st.sidebar.button("Encerrar Sessão"):
        st.session_state.logado = False
        st.rerun()

    st.title(f"Bem-vindo, {st.session_state.perfil}")
    
    # Cartões de Atalho
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.write("### 📝 Cadastros")
            st.write("Aceda ao formulário de membros.")
            
    with c2:
        if st.session_state.perfil in ["Pastores", "Secretária"]:
            with st.container(border=True):
                st.write("### 📊 Dashboard")
                st.write("Visualize métricas e gráficos.")

    st.info("Utilize o menu lateral à esquerda para navegar.")
