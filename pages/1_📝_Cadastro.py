import streamlit as st
import requests
from datetime import datetime

# 1. Configuração de Estética e Segurança
st.set_page_config(page_title="Cadastro - ISOSED", page_icon="📝", layout="centered")

st.markdown("""
    <style>
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

if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado.")
    st.stop()

# Cabeçalho Padronizado
st.markdown('<div class="header-box"><h2>📝 NOVO CADASTRO</h2><p>Inserir membro na base de dados</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

# Formulário
with st.form("form_cadastro", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    whatsapp = st.text_input("WhatsApp com DDD")
    nascimento = st.date_input("Data de Nascimento", value=datetime(01, 01, 1950))
    cargo = st.selectbox("Cargo Ministerial", ["Membro", "Obreiro(a)", "Diácono/Isa", "Presbítero", "Evangelista", "Pastor(a)"])
    consentimento = st.checkbox("Membro autorizou o uso de dados (LGPD)")
    
    if st.form_submit_button("CONCLUIR REGISTRO"):
        if nome and consentimento:
            # Lógica de envio via Apps Script aqui
            st.success(f"Cadastro de {nome} enviado!")
        else:
            st.error("Preencha o nome e aceite a LGPD.")
