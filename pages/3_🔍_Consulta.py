import streamlit as st
import pandas as pd

# 1. Configuração de Estética e Segurança
st.set_page_config(page_title="Consulta - ISOSED", page_icon="🔍", layout="wide")

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
    /* Estilização para os cards de contagem */
    .metric-card {
        background-color: #1a1a1a;
        border: 1px solid #2e7bcf;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
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
st.markdown('<div class="header-box"><h2>🔍 CONSULTA E MINISTÉRIOS</h2><p>Pesquisa de membros e resumo por departamento</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

# --- CONFIGURAÇÃO DA PLANILHA ---
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"

def obter_link_csv(url):
    if "/edit" in url:
        return url.split("/edit")[0] + "/export?format=csv"
    return url

@st.cache_data(ttl=60)
def carregar_dados(link):
    try:
        return pd.read_csv(link)
    except:
        return None

csv_url = obter_link_csv(URL_PLANILHA)
df = carregar_dados(csv_url)

if df is not None and not df.empty:
    # --- FILTRO POR MINISTÉRIO (QUANTIDADES) ---
    st.subheader("📊 Quantidade por Ministério")
    
    # Lista de ministérios padrão (deve ser igual ao do cadastro)
    lista_ministerios = ["Louvor", "Mídia", "Recepção", "Infantil", "Intercessão", "Ação Social"]
    
    # Criar colunas para exibir as contagens
    cols = st.columns(len(lista_ministerios))
    
    for i, min_nome in enumerate(lista_ministerios):
        # Conta quantas vezes o ministério aparece na coluna 'ministerio'
        # Usamos str.contains porque um membro pode ter múltiplos ministérios
        quantidade = df['ministerio'].str.contains(min_nome, na=False).sum()
        with cols[i]:
            st.markdown(f"""
                <div class="metric-card">
                    <small>{min_nome}</small>
                    <h3 style='margin:0; color:#2e7bcf;'>{quantidade}</h3>
                </div>
            """, unsafe_allow_html=True)
    
    st.divider()

    # --- CAMPO DE PESQUISA ---
    busca = st.text_input("Filtrar membros por nome:", placeholder="Ex: João Silva")
    
    if busca:
        resultado = df[df['nome'].str.contains(busca, case=False, na=False)]
        
        if not resultado.empty:
            st.success(f"Encontrado(s) {len(resultado)} registro(s):")
            st.dataframe(resultado, use_container_width=True)
            
            for i, row in resultado.iterrows():
                with st.expander(f"Ficha: {row['nome']}"):
                    c1, c2 = st.columns(2)
                    c1.write(f"**WhatsApp:** {row['whatsapp']}")
                    c1.write(f"**Cargo:** {row['cargo']}")
                    c2.write(f"**Nascimento:** {row['data_nascimento']}")
                    c2.write(f"**Ministérios:** {row['ministerio']}")
        else:
            st.warning("Nenhum membro encontrado.")
    else:
        st.info("Utilize o campo acima para pesquisar nomes específicos.")
else:
    st.warning("⚠️ Planilha não encontrada ou vazia.")

st.caption("ISOSED Cosmópolis - Gestão Ministerial")
