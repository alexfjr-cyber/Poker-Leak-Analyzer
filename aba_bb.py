import streamlit as st
import pandas as pd
import graficos
import motor

def avaliar_bb_defense(real, meta, tipo):
    desvio = real - meta
    if tipo == 'fold':
        if abs(desvio) <= 4.0: return "🟢 Sólido", "Defesa sólida."
        elif desvio > 4.0: return "🔴 Over-Fold", "Alvo fácil para roubos. Pague ou 3-Bete mais."
        else: return "🟡 Station", "Defendendo muito OOP. Reduza calls."
    elif tipo == '3bet':
        if abs(desvio) <= 2.0: return "🟢 Sólido", "Frequência de Re-steal correta."
        elif desvio < -2.0: return "🟡 Passivo", "Você está flat-callando muito do BB. Aumente re-steals."
        else: return "🔴 Agressivo Demais", "Frequência alta de 3Bet do BB."

def renderizar(df_banco, ano_sel_global, anos_disp, metas_globais):
    c_titulo, c_ano = st.columns([5, 2])
    c_titulo.title("3️⃣ Defesa do Big Blind & Blind War")
    c_titulo.markdown("Proteção do seu investimento obrigatório. Avaliação de Fold vs Steal e Re-steals.")
    ano_aba = c_ano.selectbox("📅 Selecione o Ano:", anos_disp, index=anos_disp.index(ano_sel_global) if ano_sel_global in anos_disp else 0, key="bb_ano_local")
    df_ano = df_banco[df_banco['Ano'] == ano_aba]
    st.markdown("---")

    df_geral = df_ano[df_ano['Mes'] == 'Geral']
    linha_bb_geral = df_geral[df_geral['Posicao'] == 'BB']
    
    vol_bb_anual = int(linha_bb_geral['Total_Hands'].iloc[0]) if not linha_bb_geral.empty else 0
    
    # --- 1. RELATÓRIO ANUAL ---
    c_tit_anual, c_vol_anual = st.columns([3, 1])
    c_tit_anual.subheader(f"📈 Relatório Anual Consolidado ({ano_aba})")
    c_vol_anual.info(f"📊 Volume no BB: {vol_bb_anual:,} mãos", icon="🧮")

    st.plotly_chart(graficos.desenhar_evolucao_anual(df_ano, 'BB_Fold_Steal', "Evolução do BB Fold vs Steal (%)"), use_container_width=True)

    tab_bb_ano = []
    if not linha_bb_geral.empty:
        f_steal = float(linha_bb_geral['BB_Fold_Steal'].iloc[0])
        r_steal = float(linha_bb_geral['BB_Reraise_Steal'].iloc[0])
        m_fs = metas_globais.get('BB_Fold_Steal', 55.0)
        m_rs = metas_globais.get('BB_3Bet_Steal', 14.0)
        
        st_fs, obs_fs = avaliar_bb_defense(f_steal, m_fs, 'fold')
        st_rs, obs_rs = avaliar_bb_defense(r_steal, m_rs, '3bet')
        
        tab_bb_ano.append({"Ação": "Fold vs Steal", "Real": f"{f_steal:.1f}%", "Meta Ideal": f"{m_fs:.1f}%", "Desvio": f"{f_steal-m_fs:+.1f}%", "Avaliação": st_fs, "Orientação": obs_fs})
        tab_bb_ano.append({"Ação": "3-Bet vs Steal (Re-Steal)", "Real": f"{r_steal:.1f}%", "Meta Ideal": f"{m_rs:.1f}%", "Desvio": f"{r_steal-m_rs:+.1f}%", "Avaliação": st_rs, "Orientação": obs_rs})
        st.dataframe(pd.DataFrame(tab_bb_ano), use_container_width=True, hide_index=True)

    st.markdown("---")
    
    # --- 2. INSPEÇÃO MENSAL ---
    st.subheader("📆 Inspeção Mensal Detalhada")
    meses_disp = [m for m in motor.ORDEM_MESES_PADRAO if m in df_ano[df_ano['Mes'] != 'Geral']['Mes'].unique().tolist()]
    if meses_disp:
        mes_sel = st.selectbox("Selecione o Mês:", meses_disp, key="bb_mes")
        df_mes = df_ano[df_ano['Mes'] == mes_sel]
        linha_bb_mes = df_mes[df_mes['Posicao'] == 'BB']
        
        vol_bb_mensal = int(linha_bb_mes['Total_Hands'].iloc[0]) if not linha_bb_mes.empty else 0
        st.info(f"📊 Volume do mês no BB: {vol_bb_mensal:,} mãos")

        tab_bb_mes = []
        if not linha_bb_mes.empty:
            f_steal = float(linha_bb_mes['BB_Fold_Steal'].iloc[0])
            r_steal = float(linha_bb_mes['BB_Reraise_Steal'].iloc[0])
            m_fs = metas_globais.get('BB_Fold_Steal', 55.0)
            m_rs = metas_globais.get('BB_3Bet_Steal', 14.0)
            
            st_fs, obs_fs = avaliar_bb_defense(f_steal, m_fs, 'fold')
            st_rs, obs_rs = avaliar_bb_defense(r_steal, m_rs, '3bet')
            
            tab_bb_mes.append({"Ação": "Fold vs Steal", "Real": f"{f_steal:.1f}%", "Meta Ideal": f"{m_fs:.1f}%", "Desvio": f"{f_steal-m_fs:+.1f}%", "Avaliação": st_fs, "Orientação": obs_fs})
            tab_bb_mes.append({"Ação": "3-Bet vs Steal (Re-Steal)", "Real": f"{r_steal:.1f}%", "Meta Ideal": f"{m_rs:.1f}%", "Desvio": f"{r_steal-m_rs:+.1f}%", "Avaliação": st_rs, "Orientação": obs_rs})
            st.dataframe(pd.DataFrame(tab_bb_mes), use_container_width=True, hide_index=True)