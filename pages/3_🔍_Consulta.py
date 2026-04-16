import streamlit as st
import pandas as pd

# 1. Configurações e CSS para esconder a barra lateral
st.set_page_config(page_title="Consulta - ISOSED", page_icon="🔍", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. Segurança e Navegação
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado.")
    st.stop()

if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.warning("🚫 Acesso restrito apenas à liderança.")
    st.stop()

if st.button("⬅️ Voltar ao Menu Principal"):
    st.switch_page("app.py")

st.title("🔍 Consulta de Membros")
st.divider()

# 3. Carregamento de Dados
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"
CSV_URL = URL_PLANILHA.split("/edit")[0] + "/export?format=csv"

@st.cache_data(ttl=60)
def carregar_dados():
    try:
        return pd.read_csv(CSV_URL)
    except:
        return None

df = carregar_dados()

if df is not None and not df.empty:
    # Barra de pesquisa
    nome_busca = st.text_input("Digite o nome do membro para pesquisar:", placeholder="Ex: João Silva")
    
    if nome_busca:
        # Filtra o DataFrame pelo nome (ignora maiúsculas/minúsculas)
        resultado = df[df['nome'].str.contains(nome_busca, case=False, na=False)]
        
        if not resultado.empty:
            st.success(f"Encontrado(s) {len(resultado)} registro(s):")
            st.dataframe(resultado, use_container_width=True)
        else:
            st.warning("Nenhum membro encontrado com este nome.")
    else:
        st.info("Digite um nome acima para ver os detalhes.")
else:
    st.error("Não foi possível carregar a base de dados.")
