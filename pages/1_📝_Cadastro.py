import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Proteção de Acesso
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login na página inicial.")
    st.stop()

st.set_page_config(page_title="Cadastro - ISOSED", page_icon="📝")

# --- CONFIGURAÇÃO DA CONEXÃO ---
# Substitua pelo seu link real se o erro de 'Spreadsheet specified' voltar
URL_PLANILHA = "SUA_URL_DA_PLANILHA_AQUI"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Erro de conexão: {e}")
    st.stop()

st.title("📝 Cadastro de Novo Membro")
st.write(f"Operador atual: **{st.session_state.perfil}**")

# 2. Formulário de Cadastro
with st.form("formulario_membro", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Nome Completo")
        whatsapp = st.text_input("WhatsApp (com DDD)")
        nascimento = st.date_input(
            "Data de Nascimento",
            value=datetime(1980, 1, 1),
            min_value=datetime(1920, 1, 1),
            max_value=datetime.now(),
            format="DD/MM/YYYY"
        )
    
    with col2:
        cargo = st.selectbox("Cargo Ministerial", ["Membro", "Obreiro(a)", "Diácono/Isa", "Presbítero", "Evangelista", "Pastor(a)"])
        ministerios = st.multiselect("Ministérios/Departamentos", ["Louvor", "Mídia", "Recepção", "Infantil", "Intercessão", "Ação Social"])
        status = st.selectbox("Status Inicial", ["Ativo", "Visitante"])

    st.divider()
    
    # Seção LGPD
    st.warning("⚖️ Conformidade LGPD & Lei 15.211/2025")
    consentimento = st.checkbox("O membro autorizou o tratamento de seus dados para fins institucionais da ISOSED.")

    submit = st.form_submit_button("Finalizar e Salvar Cadastro")

    # --- INÍCIO DA LÓGICA DE SALVAMENTO ---
    if submit:
        if not nome or not consentimento:
            st.error("❌ Erro: O Nome e o Consentimento são obrigatórios.")
        else:
            try:
                # Criando o DataFrame com dados limpos e em formato texto
                novo_membro = pd.DataFrame([{
                    "data_cadastro": str(datetime.now().strftime("%d/%m/%Y %H:%M")),
                    "nome": str(nome).strip(),
                    "whatsapp": str(whatsapp).strip(),
                    "data_nascimento": str(nascimento.strftime("%d/%m/%Y")),
                    "cargo": str(cargo),
                    "ministerio": str(", ".join(ministerios)),
                    "status": str(status),
                    "consentimento_lgpd": "Sim",
                    "cadastrado_por": str(st.session_state.perfil)
                }])

                # Gravação usando o método append para evitar Erro 400
                conn.update(
                    spreadsheet=URL_PLANILHA,
                    worksheet="Membros",
                    data=novo_membro,
                    append=True
                )
                
                st.success(f"✅ Sucesso! {nome} foi registrado na base da ISOSED.")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

st.markdown("---")
st.caption("ISOSED Cosmópolis - Sistema de Gestão Interna")
