import streamlit as st
import pandas as pd
import graficos
import motor

def avaliar_desvio_3bet(real, meta):
    desvio = real - meta
    if abs(desvio) <= 1.5: return "🟢 Sólido", "Agressividade bem calibrada."
    elif desvio < -1.5: return "🟡 Passivo", "Aumente o range de 3-Bet bluff."
    else: return "🔴 Over-Aggressive", "Estreite o range para não ser explorado."

def renderizar(df_banco, ano_sel_global, anos_disp, metas_globais):
    c_titulo, c_ano = st.columns([5, 2])
    c_titulo.title("4️⃣ Dinâmica e Reação de 3-Bet")
    c_titulo.markdown("Agressividade em potes aumentados: Frequência de 3Bet, Fold para 3Bet e 4Bet.")
    ano_aba = c_ano.selectbox("📅 Selecione o Ano:", anos_disp, index=anos_disp.index(ano_sel_global) if ano_sel_global in anos_disp else 0, key="3b_ano_local")
    df_ano = df_banco[df_banco['Ano'] == ano_aba]
    st.markdown("---")

    df_geral = df_ano[df_ano['Mes'] == 'Geral']
    vol_anual = int(df_geral['Total_Maos_Mes'].iloc[0]) if not df_geral.empty else 0
    media_3b_anual = df_geral['3Bet'].mean() if not df_geral.empty else 0.0
    
    # --- 1. RELATÓRIO ANUAL CONSOLIDADO ---
    c_tit_anual, c_vol_anual, c_3b_anual = st.columns([2, 1, 1])
    c_tit_anual.subheader(f"📈 Relatório Anual Consolidado ({ano_aba})")
    c_vol_anual.info(f"📊 Volume: {vol_anual:,} mãos", icon="🧮")
    c_3b_anual.info(f"🔥 Média 3-Bet: {media_3b_anual:.1f}%", icon="🎯")
    
    tab_3b_ano = []
    val_real_geral, val_meta_geral = [], []
    if not df_geral.empty:
        for p in motor.POSICOES:
            linha = df_geral[df_geral['Posicao'] == p]
            v = int(linha['Total_Hands'].iloc[0]) if not linha.empty else 0
            t3b = float(linha['3Bet'].iloc[0]) if not linha.empty else 0.0
            m_3b = metas_globais.get(f'3Bet_{p}', 10.0) # Puxa a meta posicional
            
            val_real_geral.append(t3b)
            val_meta_geral.append(m_3b)
            
            st_3b, obs_3b = avaliar_desvio_3bet(t3b, m_3b)
            tab_3b_ano.append({"Posição": p, "Volume": f"{v:,}", "3-Bet Real": f"{t3b:.1f}%", "Meta Ideal": f"{m_3b:.1f}%", "Desvio": f"{t3b-m_3b:+.1f}%", "Avaliação": st_3b, "Orientação": obs_3b})
            
        st.plotly_chart(graficos.desenhar_grafico_stat_vs_meta(motor.POSICOES, val_real_geral, val_meta_geral, '3-Bet', 'Geral', ano_aba), use_container_width=True)
        st.dataframe(pd.DataFrame(tab_3b_ano), use_container_width=True, hide_index=True)

    st.markdown("---")
    
    # --- 2. INSPEÇÃO MENSAL ---
    st.subheader("📆 Inspeção Mensal Detalhada")
    meses_disp = [m for m in motor.ORDEM_MESES_PADRAO if m in df_ano[df_ano['Mes'] != 'Geral']['Mes'].unique().tolist()]
    if meses_disp:
        mes_sel = st.selectbox("Selecione o Mês:", meses_disp, key="3b_mes")
        df_mes = df_ano[df_ano['Mes'] == mes_sel]
        vol_mensal = int(df_mes['Total_Maos_Mes'].iloc[0]) if not df_mes.empty else 0
        media_3b_mensal = df_mes['3Bet'].mean() if not df_mes.empty else 0.0
        
        c_inf_mes1, c_inf_mes2 = st.columns([1, 1])
        c_inf_mes1.info(f"📊 Volume do mês: {vol_mensal:,} mãos")
        c_inf_mes2.info(f"🔥 Média 3-Bet do mês: {media_3b_mensal:.1f}%")
        
        v_real, v_meta, tab_3b_mes = [], [], []
        for p in motor.POSICOES:
            linha = df_mes[df_mes['Posicao'] == p]
            v = int(linha['Total_Hands'].iloc[0]) if not linha.empty else 0
            r = float(linha['3Bet'].iloc[0]) if not linha.empty else 0.0
            m = metas_globais.get(f'3Bet_{p}', 10.0) # Puxa a meta posicional
            
            v_real.append(r); v_meta.append(m)
            st_3b, obs_3b = avaliar_desvio_3bet(r, m)
            tab_3b_mes.append({"Posição": p, "Volume": f"{v:,}", "3-Bet Real": f"{r:.1f}%", "Meta Ideal": f"{m:.1f}%", "Desvio": f"{r-m:+.1f}%", "Avaliação": st_3b, "Orientação": obs_3b})
            
        st.plotly_chart(graficos.desenhar_grafico_stat_vs_meta(motor.POSICOES, v_real, v_meta, '3-Bet', mes_sel, ano_aba), use_container_width=True)
        st.dataframe(pd.DataFrame(tab_3b_mes), use_container_width=True, hide_index=True)

    # --- 3. PROGRESSÃO ANUAL ---
    st.markdown("---")
    st.subheader("📊 Relatório de Progressão Anual (Evolução do 3-Bet)")
    st.plotly_chart(graficos.desenhar_grafico_anual_agrupado(df_ano, metas_globais, motor.POSICOES, '3Bet', '3Bet_', "Progressão Mensal de 3-Bet vs Meta"), use_container_width=True)