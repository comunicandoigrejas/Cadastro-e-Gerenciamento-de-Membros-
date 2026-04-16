import streamlit as st
import pandas as pd

# 1. Configuração de Estética e Segurança
st.set_page_config(page_title="Consulta - ISOSED", page_icon="🔍", layout="wide")

# CSS simplificado para evitar conflitos de sintaxe
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

# 2. Segurança de Acesso
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login.")
    st.stop()

if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.warning("🚫 Acesso restrito apenas à liderança e secretaria.")
    st.stop()

# Cabeçalho Padronizado
st.markdown('<div class="header-box"><h2>🔍 CONSULTA DE MEMBROS</h2><p>Localização rápida de registos institucional</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

# --- CONFIGURAÇÃO DA PLANILHA ---
# COLOQUE O SEU LINK ABAIXO
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"

# Lógica de conversão segura
def obter_link_csv(url):
    if "/edit" in url:
        return url.split("/edit")[0] + "/export?format=csv"
    return url

@st.cache_data(ttl=60)
def carregar_dados(link):
    try:
        return pd.read_csv(link)
    except Exception as e:
        return None

# 3. Execução
csv_url = obter_link_csv(URL_PLANILHA)
df = carregar_dados(csv_url)

if df is not None and not df.empty:
    busca = st.text_input("Digite o nome para pesquisar:", placeholder="Ex: João Silva")
    
    if busca:
        # Filtro que ignora maiúsculas/minúsculas
        resultado = df[df['nome'].str.contains(busca, case=False, na=False)]
        
        if not resultado.empty:
            st.success(f"Encontrado(s) {len(resultado)} registro(s):")
            st.dataframe(resultado, use_container_width=True)
            
            # Detalhes em Expander
            for i, row in resultado.iterrows():
                with st.expander(f"Ver ficha de: {row['nome']}"):
                    c1, c2 = st.columns(2)
                    c1.write(f"**WhatsApp:** {row['whatsapp']}")
                    c1.write(f"**Cargo:** {row['cargo']}")
                    c2.write(f"**Nascimento:** {row['data_nascimento']}")
                    c2.write(f"**Ministérios:** {row['ministerio']}")
        else:
            st.warning("Nenhum membro encontrado.")
    else:
        st.info("Digite um nome acima para iniciar a busca.")
else:
    st.warning("⚠️ Planilha não encontrada ou vazia. Verifique o link informado no código.")

st.caption("ISOSED Cosmópolis - Consulta Segura")
st.caption("Desenvolvido por Comunicando Igrejas")
