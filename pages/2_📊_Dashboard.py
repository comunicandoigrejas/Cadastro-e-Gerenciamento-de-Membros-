import streamlit as st
import pandas as pd

# 1. Configuração da Página e Segurança
st.set_page_config(page_title="Dashboard - ISOSED", page_icon="📊", layout="wide")

if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Por favor, faça login na página inicial.")
    st.stop()

# Restrição: Apenas Pastores e Secretária podem ver os dados
if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.warning("🚫 Acesso restrito. Este painel é exclusivo para a liderança.")
    st.stop()

st.title("📊 Painel de Crescimento - ISOSED")

# --- CONFIGURAÇÃO DOS DADOS ---
# Substitua o link abaixo pelo link de compartilhamento da sua planilha
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"

# Esta lógica transforma o link do navegador num link de dados CSV para o Python
if "/edit" in URL_PLANILHA:
    CSV_URL = URL_PLANILHA.split("/edit")[0] + "/export?format=csv"
else:
    CSV_URL = URL_PLANILHA

@st.cache_data(ttl=60) # Atualiza os dados a cada 60 segundos
def carregar_dados():
    try:
        # Lê os dados diretamente da nuvem Google
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha: {e}")
        return None

df = carregar_dados()

# 2. Visualização dos Dados
if df is not None and not df.empty:
    # Métricas de Destaque
    total_membros = len(df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Registos", total_membros)
    
    if "cargo" in df.columns:
        lideranca = len(df[df["cargo"] != "Membro"])
        col2.metric("Obreiros/Liderança", lideranca)
    
    col3.metric("Localidade", "Cosmópolis - SP")

    st.divider()

    # Gráficos
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Distribuição por Cargo")
        if "cargo" in df.columns:
            st.bar_chart(df["cargo"].value_counts())
        else:
            st.info("Coluna 'cargo' não encontrada.")

    with c2:
        st.subheader("Estatística de Status")
        if "status" in df.columns:
            st.area_chart(df["status"].value_counts())

    # Tabela Completa
    st.subheader("Lista Geral de Membros")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("A planilha parece estar vazia ou o link está incorreto.")
    st.info("Verifique se a aba 'Membros' é a primeira da sua planilha Google.")

st.markdown("---")
st.caption("Sistema de Gestão Interna - ISOSED Cosmópolis")
