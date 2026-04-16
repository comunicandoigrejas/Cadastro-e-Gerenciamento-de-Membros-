import streamlit as st

# 1. Configuração inicial da página
st.set_page_config(
    page_title="ISOSED Cosmópolis - Gestão",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Banco de Dados de Usuários
USUARIOS = {
    "pastor": {"senha": "123", "perfil": "Pastores"},
    "secretaria": {"senha": "456", "perfil": "Secretária"},
    "comunicacao": {"senha": "789", "perfil": "Comunicação"}
}

# 3. Inicialização do Estado de Login (CORREÇÃO AQUI)
if "logado" not in st.session_state:
    st.session_state.logado = False
if "perfil" not in st.session_state:
    st.session_state.perfil = None
if "usuario_nome" not in st.session_state:
    st.session_state.usuario_nome = ""

# 4. Funções de Autenticação
def realizar_login(usuario, senha):
    if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
        st.session_state.logado = True
        st.session_state.perfil = USUARIOS[usuario]["perfil"]
        st.session_state.usuario_nome = usuario
        return True
    return False

def realizar_logout():
    st.session_state.logado = False
    st.session_state.perfil = None
    st.session_state.usuario_nome = ""
    st.rerun()

# 5. Interface de Usuário
if not st.session_state.logado:
    # --- TELA DE LOGIN ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("⛪ Gestão de Membros - ISOSED")
        st.subheader("Portal Administrativo")
        st.markdown("Bem-vindo ao sistema da ISOSED Cosmópolis.")

    with col2:
        with st.container(border=True):
            st.markdown("### 🔒 Acesso")
            usuario_input = st.text_input("Utilizador")
            senha_input = st.text_input("Palavra-passe", type="password")
            
            if st.button("Entrar", use_container_width=True):
                if realizar_login(usuario_input, senha_input):
                    st.success("Acesso autorizado!")
                    st.rerun()
                else:
                    st.error("Utilizador ou senha incorretos.")

else:
    # --- INTERFACE APÓS LOGIN ---
    st.sidebar.title("Menu Principal")
    st.sidebar.success(f"Perfil: {st.session_state.perfil}")
    
    # Verificação extra para evitar o AttributeError
    nome_exibicao = st.session_state.get("usuario_nome", "Usuário")
    st.sidebar.markdown(f"**Utilizador:** {nome_exibicao}")
    
    if st.sidebar.button("Sair / Logoff"):
        realizar_logout()

    st.title(f"Bem-vindo, {st.session_state.perfil}")
    st.write("---")
    st.info("👈 Selecione a opção no menu lateral para continuar.")
