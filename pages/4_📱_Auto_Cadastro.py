import streamlit as st
import requests
from datetime import datetime

# 1. Configuração para Celular
st.set_page_config(page_title="Auto-Cadastro ISOSED", page_icon="📱", layout="centered")

st.markdown("""
<style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; }
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #2e7bcf;
        color: white;
        border: none;
        font-weight: bold;
        padding: 10px;
        font-size: 16px;
    }
    .btn-submit>button {
        padding: 15px;
        font-size: 18px;
        background-color: #00b300;
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

# Cabeçalho
st.markdown('<div class="header-box"><h2>⛪ BEM-VINDO À ISOSED</h2><p>Preencha seus dados para atualizar seu cadastro.</p></div>', unsafe_allow_html=True)

WEBAPP_URL = "https://script.google.com/macros/s/AKfycbzyxIGWN4xw5pGL-q1ACftSsHYwDeXTUd_EgO9ChoE8Ofcr8Y_DGWnk7bSorZpHFH2a/exec"

# --- LÓGICA DE BUSCA DE CEP (VIACEP) ---
# Salva o endereço na memória temporária da tela
if "endereco_auto" not in st.session_state:
    st.session_state.endereco_auto = {"rua": "", "bairro": ""}

st.markdown("#### 📍 1. Localize seu Endereço")
col_cep, col_btn = st.columns([2, 1])
cep_digitado = col_cep.text_input("Digite o seu CEP (Apenas números)", max_chars=9)

if col_btn.button("🔍 BUSCAR"):
    cep_limpo = cep_digitado.replace("-", "").replace(".", "").strip()
    if len(cep_limpo) == 8:
        try:
            # Conecta com a base dos Correios
            response = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=5)
            dados = response.json()
            if "erro" not in dados:
                st.session_state.endereco_auto["rua"] = dados.get("logradouro", "")
                st.session_state.endereco_auto["bairro"] = dados.get("bairro", "")
                st.success("✅ Endereço encontrado!")
            else:
                st.error("❌ CEP não encontrado.")
        except Exception:
            st.error("⚠️ Erro de conexão ao buscar o CEP.")
    else:
        st.warning("Digite um CEP válido com 8 números.")

st.markdown("---")

# --- FORMULÁRIO PRINCIPAL ---
st.markdown("#### 📝 2. Preencha seus Dados")
with st.form("form_auto_cadastro", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
    cpf = st.text_input("CPF")
    contato = st.text_input("WhatsApp com DDD (Ex: 11999999999)")
    
    st.markdown("##### Detalhes do Endereço")
    cep = st.text_input("Confirmar CEP", value=cep_digitado)
    
    # Preenchimento automático ativado nos campos abaixo
    rua = st.text_input("Rua/Logradouro", value=st.session_state.endereco_auto["rua"])
    numero = st.text_input("Número")
    bairro = st.text_input("Bairro", value=st.session_state.endereco_auto["bairro"])
    
    st.markdown("##### Informações Pessoais")
    estado_civil = st.selectbox("Estado Civil", ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"])
    conjuge = st.text_input("Nome do Cônjuge (se houver)")
    profissao = st.text_input("Profissão")
    
    local_nascimento = st.text_input("Cidade/Estado de Nascimento")
    
    hoje = datetime.now()
    inicio_limite = datetime(1950, 1, 1)
    
    data_nascimento = st.date_input("Data de Nascimento", value=datetime(2000, 1, 1), min_value=inicio_limite, max_value=hoje, format="DD/MM/YYYY")
    
    # No formulário de Auto-Cadastro:
st.markdown("##### Informações Eclesiásticas")
data_batismo = st.date_input("Data de Batismo", value=hoje, min_value=inicio_limite, max_value=hoje, format="DD/MM/YYYY")

# NOVO: Multiselect no Auto-Cadastro
lista_cargos_auto = ["Membro", "Cooperador(a)", "Obreiro(a)", "Líder", "Missionário(a)", "Diácono/Isa", "Presbítero", "Evangelista", "Pastor(a)", "Ainda não sou membro (Visitante)"]
cargos_auto = st.multiselect("Cargo(s) Ministerial(is) atual(is)", lista_cargos_auto)

dizimista = st.radio("Você é dizimista?", ["Sim", "Não"], horizontal=True)

# No dicionário de dados do envio:
dados = {
    # ... outros campos ...
    "cargo": ", ".join(cargos_auto) if cargos_auto else "Membro/Visitante",
    # ... outros campos ...
}
    
    st.markdown("---")
    st.warning("⚖️ Termo de Privacidade (LGPD)")
    consentimento = st.checkbox("Autorizo a ISOSED Cosmópolis a armazenar e utilizar meus dados para fins de comunicação e gestão eclesiástica.")
    
    st.markdown('<div class="btn-submit">', unsafe_allow_html=True)
    submit = st.form_submit_button("ENVIAR MEU CADASTRO")
    st.markdown('</div>', unsafe_allow_html=True)

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
                "cadastrado_por": "Auto-Cadastro (QR Code)"
            }
            
            try:
                response = requests.post(WEBAPP_URL, json=dados, timeout=30)
                if response.text == "Sucesso":
                    st.success("✅ Cadastro enviado com sucesso! Deus abençoe sua vida.")
                    st.balloons()
                    # Limpa a memória do endereço para o próximo irmão que for usar o mesmo celular
                    st.session_state.endereco_auto = {"rua": "", "bairro": ""}
                else:
                    st.error("Erro ao enviar. Procure a secretaria.")
            except Exception:
                st.error("Falha na conexão de internet. Tente novamente.")

st.caption("ISOSED Cosmópolis - Lei Geral de Proteção de Dados (13.709/2018)")
