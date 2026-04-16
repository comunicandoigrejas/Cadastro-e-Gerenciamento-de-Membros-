import streamlit as st
import pandas as pd

# 1. Verificação de Acesso
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Por favor, faça login na página inicial.")
    st.stop()

# 2. Restrição por Perfil (Aqui é onde liberamos apenas para Pastores e Secretária)
perfis_autorizados = ["Pastores", "Secretária"]

if st.session_state.perfil not in perfis_autorizados:
    st.warning("🚫 Acesso restrito. Este painel é exclusivo para a liderança e secretaria.")
    st.stop()

# --- Se passar daqui, o conteúdo do Dashboard aparece ---
st.title("📊 Dashboard Estratégico - ISOSED")
st.write(f"Bem-vindo, Pastor. Aqui estão os dados da congregação.")
