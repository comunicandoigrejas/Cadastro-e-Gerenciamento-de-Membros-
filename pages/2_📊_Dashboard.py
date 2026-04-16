import streamlit as st
import pandas as pd

# 1. Configurações Iniciais e CSS para esconder a barra lateral
st.set_page_config(page_title="Dashboard - ISOSED", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Segurança e Navegação
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado.")
    st.stop()

if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.warning("🚫 Acesso restrito.")
    st.stop()

if st.button("⬅️ Voltar ao Menu Principal"):
    st.switch_page("app.py")

st.title("📊 Painel de Gestão Estratégica")
st.divider()

# 3. Carregamento de Dados
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"
if "/edit" in URL_PLANILHA:
    CSV_URL = URL_PLANILHA.split("/edit")[0] + "/export?format=csv"
else:
    CSV_URL = URL_PLANILHA

@st.cache_data(ttl=60)
def load_data():
    try:
        return pd.read_csv(CSV_URL)
    except:
        return None

df = load_data()

if df is not None and not df.empty:
    # Layout igual ao que definimos nas imagens
    m1, m2, m3 = st.columns(3)
    m1.metric("Total de Membros", len(df))
    if "cargo" in df.columns:
        m2.metric("Obreiros", len(df[df["cargo"] != "Membro"]))
    m3.metric("Cidade", "Cosmópolis - SP")
    
    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Por Cargo")
        st.bar_chart(df["cargo"].value_counts())
    with c2:
        st.subheader("Lista Completa")
        st.dataframe(df, use_container_width=True)
else:
    st.warning("Nenhum dado encontrado.")
