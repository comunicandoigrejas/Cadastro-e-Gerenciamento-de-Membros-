import streamlit as st
import requests
from datetime import datetime

# 1. Configuração e Estética
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
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0%;
    }
</style>
""", unsafe_allow_html=True)

# 2. Segurança e Navegação
if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login.")
    st.stop()

st.markdown('<div class="header-box"><h2>📝 NOVO CADASTRO</h2><p>Inserir membro na base de dados institucional</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

# URL DO SEU GOOGLE APPS SCRIPT
WEBAPP_URL = "SUA_URL_DO_APPS_SCRIPT_AQUI"

# 3. Formulário de Cadastro
with st.form("form_cadastro", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Nome Completo")
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
        cpf = st.text_input("CPF")
        contato = st.text_input("Contato (WhatsApp/Telefone)")
        profissao = st.text_input("Profissão")
        
    with col2:
        estado_civil = st.selectbox("Estado Civil", ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"])
        conjuge = st.text_input("Nome do Cônjuge (se houver)")
        cargo = st.selectbox("Cargo Ministerial", ["Membro", "Obreiro(a)", "Diácono/Isa", "Presbítero", "Evangelista", "Pastor(a)"])
        dizimista = st.radio("Dizimista?", ["Sim", "Não"], horizontal=True)

    st.markdown("##### Endereço")
    c_rua, c_num = st.columns([3, 1])
    rua = c_rua.text_input("Rua/Logradouro")
    numero = c_num.text_input("Nº")
    
    c_bairro, c_cep = st.columns(2)
    bairro = c_bairro.text_input("Bairro")
    cep = c_cep.text_input("CEP")

    st.markdown("##### Datas e Localidade")
    hoje = datetime.now()
    c_nasc_loc, c_nasc_data = st.columns(2)
    local_nascimento = c_nasc_loc.text_input("Local de Nascimento (Cidade/UF)")
    data_nascimento = c_nasc_data.date_input(
        "Data de Nascimento", 
        value=datetime(2000, 1, 1),
        min_value=datetime(1950, 1, 1),
        max_value=hoje,
        format="DD/MM/YYYY"
    )
    
    data_batismo = st.date_input("Batizado dia", value=hoje, format="DD/MM/YYYY")
    
    st.markdown("---")
    consentimento = st.checkbox("Confirmo que o membro autorizou a coleta destes dados (LGPD).")
    
    submit = st.form_submit_button("FINALIZAR E SALVAR REGISTRO")

    if submit:
        if not nome or not consentimento:
            st.error("❌ O Nome e o Consentimento são obrigatórios.")
        elif "SUA_URL" in WEBAPP_URL:
            st.error("⚠️ Configure a URL do Apps Script.")
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
                "cadastrado_por": st.session_state.perfil
            }
            
            try:
                response = requests.post(WEBAPP_URL, json=dados, timeout=30)
                if response.text == "Sucesso":
                    st.success(f"✅ Sucesso! {nome} foi registrado na base da ISOSED.")
                    st.balloons()
                else:
                    st.error(f"Erro no servidor: {response.text}")
            except Exception as e:
                st.error(f"Falha na conexão: {e}")

st.caption("ISOSED Cosmópolis - Gestão de Dados Segura")
