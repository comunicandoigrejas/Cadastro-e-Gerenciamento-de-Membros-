import streamlit as st
import pandas as pd

# 1. Configuração de Estética e Segurança
st.set_page_config(page_title="Consulta - ISOSED", page_icon="🔍", layout="wide")

# CSS para manter o padrão visual de Central de Comando e esconder a barra lateral
st.markdown("""
<style>
/* Esconde a barra de ferramentas superior (Share, Edit, GitHub, etc) */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
    .main { background-color: #0e1117; }
    
    /* Estilização dos Botões de Ministério */
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
    
    /* Link estilizado como botão para a ficha PDF */
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

# 2. Segurança de Acesso
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login.")
    st.stop()

if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.warning("🚫 Acesso restrito apenas à liderança e secretaria.")
    st.stop()

# Cabeçalho Padronizado
st.markdown('<div class="header-box"><h2>🔍 CONSULTA E MINISTÉRIOS</h2><p>Pesquisa detalhada e prova de consentimento LGPD</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

# --- CONFIGURAÇÃO DA PLANILHA ---
# Certifique-se de que a coluna do link da ficha na planilha se chama 'link_ficha'
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
    
    # 3. BOTÕES DE FILTRO POR MINISTÉRIO (QUANTIDADES)
    st.subheader("📊 Filtro por Departamento")
    lista_ministerios = ["Louvor", "Mídia", "Recepção", "Infantil", "Intercessão", "Ação Social"]
    
    if "filtro_min" not in st.session_state:
        st.session_state.filtro_min = None

    cols = st.columns(len(lista_ministerios))
    
    for i, min_nome in enumerate(lista_ministerios):
        # Conta membros ativos no ministério
        qtd = df['ministerio'].str.contains(min_nome, na=False).sum()
        if cols[i].button(f"{min_nome}\n({qtd})"):
            st.session_state.filtro_min = min_nome

    # Opção para limpar filtro selecionado
    if st.session_state.filtro_min:
        if st.button(f"❌ Limpar Filtro: {st.session_state.filtro_min}"):
            st.session_state.filtro_min = None
            st.rerun()

    st.divider()

    # 4. LÓGICA DE BUSCA E EXIBIÇÃO
    busca = st.text_input("Pesquisar por nome específico:", placeholder="Ex: João Silva")
    
    # Filtragem dos dados
    df_exibir = df.copy()
    if st.session_state.filtro_min:
        df_exibir = df_exibir[df_exibir['ministerio'].str.contains(st.session_state.filtro_min, na=False)]
    if busca:
        df_exibir = df_exibir[df_exibir['nome'].str.contains(busca, case=False, na=False)]

    # Exibição dos Resultados em Cards Individuais
    if not df_exibir.empty:
        st.success(f"Exibindo {len(df_exibir)} registro(s):")
        
        for i, row in df_exibir.iterrows():
            with st.expander(f"👤 {row['nome']} - {row['cargo']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**📞 WhatsApp:** {row['whatsapp']}")
                    st.write(f"**🎂 Nascimento:** {row['data_nascimento']}")
                with c2:
                    st.write(f"**🏛️ Ministérios:** {row['ministerio']}")
                    st.write(f"**🕒 Cadastrado em:** {row['data_cadastro']}")
                
                st.divider()
                
                # BUSCA DA FICHA DIGITALIZADA (GOOGLE DRIVE)
                # Verifica se existe o link na coluna 'link_ficha' da planilha
                if "link_ficha" in row and pd.notnull(row['link_ficha']):
                    st.markdown(f'<a href="{row["link_ficha"]}" target="_blank" class="pdf-button">📄 ABRIR FICHA ASSINADA (PDF)</a>', unsafe_allow_html=True)
                else:
                    st.info("ℹ️ Ficha digitalizada não vinculada a este registro.")
    else:
        st.warning("Nenhum membro encontrado com os critérios atuais.")
else:
    st.error("⚠️ Erro: Não foi possível carregar a base de dados. Verifique o link da planilha.")

st.markdown("---")
st.caption("ISOSED Cosmópolis - Sistema em conformidade com a Lei 13.709/2018 (LGPD)")
st.caption("Desenvolvido por Comunicando igrejas")
