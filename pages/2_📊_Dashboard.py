import streamlit as st
import pandas as pd

# 1. Configuração de Estética e Segurança
st.set_page_config(page_title="Dashboard - ISOSED", page_icon="📊", layout="wide")

# CSS para manter o padrão visual de Central de Comando
st.markdown("""
<style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #2e7bcf;
        font-weight: bold;
    }
    .header-box {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #0a0a0a 0%, #003366 100%);
        border-radius: 12px;
        margin-bottom: 20px;
        color: white;
        border: 1px solid #2e7bcf;
    }
</style>
""", unsafe_allow_html=True)

if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login.")
    st.stop()

if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.warning("🚫 Acesso restrito apenas à liderança e secretaria.")
    st.stop()

# Cabeçalho Centralizado com Degradê
st.markdown('<div class="header-box"><h2>📊 DASHBOARD ESTRATÉGICO</h2><p>Indicadores de Crescimento e Gestão ISOSED</p></div>', unsafe_allow_html=True)

# Botão de Voltar no padrão preto/azul
if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

# --- CONFIGURAÇÃO DOS DADOS ---
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"

if "/edit" in URL_PLANILHA:
    CSV_URL = URL_PLANILHA.split("/edit")[0] + "/export?format=csv"
else:
    CSV_URL = URL_PLANILHA

@st.cache_data(ttl=60)
def carregar_dados():
    try:
        return pd.read_csv(CSV_URL)
    except:
        return None

df = carregar_dados()

# 2. Visualização dos Indicadores
if df is not None and not df.empty:
    # Cartões de Métricas no topo
    st.subheader("📌 Indicadores Rápidos")
    m1, m2, m3, m4 = st.columns(4)
    
    m1.metric("Total de Membros", len(df))
    
    if "cargo" in df.columns:
        obreiros = len(df[df["cargo"] != "Membro"])
        m2.metric("Corpo de Obreiros", obreiros)
    
    if "status" in df.columns:
        visitantes = len(df[df["status"] == "Visitante"])
        m3.metric("Visitantes Ativos", visitantes)
        
    m4.metric("Unidade", "Cosmópolis - SP")

    st.divider()

    # Gráficos de Análise
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("👥 Composição Ministerial")
        if "cargo" in df.columns:
            st.bar_chart(df["cargo"].value_counts())

    with c2:
        st.subheader("📈 Status dos Registros")
        if "status" in df.columns:
            st.area_chart(df["status"].value_counts())

else:
    st.warning("⚠️ Não foi possível carregar os dados ou a planilha está vazia.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("ISOSED Cosmópolis - Dashboard Analítico")
st.caption("Desenvolvido por Comunicando Igrejas")
