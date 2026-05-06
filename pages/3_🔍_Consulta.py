import streamlit as st
import pandas as pd

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

st.markdown('<div class="header-box"><h2>🔍 CONSULTA DE MEMBROS</h2><p>Ficha completa, prontuário digital e emissão de credenciais</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"

def obter_link_csv(url):
    if "/edit" in url:
        return url.split("/edit")[0] + "/export?format=csv"
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
    
    # FILTRO POR ÍCONES
    st.subheader("👥 Filtrar por Cargo Ministerial")
    icones_cargos = {
        "Membro": "👤", "Cooperador(a)": "🤝", "Obreiro(a)": "🛠️",
        "Líder": "⭐", "Missionário(a)": "🌍", "Diácono/Isa": "🍷",
        "Presbítero": "📜", "Evangelista": "📢", "Pastor(a)": "🛡️",
        "Visitante": "👋"
    }

    if "filtro_cargo_consulta" not in st.session_state:
        st.session_state.filtro_cargo_consulta = "Todos"

    cols_cargos = st.columns(5)
    
    if st.button("📋 EXIBIR TODOS"):
        st.session_state.filtro_cargo_consulta = "Todos"

    cargos_lista = list(icones_cargos.keys())
    for i, cargo in enumerate(cargos_lista):
        col_idx = i % 5
        icone = icones_cargos[cargo]
        if cols_cargos[col_idx].button(f"{icone}\n{cargo}"):
            st.session_state.filtro_cargo_consulta = cargo

    st.divider()

    # BUSCA
    busca = st.text_input(f"Pesquisar nome (Filtro atual: {st.session_state.filtro_cargo_consulta}):", placeholder="Ex: João Silva")
    
    df_f = df.copy()
    if st.session_state.filtro_cargo_consulta != "Todos":
        df_f = df_f[df_f['Cargo'].astype(str).str.contains(st.session_state.filtro_cargo_consulta, na=False)]
    
    if busca and "Nome" in df_f.columns:
        df_f = df_f[df_f['Nome'].astype(str).str.contains(busca, case=False, na=False)]

    if not df_f.empty:
        st.success(f"Encontrado(s) {len(df_f)} registro(s):")
        
        for i, row in df_f.iterrows():
            nome = row.get("Nome", "Sem Nome")
            cargo = row.get("Cargo", "Membro")
            cpf = row.get('CPF', '')
            data_nasc = row.get('Data Nascimento', '')
            data_batismo = row.get('Data Batismo', '')
            
            with st.expander(f"👤 {nome} - {cargo}"):
                
                # --- DADOS DA FICHA ---
                st.markdown('<div class="section-title">📋 Dados Pessoais</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                c1.write(f"**🚻 Sexo:** {row.get('Sexo', '')}")
                c1.write(f"**🎂 Nascimento:** {data_nasc} ({row.get('Local Nascimento', '')})")
                c1.write(f"**🪪 CPF:** {cpf}")
                
                c2.write(f"**💍 Estado Civil:** {row.get('Estado Civil', '')}")
                conjuge = row.get("Cônjuge", "")
                if conjuge: c2.write(f"**👩‍❤️‍👨 Cônjuge:** {conjuge}")
                c2.write(f"**💼 Profissão:** {row.get('Profissão', '')}")

                st.markdown('<div class="section-title">⛪ Informações Eclesiásticas & Contato</div>', unsafe_allow_html=True)
                c3, c4 = st.columns(2)
                c3.write(f"**🕊️ Batismo:** {data_batismo}")
                c3.write(f"**🛡️ Cargo(s):** {cargo}")
                
                c4.write(f"**📞 WhatsApp:** {row.get('Contato', '')}")
                dizimista = row.get("Dizimista", "")
                c4.write(f"**💰 Dizimista:** {'💎 Sim' if dizimista == 'Sim' else '⚪ Não'}")

                st.markdown('<div class="section-title">📍 Endereço</div>', unsafe_allow_html=True)
                st.write(f"🏠 {row.get('Rua', '')}, {row.get('Nº', '')} - {row.get('Bairro', '')} | **CEP:** {row.get('CEP', '')}")

                st.markdown('<div class="section-title">🔒 Sistema & Documentos</div>', unsafe_allow_html=True)
                
                # --- GERADOR DE CARTEIRINHA EM HTML ---
                html_carteirinha = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <meta charset="UTF-8">
                <title>Carteirinha - {nome}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f0f0f0; margin: 0; }}
                    .card {{ width: 8.6cm; height: 5.4cm; background: white; border-radius: 8px; border: 2px solid #003366; padding: 10px; box-sizing: border-box; position: relative; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                    .header {{ background: #003366; color: white; text-align: center; padding: 5px; border-radius: 4px 4px 0 0; font-weight: bold; font-size: 14px; margin: -10px -10px 10px -10px; }}
                    .title {{ text-align: center; font-size: 10px; font-weight: bold; color: #666; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }}
                    .info {{ font-size: 11px; margin-bottom: 4px; color: #333; }}
                    .info strong {{ color: #003366; }}
                    .footer {{ position: absolute; bottom: 8px; left: 10px; right: 10px; text-align: center; font-size: 8px; color: #999; border-top: 1px solid #ccc; padding-top: 5px; }}
                    .photo-placeholder {{ position: absolute; top: 40px; right: 10px; width: 2cm; height: 2.5cm; border: 1px dashed #ccc; text-align: center; line-height: 2.5cm; font-size: 10px; color: #999; background: #f9f9f9; }}
                    @media print {{
                        body {{ background: white; align-items: flex-start; justify-content: flex-start; }}
                        .card {{ box-shadow: none; border: 1px solid #000; }}
                        @page {{ margin: 0; size: auto; }}
                    }}
                </style>
                </head>
                <body>
                    <div class="card">
                        <div class="header">ISOSED COSMÓPOLIS</div>
                        <div class="title">Credencial de Membro</div>
                        <div class="photo-placeholder">FOTO 3x4</div>
                        <div class="info"><strong>Nome:</strong> {nome}</div>
                        <div class="info"><strong>Cargo:</strong> {cargo}</div>
                        <div class="info"><strong>CPF:</strong> {cpf}</div>
                        <div class="info"><strong>Nasc:</strong> {data_nasc}</div>
                        <div class="info"><strong>Batismo:</strong> {data_batismo}</div>
                        <div class="footer">Documento de uso interno - Validade Indeterminada</div>
                    </div>
                    <script>
                        window.onload = function() {{ window.print(); }}
                    </script>
                </body>
                </html>
                """
                
                # Layout dos botões finais
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    # Botão para baixar a carteirinha gerada
                    st.download_button(
                        label="🪪 GERAR CARTEIRINHA PARA IMPRESSÃO",
                        data=html_carteirinha,
                        file_name=f"Carteirinha_{nome.replace(' ', '_')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                    
                with btn_col2:
                    if "Link Ficha" in df_f.columns and str(row.get('Link Ficha')).startswith("http"):
                        st.markdown(f'<a href="{row["Link Ficha"]}" target="_blank" class="pdf-button" style="margin-top:0;">📄 ABRIR FICHA LGPD</a>', unsafe_allow_html=True)
                    else:
                        st.info("ℹ️ Ficha LGPD não vinculada.")

    else:
        st.warning("Nenhum membro encontrado com os filtros atuais.")
else:
    st.error("⚠️ Erro: Não foi possível carregar a base de dados.")

st.markdown("---")
st.caption("ISOSED Cosmópolis - Sistema em conformidade com a Lei 13.709/2018 (LGPD)")import streamlit as st
import pandas as pd

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

st.markdown('<div class="header-box"><h2>🔍 CONSULTA DE MEMBROS</h2><p>Ficha completa, prontuário digital e emissão de credenciais</p></div>', unsafe_allow_html=True)

if st.button("⬅️ VOLTAR AO MENU PRINCIPAL"):
    st.switch_page("app.py")

st.divider()

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jtaWUZGAlDcCNctxIOyFaTUJ-Bt73L1WiVXxsBHqmas/edit?gid=0#gid=0"

def obter_link_csv(url):
    if "/edit" in url:
        return url.split("/edit")[0] + "/export?format=csv"
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
    
    # 2. BUSCA DIRETA POR NOME
    st.subheader("🔍 Localizar Membro")
    busca = st.text_input("Pesquisar por nome ou sobrenome:", placeholder="Ex: João Silva")
    
    df_f = df.copy()
    
    if busca and "Nome" in df_f.columns:
        df_f = df_f[df_f['Nome'].astype(str).str.contains(busca, case=False, na=False)]

    st.divider()

    # 3. EXIBIÇÃO DOS DADOS
    if not df_f.empty:
        st.success(f"Encontrado(s) {len(df_f)} registro(s):")
        
        for i, row in df_f.iterrows():
            nome = row.get("Nome", "Sem Nome")
            cargo = row.get("Cargo", "Membro")
            cpf = row.get('CPF', '')
            data_nasc = row.get('Data Nascimento', '')
            data_batismo = row.get('Data Batismo', '')
            
            with st.expander(f"👤 {nome} - {cargo}"):
                
                # --- DADOS DA FICHA ---
                st.markdown('<div class="section-title">📋 Dados Pessoais</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                c1.write(f"**🚻 Sexo:** {row.get('Sexo', '')}")
                c1.write(f"**🎂 Nascimento:** {data_nasc} ({row.get('Local Nascimento', '')})")
                c1.write(f"**🪪 CPF:** {cpf}")
                
                c2.write(f"**💍 Estado Civil:** {row.get('Estado Civil', '')}")
                conjuge = row.get("Cônjuge", "")
                if conjuge: c2.write(f"**👩‍❤️‍👨 Cônjuge:** {conjuge}")
                c2.write(f"**💼 Profissão:** {row.get('Profissão', '')}")

                st.markdown('<div class="section-title">⛪ Informações Eclesiásticas & Contato</div>', unsafe_allow_html=True)
                c3, c4 = st.columns(2)
                c3.write(f"**🕊️ Batismo:** {data_batismo}")
                c3.write(f"**🛡️ Cargo(s):** {cargo}")
                
                c4.write(f"**📞 WhatsApp:** {row.get('Contato', '')}")
                dizimista = row.get("Dizimista", "")
                c4.write(f"**💰 Dizimista:** {'💎 Sim' if dizimista == 'Sim' else '⚪ Não'}")

                st.markdown('<div class="section-title">📍 Endereço</div>', unsafe_allow_html=True)
                st.write(f"🏠 {row.get('Rua', '')}, {row.get('Nº', '')} - {row.get('Bairro', '')} | **CEP:** {row.get('CEP', '')}")

                st.markdown('<div class="section-title">🔒 Sistema & Documentos</div>', unsafe_allow_html=True)
                
                # --- GERADOR DE CARTEIRINHA EM HTML ---
                html_carteirinha = f"""
                <!DOCTYPE html>
                <html>
                <head>
                <meta charset="UTF-8">
                <title>Carteirinha - {nome}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f0f0f0; margin: 0; }}
                    .card {{ width: 8.6cm; height: 5.4cm; background: white; border-radius: 8px; border: 2px solid #003366; padding: 10px; box-sizing: border-box; position: relative; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
                    .header {{ background: #003366; color: white; text-align: center; padding: 5px; border-radius: 4px 4px 0 0; font-weight: bold; font-size: 14px; margin: -10px -10px 10px -10px; }}
                    .title {{ text-align: center; font-size: 10px; font-weight: bold; color: #666; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }}
                    .info {{ font-size: 11px; margin-bottom: 4px; color: #333; }}
                    .info strong {{ color: #003366; }}
                    .footer {{ position: absolute; bottom: 8px; left: 10px; right: 10px; text-align: center; font-size: 8px; color: #999; border-top: 1px solid #ccc; padding-top: 5px; }}
                    .photo-placeholder {{ position: absolute; top: 40px; right: 10px; width: 2cm; height: 2.5cm; border: 1px dashed #ccc; text-align: center; line-height: 2.5cm; font-size: 10px; color: #999; background: #f9f9f9; }}
                    @media print {{
                        body {{ background: white; align-items: flex-start; justify-content: flex-start; }}
                        .card {{ box-shadow: none; border: 1px solid #000; }}
                        @page {{ margin: 0; size: auto; }}
                    }}
                </style>
                </head>
                <body>
                    <div class="card">
                        <div class="header">ISOSED COSMÓPOLIS</div>
                        <div class="title">Credencial de Membro</div>
                        <div class="photo-placeholder">FOTO 3x4</div>
                        <div class="info"><strong>Nome:</strong> {nome}</div>
                        <div class="info"><strong>Cargo:</strong> {cargo}</div>
                        <div class="info"><strong>CPF:</strong> {cpf}</div>
                        <div class="info"><strong>Nasc:</strong> {data_nasc}</div>
                        <div class="info"><strong>Batismo:</strong> {data_batismo}</div>
                        <div class="footer">Documento de uso interno - Validade Indeterminada</div>
                    </div>
                    <script>
                        window.onload = function() {{ window.print(); }}
                    </script>
                </body>
                </html>
                """
                
                # Layout dos botões finais
                btn_col1, btn_col2 = st.columns(2)
                
                with btn_col1:
                    st.download_button(
                        label="🪪 GERAR CARTEIRINHA PARA IMPRESSÃO",
                        data=html_carteirinha,
                        file_name=f"Carteirinha_{nome.replace(' ', '_')}.html",
                        mime="text/html",
                        use_container_width=True
                    )
                    
                with btn_col2:
                    if "Link Ficha" in df_f.columns and str(row.get('Link Ficha')).startswith("http"):
                        st.markdown(f'<a href="{row["Link Ficha"]}" target="_blank" class="pdf-button" style="margin-top:0;">📄 ABRIR FICHA LGPD</a>', unsafe_allow_html=True)
                    else:
                        st.info("ℹ️ Ficha LGPD não vinculada.")

    else:
        # Só exibe o aviso se a pessoa de fato tentou buscar alguma coisa
        if busca:
            st.warning("Nenhum membro encontrado com este nome.")
        else:
            st.info("👆 Digite o nome do membro acima para visualizar a ficha e gerar a carteirinha.")
else:
    st.error("⚠️ Erro: Não foi possível carregar a base de dados.")

st.markdown("---")
st.caption("ISOSED Cosmópolis - Sistema em conformidade com a Lei 13.709/2018 (LGPD)")
st.caption("Desenvolvido por Comunicando Igrejas")
