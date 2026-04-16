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
# Certifique-se de que o link abaixo está correto e "limpo"
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error(f"Erro de conexão: {e}")
    st.stop()

st.title("📝 Cadastro de Novo Membro")

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
    
    st.warning("⚖️ Conformidade LGPD & Lei 15.211/2025")
    consentimento = st.checkbox("O membro autorizou o tratamento de dados.")

    submit = st.form_submit_button("Finalizar e Salvar Cadastro")

    if submit:
        if not nome or not consentimento:
            st.error("❌ Erro: Nome e Consentimento são obrigatórios.")
        else:
            try:
                # Criando a nova linha
                nova_linha = pd.DataFrame([{
                    "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "nome": str(nome).strip(),
                    "whatsapp": str(whatsapp).strip(),
                    "data_nascimento": nascimento.strftime("%d/%m/%Y"),
                    "cargo": str(cargo),
                    "ministerio": ", ".join(ministerios),
                    "status": str(status),
                    "consentimento_lgpd": "Sim",
                    "cadastrado_por": str(st.session_state.perfil)
                }])

                # MÉTODO CORRETO: Ler -> Concatenar -> Atualizar
                # Lendo dados atuais
                dados_existentes = conn.read(spreadsheet=URL_PLANILHA, worksheet="Membros")
                
                # Juntando os dados antigos com o novo membro
                dados_atualizados = pd.concat([dados_existentes, nova_linha], ignore_index=True)
                
                # Enviando tudo de volta para a planilha
                conn.update(spreadsheet=URL_PLANILHA, worksheet="Membros", data=dados_atualizados)
                
                st.success(f"✅ Sucesso! {nome} foi registrado.")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

st.markdown("---")
st.caption("ISOSED Cosmópolis - Gestão Interna")
