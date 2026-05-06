import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuração de Estética e Segurança
st.set_page_config(page_title="Dashboard - ISOSED", page_icon="📊", layout="wide")

# CSS para o padrão "Central de Comando" com ajustes de fonte e cor
st.markdown("""
<style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; }
    .main { background-color: #0e1117; }
    
    /* Botão de Voltar */
    .btn-voltar>button {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #2e7bcf;
        font-weight: bold;
        width: 100%;
    }

    /* Estilo dos Cards/Ícones de Cargo */
    .stButton>button {
        width: 100%;
        height: 100px;
        border-radius: 12px;
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #2e7bcf;
        font-size: 14px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2e7bcf;
        border-color: white;
        transform: translateY(-5px);
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
    
    .metric-box {
        background-color: #1a1a1a;
        border: 2px solid #2e7bcf;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Ajuste solicitado: Fonte branca e Maiúsculo */
    .metric-box small {
        color: white !important;
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Faça login no menu principal.")
    st.stop()

st.markdown('<div class="header-box"><h2>📊 DASHBOARD ESTRATÉGICO</h2><p>Consulte estatísticas por cargo e aniversariantes por mês</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL", key="voltar"):
    st.switch_page("app.py")

st.divider()

# --- CARREGAMENTO DE DADOS ---
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"

def obter_link_csv(url):
    if "/edit" in url: return url.split("/edit")[0] + "/export?format=csv"
    return url

@st.cache_data(ttl=60)
def carregar_dados(link):
    try:
        df = pd.read_csv(link)
        df.columns = df.columns.str.strip()
        return df
    except: return None

df = carregar_dados(obter_link_csv(URL_PLANILHA))

if df is not None and not df.empty:
    
    # 2. SELEÇÃO POR ÍCONES (CARGOS)
    st.subheader("👥 Filtrar por Cargo Ministerial")
    
    icones_cargos = {
        "Membro": "👤",
        "Cooperador(a)": "🤝",
        "Obreiro(a)": "🛠️",
        "Líder": "⭐",
        "Missionário(a)": "🌍",
        "Diácono/Isa": "🍷",
        "Presbítero": "📜",
        "Evangelista": "📢",
        "Pastor(a)": "🛡️"
    }

    if "cargo_selecionado" not in st.session_state:
        st.session_state.cargo_selecionado = "Todos"

    cargos_lista = list(icones_cargos.keys())
    cols = st.columns(len(cargos_lista) // 3 + 1)
    
    if st.button("📋 EXIBIR TODOS OS CARGOS"):
        st.session_state.cargo_selecionado = "Todos"

    for i, cargo in enumerate(cargos_lista):
        col_idx = i % len(cols)
        icone = icones_cargos.get(cargo, "🔹")
        if cols[col_idx].button(f"{icone}\n{cargo}"):
            st.session_state.cargo_selecionado = cargo

    st.divider()

    # 3. FILTRO DE ANIVERSARIANTES POR MÊS
    st.subheader("📅 Filtro de Aniversariantes")
    meses_dict = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
        7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    
    mes_atual_idx = datetime.now().month
    mes_selecionado_nome = st.selectbox("Escolha o mês para consulta:", list(meses_dict.values()), index=mes_atual_idx - 1)
    mes_selecionado_num = [k for k, v in meses_dict.items() if v == mes_selecionado_nome][0]

    st.divider()

    # 4. FILTRAGEM DOS DADOS
    df_f = df.copy()
    
    # Filtro por Cargo
    if st.session_state.cargo_selecionado != "Todos":
        df_f = df_f[df_f['Cargo'].astype(str).str.contains(st.session_state.cargo_selecionado, na=False)]

    # 5. EXIBIÇÃO DA MÉTRICA (TOTAL)
    st.markdown(f"""
        <div class="metric-box">
            <small>TOTAL DE MEMBROS NO FILTRO: {st.session_state.cargo_selecionado}</small>
            <h1 style='color:#2e7bcf; margin:0;'>{len(df_f)}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Lista de Membros do Cargo Selecionado
    st.subheader(f"📋 Lista de Nomes - {st.session_state.cargo_selecionado}")
    cols_para_mostrar = ["Nome", "Cargo", "Contato", "Bairro"]
    existentes = [c for c in cols_para_mostrar if c in df_f.columns]
    st.dataframe(df_f[existentes], use_container_width=True, hide_index=True)

    st.divider()

    # 6. ANIVERSARIANTES DO MÊS SELECIONADO
    st.subheader(f"🎂 Aniversariantes de {mes_selecionado_nome}")
    
    if "Data Nascimento" in df_f.columns:
        # Converte para data para extrair o mês e o dia
        df_f['DT_NASC'] = pd.to_datetime(df_f['Data Nascimento'], format='%d/%m/%Y', errors='coerce')
        df_niver = df_f[df_f['DT_NASC'].dt.month == mes_selecionado_num].copy()
        
        if not df_niver.empty:
            df_niver['Dia'] = df_niver['DT_NASC'].dt.day.astype(int)
            df_niver = df_niver.sort_values(by='Dia')
            st.success(f"Encontrados {len(df_niver)} aniversariantes em {mes_selecionado_nome} para este grupo.")
            
            # Exibição organizada
            st.table(df_niver[['Dia', 'Nome', 'Contato']])
        else:
            st.info(f"Nenhum aniversariante encontrado no mês de {mes_selecionado_nome} para o filtro selecionado.")
    else:
        st.warning("Coluna 'Data Nascimento' não encontrada na planilha.")

else:
    st.warning("⚠️ Planilha não carregada. Verifique a URL.")

st.caption("ISOSED Cosmópolis - Inteligência Eclesiástica")
st.caption("Desenvolvido por Comunicando Igrejas")
