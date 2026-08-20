import plotly.graph_objects as go

def desenhar_grafico_winrate_pareado(eixo_x, bb_real, ev_bb, titulo):
    fig = go.Figure()
    cores_bb = ['#00e676' if val >= 0 else '#ff1744' for val in bb_real]
    cores_ev = ['#ffd600' if ev > bb else '#b388ff' for ev, bb in zip(ev_bb, bb_real)]

    # 1. Adicionamos as barras físicas normais (escondidas da legenda)
    fig.add_trace(go.Bar(x=eixo_x, y=bb_real, marker_color=cores_bb, text=[f"{val:+.1f}" for val in bb_real], textposition='outside', showlegend=False))
    fig.add_trace(go.Bar(x=eixo_x, y=ev_bb, marker_color=cores_ev, text=[f"{val:+.1f}" for val in ev_bb], textposition='outside', showlegend=False))

    # 2. Criamos a legenda usando "Marcadores" (Scatter/Quadrados) em vez de Barras. 
    # Isso impede que o gráfico reserve espaço em branco entre as colunas!
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#00e676', symbol='square', size=15), name='bb/100 (Lucro)'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#ff1744', symbol='square', size=15), name='bb/100 (Prejuízo)'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#ffd600', symbol='square', size=15), name='EV (Bad Run / Azar)'))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(color='#b388ff', symbol='square', size=15), name='EV (Good Run / Sorte)'))

    fig.update_layout(
        title=f"📊 {titulo}", 
        barmode='group', 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='white'), 
        legend=dict(orientation="h", yanchor="bottom", y=1.15, xanchor="right", x=1), 
        yaxis=dict(title='bb / 100 mãos', gridcolor='rgba(255,255,255,0.1)', zeroline=True, zerolinecolor='rgba(255,255,255,0.3)'), 
        xaxis=dict(type='category', gridcolor='rgba(255,255,255,0.05)')
    )
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

import plotly.graph_objects as go

def desenhar_grafico_stat_vs_meta(eixos_x, valores_reais, valores_meta, nome_stat, periodo, ano):
    fig = go.Figure()

    # Lógica de cor dinâmica: Verde Neon se o desvio for aceitável (<= 2%), Rosa/Vermelho Neon se for Leak Grave
    cores_barras = ['#00e676' if abs(r - m) <= 2.0 else '#ff1744' for r, m in zip(valores_reais, valores_meta)]

    # 1. A Barra Real (Cantos arredondados, leve transparência e borda forte para dar "Glow")
    fig.add_trace(go.Bar(
        x=eixos_x,
        y=valores_reais,
        name=f"{nome_stat} Real",
        marker=dict(
            color=cores_barras,
            opacity=0.75,
            line=dict(color=cores_barras, width=2) # Borda luminosa
        ),
        text=[f"{v:.1f}%" for v in valores_reais],
        textposition='outside',
        textfont=dict(color='white', size=13, family="Arial Black"),
        hovertemplate="<b>Posição: %{x}</b><br>Realizado: %{y:.1f}%<extra></extra>"
    ))

    # 2. A Linha da Meta (Linha pontilhada luminosa com formato de diamante, flutuando sobre as barras)
    fig.add_trace(go.Scatter(
        x=eixos_x,
        y=valores_meta,
        name="Meta Ideal",
        mode='lines+markers',
        line=dict(color='#00e5ff', width=3, dash='dot'), # Ciano Neon (Azul claro brilhante)
        marker=dict(symbol='diamond', size=12, color='#0e1117', line=dict(width=2, color='#00e5ff')),
        hovertemplate="Meta: %{y:.1f}%<extra></extra>"
    ))

    # 3. Layout Premium: Limpeza de fundo, tipografia moderna e legenda encaixada
    fig.update_layout(
        title=dict(
            text=f"<b>{nome_stat}</b>: Performance vs Meta ({periodo})",
            font=dict(size=18, color='#FAFAFA', family="sans-serif"),
            x=0.01
        ),
        plot_bgcolor='rgba(0,0,0,0)',  # Fundo 100% invisível
        paper_bgcolor='rgba(0,0,0,0)', # Fundo 100% invisível
        font=dict(color='#A0AEC0', family="sans-serif"),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.05,
            xanchor="right", x=1,
            bgcolor='rgba(255,255,255,0.05)', # Caixa de legenda translúcida
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1,
            font=dict(size=12, color="white")
        ),
        margin=dict(l=20, r=20, t=80, b=20),
        hovermode="x unified", # Tooltip junta todas as infos num único card ao passar o mouse
        xaxis=dict(
            showgrid=False,
            linecolor='rgba(255,255,255,0.1)',
            tickfont=dict(size=14, color='white', family="Arial Black")
        ),
        yaxis=dict(
            title='',
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)', # Gridline quase invisível
            gridwidth=1,
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.2)'
        ),
        barmode='overlay' # Permite que a linha flutue por cima da barra sem empurrá-la pro lado
    )
    
    # Aplica arredondamento nas pontas das barras (Requer versões recentes do Plotly)
    try:
        fig.update_traces(marker_cornerradius=5, selector=dict(type='bar'))
    except ValueError:
        pass # Fallback caso a versão do servidor ainda não suporte cornerradius

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
