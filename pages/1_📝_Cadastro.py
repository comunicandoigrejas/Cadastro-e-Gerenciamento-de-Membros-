import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Verificação de segurança
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("Inicie sessão na página principal.")
    st.stop()

st.set_page_config(page_title="Cadastro - ISOSED", page_icon="📝")

# --- CONFIGURAÇÃO DA CONEXÃO ---
# Coloque o link da sua planilha aqui para garantir que ele nunca 'suma'
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Erro técnico na ligação com a base de dados.")
    st.stop()

st.title("📝 Cadastro de Membro")

with st.form("form_cadastro", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    whatsapp = st.text_input("Telemóvel/WhatsApp")
    
    # Ajuste de data conforme solicitado (desde 1920)
    nascimento = st.date_input(
        "Data de Nascimento",
        value=datetime(1980, 1, 1),
        min_value=datetime(1920, 1, 1),
        max_value=datetime.now(),
        format="DD/MM/YYYY"
    )
    
    cargo = st.selectbox("Cargo", ["Membro", "Obreiro(a)", "Diácono/Isa", "Presbítero", "Evangelista", "Pastor(a)"])
    ministerios = st.multiselect("Ministérios", ["Louvor", "Mídia", "Recepção", "Infantil", "Intercessão"])
    
    st.warning("⚖️ Termo de Responsabilidade (LGPD)")
    consentimento = st.checkbox("O membro autoriza a custódia destes dados pela ISOSED Cosmópolis.")
    
    submit = st.form_submit_button("Gravar no Sistema")

    if submit:
        if not nome or not consentimento:
            st.error("Nome e Consentimento são obrigatórios.")
        else:
            try:
                # Criar o registo em formato de texto para evitar erro 400
                novo_registo = pd.DataFrame([{
                    "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "nome": str(nome),
                    "whatsapp": str(whatsapp),
                    "data_nascimento": nascimento.strftime("%d/%m/%Y"),
                    "cargo": str(cargo),
                    "ministerio": ", ".join(ministerios),
                    "status": "Ativo",
                    "consentimento_lgpd": "Sim",
                    "cadastrado_por": st.session_state.perfil
                }])

                # LER E ATUALIZAR (Passando explicitamente a folha e o URL)
                dados_atuais = conn.read(spreadsheet=URL_PLANILHA, worksheet="Membros")
                df_final = pd.concat([dados_atuais, novo_registo], ignore_index=True)
                
                conn.update(spreadsheet=URL_PLANILHA, worksheet="Membros", data=df_final)
                
                st.success(f"Registo de {nome} efetuado com sucesso!")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao comunicar com a Planilha: {e}")

st.caption("ISOSED Cosmópolis - Sistema de Gestão Interna")
