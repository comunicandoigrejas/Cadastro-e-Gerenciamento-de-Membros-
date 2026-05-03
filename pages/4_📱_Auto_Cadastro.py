import streamlit as st
import requests
from datetime import datetime

# 1. Configuração para Celular
st.set_page_config(page_title="Auto-Cadastro ISOSED", page_icon="📱", layout="centered")

st.markdown("""
<style>
    /* Esconde menu lateral e barra superior do Streamlit */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; }
    .main { background-color: #0e1117; }
    
    /* Botão de Envio de destaque */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #2e7bcf;
        color: white;
        border: none;
        font-weight: bold;
        padding: 15px;
        font-size: 18px;
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

# Cabeçalho de Boas-Vindas
st.markdown('<div class="header-box"><h2>⛪ BEM-VINDO À ISOSED</h2><p>Preencha seus dados para atualizar seu cadastro em nossa congregação.</p></div>', unsafe_allow_html=True)

# URL DO SEU GOOGLE APPS SCRIPT
WEBAPP_URL = "SUA_URL_DO_APPS_SCRIPT_AQUI"

st.info("💡 Por favor, preencha todos os campos com atenção.")

# 2. Formulário (Otimizado para a tela do celular, sem colunas duplas)
with st.form("form_auto_cadastro", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
    cpf = st.text_input("CPF")
    contato = st.text_input("WhatsApp com DDD (Ex: 11999999999)")
    
    st.markdown("---")
    st.markdown("#### Endereço")
    rua = st.text_input("Rua/Logradouro")
    numero = st.text_input("Número")
    bairro = st.text_input("Bairro")
    cep = st.text_input("CEP")
    
    st.markdown("---")
    st.markdown("#### Informações Pessoais")
    estado_civil = st.selectbox("Estado Civil", ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"])
    conjuge = st.text_input("Nome do Cônjuge (se houver)")
    profissao = st.text_input("Profissão")
    
    local_nascimento = st.text_input("Cidade/Estado de Nascimento")
    
    hoje = datetime.now()
    inicio_limite = datetime(1950, 1, 1)
    
    data_nascimento = st.date_input("Data de Nascimento", value=datetime(2000, 1, 1), min_value=inicio_limite, max_value=hoje, format="DD/MM/YYYY")
    
    st.markdown("---")
    st.markdown("#### Informações Eclesiásticas")
    data_batismo = st.date_input("Data de Batismo", value=hoje, min_value=inicio_limite, max_value=hoje, format="DD/MM/YYYY")
    cargo = st.selectbox("Cargo Ministerial atual", ["Membro", "Obreiro(a)", "Diácono/Isa", "Presbítero", "Evangelista", "Pastor(a)", "Ainda não sou membro (Visitante)"])
    dizimista = st.radio("Você é dizimista?", ["Sim", "Não"], horizontal=True)
    
    st.markdown("---")
    st.warning("⚖️ Termo de Privacidade (LGPD)")
    consentimento = st.checkbox("Autorizo a ISOSED Cosmópolis a armazenar e utilizar meus dados para fins de comunicação e gestão eclesiástica.")
    
    submit = st.form_submit_button("ENVIAR MEU CADASTRO")

    if submit:
        if not nome or not contato or not consentimento:
            st.error("❌ Por favor, preencha o Nome, o Contato e aceite o Termo de Privacidade.")
        else:
            dados = {
                "data_cadastro": hoje.strftime("%d/%m/%Y %H:%M"),
                "nome": str(nome).strip(),
                "sexo": str(sexo),
                "rua": str(rua),
                "numero": str(numero),
                "bairro": str(bairro),
                "cep": str(cep),
                "local_nascimento": str(local_nascimento),
                "data_nascimento": data_nascimento.strftime("%d/%m/%Y"),
                "data_batismo": data_batismo.strftime("%d/%m/%Y"),
                "contato": str(contato),
                "profissao": str(profissao),
                "cpf": str(cpf),
                "estado_civil": str(estado_civil),
                "conjuge": str(conjuge),
                "cargo": str(cargo),
                "dizimista": str(dizimista),
                "consentimento_lgpd": "Sim",
                "cadastrado_por": "Auto-Cadastro (QR Code)" # Identifica que veio pelo QR Code
            }
            
            try:
                response = requests.post(WEBAPP_URL, json=dados, timeout=30)
                if response.text == "Sucesso":
                    st.success("✅ Cadastro enviado com sucesso! Deus abençoe sua vida.")
                    st.balloons()
                else:
                    st.error("Erro ao enviar. Tente novamente ou procure a secretaria.")
            except Exception as e:
                st.error("Falha na conexão de internet. Tente novamente.")

st.caption("ISOSED Cosmópolis - Lei Geral de Proteção de Dados (13.709/2018)")
