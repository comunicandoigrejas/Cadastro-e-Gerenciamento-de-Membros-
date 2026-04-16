import streamlit as st

# Proteção de Acesso
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("Por favor, faça login na página inicial.")
    st.stop()

st.title("📝 Cadastro de Membros")
st.write(f"Acesso liberado para: {st.session_state.perfil}")

# Em breve: Código do formulário e conexão com Planilha
