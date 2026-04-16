import streamlit as st
import pandas as pd

st.set_page_config(page_title="Consulta - ISOSED", page_icon="🔍", layout="wide")

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

if st.session_state.perfil not in ["Pastores", "Secretária"]:
    st.error("Acesso restrito.")
    st.stop()

st.markdown('<div class="header-box"><h2>🔍 CONSULTA DE MEMBROS</h2><p>Localização rápida de registos</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

busca = st.text_input("Digite o nome para pesquisar...")
# Lógica de carregamento de DataFrame aqui
