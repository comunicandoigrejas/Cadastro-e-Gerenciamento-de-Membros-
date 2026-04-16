import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Proteção de Acesso (Verifica se está logado)
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login na página inicial.")
    st.stop()

st.set_page_config(page_title="Cadastro - ISOSED", page_icon="📝")

st.title("📝 Cadastro de Novo Membro")
st.write(f"Operador atual: **{st.session_state.perfil}**")

# 2. Conexão com Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Erro ao conectar com a planilha. Verifique as 'Secrets' no Streamlit Cloud.")
    st.stop()

# 3. Formulário de Cadastro
with st.form("formulario_membro", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
       with col1:
        nome = st.text_input("Nome Completo")
        whatsapp = st.text_input("WhatsApp (com DDD)")
        
        # Calendário configurado para idades variadas
        nascimento = st.date_input(
            "Data de Nascimento",
            value=datetime(2000, 1, 1),
            min_value=datetime(1930, 1, 1),
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

    if submit:
        if not nome or not consentimento:
            st.error("❌ Erro: O Nome e o Consentimento são obrigatórios.")
        else:
            try:
     # Preparando os dados de forma simplificada para evitar Erro 400
novo_membro = pd.DataFrame([{
            "data_cadastro": str(datetime.now().strftime("%d/%m/%Y %H:%M")),
            "nome": str(nome),
            "whatsapp": str(whatsapp),
            "data_nascimento": str(nascimento.strftime("%d/%m/%Y")), # Formata a data como texto
            "cargo": str(cargo),
            "ministerio": str(", ".join(ministerios)),
            "status": str(status),
            "consentimento_lgpd": "Sim",
            "cadastrado_por": str(st.session_state.perfil)
}])
                # Ler dados existentes
                df_existente = conn.read(worksheet="Membros")
                
                # Juntar e atualizar
                df_final = pd.concat([df_existente, novo_membro], ignore_index=True)
                conn.update(worksheet="Membros", data=df_final)
                
                st.success(f"✅ Sucesso! {nome} foi registrado na base de dados.")
                st.balloons()
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

# Rodapé institucional
st.markdown("---")
st.caption("ISOSED Cosmópolis - Sistema de Gestão Interna")
