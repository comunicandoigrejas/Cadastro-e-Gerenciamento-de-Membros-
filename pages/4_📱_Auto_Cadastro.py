import streamlit as st
import requests
from datetime import datetime

# 1. Configuração para Celular
st.set_page_config(page_title="Auto-Cadastro ISOSED", page_icon="📱", layout="centered")

# CSS focado na visualização mobile (oculta menus e barra superior)
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

st.markdown('<div class="header-box"><h2>⛪ BEM-VINDO À ISOSED</h2><p>Preencha seus dados para atualizar seu cadastro na congregação.</p></div>', unsafe_allow_html=True)

# URL DO SEU GOOGLE APPS SCRIPT
WEBAPP_URL = "SUA_URL_DO_APPS_SCRIPT_AQUI"

# Memória temporária para o endereço (Impede que o endereço suma ao digitar outras coisas)
if "endereco_auto" not in st.session_state:
    st.session_state.endereco_auto = {"rua": "", "bairro": ""}

# --- 1. BUSCA DE CEP (Fora do formulário para não recarregar a página) ---
st.markdown("#### 📍 1. Localize seu Endereço")
col_cep, col_btn = st.columns([2, 1])
cep_digitado = col_cep.text_input("Digite o seu CEP (Apenas números)", max_chars=9)

if col_btn.button("🔍 BUSCAR"):
    cep_limpo = cep_digitado.replace("-", "").replace(".", "").strip()
    if len(cep_limpo) == 8:
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=5)
            dados_cep = response.json()
            if "erro" not in dados_cep:
                st.session_state.endereco_auto["rua"] = dados_cep.get("logradouro", "")
                st.session_state.endereco_auto["bairro"] = dados_cep.get("bairro", "")
                st.success("✅ Endereço encontrado!")
            else:
                st.error("❌ CEP não encontrado.")
        except Exception:
            st.error("⚠️ Erro de conexão ao buscar o CEP.")
    else:
        st.warning("Digite um CEP válido com 8 números.")

st.markdown("---")

# --- 2. FORMULÁRIO PRINCIPAL ---
st.markdown("#### 📝 2. Preencha seus Dados")
with st.form("form_auto_cadastro", clear_on_submit=True):
    nome = st.text_input("Nome Completo")
    sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
    cpf = st.text_input("CPF")
    contato = st.text_input("WhatsApp com DDD (Ex: 11999999999)")
    
    st.markdown("##### Detalhes do Endereço")
    cep = st.text_input("Confirmar CEP", value=cep_digitado)
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
    
    st.markdown("##### Informações Eclesiásticas")
    data_batismo = st.date_input("Data de Batismo", value=hoje, min_value=inicio_limite, max_value=hoje, format="DD/MM/YYYY")
    
    # Campo de Múltipla Escolha com todos os cargos atualizados
    lista_cargos_auto = ["Membro", "Cooperador(a)", "Obreiro(a)", "Líder", "Missionário(a)", "Diácono/Isa", "Presbítero", "Evangelista", "Pastor(a)", "Ainda não sou membro (Visitante)"]
    cargos_auto = st.multiselect("Cargo(s) Ministerial(is) atual(is) (Pode escolher mais de um)", lista_cargos_auto)
    
    dizimista = st.radio("Você é dizimista?", ["Sim", "Não"], horizontal=True)
    
    st.markdown("---")
    st.warning("⚖️ Termo de Privacidade (LGPD)")
    consentimento = st.checkbox("Autorizo a ISOSED Cosmópolis a armazenar e utilizar meus dados para fins de comunicação e gestão eclesiástica.")
    
    # Botão de envio destacado
    st.markdown('<div class="btn-submit">', unsafe_allow_html=True)
    submit = st.form_submit_button("ENVIAR MEU CADASTRO")
    st.markdown('</div>', unsafe_allow_html=True)

    # Processamento do formulário após o clique
    if submit:
        if not nome or not contato or not consentimento:
            st.error("❌ Por favor, preencha o Nome, o Contato e aceite o Termo de Privacidade.")
        elif "SUA_URL" in WEBAPP_URL:
            st.error("⚠️ Aviso ao Administrador: Configure a URL do Apps Script no código.")
        else:
            # Junta os múltiplos cargos escolhidos (Ex: "Presbítero, Líder"). Se vazio, coloca Visitante.
            cargo_final_auto = ", ".join(cargos_auto) if cargos_auto else "Membro/Visitante"
            
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
                "cargo": cargo_final_auto,
                "dizimista": str(dizimista),
                "consentimento_lgpd": "Sim",
                "cadastrado_por": "Auto-Cadastro (QR Code)"
            }
            
            try:
                response = requests.post(WEBAPP_URL, json=dados, timeout=30)
                if response.text == "Sucesso":
                    st.success("✅ Cadastro enviado com sucesso! Deus abençoe sua vida.")
                    st.balloons()
                    # Limpa o endereço da memória para a próxima pessoa que usar o mesmo celular
                    st.session_state.endereco_auto = {"rua": "", "bairro": ""}
                else:
                    st.error(f"Erro no servidor. Procure a secretaria. Log: {response.text}")
            except Exception:
                st.error("Falha na conexão de internet. Verifique seu sinal e tente novamente.")

st.caption("ISOSED Cosmópolis - Lei Geral de Proteção de Dados (13.709/2018)")
st.caption("Desenvolvido por Comunicando Igrejas")
