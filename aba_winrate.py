import streamlit as st
import pandas as pd
import graficos
import motor

def avaliar_winrate(bb, ev):
    if ev > 5.0: st_badge = "🟢 Crusher"
    elif ev > 0.0: st_badge = "🟡 Lucrativo"
    else: st_badge = "🔴 Perdedor"
    
    if ev > bb + 1.5: obs = "Jogou bem, mas sofreu com azar (Bad Run)."
    elif bb > ev + 1.5: obs = "Lucro inflado por variância positiva (Sorte)."
    else: obs = "Resultados alinhados à matemática."
    
    if ev <= 0: obs = "Ajustes técnicos urgentes. EV negativo."
    return st_badge, obs

def renderizar(df_banco, ano_sel_global, anos_disp):
    c_titulo, c_ano = st.columns([5, 2])
    c_titulo.title("🏠 Mapa de Lucratividade (Winrate)")
    c_titulo.markdown("A verdadeira métrica de habilidade: EV bb/100 (Teórico) cruzado com o seu bb/100 (Real).")
    
    ano_aba = c_ano.selectbox("📅 Selecione o Ano:", anos_disp, index=anos_disp.index(ano_sel_global) if ano_sel_global in anos_disp else 0, key="win_ano_local")
    df_ano = df_banco[df_banco['Ano'] == ano_aba]
    st.markdown("---")

    df_geral = df_ano[df_ano['Mes'] == 'Geral']
    
    # --- 1. RELATÓRIO ANUAL ---
    vol_anual = int(df_geral['Total_Maos_Mes'].iloc[0]) if not df_geral.empty else 0
    c_tit_anual, c_vol_anual = st.columns([3, 1])
    c_tit_anual.subheader(f"📈 Relatório Anual Consolidado ({ano_aba})")
    c_vol_anual.info(f"📊 Volume Total: {vol_anual:,} mãos", icon="🧮")
    
    posicoes_calc = motor.POSICOES + ['Geral (Média)']
    bb_anual_lista, ev_anual_lista, tab_win_anual = [], [], []
    
    if not df_geral.empty:
        soma_bb, soma_ev, soma_vol = 0, 0, 0
        for p in motor.POSICOES:
            linha = df_geral[df_geral['Posicao'] == p]
            v = int(linha['Total_Hands'].iloc[0]) if not linha.empty else 0
            bb = float(linha['Bb100'].iloc[0]) if not linha.empty else 0.0
            ev = float(linha['EvBb100'].iloc[0]) if not linha.empty else 0.0
            
            soma_bb += (bb * v)
            soma_ev += (ev * v)
            soma_vol += v
            
            bb_anual_lista.append(bb); ev_anual_lista.append(ev)
            st_badge, obs = avaliar_winrate(bb, ev)
            tab_win_anual.append({"Posição": p, "Volume": f"{v:,}", "bb/100 Real": f"{bb:+.1f}", "EV bb/100": f"{ev:+.1f}", "Fator Variância": f"{(bb-ev):+.1f} bb", "Avaliação": st_badge, "Orientação": obs})
            
        bb_medio = soma_bb / soma_vol if soma_vol > 0 else 0
        ev_medio = soma_ev / soma_vol if soma_vol > 0 else 0
        bb_anual_lista.append(bb_medio); ev_anual_lista.append(ev_medio)
        st_badge, obs = avaliar_winrate(bb_medio, ev_medio)
        tab_win_anual.append({"Posição": "Geral (Média)", "Volume": f"{soma_vol:,}", "bb/100 Real": f"{bb_medio:+.1f}", "EV bb/100": f"{ev_medio:+.1f}", "Fator Variância": f"{(bb_medio-ev_medio):+.1f} bb", "Avaliação": st_badge, "Orientação": obs})

        st.plotly_chart(graficos.desenhar_grafico_winrate_pareado(posicoes_calc, bb_anual_lista, ev_anual_lista, "Lucratividade por Posição (Ano)"), use_container_width=True)
        st.dataframe(pd.DataFrame(tab_win_anual), use_container_width=True, hide_index=True)

    st.markdown("---")
    
    # --- 2. PROGRESSÃO MENSAL ---
    st.subheader("📊 Relatório de Progressão Anual (Winrate Médio Geral)")
    meses_disp = [m for m in motor.ORDEM_MESES_PADRAO if m in df_ano[df_ano['Mes'] != 'Geral']['Mes'].unique().tolist()]
    if meses_disp:
        bb_meses, ev_meses = [], []
        for m in meses_disp:
            df_m = df_ano[df_ano['Mes'] == m]
            v_total = df_m['Total_Hands'].sum()
            bb_m = (df_m['Bb100'] * df_m['Total_Hands']).sum() / v_total if v_total > 0 else 0
            ev_m = (df_m['EvBb100'] * df_m['Total_Hands']).sum() / v_total if v_total > 0 else 0
            bb_meses.append(bb_m); ev_meses.append(ev_m)
            
        st.plotly_chart(graficos.desenhar_grafico_winrate_pareado(meses_disp, bb_meses, ev_meses, "Média de Lucratividade Mês a Mês"), use_container_width=True)

    st.markdown("---")

    # --- 3. INSPEÇÃO MENSAL ---
    st.subheader("📆 Inspeção Mensal Detalhada por Posição")
    if meses_disp:
        mes_sel = st.selectbox("Selecione o Mês:", meses_disp, key="win_mes")
        df_mes = df_ano[df_ano['Mes'] == mes_sel]
        vol_m = df_mes['Total_Hands'].sum()
        st.caption(f"Volume do mês selecionado: {vol_m:,} mãos.")
        
        bb_m_list, ev_m_list, tab_win_m = [], [], []
        soma_bb, soma_ev = 0, 0
        for p in motor.POSICOES:
            linha = df_mes[df_mes['Posicao'] == p]
            v = int(linha['Total_Hands'].iloc[0]) if not linha.empty else 0
            bb = float(linha['Bb100'].iloc[0]) if not linha.empty else 0.0
            ev = float(linha['EvBb100'].iloc[0]) if not linha.empty else 0.0
            soma_bb += (bb * v); soma_ev += (ev * v)
            
            bb_m_list.append(bb); ev_m_list.append(ev)
            st_badge, obs = avaliar_winrate(bb, ev)
            tab_win_m.append({"Posição": p, "Volume": f"{v:,}", "bb/100 Real": f"{bb:+.1f}", "EV bb/100": f"{ev:+.1f}", "Fator Variância": f"{(bb-ev):+.1f} bb", "Avaliação": st_badge, "Orientação": obs})
        
        bb_medio = soma_bb / vol_m if vol_m > 0 else 0
        ev_medio = soma_ev / vol_m if vol_m > 0 else 0
        bb_m_list.append(bb_medio); ev_m_list.append(ev_medio)
        st_badge, obs = avaliar_winrate(bb_medio, ev_medio)
        tab_win_m.append({"Posição": "Geral (Média)", "Volume": f"{vol_m:,}", "bb/100 Real": f"{bb_medio:+.1f}", "EV bb/100": f"{ev_medio:+.1f}", "Fator Variância": f"{(bb_medio-ev_medio):+.1f} bb", "Avaliação": st_badge, "Orientação": obs})

        st.plotly_chart(graficos.desenhar_grafico_winrate_pareado(posicoes_calc, bb_m_list, ev_m_list, f"Lucratividade em {mes_sel}"), use_container_width=True)
        st.dataframe(pd.DataFrame(tab_win_m), use_container_width=True, hide_index=True)