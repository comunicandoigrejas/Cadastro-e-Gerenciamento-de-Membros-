import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuração de Estética e Segurança
st.set_page_config(page_title="Dashboard - ISOSED", page_icon="📊", layout="wide")

# CSS para o padrão "Central de Comando"
st.markdown("""
<style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; }
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
    .metric-card {
        background-color: #1a1a1a;
        border: 1px solid #2e7bcf;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login.")
    st.stop()

if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.warning("🚫 Acesso restrito apenas à liderança e secretaria.")
    st.stop()

st.markdown('<div class="header-box"><h2>📊 DASHBOARD ESTRATÉGICO</h2><p>Indicadores de Crescimento e Aniversariantes ISOSED</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

# --- CONFIGURAÇÃO DOS DADOS ---
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
    df.columns = df.columns.str.strip() # Limpa os nomes das colunas
    
    # 2. PREPARAÇÃO DOS FILTROS
    # Tenta achar a coluna Ministério, se não achar, usa Cargo
    col_depto = None
    for col in ["Ministério", "Departamento", "Cargo"]:
        if col in df.columns:
            col_depto = col
            break

    # Converte as datas de nascimento para formato de data real e extrai o Mês
    if "Data Nascimento" in df.columns:
        df['Data_Nasc_DT'] = pd.to_datetime(df['Data Nascimento'], format='%d/%m/%Y', errors='coerce')
        df['Mes_Num'] = df['Data_Nasc_DT'].dt.month
    else:
        df['Mes_Num'] = pd.NA

    # Dicionário de Meses
    meses_dict = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho",
                  7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
    
    mes_atual = datetime.now().month

    # --- ÁREA DE FILTROS ---
    st.subheader("🎛️ Filtros do Painel")
    f1, f2 = st.columns(2)
    
    with f1:
        if col_depto:
            # Pega todos os cargos/departamentos únicos (mesmo os separados por vírgula)
            todos_deptos = set()
            for val in df[col_depto].dropna():
                for v in str(val).split(","):
                    todos_deptos.add(v.strip())
            
            lista_deptos = ["Todos"] + sorted(list(todos_deptos))
            filtro_depto = st.selectbox("Filtrar por Departamento/Cargo", lista_deptos)
        else:
            filtro_depto = "Todos"
            st.info("Nenhuma coluna de Cargo ou Ministério encontrada.")

    with f2:
        lista_meses = ["Todos"] + list(meses_dict.values())
        # O sistema já abre automaticamente no mês atual!
        filtro_mes = st.selectbox("Aniversariantes do Mês", lista_meses, index=mes_atual)

    # --- APLICANDO O FILTRO GERAL DE DEPARTAMENTO ---
    df_filtrado = df.copy()
    if filtro_depto != "Todos" and col_depto:
        df_filtrado = df_filtrado[df_filtrado[col_depto].astype(str).str.contains(filtro_depto, case=False, na=False)]

    st.divider()

    # 3. INDICADORES RÁPIDOS (Baseados no departamento escolhido)
    st.subheader(f"📌 Indicadores: {filtro_depto}")
    m1, m2, m3, m4 = st.columns(4)
    
    m1.markdown(f"<div class='metric-card'><small>Total de Registros</small><h2 style='margin:0;'>{len(df_filtrado)}</h2></div>", unsafe_allow_html=True)
    
    if "Sexo" in df_filtrado.columns:
        homens = len(df_filtrado[df_filtrado["Sexo"] == "Masculino"])
        mulheres = len(df_filtrado[df_filtrado["Sexo"] == "Feminino"])
        m2.markdown(f"<div class='metric-card'><small>Homens</small><h2 style='margin:0;'>{homens}</h2></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class='metric-card'><small>Mulheres</small><h2 style='margin:0;'>{mulheres}</h2></div>", unsafe_allow_html=True)
        
    m4.markdown(f"<div class='metric-card'><small>Unidade</small><h4 style='margin:0; padding-top:5px;'>Cosmópolis/SP</h4></div>", unsafe_allow_html=True)

    # 4. GRÁFICOS
    c1, c2 = st.columns(2)
    with c1:
        st.write("**Composição Ministerial/Cargos**")
        if "Cargo" in df_filtrado.columns:
            st.bar_chart(df_filtrado["Cargo"].value_counts())

    with c2:
        st.write("**Proporção de Dizimistas**")
        if "Dizimista" in df_filtrado.columns:
            st.bar_chart(df_filtrado["Dizimista"].value_counts())

    st.divider()

    # 5. MÓDULO DE ANIVERSARIANTES
    st.subheader(f"🎂 Aniversariantes - {filtro_mes}")
    
    # Filtra pelo mês selecionado
    if filtro_mes != "Todos":
        # Descobre o número do mês com base no nome selecionado
        numero_mes = [k for k, v in meses_dict.items() if v == filtro_mes][0]
        df_niver = df_filtrado[df_filtrado['Mes_Num'] == numero_mes].copy()
    else:
        df_niver = df_filtrado[df_filtrado['Mes_Num'].notna()].copy()

    if not df_niver.empty:
        # Extrai o Dia para poder ordenar do dia 1 ao dia 31
        df_niver['Dia'] = df_niver['Data_Nasc_DT'].dt.day.astype('Int64')
        df_niver = df_niver.sort_values(by='Dia')
        
        # Cria uma tabela bonita só com as informações essenciais
        colunas_exibir = {}
        if "Nome" in df_niver.columns: colunas_exibir['Nome'] = df_niver['Nome']
        colunas_exibir['Dia do Niver'] = df_niver['Dia']
        if "Contato" in df_niver.columns: colunas_exibir['WhatsApp'] = df_niver['Contato']
        if col_depto: colunas_exibir['Cargo/Depto'] = df_niver[col_depto]
        
        tabela_niver = pd.DataFrame(colunas_exibir)
        
        st.success(f"Encontramos {len(df_niver)} aniversariante(s)!")
        st.dataframe(tabela_niver, use_container_width=True, hide_index=True)
    else:
        st.info(f"Nenhum aniversariante encontrado em {filtro_mes} para o filtro atual.")

else:
    st.warning("⚠️ Não foi possível carregar os dados. Verifique a URL da planilha.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("ISOSED Cosmópolis - Dashboard Analítico")
st.caption("Desenvolvido por Comunicando Igrejas")
