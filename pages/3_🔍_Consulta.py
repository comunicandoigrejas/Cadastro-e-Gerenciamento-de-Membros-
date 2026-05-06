import streamlit as st
import pandas as pd

# 1. Configuração de Estética e Segurança
st.set_page_config(page_title="Consulta - ISOSED", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; }
    .main { background-color: #0e1117; }
    
    /* Botões Padrão e de Cargo */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #2e7bcf;
        font-weight: bold;
        transition: 0.3s;
        height: auto;
        padding: 15px 5px;
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
        margin-top: 15px;
    }
    
    /* Títulos dentro do Expander */
    .section-title {
        color: #2e7bcf;
        font-size: 16px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 10px;
        border-bottom: 1px solid #1a1a1a;
        padding-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login.")
    st.stop()

if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.warning("🚫 Acesso restrito apenas à liderança e secretaria.")
    st.stop()

st.markdown('<div class="header-box"><h2>🔍 CONSULTA DE MEMBROS</h2><p>Ficha completa, prontuário digital e consentimento LGPD</p></div>', unsafe_allow_html=True)

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
        df = pd.read_csv(link)
        df.columns = df.columns.str.strip() # Limpa espaços nos cabeçalhos
        # Substitui valores "NaN" (vazios) por string vazia para não quebrar o visual
        df = df.fillna("") 
        return df
    except:
        return None

df = carregar_dados(obter_link_csv(URL_PLANILHA))

if df is not None and not df.empty:
    
    # 2. FILTRO POR ÍCONES DE CARGO (Igual ao Dashboard)
    st.subheader("👥 Filtrar por Cargo Ministerial")
    
    icones_cargos = {
        "Membro": "👤", "Cooperador(a)": "🤝", "Obreiro(a)": "🛠️",
        "Líder": "⭐", "Missionário(a)": "🌍", "Diácono/Isa": "🍷",
        "Presbítero": "📜", "Evangelista": "📢", "Pastor(a)": "🛡️",
        "Visitante": "👋"
    }

    if "filtro_cargo_consulta" not in st.session_state:
        st.session_state.filtro_cargo_consulta = "Todos"

    cols_cargos = st.columns(5)
    
    if st.button("📋 EXIBIR TODOS"):
        st.session_state.filtro_cargo_consulta = "Todos"

    cargos_lista = list(icones_cargos.keys())
    for i, cargo in enumerate(cargos_lista):
        col_idx = i % 5
        icone = icones_cargos[cargo]
        if cols_cargos[col_idx].button(f"{icone}\n{cargo}"):
            st.session_state.filtro_cargo_consulta = cargo

    st.divider()

    # 3. BUSCA POR NOME
    busca = st.text_input(f"Pesquisar nome (Filtro atual: {st.session_state.filtro_cargo_consulta}):", placeholder="Ex: João Silva")
    
    # Aplicando os Filtros
    df_f = df.copy()
    if st.session_state.filtro_cargo_consulta != "Todos":
        df_f = df_f[df_f['Cargo'].astype(str).str.contains(st.session_state.filtro_cargo_consulta, na=False)]
    
    if busca and "Nome" in df_f.columns:
        df_f = df_f[df_f['Nome'].astype(str).str.contains(busca, case=False, na=False)]

    # 4. EXIBIÇÃO DOS RESULTADOS COMPLETOS
    if not df_f.empty:
        st.success(f"Encontrado(s) {len(df_f)} registro(s):")
        
        for i, row in df_f.iterrows():
            nome = row.get("Nome", "Sem Nome")
            cargo = row.get("Cargo", "Membro")
            
            # Card Expansível
            with st.expander(f"👤 {nome} - {cargo}"):
                
                # --- DADOS PESSOAIS ---
                st.markdown('<div class="section-title">📋 Dados Pessoais</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                c1.write(f"**🚻 Sexo:** {row.get('Sexo', '')}")
                c1.write(f"**🎂 Nascimento:** {row.get('Data Nascimento', '')} ({row.get('Local Nascimento', '')})")
                c1.write(f"**🪪 CPF:** {row.get('CPF', '')}")
                
                c2.write(f"**💍 Estado Civil:** {row.get('Estado Civil', '')}")
                conjuge = row.get("Cônjuge", "")
                if conjuge:
                    c2.write(f"**👩‍❤️‍👨 Cônjuge:** {conjuge}")
                c2.write(f"**💼 Profissão:** {row.get('Profissão', '')}")

                # --- DADOS ECLESIÁSTICOS ---
                st.markdown('<div class="section-title">⛪ Informações Eclesiásticas & Contato</div>', unsafe_allow_html=True)
                c3, c4 = st.columns(2)
                c3.write(f"**🕊️ Batismo:** {row.get('Data Batismo', '')}")
                c3.write(f"**🛡️ Cargo(s):** {cargo}")
                
                c4.write(f"**📞 WhatsApp:** {row.get('Contato', '')}")
                dizimista = row.get("Dizimista", "")
                icone_dizimo = "💎 Sim" if dizimista == "Sim" else "⚪ Não"
                c4.write(f"**💰 Dizimista:** {icone_dizimo}")

                # --- ENDEREÇO ---
                st.markdown('<div class="section-title">📍 Endereço</div>', unsafe_allow_html=True)
                rua = row.get("Rua", "")
                num = row.get("Nº", "")
                bairro = row.get("Bairro", "")
                cep = row.get("CEP", "")
                st.write(f"🏠 {rua}, {num} - {bairro} | **CEP:** {cep}")

                # --- SISTEMA E LGPD ---
                st.markdown('<div class="section-title">🔒 Segurança do Sistema</div>', unsafe_allow_html=True)
                st.caption(f"🕒 Cadastrado em: {row.get('Data Cadastro', '')} | ✍️ Por: {row.get('Cadastrado Por', '')}")
                st.caption(f"⚖️ Consentimento LGPD: {row.get('Consentimento LGPD', '')}")
                
                # BUSCA DA FICHA DIGITALIZADA (Botão PDF)
                if "Link Ficha" in df_f.columns and str(row.get('Link Ficha')).startswith("http"):
                    st.markdown(f'<a href="{row["Link Ficha"]}" target="_blank" class="pdf-button">📄 ABRIR FICHA ASSINADA (PDF)</a>', unsafe_allow_html=True)

    else:
        st.warning("Nenhum membro encontrado com os filtros atuais.")
else:
    st.error("⚠️ Erro: Não foi possível carregar a base de dados. Verifique a URL da planilha.")

st.markdown("---")
st.caption("ISOSED Cosmópolis - Sistema em conformidade com a Lei 13.709/2018 (LGPD)")
st.caption("Desenvolvido por Comunicando Igrejas")
