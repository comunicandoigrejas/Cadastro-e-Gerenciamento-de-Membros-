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
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2e7bcf;
        border-color: white;
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
    st.error("⚠️ Acesso negado.")
    st.stop()

if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.warning("🚫 Acesso restrito à liderança.")
    st.stop()

# Cabeçalho Padronizado
st.markdown('<div class="header-box"><h2>🔍 CONSULTA E MINISTÉRIOS</h2><p>Clique em um ministério para filtrar ou use a busca por nome</p></div>', unsafe_allow_html=True)

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
    
    # 2. BOTÕES DE FILTRO POR MINISTÉRIO
    st.subheader("📊 Filtrar por Departamento")
    lista_ministerios = ["Louvor", "Mídia", "Recepção", "Infantil", "Intercessão", "Ação Social"]
    
    # Inicializa o filtro no estado da sessão se não existir
    if "filtro_min" not in st.session_state:
        st.session_state.filtro_min = None

    cols = st.columns(len(lista_ministerios))
    
    for i, min_nome in enumerate(lista_ministerios):
        qtd = df['ministerio'].str.contains(min_nome, na=False).sum()
        # O botão exibe o nome e a quantidade
        if cols[i].button(f"{min_nome}\n({qtd})"):
            st.session_state.filtro_min = min_nome

    if st.session_state.filtro_min:
        if st.button(f"❌ Limpar Filtro: {st.session_state.filtro_min}"):
            st.session_state.filtro_min = None
            st.rerun()

    st.divider()

    # 3. LÓGICA DE EXIBIÇÃO E BUSCA
    busca = st.text_input("Ou pesquise um nome específico:", placeholder="Ex: João Silva")
    
    # Aplicando os filtros
    df_exibir = df.copy()
    
    if st.session_state.filtro_min:
        df_exibir = df_exibir[df_exibir['ministerio'].str.contains(st.session_state.filtro_min, na=False)]
    
    if busca:
        df_exibir = df_exibir[df_exibir['nome'].str.contains(busca, case=False, na=False)]

    # Exibição dos Resultados
    if not df_exibir.empty:
        st.success(f"Exibindo {len(df_exibir)} registro(s):")
        st.dataframe(df_exibir, use_container_width=True)
        
        for i, row in df_exibir.iterrows():
            with st.expander(f"Ver ficha: {row['nome']}"):
                c1, c2 = st.columns(2)
                c1.write(f"**WhatsApp:** {row['whatsapp']}")
                c1.write(f"**Cargo:** {row['cargo']}")
                c2.write(f"**Nascimento:** {row['data_nascimento']}")
                c2.write(f"**Ministérios:** {row['ministerio']}")
    else:
        st.warning("Nenhum membro encontrado para os critérios selecionados.")

else:
    st.error("⚠️ Planilha não encontrada ou vazia.")

st.caption("ISOSED Cosmópolis - Gestão Ministerial")
