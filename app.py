import streamlit as st

# 1. Configuração de Estética e Layout
st.set_page_config(
    page_title="ISOSED Cosmópolis - Portal de Gestão",
    page_icon="⛪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilização CSS para aproximar do layout da imagem (Dark Mode & Professional)
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
    }
    .login-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #1a1a1a, #2e7bcf);
        border-radius: 10px;
        margin-bottom: 25px;
        color: white;
    }
    </style>
    """, unsafe_allow_status_code=True)

# 2. Inicialização do Estado
if "logado" not in st.session_state:
    st.session_state.logado = False
if "perfil" not in st.session_state:
    st.session_state.perfil = None

# Base de Dados de Usuários (Mantenha as suas senhas reais aqui)
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
    # Cabeçalho baseado na imagem
    st.markdown("""
        <div class="login-header">
            <h1>INSTITUCIONAL ISOSED</h1>
            <p>Sistema Inteligente de Gestão Eclesiástica - Cosmópolis/SP</p>
        </div>
    """, unsafe_allow_status_code=True)

    with st.container():
        left_co, cent_co, last_co = st.columns([1,2,1])
        with cent_co:
            st.subheader("Autenticação Requerida")
            usuario = st.text_input("Identificação do Usuário", placeholder="Ex: pastor")
            senha = st.text_input("Chave de Acesso", type="password", placeholder="••••••••")
            
            if st.button("ACESSAR PORTAL"):
                if validar_login(usuario, senha):
                    st.rerun()
                else:
                    st.error("Credenciais não reconhecidas pelo sistema.")
            
            st.markdown("---")
            st.caption("Acesso monitorado. Em conformidade com a LGPD.")

# --- APÓS O LOGIN (MENU PRINCIPAL) ---
else:
    st.sidebar.title(f"⛪ ISOSED")
    st.sidebar.write(f"Conectado como: **{st.session_state.perfil}**")
    
    if st.sidebar.button("Encerrar Sessão"):
        st.session_state.logado = False
        st.rerun()

    # Página Inicial Pós-Login
    st.title(f"Bem-vindo ao Portal, {st.session_state.perfil}")
    
    # Cartões de Atalho Estilizados
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.write("### 📝 Cadastros")
            st.write("Registrar novos membros e visitantes.")
    with c2:
        if st.session_state.perfil in ["Pastores", "Secretária"]:
            with st.container(border=True):
                st.write("### 📊 Dashboard")
                st.write("Análise de crescimento e indicadores.")

    st.info("Utilize o menu lateral para navegar entre as funções.")
