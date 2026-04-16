import streamlit as st
import pandas as pd

# 1. Verificação de Segurança
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Por favor, faça login na página inicial.")
    st.stop()

if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.warning("🚫 Acesso restrito à liderança.")
    st.stop()

st.set_page_config(page_title="Dashboard - ISOSED", page_icon="📊", layout="wide")

st.title("📊 Painel de Crescimento - ISOSED")
st.write("Dados atualizados em tempo real da congregação em Cosmópolis.")

# 2. Função para ler os dados da planilha
# Substitua pelo seu link da planilha (o link normal de visualização)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"
CSV_URL = URL_PLANILHA.replace("/edit#gid=", "/export?format=csv&gid=")

@st.cache_data(ttl=60) # Atualiza os dados a cada 1 minuto
def carregar_dados():
    try:
        # Lê a planilha convertendo para CSV automaticamente
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados da planilha: {e}")
        return None

df = carregar_dados()

if df is not None and not df.empty:
    # --- MÉTRICAS PRINCIPAIS ---
    total_membros = len(df)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Membros", total_membros)
    
    # Exemplo de contagem por cargo
    if "cargo" in df.columns:
        obreiros = len(df[df["cargo"] != "Membro"])
        col2.metric("Liderança/Obreiros", obreiros)
    
    col3.metric("Cidade", "Cosmópolis - SP")

    st.divider()

    # --- GRÁFICOS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Distribuição por Cargo")
        if "cargo" in df.columns:
            contagem_cargo = df["cargo"].value_counts()
            st.bar_chart(contagem_cargo)

    with c2:
        st.subheader("Novos Membros por Mês")
        if "data_cadastro" in df.columns:
            df["data_cadastro"] = pd.to_datetime(df["data_cadastro"], dayfirst=True, errors='coerce')
            df['mes'] = df['data_cadastro'].dt.strftime('%m/%Y')
            evolucao = df['mes'].value_counts().sort_index()
            st.line_chart(evolucao)

    # --- TABELA DETALHADA ---
    st.subheader("Lista Geral de Registros")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("Ainda não existem dados cadastrados ou a planilha está vazia.")
    st.info("Realize o primeiro cadastro no menu lateral para visualizar as estatísticas.")

st.caption("ISOSED Cosmópolis - Sistema em conformidade com a LGPD.")
