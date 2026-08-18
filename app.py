import streamlit as st
import pandas as pd
import motor

import aba_rfi
import aba_winrate
import aba_3bet
import aba_bb
import aba_metas

st.set_page_config(page_title="High Stakes Analytics", layout="wide", initial_sidebar_state="expanded")

# Inicia a memória virtual da sessão
if 'df_banco' not in st.session_state:
    st.session_state['df_banco'] = pd.DataFrame()
if 'metas_globais' not in st.session_state:
    st.session_state['metas_globais'] = motor.METAS_PADRAO_GLOBAIS.copy()

# -------------------------------------------------------------
# MENU LATERAL & SINCRONIZAÇÃO
# -------------------------------------------------------------
st.sidebar.title("🃏 Painel de Controle")
st.sidebar.markdown("---")
menu = st.sidebar.radio("Navegação da Trilha:", [
    "🏠 Visão Geral (Winrate)",
    "1️⃣ Open Raise (RFI)",
    "2️⃣ Estratégia Short Stack",
    "3️⃣ Defesa do Big Blind",
    "4️⃣ Dinâmica de 3-Bet",
    "5️⃣ C-Bet Flop IP",
    "6️⃣ BB vs Multi-way",
    "7️⃣ Blind War (SB)",
    "8️⃣ Blind War (BB)",
    "9️⃣ SB vs RFI",
    "🔟 BU vs RFI",
    "⚙️ Configuração de Metas"
])

st.sidebar.markdown("---")
st.sidebar.subheader("📁 Central de Uploads")
st.sidebar.markdown("Selecione seus relatórios mensais e o `geralYYYY.csv`")

arquivos_upados = st.sidebar.file_uploader("Arraste os arquivos CSV aqui", type=['csv'], accept_multiple_files=True)

if st.sidebar.button("⚡ Processar Dados", type="primary", use_container_width=True):
    if arquivos_upados:
        with st.spinner("Analisando mãos..."):
            df_novo, msg = motor.processar_arquivos_upload(arquivos_upados)
            if not df_novo.empty:
                st.session_state['df_banco'] = df_novo
                st.sidebar.success(msg)
            else:
                st.sidebar.error(msg)
    else:
        st.sidebar.warning("Envie os arquivos antes de processar.")

# --- NOVO: BOTÃO DE DOWNLOAD DO TEMPLATE HM2 ---
st.sidebar.markdown("---")
st.sidebar.subheader("🛠️ Instalação (HM2)")
st.sidebar.markdown("Importe este template no seu HM2 para garantir a exportação correta das métricas.")

try:
    with open("ByPosition.Tournament.Report", "rb") as template_file:
        st.sidebar.download_button(
            label="⬇️ Baixar Template HM2",
            data=template_file,
            file_name="ByPosition.Tournament.Report",
            mime="application/octet-stream",
            use_container_width=True
        )
except FileNotFoundError:
    st.sidebar.warning("Arquivo de template não encontrado no servidor.")
# -----------------------------------------------

df_banco = st.session_state['df_banco']
METAS_GLOBAIS = st.session_state['metas_globais']
if df_banco.empty and menu != "⚙️ Configuração de Metas":
    st.info("👋 **Bem-vindo ao Head Coach Virtual!**")
    st.warning("👈 Envie seus arquivos CSV do Hold'em Manager 2 no menu lateral para gerar os diagnósticos.")
    st.stop()

anos_disp = sorted(df_banco['Ano'].unique().tolist()) if not df_banco.empty else []
ano_sel_global = anos_disp[-1] if anos_disp else None

max_desvio_rfi = 0.0
if not df_banco.empty:
    df_geral_alerta = df_banco[(df_banco['Ano'] == ano_sel_global) & (df_banco['Mes'] == 'Geral')]
    if not df_geral_alerta.empty:
        for p in ['EP', 'MP', 'CO', 'BU', 'SB']:
            linha = df_geral_alerta[df_geral_alerta['Posicao'] == p]
            if not linha.empty:
                diff = abs(float(linha['RFI'].iloc[0]) - METAS_GLOBAIS.get(f'RFI_{p}', 0.0))
                if diff > max_desvio_rfi: max_desvio_rfi = diff

# =============================================================
# ROTEAMENTO DAS ABAS
# =============================================================

if menu == "1️⃣ Open Raise (RFI)":
    aba_rfi.renderizar(df_banco, ano_sel_global, anos_disp, METAS_GLOBAIS)

elif menu == "🏠 Visão Geral (Winrate)":
    aba_winrate.renderizar(df_banco, ano_sel_global, anos_disp)
    
elif menu == "4️⃣ Dinâmica de 3-Bet":
    if max_desvio_rfi > 4.0:
        st.warning(f"🚨 **Alerta do Head Coach:** O seu RFI possui um desvio crítico (>4%). Priorize a aba RFI.")
    aba_3bet.renderizar(df_banco, ano_sel_global, anos_disp, METAS_GLOBAIS)

elif menu == "3️⃣ Defesa do Big Blind":
    if max_desvio_rfi > 4.0:
        st.warning("🚨 **Alerta do Head Coach:** Corrija os vazamentos do seu Open Raise (RFI) antes de focar em blind defense.")
    aba_bb.renderizar(df_banco, ano_sel_global, anos_disp, METAS_GLOBAIS)

elif menu == "⚙️ Configuração de Metas":
    aba_metas.renderizar(METAS_GLOBAIS)

else:
    st.title(menu)
    st.warning("🚧 **Módulo em Construção** 🚧")
    st.markdown("Esta fase está mapeada na arquitetura do sistema e será desenvolvida em breve.")
