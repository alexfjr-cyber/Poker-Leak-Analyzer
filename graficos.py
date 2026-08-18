import plotly.graph_objects as go

def desenhar_grafico_winrate_pareado(eixo_x, bb_real, ev_bb, titulo):
    fig = go.Figure()
    cores_bb = ['#00e676' if val >= 0 else '#ff1744' for val in bb_real]
    cores_ev = ['#ffd600' if ev > bb else '#b388ff' for ev, bb in zip(ev_bb, bb_real)]

    fig.add_trace(go.Bar(x=eixo_x, y=bb_real, name='bb/100 Real', marker_color=cores_bb, text=[f"{val:+.1f}" for val in bb_real], textposition='outside'))
    fig.add_trace(go.Bar(x=eixo_x, y=ev_bb, name='EV bb/100 (Habilidade)', marker_color=cores_ev, text=[f"{val:+.1f}" for val in ev_bb], textposition='outside'))

    fig.update_layout(title=f"📊 {titulo}", barmode='group', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1), yaxis=dict(title='bb / 100 mãos', gridcolor='rgba(255,255,255,0.1)', zeroline=True, zerolinecolor='rgba(255,255,255,0.3)'), xaxis=dict(type='category', gridcolor='rgba(255,255,255,0.05)'))
    return fig

def desenhar_evolucao_anual(df_ano, metrica, titulo, posicoes=None):
    fig = go.Figure()
    df_temporal = df_ano[df_ano['Mes'] != 'Geral'].copy()
    from motor import ORDEM_MESES_PADRAO
    meses_presentes = [m for m in ORDEM_MESES_PADRAO if m in df_temporal['Mes'].values]
    cores = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4']

    if posicoes:
        for i, p in enumerate(posicoes):
            df_pos = df_temporal[df_temporal['Posicao'] == p]
            valores = [df_pos[df_pos['Mes'] == m][metrica].iloc[0] if not df_pos[df_pos['Mes'] == m].empty else None for m in meses_presentes]
            fig.add_trace(go.Scatter(x=meses_presentes, y=valores, mode='lines+markers', name=p, line=dict(width=3, color=cores[i])))
    else:
        valores = [df_temporal[df_temporal['Mes'] == m][metrica].mean() for m in meses_presentes]
        fig.add_trace(go.Scatter(x=meses_presentes, y=valores, mode='lines+markers', name='Média Geral', line=dict(width=3, color='#00e676')))

    fig.update_layout(title=f"📈 {titulo}", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), hovermode="x unified", yaxis=dict(gridcolor='rgba(255,255,255,0.1)'), xaxis=dict(type='category', gridcolor='rgba(255,255,255,0.05)'))
    return fig

def desenhar_grafico_stat_vs_meta(posicoes, valores_real, valores_meta, nome_stat, mes, ano):
    fig = go.Figure()
    
    # 1. Adiciona a barra real PRIMEIRO para o gráfico entender que o eixo X é texto (posições)
    fig.add_trace(go.Bar(x=posicoes, y=valores_real, name=f'Real ({mes})', marker_color='#2979ff', width=0.5, text=[f"{v:.1f}%" for v in valores_real], textposition='outside'))
    
    # 2. Marcador Fake apenas para aparecer na Legenda (usando a primeira posição para não quebrar o eixo)
    fig.add_trace(go.Scatter(x=[posicoes[0]], y=[None], mode='lines', name='🎯 Meta Ideal', line=dict(color='#ffea00', width=4)))

    # 3. Desenho das linhas físicas que sobrepõem as barras
    shapes = []
    for i, meta in enumerate(valores_meta):
        shapes.append(dict(type="line", x0=i-0.4, x1=i+0.4, y0=meta, y1=meta, line=dict(color="#ffea00", width=4), xref="x", yref="y", layer="above"))

    fig.update_layout(title=f"🎯 {nome_stat} por Posição: Real vs Meta — {mes}/{ano}", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), yaxis=dict(title=f'% de {nome_stat}', gridcolor='rgba(255,255,255,0.1)'), xaxis=dict(type='category', gridcolor='rgba(255,255,255,0.05)'), shapes=shapes)
    return fig

def desenhar_grafico_anual_agrupado(df_ano, metas_dict, posicoes, metrica_db, prefixo_meta, titulo):
    fig = go.Figure()
    from motor import ORDEM_MESES_PADRAO
    df_temporal = df_ano[df_ano['Mes'] != 'Geral']
    meses_presentes = [m for m in ORDEM_MESES_PADRAO if m in df_temporal['Mes'].values]
    cores_meses = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#109618', '#990099']
    
    # 1. Desenha as barras de todos os meses primeiro
    for i, mes in enumerate(meses_presentes):
        valores_mes = []
        for p in posicoes:
            linha = df_temporal[(df_temporal['Posicao'] == p) & (df_temporal['Mes'] == mes)]
            valores_mes.append(float(linha[metrica_db].iloc[0]) if not linha.empty else 0.0)
            
        fig.add_trace(go.Bar(x=posicoes, y=valores_mes, name=mes, marker_color=cores_meses[i % len(cores_meses)], text=[f"{v:.1f}%" if v > 0 else "" for v in valores_mes], textposition='inside', textfont=dict(size=10)))

    # 2. Marcador Fake para Legenda
    fig.add_trace(go.Scatter(x=[posicoes[0]], y=[None], mode='lines', name='🎯 Meta', line=dict(color='#ffea00', width=4)))

    # 3. Desenho das linhas de meta sobrepostas
    shapes = []
    for i, p in enumerate(posicoes):
        meta = metas_dict.get(f"{prefixo_meta}{p}" if prefixo_meta else metrica_db, 0.0)
        shapes.append(dict(type="line", x0=i-0.45, x1=i+0.45, y0=meta, y1=meta, line=dict(color="#ffea00", width=4), xref="x", yref="y", layer="above"))

    fig.update_layout(
        title=f"📊 {titulo}", 
        barmode='group', 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='white'), 
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1), 
        yaxis=dict(title='%', gridcolor='rgba(255,255,255,0.1)'), 
        xaxis=dict(type='category', gridcolor='rgba(255,255,255,0.05)'), # Eixo X forçado como categoria
        shapes=shapes
    )
    return fig