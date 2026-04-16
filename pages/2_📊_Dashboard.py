import streamlit as st
import pandas as pd
if st.button("⬅️ Voltar ao Menu Principal"):
    st.switch_page("app.py")
st.divider()
# 1. Configuração de Layout (Wide para caber os cartões de métricas)
st.set_page_config(page_title="Dashboard - ISOSED", page_icon="📊", layout="wide")

# Proteção de Acesso
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Por favor, faça login na página inicial.")
    st.stop()

# Restrição apenas para o Pastor e Secretaria
if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.warning("🚫 Acesso restrito. Este painel é exclusivo para a liderança.")
    st.stop()

st.title("📊 Gestão Estratégica - ISOSED Cosmópolis")

# --- CONFIGURAÇÃO DO LINK DA PLANILHA ---
# Substitua pelo seu link real da planilha Google
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"

if "/edit" in URL_PLANILHA:
    CSV_URL = URL_PLANILHA.split("/edit")[0] + "/export?format=csv"
else:
    CSV_URL = URL_PLANILHA

@st.cache_data(ttl=60)
def carregar_dados():
    try:
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None

df = carregar_dados()

if df is not None and not df.empty:
    # --- LAYOUT DE MÉTRICAS (CARTÕES SUPERIORES) ---
    st.markdown("### Indicadores Principais")
    m1, m2, m3, m4 = st.columns(4)
    
    total_membros = len(df)
    m1.metric("Total de Membros", total_membros)
    
    if "cargo" in df.columns:
        obreiros = len(df[df["cargo"] != "Membro"])
        m2.metric("Corpo de Obreiros", obreiros)
    
    if "status" in df.columns:
        visitantes = len(df[df["status"] == "Visitante"])
        m3.metric("Visitantes Ativos", visitantes)
        
    m4.metric("Unidade", "Cosmópolis - SP")

    st.divider()

    # --- LAYOUT DE GRÁFICOS (DUAS COLUNAS) ---
    col_esq, col_dir = st.columns(2)

    with col_esq:
        st.subheader("📊 Distribuição por Cargo")
        if "cargo" in df.columns:
            # Gráfico de barras horizontais para melhor leitura de cargos
            st.bar_chart(df["cargo"].value_counts())
        else:
            st.info("Coluna 'cargo' não encontrada na planilha.")

    with col_dir:
        st.subheader("📈 Crescimento Mensal")
        if "data_cadastro" in df.columns:
            try:
                df['data_cadastro'] = pd.to_datetime(df['data_cadastro'], dayfirst=True)
                df['mes_ano'] = df['data_cadastro'].dt.strftime('%m/%Y')
                st.line_chart(df['mes_ano'].value_counts().sort_index())
            except:
                st.info("Aguardando mais dados cronológicos para o gráfico.")

    st.divider()

    # --- TABELA DE DADOS (VISÃO GERAL) ---
    st.subheader("📋 Lista Geral Detalhada")
    # Filtro simples para pesquisa rápida
    busca = st.text_input("Filtrar por nome na tabela:")
    if busca:
        df_filtrado = df[df['nome'].str.contains(busca, case=False, na=False)]
        st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)

else:
    st.warning("⚠️ Planilha sem dados ou link incorreto.")
    st.info("Dica: Arraste a aba 'Membros' para ser a primeira da sua planilha Google.")

st.caption("ISOSED Cosmópolis - Sistema em conformidade com a LGPD e Lei 15.211/2025.")
