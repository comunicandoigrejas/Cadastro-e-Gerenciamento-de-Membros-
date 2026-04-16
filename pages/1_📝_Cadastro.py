import streamlit as st
import requests
from datetime import datetime

# 1. Configurações Iniciais e CSS para esconder a barra lateral
st.set_page_config(page_title="Cadastro - ISOSED", page_icon="📝", layout="centered")

st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Navegação e Segurança
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login.")
    st.stop()

if st.button("⬅️ Voltar ao Menu Principal"):
    st.switch_page("app.py")

st.title("📝 Cadastro de Membro")
st.divider()

# 3. Formulário
with st.form("form_membro", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    whatsapp = st.text_input("WhatsApp")
    nascimento = st.date_input("Data de Nascimento", value=datetime(1980,1,1), min_value=datetime(1920,1,1))
    cargo = st.selectbox("Cargo", ["Membro", "Obreiro(a)", "Diácono/Isa", "Presbítero", "Evangelista", "Pastor(a)"])
    ministerios = st.multiselect("Ministérios", ["Louvor", "Mídia", "Recepção", "Infantil", "Intercessão"])
    consentimento = st.checkbox("Autorizo o uso de dados (LGPD)")
    
    submit = st.form_submit_button("SALVAR CADASTRO")

    if submit:
        if not nome or not consentimento:
            st.error("Nome e Consentimento são obrigatórios.")
        else:
            WEBAPP_URL = "SUA_URL_DO_APPS_SCRIPT_AQUI"
            dados = {
                "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M"),
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
                res = requests.post(WEBAPP_URL, json=dados, timeout=10)
                if res.text == "Sucesso":
                    st.success("✅ Membro cadastrado com sucesso!")
                    st.balloons()
                else:
                    st.error(f"Erro na planilha: {res.text}")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")
