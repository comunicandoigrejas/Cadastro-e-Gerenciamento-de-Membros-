import streamlit as st
import requests
from datetime import datetime

# 1. Proteção de Acesso
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login na página inicial.")
    st.stop()

st.set_page_config(page_title="Cadastro - ISOSED", page_icon="📝")

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
    
    st.warning("⚖️ Conformidade LGPD & Lei 15.211/2025")
    consentimento = st.checkbox("O membro autorizou o tratamento de dados.")

    submit = st.form_submit_button("Finalizar e Salvar Cadastro")

    # --- LÓGICA DE ENVIO VIA APPS SCRIPT ---
    if submit:
        if not nome or not consentimento:
            st.error("❌ Erro: Nome e Consentimento são obrigatórios.")
        else:
            # substitua o link abaixo pelo link que termina em /exec
            WEBAPP_URL = "https://script.google.com/macros/s/AKfycbweynuNo3p4lv7eC3xT7iW0QJwP7N9SvrE-XBECwq7ACEO6BiMyGSAeE2RBl7izXELn/exec"
            
            dados = {
                "data_cadastro": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "nome": str(nome).strip(),
                "whatsapp": str(whatsapp).strip(),
                "data_nascimento": nascimento.strftime("%d/%m/%Y"),
                "cargo": str(cargo),
                "ministerio": ", ".join(ministerios),
                "status": str(status),
                "consentimento_lgpd": "Sim",
                "cadastrado_por": str(st.session_state.perfil)
            }
            
            try:
                # O comando 'timeout=10' evita que o app fique travado se o Google demorar
                response = requests.post(WEBAPP_URL, json=dados, timeout=10)
                
                if response.text == "Sucesso":
                    st.success(f"✅ Sucesso! {nome} foi registrado com sucesso.")
                    st.balloons()
                else:
                    st.error(f"O Google Sheets respondeu com erro: {response.text}")
            except Exception as e:
                st.error(f"Erro ao conectar com o script da planilha: {e}")

st.markdown("---")
st.caption("ISOSED Cosmópolis - Sistema de Gestão Interna")
