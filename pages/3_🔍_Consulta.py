import streamlit as st
import pandas as pd

# 1. Configuração de Estética e Segurança
st.set_page_config(page_title="Consulta - ISOSED", page_icon="🔍", layout="wide")

# CSS para manter o padrão visual e esconder a barra lateral
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

# Cabeçalho Padronizado
st.markdown('<div class="header-box"><h2>🔍 CONSULTA DE MEMBROS</h2><p>Localização rápida e detalhada de registos institucional</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

# --- CONFIGURAÇÃO DA PLANILHA ---
# Coloque aqui o link da sua planilha Google (o mesmo que você abre no navegador)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"

# Converte o link para o formato de exportação CSV
if "/edit" in URL_PLANILHA:
    CSV_URL = URL_PLANILHA.split("/edit")[0] + "/export?format=csv"
else:
    CSV_URL = URL_PLANILHA

@st.cache_data(ttl=60)
def carregar_dados():
    try:
        # Lê os dados diretamente da nuvem
        df = pd.read_csv(CSV_URL)
        return df
    except Exception as e:
        st.error(f"Erro ao acessar a base de dados: {e}")
        return None

# 2. Execução da Consulta
df = carregar_dados()

if df is not None and not df.empty:
    # Campo de pesquisa estilizado
    nome_busca = st.text_input("Pesquisar por nome:", placeholder="Ex: João Silva")
    
    if nome_busca:
        # Filtra ignorando maiúsculas/minúsculas
        resultado = df[df['nome'].str.contains(nome_busca, case=False, na=False)]
        
        if not resultado.empty:
            st.success(f"Encontrado(s) {len(resultado)} registro(s):")
            # Exibe a tabela apenas com os resultados
            st.dataframe(resultado, use_container_width=True)
            
            # Opção de ver detalhes individuais em cards (opcional)
            for i, row in resultado.iterrows():
                with st.expander(f"Ficha Detalhada: {row['nome']}"):
                    c1, c2 = st.columns(2)
                    c1.write(f"**WhatsApp:** {row['whatsapp']}")
                    c1.write(f"**Cargo:** {row['cargo']}")
                    c2.write(f"**Nascimento:** {row['data_nascimento']}")
                    c2.write(f"**Ministérios:** {row['ministerio']}")
        else:
            st.warning("Nenhum membro encontrado com este nome.")
    else:
        st.info("Digite um nome acima para iniciar a busca.")
else:
    st.warning("⚠️ A base de dados está vazia ou o link da planilha está incorreto.")

st.caption("ISOSED Cosmópolis - Consulta Segura (LGPD)"
st.caption("Desenvolvido por Comunicando Igrejas")
