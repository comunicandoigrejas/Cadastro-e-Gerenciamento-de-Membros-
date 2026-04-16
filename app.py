import streamlit as st

# 1. Configuração inicial da página (Deve ser a primeira linha de código)
st.set_page_config(
    page_title="ISOSED Cosmópolis - Gestão",
    page_icon="⛪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Banco de Dados de Usuários e Perfis
# Recomenda-se futuramente mover as senhas para o menu 'Secrets' do Streamlit
USUARIOS = {
    "pastor": {"senha": "123", "perfil": "Pastores"},
    "secretaria": {"senha": "456", "perfil": "Secretária"},
    "comunicacao": {"senha": "789", "perfil": "Comunicação"}
}

# 3. Inicialização do Estado de Login
if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.perfil = None
    st.session_state.usuario_nome = None

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
    st.session_state.usuario_nome = None
    st.rerun()

# 5. Interface de Usuário
if not st.session_state.logado:
    # --- TELA DE LOGIN ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("⛪ Gestão de Membros - ISOSED")
        st.subheader("Portal Administrativo")
        st.markdown("""
        Bem-vindo ao sistema de gestão da **ISOSED Cosmópolis**. 
        Este ambiente é seguro e monitorado em conformidade com a **LGPD** e a **Lei nº 15.211/2025**.
        
        Utilize as suas credenciais para aceder às ferramentas de acordo com o seu perfil.
        """)
        st.image("https://img.icons8.com/fluency/200/church.png") # Ícone ilustrativo

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
    # Barra Lateral
    st.sidebar.title("Menu Principal")
    st.sidebar.success(f"Perfil: {st.session_state.perfil}")
    st.sidebar.markdown(f"**Utilizador:** {st.session_state.usuario_nome}")
    
    if st.sidebar.button("Sair / Logoff"):
        realizar_logout()

    # Painel Principal
    st.title(f"Bem-vindo, {st.session_state.perfil}")
    st.write("---")
    
    # Mensagens de orientação baseadas no perfil
    if st.session_state.perfil == "Pastores":
        st.markdown("### 📊 Visão Estratégica")
        st.write("Tem acesso completo aos indicadores de crescimento e gestão de membros.")
    
    elif st.session_state.perfil == "Secretária":
        st.markdown("### 📝 Gestão de Registos")
        st.write("Foque na manutenção e atualização da base de dados da congregação.")
        
    elif st.session_state.perfil == "Comunicação":
        st.markdown("### 📢 Portal de Cadastro")
        st.warning("O seu perfil permite apenas o **Cadastro de Novos Membros**.")

    st.info("👈 Selecione a opção **'Cadastro'** ou **'Dashboard'** no menu lateral para continuar.")

    # Rodapé de Conformidade Legal
    st.divider()
    st.markdown("""
    <div style='text-align: center; font-size: 0.8em; color: gray;'>
        <b>ISOSED Cosmópolis</b><br>
        Sistema em conformidade com a Lei nº 13.709/2018 (LGPD) e Lei nº 15.211/2025.
    </div>
    """, unsafe_allow_html=True)
