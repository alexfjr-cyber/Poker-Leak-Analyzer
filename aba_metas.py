import streamlit as st

def renderizar(metas_globais):
    st.title("⚙️ Configuração de Parâmetros e Metas")
    st.markdown("Defina a base matemática (Target Stats) que o motor usará para diagnosticar o seu jogo. *(As alterações duram até você fechar a aba)*")
    
    with st.form("form_metas_completas"):
        st.subheader("1. Open Raise (RFI %)")
        col1, col2, col3, col4, col5 = st.columns(5)
        n_metas = {}
        n_metas['RFI_EP'] = col1.number_input("EP", value=float(metas_globais.get('RFI_EP', 18.0)))
        n_metas['RFI_MP'] = col2.number_input("MP", value=float(metas_globais.get('RFI_MP', 24.0)))
        n_metas['RFI_CO'] = col3.number_input("CO", value=float(metas_globais.get('RFI_CO', 30.0)))
        n_metas['RFI_BU'] = col4.number_input("BU", value=float(metas_globais.get('RFI_BU', 50.0)))
        n_metas['RFI_SB'] = col5.number_input("SB", value=float(metas_globais.get('RFI_SB', 45.0)))
        
        st.markdown("---")
        st.subheader("2. Frequência de 3-Bet por Posição (%)")
        t1, t2, t3, t4, t5, t6 = st.columns(6)
        n_metas['3Bet_EP'] = t1.number_input("3Bet EP", value=float(metas_globais.get('3Bet_EP', 6.0)))
        n_metas['3Bet_MP'] = t2.number_input("3Bet MP", value=float(metas_globais.get('3Bet_MP', 8.0)))
        n_metas['3Bet_CO'] = t3.number_input("3Bet CO", value=float(metas_globais.get('3Bet_CO', 10.0)))
        n_metas['3Bet_BU'] = t4.number_input("3Bet BU", value=float(metas_globais.get('3Bet_BU', 12.0)))
        n_metas['3Bet_SB'] = t5.number_input("3Bet SB", value=float(metas_globais.get('3Bet_SB', 14.0)))
        n_metas['3Bet_BB'] = t6.number_input("3Bet BB", value=float(metas_globais.get('3Bet_BB', 11.0)))

        st.markdown("---")
        st.subheader("3. Frequências Gerais e Defesas")
        col6, col7, col8, col9, col10 = st.columns(5)
        n_metas['VPIP'] = col6.number_input("VPIP (%)", value=float(metas_globais.get('VPIP', 25.0)))
        n_metas['PFR'] = col7.number_input("PFR (%)", value=float(metas_globais.get('PFR', 20.0)))
        n_metas['FoldTo3Bet'] = col8.number_input("Fold vs 3-Bet (%)", value=float(metas_globais.get('FoldTo3Bet', 50.0)))
        n_metas['FourBet'] = col9.number_input("4-Bet (%)", value=float(metas_globais.get('FourBet', 12.0)))
        n_metas['FoldTo4Bet'] = col10.number_input("Fold vs 4-Bet (%)", value=float(metas_globais.get('FoldTo4Bet', 55.0)))

        st.markdown("---")
        st.subheader("4. Guerra de Blinds e Pós-Flop")
        cb1, cb2, cb3, cb4 = st.columns(4)
        n_metas['BB_Fold_Steal'] = cb1.number_input("BB Fold vs Steal", value=float(metas_globais.get('BB_Fold_Steal', 55.0)))
        n_metas['BB_3Bet_Steal'] = cb2.number_input("BB 3-Bet vs Steal", value=float(metas_globais.get('BB_3Bet_Steal', 14.0)))
        n_metas['SB_Steal'] = cb3.number_input("SB Steal", value=float(metas_globais.get('SB_Steal', 50.0)))
        n_metas['BB_Defend_SB_Steal'] = cb4.number_input("BB Defend vs SB", value=float(metas_globais.get('BB_Defend_SB_Steal', 40.0)))
        
        cp1, cp2, cp3, cp4, cp5 = st.columns(5)
        n_metas['CBetFlop'] = cp1.number_input("C-Bet Flop Geral", value=float(metas_globais.get('CBetFlop', 60.0)))
        n_metas['CBetFlopIP'] = cp2.number_input("C-Bet Flop (IP)", value=float(metas_globais.get('CBetFlopIP', 65.0)))
        n_metas['CBetFlopOOP'] = cp3.number_input("C-Bet Flop (OOP)", value=float(metas_globais.get('CBetFlopOOP', 45.0)))
        n_metas['CheckRaiseFlop'] = cp4.number_input("Check-Raise Flop", value=float(metas_globais.get('CheckRaiseFlop', 12.0)))
        n_metas['BetFlopSkippedCBet'] = cp5.number_input("Bet vs Missed CBet", value=float(metas_globais.get('BetFlopSkippedCBet', 45.0)))

        cw1, cw2, cw3 = st.columns(3)
        n_metas['Agg'] = cw1.number_input("Fator de Agressão (Agg)", value=float(metas_globais.get('Agg', 2.5)))
        n_metas['WTSD'] = cw2.number_input("WTSD (%)", value=float(metas_globais.get('WTSD', 30.0)))
        n_metas['WSD'] = cw3.number_input("W$SD (%)", value=float(metas_globais.get('WSD', 52.0)))

        if st.form_submit_button("💾 Salvar Banco de Metas", type="primary"):
            st.session_state['metas_globais'] = n_metas
            st.success("Configurações atualizadas para a sua sessão!")
            st.rerun()