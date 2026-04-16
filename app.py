import streamlit as st

# Configuração da Página
st.set_page_config(page_title="ISOSED Cosmópolis - Gestão", page_icon="⛪", layout="wide")

# --- BANCO DE DADOS DE USUÁRIOS ---
# Usuários e Perfis conforme solicitado
USUARIOS = {
    "pastor": {"senha": "123", "perfil": "Pastores"},
    "secretaria": {"senha": "456", "perfil": "Secretária"},
    "comunicacao": {"senha": "789", "perfil": "Comunicação"}
}

# Inicialização do estado de login
if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.perfil = None

# Função de Login
def realizar_login():
    with st.container():
        st.markdown("### 🔒 Acesso ao Sistema")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            if usuario in USUARIOS and USUARIOS[usuario]["senha"] == senha:
                st.session_state.logado = True
                st.session_state.perfil = USUARIOS[usuario]["perfil"]
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

# Lógica de Exibição
if not st.session_state.logado:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("⛪ Gestão de Membros - ISOSED")
        st.write("Bem-vindo ao sistema administrativo da ISOSED Cosmópolis.")
        st.info("Utilize suas credenciais para acessar as ferramentas de gestão.")
    with col2:
        realizar_login()
else:
    st.sidebar.success(f"Perfil: {st.session_state.perfil}")
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.session_state.perfil = None
        st.rerun()

    st.title(f"Painel Central - {st.session_state.perfil}")
    st.write("---")
    st.markdown(f"Olá! Você está logado como **{st.session_state.perfil}**.")
    st.info("👈 Use o menu lateral para navegar pelas funções de Cadastro ou Dashboard.")
