import streamlit as st

# 1. Configuração e Estética (Sempre o primeiro comando)
st.set_page_config(
    page_title="ISOSED Cosmópolis - Portal",
    page_icon="⛪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. INICIALIZAÇÃO SEGURA DO ESTADO (Evita o AttributeError)
if "logado" not in st.session_state:
    st.session_state.logado = False
if "perfil" not in st.session_state:
    st.session_state.perfil = None

# CSS para o padrão "Central de Comando"
st.markdown("""
<style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        height: 120px;
        border-radius: 12px;
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #2e7bcf;
        white-space: pre-wrap;
        font-size: 16px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2e7bcf;
        border-color: white;
    }
    .login-header {
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, #0a0a0a 0%, #003366 100%);
        border-radius: 15px;
        margin-bottom: 25px;
        color: white;
        border: 1px solid #2e7bcf;
    }
</style>
""", unsafe_allow_html=True)

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

# --- LÓGICA DE TELAS ---

# Se NÃO estiver logado, mostra tela de login
if not st.session_state.logado:
    st.markdown("""
        <div class="login-header">
            <h1>INSTITUCIONAL ISOSED</h1>
            <p>Sistema de Gestão Eclesiástica | Cosmópolis/SP</p>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        left_co, cent_co, last_co = st.columns([0.5, 3, 0.5])
        with cent_co:
            with st.form("login_form"):
                u = st.text_input("Usuário")
                s = st.text_input("Senha", type="password")
                if st.form_submit_button("ACESSAR PORTAL"):
                    if validar_login(u, s):
                        st.rerun()
                    else:
                        st.error("Credenciais incorretas.")

# Se ESTIVER logado, mostra o Menu de Comandos
else:
    st.markdown(f"""
        <div class="login-header">
            <h1>CENTRAL DE COMANDO</h1>
            <p>Operador: {st.session_state.perfil} | ISOSED Cosmópolis</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("📝 NOVO CADASTRO\nRegistrar membros e visitantes na base de dados."):
            st.switch_page("pages/1_📝_Cadastro.py")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.session_state.perfil in ["Pastores", "Secretária"]:
            if st.button("📊 DASHBOARD\nAnálise de indicadores e crescimento da congregação."):
                st.switch_page("pages/2_📊_Dashboard.py")
        else:
            st.button("🔒 DASHBOARD RESTRITO\nAcesso exclusivo para liderança estratégica.", disabled=True)

    with c2:
        if st.session_state.perfil in ["Pastores", "Secretária"]:
            if st.button("🔍 CONSULTAR\nLocalizar dados e fichas assinadas (LGPD) rapidamente."):
                st.switch_page("pages/3_🔍_Consulta.py")
        else:
            st.button("🔒 CONSULTA RESTRITA\nAcesso permitido apenas para secretaria.", disabled=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚪 ENCERRAR SESSÃO\nSair do sistema e garantir a segurança dos dados."):
            st.session_state.logado = False
            st.session_state.perfil = None
            st.rerun()

    st.caption("ISOSED Cosmópolis - Gestão Inteligente v2.0")
