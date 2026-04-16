import streamlit as st
import requests
from datetime import datetime

# 1. Configuração e Estética
st.set_page_config(page_title="Cadastro - ISOSED", page_icon="📝", layout="centered")

# CSS corrigido para evitar SyntaxError
st.markdown("""
<style>
/* Esconde a barra de ferramentas superior (Share, Edit, GitHub, etc) */
    header[data-testid="stHeader"] {
        display: none !important;
    }
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

# 2. Segurança e Navegação
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login.")
    st.stop()

# Cabeçalho Padronizado
st.markdown('<div class="header-box"><h2>📝 NOVO CADASTRO</h2><p>Inserir membro na base de dados institucional</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

# --- CONFIGURAÇÃO DA CONEXÃO ---
# COLOQUE ABAIXO O SEU LINK DO APPS SCRIPT (TERMINADO EM /exec)
WEBAPP_URL = "https://script.google.com/macros/s/AKfycbweynuNo3p4lv7eC3xT7iW0QJwP7N9SvrE-XBECwq7ACEO6BiMyGSAeE2RBl7izXELn/exec"

# 3. Formulário de Cadastro
with st.form("form_cadastro", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    whatsapp = st.text_input("WhatsApp com DDD (Somente números)")
    
    # Ajuste das Datas: Início em 1950 e final hoje
    hoje = datetime.now()
    nascimento = st.date_input(
        "Data de Nascimento", 
        value=datetime(2000, 1, 1),
        min_value=datetime(1950, 1, 1),
        max_value=hoje,
        format="DD/MM/YYYY"
    )
    
    cargo = st.selectbox("Cargo Ministerial", ["Membro", "Obreiro(a)", "Diácono/Isa", "Presbítero", "Evangelista", "Pastor(a)"])
    ministerios = st.multiselect("Departamentos", ["Louvor", "Mídia", "Recepção", "Infantil", "Intercessão", "Ação Social"])
    
    st.markdown("---")
    st.warning("⚖️ Conformidade LGPD")
    consentimento = st.checkbox("Confirmo que o membro autorizou a coleta destes dados.")
    
    submit = st.form_submit_button("FINALIZAR E SALVAR REGISTRO")

    if submit:
        if not nome or not consentimento:
            st.error("❌ Erro: O Nome e o Consentimento são obrigatórios.")
        elif "SUA_URL" in WEBAPP_URL:
            st.error("⚠️ Erro: Você esqueceu de colocar a URL do seu Apps Script no código.")
        else:
            dados = {
                "data_cadastro": hoje.strftime("%d/%m/%Y %H:%M"),
                "nome": str(nome).strip(),
                "whatsapp": str(whatsapp).strip(),
                "data_nascimento": nascimento.strftime("%d/%m/%Y"),
                "cargo": str(cargo),
                "ministerio": ", ".join(ministerios),
                "status": "Ativo",
                "consentimento_lgpd": "Sim",
                "cadastrado_por": st.session_state.perfil
            }
            
            try:
                response = requests.post(WEBAPP_URL, json=dados, timeout=30)
                if response.text == "Sucesso":
                    st.success(f"✅ Sucesso! {nome} foi registrado.")
                    st.balloons()
                else:
                    st.error(f"Erro no servidor: {response.text}")
            except Exception as e:
                st.error(f"Falha na conexão: {e}")

st.caption("ISOSED Cosmópolis - Gestão de Dados Segura")
st.caption("Desenvolvido por Comunicando Igrejas")
