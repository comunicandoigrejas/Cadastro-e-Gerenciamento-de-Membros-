import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuração de Estética e Segurança
st.set_page_config(page_title="Dashboard - ISOSED", page_icon="📊", layout="wide")

# CSS para criar os botões de ícones e manter o padrão Central de Comando
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
</style>
""", unsafe_allow_html=True)

if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Faça login no menu principal.")
    st.stop()

st.markdown('<div class="header-box"><h2>📊 DASHBOARD ESTRATÉGICO</h2><p>Selecione um cargo para ver a lista de membros e estatísticas</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL", key="voltar"):
    st.switch_page("app.py")

st.divider()

# --- CARREGAMENTO DE DADOS ---
URL_PLANILHA = "SUA_URL_DA_PLANILHA_AQUI"

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
    
    # Dicionário de Ícones para cada Cargo
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

    # Criar grade de botões (3 colunas)
    cargos_lista = list(icones_cargos.keys())
    cols = st.columns(len(cargos_lista) // 3 + 1)
    
    # Botão para ver "Todos"
    if st.button("📋 EXIBIR TODOS"):
        st.session_state.cargo_selecionado = "Todos"

    # Botões com ícones
    for i, cargo in enumerate(cargos_lista):
        col_idx = i % len(cols)
        icone = icones_cargos.get(cargo, "🔹")
        if cols[col_idx].button(f"{icone}\n{cargo}"):
            st.session_state.cargo_selecionado = cargo

    st.divider()

    # 3. FILTRAGEM E EXIBIÇÃO DE RESULTADOS
    df_f = df.copy()
    if st.session_state.cargo_selecionado != "Todos":
        df_f = df_f[df_f['Cargo'].astype(str).str.contains(st.session_state.cargo_selecionado, na=False)]

    # Painel de Quantidade
    st.markdown(f"""
        <div class="metric-box">
            <small>Total de membros no filtro: <b>{st.session_state.cargo_selecionado}</b></small>
            <h1 style='color:#2e7bcf; margin:0;'>{len(df_f)}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Lista de Nomes (Tabela Limpa)
    st.subheader(f"📋 Lista de Nomes - {st.session_state.cargo_selecionado}")
    
    colunas_focadas = ["Nome", "Cargo", "Contato", "Bairro"]
    # Garante que as colunas existem antes de mostrar
    cols_existentes = [c for c in colunas_focadas if c in df_f.columns]
    
    st.dataframe(
        df_f[cols_existentes], 
        use_container_width=True, 
        hide_index=True
    )

    st.divider()

    # 4. ANIVERSARIANTES DO MÊS ATUAL (Mantido como solicitado anteriormente)
    mes_atual = datetime.now().month
    meses_nome = {1:"Janeiro", 2:"Fevereiro", 3:"Março", 4:"Abril", 5:"Maio", 6:"Junho", 
                  7:"Julho", 8:"Agosto", 9:"Setembro", 10:"Outubro", 11:"Novembro", 12:"Dezembro"}
    
    st.subheader(f"🎂 Aniversariantes de {meses_nome[mes_atual]}")
    
    if "Data Nascimento" in df_f.columns:
        df_f['DT_NASC'] = pd.to_datetime(df_f['Data Nascimento'], format='%d/%m/%Y', errors='coerce')
        df_niver = df_f[df_f['DT_NASC'].dt.month == mes_atual].copy()
        
        if not df_niver.empty:
            df_niver['Dia'] = df_niver['DT_NASC'].dt.day.astype(int)
            df_niver = df_niver.sort_values(by='Dia')
            st.success(f"Temos {len(df_niver)} aniversariantes este mês no grupo selecionado!")
            st.table(df_niver[['Dia', 'Nome', 'Contato']])
        else:
            st.info("Nenhum aniversariante neste grupo para o mês atual.")

else:
    st.warning("⚠️ Planilha não carregada. Verifique a URL.")

st.caption("ISOSED Cosmópolis - Gestão Ministerial Estratégica")
st.caption("Desenvolvido por Comunicando Igrejas")
