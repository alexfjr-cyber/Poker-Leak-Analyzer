import streamlit as st
import pandas as pd
import graficos
import motor

def avaliar_desvio_rfi(desvio, posicao):
    """Gera o status e a observação de estudo baseado na diferença da meta."""
    if abs(desvio) <= 2.0: return "🟢 Sólido", "Frequência calibrada. Mantenha os ranges atuais."
    elif abs(desvio) <= 4.0: return "🟡 Atenção", f"{'Amplie' if desvio < 0 else 'Reduza'} marginalmente as mãos de abertura."
    else: return "🔴 Leak Grave", f"{'Abra mais mãos' if desvio < 0 else 'Corte as mãos fracas'}. Desvio compromete o pós-flop."

def renderizar(df_banco, ano_sel, anos_disp, metas_globais):
    c_titulo, c_ano = st.columns([5, 2])
    c_titulo.title("1️⃣ Open Raise (RFI)")
    c_titulo.markdown("O fundamento do poker. Jogue as mãos certas nas posições certas.")
    
    # Se o ano selecionado no menu global mudar, este selectbox acompanha
    ano_aba = c_ano.selectbox("📅 Selecione o Ano:", anos_disp, index=anos_disp.index(ano_sel) if ano_sel in anos_disp else 0, key="rfi_ano_local")
        
    df_ano = df_banco[df_banco['Ano'] == ano_aba]
    df_geral = df_ano[df_ano['Mes'] == 'Geral']
    vol_anual = int(df_geral['Total_Maos_Mes'].iloc[0]) if not df_geral.empty else int(df_ano['Total_Hands'].sum())
    st.markdown("---")

    # --- 1. RELATÓRIO ANUAL CONSOLIDADO ---
    c_tit_anual, c_vol_anual = st.columns([3, 1])
    c_tit_anual.subheader(f"📈 Relatório Anual Consolidado ({ano_aba})")
    c_vol_anual.info(f"📊 Volume: {vol_anual:,} mãos", icon="🧮")

    tabela_anual = []
    val_real_geral, val_meta_geral = [], []
    if not df_geral.empty:
        for p in ['EP', 'MP', 'CO', 'BU', 'SB']:
            linha = df_geral[df_geral['Posicao'] == p]
            v = int(linha['Total_Hands'].iloc[0]) if not linha.empty else 0
            r = float(linha['RFI'].iloc[0]) if not linha.empty else 0.0
            m = metas_globais.get(f'RFI_{p}', 0.0)
            
            val_real_geral.append(r)
            val_meta_geral.append(m)
            
            st_badge, obs = avaliar_desvio_rfi(r - m, p)
            tabela_anual.append({"Posição": p, "Volume": f"{v:,}", "RFI Real": f"{r:.1f}%", "Meta Ideal": f"{m:.1f}%", "Desvio": f"{r-m:+.1f}%", "Avaliação": st_badge, "Orientação": obs})
        
        st.plotly_chart(graficos.desenhar_grafico_stat_vs_meta(['EP', 'MP', 'CO', 'BU', 'SB'], val_real_geral, val_meta_geral, 'RFI', 'Geral (Ano)', ano_aba), use_container_width=True)
        st.dataframe(pd.DataFrame(tabela_anual), use_container_width=True, hide_index=True)
    else:
        st.info("Arquivo 'geral' anual não encontrado para este ano.")

    st.markdown("---")
    
    # --- 2. INSPEÇÃO MENSAL ---
    st.subheader("📆 Inspeção Mensal Detalhada")
    meses_disp = [m for m in motor.ORDEM_MESES_PADRAO if m in df_ano[df_ano['Mes'] != 'Geral']['Mes'].unique().tolist()]
    
    if meses_disp:
        mes_sel = st.selectbox("Selecione o Mês:", meses_disp, key="rfi_mes")
        df_mes = df_ano[df_ano['Mes'] == mes_sel]
        vol_mensal = int(df_mes['Total_Maos_Mes'].iloc[0]) if not df_mes.empty else 0
        st.caption(f"Volume do mês selecionado: {vol_mensal:,} mãos.")
        
        tab_mes, v_real, v_meta = [], [], []
        for p in ['EP', 'MP', 'CO', 'BU', 'SB']:
            linha = df_mes[df_mes['Posicao'] == p]
            v = int(linha['Total_Hands'].iloc[0]) if not linha.empty else 0
            r = float(linha['RFI'].iloc[0]) if not linha.empty else 0.0
            m = metas_globais.get(f'RFI_{p}', 0.0)
            v_real.append(r); v_meta.append(m)
            st_badge, obs = avaliar_desvio_rfi(r - m, p)
            tab_mes.append({"Posição": p, "Volume": f"{v:,}", "RFI Real": f"{r:.1f}%", "Meta Ideal": f"{m:.1f}%", "Desvio": f"{r-m:+.1f}%", "Avaliação": st_badge, "Orientação": obs})
            
        st.plotly_chart(graficos.desenhar_grafico_stat_vs_meta(['EP', 'MP', 'CO', 'BU', 'SB'], v_real, v_meta, 'RFI', mes_sel, ano_aba), use_container_width=True)
        st.dataframe(pd.DataFrame(tab_mes), use_container_width=True, hide_index=True)

    # --- 3. PROGRESSÃO ANUAL ---
    st.markdown("---")
    st.subheader("📊 Relatório de Progressão Anual")
    st.markdown("Acompanhe a evolução do seu Open Raise mês a mês e avalie a consistência das correções.")
    st.plotly_chart(graficos.desenhar_grafico_anual_agrupado(df_ano, metas_globais, ['EP', 'MP', 'CO', 'BU', 'SB'], 'RFI', 'RFI_', "Progressão Mensal de RFI vs Meta"), use_container_width=True)