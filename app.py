import streamlit as st

# 1. Configuração e CSS Avançado
st.set_page_config(page_title="ISOSED - Portal", page_icon="⛪", layout="centered")

st.markdown("""
    <style>
    /* Esconde barra lateral */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
    
    /* Estilização dos Botões como 'Cards' da Imagem */
    .stButton>button {
        width: 100%;
        height: 120px; /* Mais alto para caber a descrição */
        border-radius: 12px;
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #2e7bcf;
        white-space: pre-wrap; /* Permite quebras de linha */
        font-size: 18px;
        font-weight: bold;
        transition: 0.3s;
        line-height: 1.4;
    }
    
    .stButton>button:hover {
        background-color: #2e7bcf;
        border-color: #ffffff;
        transform: translateY(-2px);
    }

    /* Estilização da Descrição (simulada via texto) */
    .btn-desc {
        display: block;
        font-size: 12px;
        font-weight: normal;
        opacity: 0.8;
        margin-top: 5px;
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

# ... (Mantenha aqui a sua lógica de login e inicialização de sessão) ...

if st.session_state.logado:
    st.markdown(f"""
        <div class="login-header">
            <h1>CENTRAL DE COMANDO</h1>
            <p>Operador: {st.session_state.perfil} | ISOSED Cosmópolis</p>
        </div>
    """, unsafe_allow_html=True)

    # Grid 2x2 com Descrições conforme a imagem
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        # Título \n Descrição (O \n faz a quebra de linha)
        if st.button("📝 NOVO CADASTRO\nRegistrar membros e visitantes na base de dados."):
            st.switch_page("pages/1_📝_Cadastro.py")

    with row1_col2:
        if st.session_state.perfil in ["Pastores", "Secretária"]:
            if st.button("🔍 CONSULTAR\nLocalizar dados de membros cadastrados rapidamente."):
                st.switch_page("pages/3_🔍_Consulta.py")
        else:
            st.button("🔒 CONSULTA RESTRITA\nAcesso permitido apenas para liderança e secretaria.", disabled=True)

    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        if st.session_state.perfil in ["Pastores", "Secretária"]:
            if st.button("📊 DASHBOARD\nAnálise de indicadores e crescimento da congregação."):
                st.switch_page("pages/2_📊_Dashboard.py")
        else:
            st.button("🔒 DASHBOARD RESTRITO\nAcesso exclusivo para acompanhamento estratégico.", disabled=True)

    with row2_col2:
        if st.button("🚪 ENCERRAR SESSÃO\nSair do sistema e garantir a segurança dos dados."):
            st.session_state.logado = False
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("ISOSED Cosmópolis - Gestão Inteligente v2.0")
