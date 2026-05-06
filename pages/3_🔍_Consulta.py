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
        white-space: pre-wrap;
        height: auto;
        padding: 10px 5px;
    }
    .stButton>button:hover {
        background-color: #2e7bcf;
        border-color: white;
        transform: scale(1.02);
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
    
    .pdf-button {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #d32f2f;
        color: white !important;
        padding: 10px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login.")
    st.stop()

if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.warning("🚫 Acesso restrito apenas à liderança e secretaria.")
    st.stop()

st.markdown('<div class="header-box"><h2>🔍 CONSULTA DE MEMBROS</h2><p>Pesquisa detalhada e prova de consentimento LGPD</p></div>', unsafe_allow_html=True)

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
    # Remove espaços ocultos dos nomes das colunas da planilha para evitar erros
    df.columns = df.columns.str.strip()
    
    # 3. LÓGICA DE BUSCA
    busca = st.text_input("Pesquisar por nome específico:", placeholder="Ex: João Silva")
    df_exibir = df.copy()
    
    # Filtro por nome usando o novo cabeçalho exato: "Nome"
    if busca and "Nome" in df_exibir.columns:
        df_exibir = df_exibir[df_exibir['Nome'].astype(str).str.contains(busca, case=False, na=False)]

    if not df_exibir.empty:
        st.success(f"Exibindo {len(df_exibir)} registro(s):")
        
        for i, row in df_exibir.iterrows():
            # Acessando com segurança usando os NOVOS nomes exatos das colunas da planilha
            nome_exibir = row.get("Nome", "Sem Nome")
            cargo_exibir = row.get("Cargo", "N/A")
            contato_exibir = row.get("Contato", "N/A")
            nasc_exibir = row.get("Data Nascimento", "N/A")
            cadastro_exibir = row.get("Data Cadastro", "N/A")
            bairro_exibir = row.get("Bairro", "N/A")
            profissao_exibir = row.get("Profissão", "N/A")
            
            with st.expander(f"👤 {nome_exibir} - {cargo_exibir}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**📞 Contato:** {contato_exibir}")
                    st.write(f"**🎂 Nascimento:** {nasc_exibir}")
                    st.write(f"**🏠 Bairro:** {bairro_exibir}")
                with c2:
                    st.write(f"**💼 Profissão:** {profissao_exibir}")
                    st.write(f"**🕒 Cadastrado em:** {cadastro_exibir}")
                
                st.divider()
                
                # BUSCA DA FICHA DIGITALIZADA
                if "Link Ficha" in df_exibir.columns and pd.notnull(row.get('Link Ficha')):
                    st.markdown(f'<a href="{row["Link Ficha"]}" target="_blank" class="pdf-button">📄 ABRIR FICHA ASSINADA (PDF)</a>', unsafe_allow_html=True)
                else:
                    st.info("ℹ️ Crie uma coluna 'Link Ficha' na planilha e cole o link do PDF para ver o botão aqui.")
    else:
        st.warning("Nenhum membro encontrado.")
else:
    st.error("⚠️ Erro: Não foi possível carregar a base de dados. Verifique a URL.")

st.markdown("---")
st.caption("ISOSED Cosmópolis - Sistema em conformidade com a Lei 13.709/2018 (LGPD)")
st.caption("Desenvolvido por Comunicando Igrejas")
