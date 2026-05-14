import streamlit as st
import pandas as pd
import re  # Nova biblioteca para ler e converter os links

# 1. Configuração de Estética e Segurança
st.set_page_config(page_title="Consulta - ISOSED", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] { display: none; }
    header[data-testid="stHeader"] { visibility: hidden; height: 0%; }
    .main { background-color: #0e1117; }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #2e7bcf;
        font-weight: bold;
        transition: 0.3s;
        height: auto;
        padding: 15px 5px;
    }
    .stButton>button:hover {
        background-color: #2e7bcf;
        border-color: white;
        transform: scale(1.02);
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
    
    .pdf-button {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #d32f2f;
        color: white !important;
        padding: 10px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 15px;
    }
    
    .section-title {
        color: #2e7bcf;
        font-size: 16px;
        font-weight: bold;
        margin-top: 10px;
        margin-bottom: 10px;
        border-bottom: 1px solid #1a1a1a;
        padding-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

if "logado" not in st.session_state or not st.session_state.logado:
    st.error("⚠️ Acesso negado. Por favor, faça login.")
    st.stop()

st.markdown('<div class="header-box"><h2>🔍 CONSULTA DE MEMBROS</h2><p>Ficha completa, prontuário digital e emissão de formulários</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

# Coloque sua URL entre as aspas:
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"

def obter_link_csv(url):
    if "/edit" in url:
        return url.split("/edit")[0] + "/export?format=csv"
    return url

# Função MÁGICA para converter o link do Google Drive
def converter_link_drive(url):
    url = str(url).strip()
    if "drive.google.com" in url:
        # Procura o ID no formato /file/d/ID/
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/uc?export=view&id={file_id}"
        # Procura o ID no formato ?id=ID
        match2 = re.search(r'id=([a-zA-Z0-9_-]+)', url)
        if match2:
            file_id = match2.group(1)
            return f"https://drive.google.com/uc?export=view&id={file_id}"
    return url

@st.cache_data(ttl=60)
def carregar_dados(link):
    try:
        df = pd.read_csv(link)
        df.columns = df.columns.str.strip()
        df = df.fillna("") 
        return df
    except:
        return None

df = carregar_dados(obter_link_csv(URL_PLANILHA))

if df is not None and not df.empty:
    
    st.subheader("🔍 Localizar Membro")
    busca = st.text_input("Pesquisar por nome ou sobrenome:", placeholder="Ex: João Silva")
    
    df_f = df.copy()
    
    if busca and "Nome" in df_f.columns:
        df_f = df_f[df_f['Nome'].astype(str).str.contains(busca, case=False, na=False)]

    st.divider()

    if not df_f.empty:
        st.success(f"Encontrado(s) {len(df_f)} registro(s):")
        
        for i, row in df_f.iterrows():
            num_cadastro = str(row.get("Nº Cadastro", "-"))
            nome = str(row.get("Nome", "Sem Nome"))
            cargo = str(row.get("Cargo", "Membro"))
            cpf = str(row.get('CPF', ''))
            data_nasc = str(row.get('Data Nascimento', ''))
            data_batismo = str(row.get('Data Batismo', ''))
            conjuge = str(row.get("Cônjuge", ""))
            dizimista = str(row.get("Dizimista", ""))
            
            # --- PEGA E CONVERTE O LINK DA FOTO ---
            foto_original = str(row.get("Link Foto", "")).strip()
            foto_url = converter_link_drive(foto_original)
            
            with st.expander(f"👤 [{num_cadastro}] {nome} - {cargo}"):
                
                st.markdown('<div class="section-title">📋 Dados Pessoais</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                c1.write(f"**🔢 Nº Cadastro:** {num_cadastro}")
                c1.write(f"**🚻 Sexo:** {row.get('Sexo', '')}")
                c1.write(f"**🎂 Nascimento:** {data_nasc} ({row.get('Local Nascimento', '')})")
                c1.write(f"**🪪 CPF:** {cpf}")
                
                c2.write(f"**💍 Estado Civil:** {row.get('Estado Civil', '')}")
                if conjuge:
                    c2.write(f"**👩‍❤️‍👨 Cônjuge:** {conjuge}")
                c2.write(f"**💼 Profissão:** {row.get('Profissão', '')}")

                st.markdown('<div class="section-title">⛪ Informações Eclesiásticas & Contato</div>', unsafe_allow_html=True)
                c3, c4 = st.columns(2)
                c3.write(f"**🕊️ Batismo:** {data_batismo}")
                c3.write(f"**🛡️ Cargo(s):** {cargo}")
                
                c4.write(f"**📞 WhatsApp:** {row.get('Contato', '')}")
                icone_dizimo = "💎 Sim" if dizimista == "Sim" else "⚪ Não"
                c4.write(f"**💰 Dizimista:** {icone_dizimo}")

                st.markdown('<div class="section-title">📍 Endereço</div>', unsafe_allow_html=True)
                st.write(f"🏠 {row.get('Rua', '')}, {row.get('Nº', '')} - {row.get('Bairro', '')} | **CEP:** {row.get('CEP', '')}")

                st.markdown('<div class="section-title">🔒 Sistema & Documentos</div>', unsafe_allow_html=True)
                st.write(f"**📅 Data de Inserção no Sistema:** {row.get('Data Cadastro', '')}")
                
                # --- PREPARA A CAIXA DA FOTO PARA O HTML ---
                if foto_url.startswith("http"):
                    html_foto_box = f'<img src="{foto_url}" alt="Foto de {nome}" style="width: 100%; height: 100%; object-fit: cover;">'
                else:
                    html_foto_box = 'FOTO 3x4'

                # --- GERADOR DE FICHA COMPLETA A4 (HTML PARA IMPRESSÃO) ---
                html_ficha_completa = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <meta charset="UTF-8">
                <title>Ficha de Cadastro - {nome}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 20px; display: flex; justify-content: center; }}
                    .page {{ width: 210mm; min-height: 297mm; background: white; padding: 20mm; box-sizing: border-box; box-shadow: 0 0 10px rgba(0,0,0,0.1); position: relative; }}
                    .header {{ text-align: center; margin-bottom: 30px; border-bottom: 2px solid #003366; padding-bottom: 10px; }}
                    .header h1 {{ margin: 0; color: #003366; font-size: 24px; text-transform: uppercase; }}
                    .header h2 {{ margin: 5px 0 0 0; color: #666; font-size: 16px; }}
                    .photo-box {{ position: absolute; top: 20mm; right: 20mm; width: 30mm; height: 40mm; border: 1px dashed #333; display: flex; justify-content: center; align-items: center; color: #999; font-size: 12px; font-weight: bold; overflow: hidden; background: #fafafa; }}
                    .section-title {{ font-size: 14px; color: #003366; font-weight: bold; margin-top: 25px; border-bottom: 1px solid #ccc; padding-bottom: 3px; margin-bottom: 15px; text-transform: uppercase; }}
                    .row {{ display: flex; margin-bottom: 12px; flex-wrap: wrap; width: 80%; }}
                    .row-full {{ width: 100%; }}
                    .field {{ font-size: 12px; margin-right: 20px; margin-bottom: 5px; }}
                    .field strong {{ color: #333; }}
                    .field-value {{ border-bottom: 1px solid #000; padding: 0 5px; min-width: 50px; display: inline-block; color: #000; font-weight: bold; }}
                    .signature-area {{ margin-top: 60px; text-align: center; }}
                    .signature-line {{ width: 60%; border-top: 1px solid #000; margin: 0 auto 5px auto; }}
                    @media print {{
                        body {{ background: white; padding: 0; display: block; }}
                        .page {{ box-shadow: none; width: 100%; min-height: auto; padding: 0; }}
                        @page {{ margin: 15mm; size: A4; }}
                    }}
                </style>
                </head>
                <body>
                    <div class="page">
                        <div class="header">
                            <h1>ISOSED COSMÓPOLIS</h1>
                            <h2>Ficha Completa de Cadastro de Membro</h2>
                        </div>
                        
                        <!-- CAIXA DA FOTO DINÂMICA -->
                        <div class="photo-box">
                            {html_foto_box}
                        </div>
                        
                        <div class="row row-full">
                            <div class="field"><strong>Nº de Cadastro:</strong> <span class="field-value">{num_cadastro}</span></div>
                            <div class="field"><strong>Data do Registro:</strong> <span class="field-value">{row.get('Data Cadastro', '')}</span></div>
                        </div>

                        <div class="section-title">Dados Pessoais</div>
                        <div class="row row-full">
                            <div class="field" style="flex: 1;"><strong>Nome Completo:</strong> <span class="field-value" style="width: 90%;">{nome}</span></div>
                        </div>
                        <div class="row row-full">
                            <div class="field"><strong>Sexo:</strong> <span class="field-value">{row.get('Sexo', '')}</span></div>
                            <div class="field"><strong>Data de Nascimento:</strong> <span class="field-value">{data_nasc}</span></div>
                            <div class="field"><strong>Local Nasc:</strong> <span class="field-value">{row.get('Local Nascimento', '')}</span></div>
                        </div>
                        <div class="row row-full">
                            <div class="field"><strong>CPF:</strong> <span class="field-value">{cpf}</span></div>
                            <div class="field"><strong>Profissão:</strong> <span class="field-value">{row.get('Profissão', '')}</span></div>
                            <div class="field"><strong>Estado Civil:</strong> <span class="field-value">{row.get('Estado Civil', '')}</span></div>
                        </div>
                        <div class="row row-full">
                            <div class="field" style="flex: 1;"><strong>Nome do Cônjuge:</strong> <span class="field-value" style="width: 80%;">{conjuge if conjuge else "______________________________________________________"}</span></div>
                        </div>

                        <div class="section-title">Endereço e Contato</div>
                        <div class="row row-full">
                            <div class="field" style="flex: 1;"><strong>Logradouro:</strong> <span class="field-value" style="width: 80%;">{row.get('Rua', '')}</span></div>
                            <div class="field"><strong>Nº:</strong> <span class="field-value">{row.get('Nº', '')}</span></div>
                        </div>
                        <div class="row row-full">
                            <div class="field"><strong>Bairro:</strong> <span class="field-value">{row.get('Bairro', '')}</span></div>
                            <div class="field"><strong>CEP:</strong> <span class="field-value">{row.get('CEP', '')}</span></div>
                            <div class="field"><strong>WhatsApp/Contato:</strong> <span class="field-value">{row.get('Contato', '')}</span></div>
                        </div>

                        <div class="section-title">Informações Eclesiásticas</div>
                        <div class="row row-full">
                            <div class="field"><strong>Data de Batismo:</strong> <span class="field-value">{data_batismo}</span></div>
                            <div class="field"><strong>Cargo(s) Ministerial(is):</strong> <span class="field-value">{cargo}</span></div>
                            <div class="field"><strong>Dizimista:</strong> <span class="field-value">{dizimista}</span></div>
                        </div>
                        
                        <div class="section-title">Termo de Consentimento e Privacidade (LGPD)</div>
                        <div style="font-size: 11px; text-align: justify; color: #333; line-height: 1.5; margin-bottom: 10px;">
                            Autorizo a ISOSED Cosmópolis a coletar, armazenar e utilizar meus dados pessoais aqui fornecidos para fins exclusivos de gestão eclesiástica, comunicação pastoral e organização interna, em conformidade com a Lei Geral de Proteção de Dados (Lei nº 13.709/2018).
                        </div>
                        <div class="row row-full">
                            <div class="field"><strong>Aceite Digital no Sistema:</strong> <span class="field-value">{row.get('Consentimento LGPD', '')}</span></div>
                            <div class="field"><strong>Responsável pelo Cadastro:</strong> <span class="field-value">{row.get('Cadastrado Por', '')}</span></div>
                        </div>

                        <div class="signature-area">
                            <div class="signature-line"></div>
                            <div class="field"><strong>Assinatura do Membro / Responsável</strong></div>
                            <div style="font-size: 10px; color: #666; margin-top: 5px;">Declaro que as informações preenchidas são verdadeiras.</div>
                        </div>
                    </div>
                    <script>
                        window.onload = function() {{ window.print(); }};
                    </script>
                </body>
                </html>
                """
                
                # Botões finais
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    nome_arquivo = f"Ficha_Cadastro_{nome.replace(' ', '_')}.html"
                    st.download_button(
                        label="🖨️ GERAR FICHA COMPLETA (A4)",
                        data=html_ficha_completa,
                        file_name=nome_arquivo,
                        mime="text/html",
                        use_container_width=True
                    )
                    
                with btn_col2:
                    link_ficha = str(row.get('Link Ficha', ''))
                    if "Link Ficha" in df_f.columns and link_ficha.startswith("http"):
                        st.markdown(f'<a href="{link_ficha}" target="_blank" class="pdf-button" style="margin-top:0;">📄 ABRIR ARQUIVO ASSINADO</a>', unsafe_allow_html=True)
                    else:
                        st.info("ℹ️ Ficha digitalizada não vinculada.")

    else:
        if busca:
            st.warning("Nenhum membro encontrado com este nome.")
        else:
            st.info("👆 Digite o nome do membro acima para visualizar a ficha completa.")
else:
    st.error("⚠️ Erro: Não foi possível carregar a base de dados.")

st.markdown("---")
st.caption("ISOSED Cosmópolis - Sistema de Gestão Institucional")
st.caption("Desenvolvido por Comunicando Igrejas")
