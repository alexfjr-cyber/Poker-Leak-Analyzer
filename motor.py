import pandas as pd

POSICOES = ['SB', 'BB', 'EP', 'MP', 'CO', 'BU']
ORDEM_MESES_PADRAO = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro', 'Geral']
MAPA_MESES = {'01': 'Janeiro', '02': 'Fevereiro', '03': 'Março', '04': 'Abril', '05': 'Maio', '06': 'Junho', '07': 'Julho', '08': 'Agosto', '09': 'Setembro', '10': 'Outubro', '11': 'Novembro', '12': 'Dezembro'}

# 🔥 DIGITE AQUI O SEU PADRÃO ATUALIZADO ANTES DE IR PARA A NUVEM
METAS_PADRAO_GLOBAIS = {
    'RFI_EP': 18.0, 'RFI_MP': 23.0, 'RFI_CO': 33.0, 'RFI_BU': 50.0, 'RFI_SB': 50.0,
    '3Bet_EP': 5.5, '3Bet_MP': 7.0, '3Bet_CO': 8.0, '3Bet_BU': 11.0, '3Bet_SB': 13.0, '3Bet_BB': 15.0,
    'VPIP': 25.0, 'PFR': 22.0,
    'FoldTo3Bet': 50.0, 'FourBet': 12.0, 'FoldTo4Bet': 50.0, '3Bet': 10.0,
    'BB_Fold_Steal': 35.0, 'BB_3Bet_Steal': 14.0, 'SB_Steal': 60.0,
    'BB_Defend_SB_Steal': 60.0, 'BB_Raise_SB_Steal': 15.0,
    'CBetFlop': 60.0, 'CBetFlopIP': 65.0, 'CBetFlopOOP': 40.0,
    'CheckRaiseFlop': 13.5, 'BetFlopSkippedCBet': 70.0,
    'Agg': 2.5, 'WTSD': 30.0, 'WSD': 52.0
}

def ler_valor_seguro(linha, colunas_possiveis):
    if isinstance(colunas_possiveis, str): colunas_possiveis = [colunas_possiveis]
    for col in colunas_possiveis:
        if col in linha.columns:
            try:
                val = linha[col].iloc[0]
                if pd.isna(val) or str(val).strip().lower() == 'na': continue
                if isinstance(val, str): val = val.replace(',', '.')
                return float(val)
            except Exception:
                continue
    return 0.0

def processar_arquivos_upload(arquivos_upados):
    """Processa os arquivos CSV diretamente da memória do navegador."""
    if not arquivos_upados:
        return pd.DataFrame(), "Nenhum arquivo enviado."
    
    novas_linhas = []
    try:
        for arquivo in arquivos_upados:
            nome_base = arquivo.name
            if nome_base.lower().startswith('geral'):
                ano = int(nome_base[5:9])
                mes = "Geral"
            else:
                ano = int(nome_base[:4])
                mes = MAPA_MESES.get(nome_base[4:6])
            
            if not mes: continue

            df_csv = pd.read_csv(arquivo, sep=',', decimal=',', na_values=['na', 'NaN', ''])
            df_csv.columns = [c.strip() for c in df_csv.columns]
            df_csv['Position'] = df_csv['Position'].replace({'BTN': 'BU'})
            total_maos_mes = int(df_csv['Total Hands'].sum()) if 'Total Hands' in df_csv.columns else 0

            for p in POSICOES:
                linha_pos = df_csv[df_csv['Position'] == p]
                if not linha_pos.empty:
                    f3b_ip = ler_valor_seguro(linha_pos, 'TOT Fold to IP 3Bet')
                    f3b_blinds = ler_valor_seguro(linha_pos, 'TOT Fold to Blinds 3Bet')
                    f3b_sb = ler_valor_seguro(linha_pos, 'Small Blind Fold to 3Bet')
                    folds_validos = [f for f in [f3b_ip, f3b_blinds, f3b_sb] if f > 0]
                    fold_3b_final = sum(folds_validos) / len(folds_validos) if folds_validos else 0.0

                    novas_linhas.append({
                        'Ano': ano, 'Mes': mes, 'Posicao': p, 
                        'Total_Hands': int(ler_valor_seguro(linha_pos, 'Total Hands')),
                        'VPIP': ler_valor_seguro(linha_pos, 'VPIP'), 'PFR': ler_valor_seguro(linha_pos, 'PFR'),
                        'RFI': ler_valor_seguro(linha_pos, 'UO PFR%'), '3Bet': ler_valor_seguro(linha_pos, '3Bet'),
                        'FoldTo3Bet': fold_3b_final,
                        'FourBet': ler_valor_seguro(linha_pos, 'vs 3Bet Raise%'),
                        'FoldTo4Bet': ler_valor_seguro(linha_pos, 'vs 4Bet Fold%'),
                        'Bb100': ler_valor_seguro(linha_pos, 'bb/100'), 'EvBb100': ler_valor_seguro(linha_pos, 'EV bb/100'),
                        'CBetFlop': ler_valor_seguro(linha_pos, 'Flop CBet%'),
                        'CBetFlopIP': ler_valor_seguro(linha_pos, 'Flop CBet IP%'), 'CBetFlopOOP': ler_valor_seguro(linha_pos, 'Flop CBet OOP%'),
                        'CheckRaiseFlop': ler_valor_seguro(linha_pos, 'Check Raise Flop%'),
                        'BetFlopSkippedCBet': ler_valor_seguro(linha_pos, 'Bet Flop vs Skipped CBet'),
                        'Agg': ler_valor_seguro(linha_pos, 'Agg'), 'WTSD': ler_valor_seguro(linha_pos, 'WTSD%'), 'WSD': ler_valor_seguro(linha_pos, 'W$SD%'),
                        'BB_Reraise_Steal': ler_valor_seguro(linha_pos, 'BB Reraise Steal'), 'BB_Fold_Steal': ler_valor_seguro(linha_pos, 'BB Fold to Steal'),
                        'SB_Steal': ler_valor_seguro(linha_pos, 'Steal from SB'), 'BB_Defend_SB_Steal': ler_valor_seguro(linha_pos, 'BB Defend SB Steal'),
                        'BB_Raise_SB_Steal': ler_valor_seguro(linha_pos, 'BB Reraise SB Steal'), 
                        'Total_Maos_Mes': total_maos_mes
                    })

        df_banco = pd.DataFrame(novas_linhas)
        return df_banco, "Sucesso! Gráficos atualizados com os dados enviados."
    except Exception as e:
        return pd.DataFrame(), f"Erro ao processar: {e}"
