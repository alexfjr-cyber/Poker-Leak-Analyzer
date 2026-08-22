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

import plotly.graph_objects as go

import plotly.graph_objects as go

def desenhar_grafico_stat_vs_meta(eixos_x, valores_reais, valores_meta, nome_stat, periodo, ano):
    fig = go.Figure()

    # Cor dinâmica das barras reais baseada no desvio individual de cada posição
    cores_barras = ['#00e676' if abs(r - m) <= 2.0 else '#ff1744' for r, m in zip(valores_reais, valores_meta)]

    # 1. Barra Real (O que você realmente jogou em cada posição)
    fig.add_trace(go.Bar(
        x=eixos_x,
        y=valores_reais,
        name=f"{nome_stat} Real",
        marker=dict(
            color=cores_barras,
            opacity=0.85,
            line=dict(color=cores_barras, width=1.5)
        ),
        text=[f"{v:.1f}%" for v in valores_reais],
        textposition='outside',
        textfont=dict(color='white', size=12, family="Arial Black"),
        hovertemplate="<b>Posição: %{x}</b><br>Realizado: %{y:.1f}%<extra></extra>"
    ))

    # 2. Barra de Meta Individual (Separada ao lado para cada posição de forma independente)
    fig.add_trace(go.Bar(
        x=eixos_x,
        y=valores_meta,
        name="Meta Ideal",
        marker=dict(
            color='#00e5ff', # Ciano Neon para destacar a meta
            opacity=0.4,     # Transparente para dar elegância
            line=dict(color='#00e5ff', width=1.5) # CORRIGIDO: Removido o dash='dot' que causava o erro
        ),
        text=[f"{v:.1f}%" for v in valores_meta],
        textposition='outside',
        textfont=dict(color='#00e5ff', size=11, family="sans-serif"),
        hovertemplate="<b>Posição: %{x}</b><br>Meta Ideal: %{y:.1f}%<extra></extra>"
    ))

    # 3. Layout Moderno e Limpo
    fig.update_layout(
        title=dict(
            text=f"<b>{nome_stat}</b>: Performance vs Meta Individual ({periodo})",
            font=dict(size=18, color='#FAFAFA', family="sans-serif"),
            x=0.01
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#A0AEC0', family="sans-serif"),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.08,
            xanchor="right", x=1,
            bgcolor='rgba(255,255,255,0.05)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1,
            font=dict(size=12, color="white")
        ),
        margin=dict(l=20, r=20, t=80, b=20),
        barmode='group', # Mantém as barras agrupadas lado a lado
        xaxis=dict(
            showgrid=False,
            linecolor='rgba(255,255,255,0.1)',
            tickfont=dict(size=14, color='white', family="Arial Black")
        ),
        yaxis=dict(
            title='',
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=1,
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.2)'
        )
    )
    
    # Arredondamento estético nas pontas das barras
    try:
        fig.update_traces(marker_cornerradius=4, selector=dict(type='bar'))
    except ValueError:
        pass

    return fig
    
def desenhar_grafico_anual_agrupado(df_ano, metas_globais, posicoes, stat_nome, prefixo_meta, titulo):
    fig = go.Figure()
    
    # Filtra apenas os meses reais (remove a linha 'Geral' do gráfico de progressão)
    df_meses = df_ano[df_ano['Mes'] != 'Geral']
    meses_ordenados = df_meses['Mes'].unique().tolist()
    
    # Paleta de Cores Premium para as 5 posições (Neon colors)
    paleta = {
        'EP': '#b388ff', # Roxo Neon
        'MP': '#82b1ff', # Azul Neon
        'CO': '#84ffff', # Ciano
        'BU': '#b9f6ca', # Verde Neon
        'SB': '#ffd180'  # Laranja/Amarelo Neon
    }

    for pos in posicoes:
        linha_pos = df_meses[df_meses['Posicao'] == pos]
        valores_reais = linha_pos[stat_nome].tolist()
        meta = metas_globais.get(f"{prefixo_meta}{pos}", 0.0)
        cor = paleta.get(pos, '#ffffff')
        
        # 1. As Barras Reais (Performance do mês)
        fig.add_trace(go.Bar(
            x=linha_pos['Mes'],
            y=valores_reais,
            name=f"{pos} Real",
            marker=dict(
                color=cor, 
                opacity=0.75,
                line=dict(color=cor, width=1.5)
            ),
            hovertemplate=f"<b>Posição: {pos}</b><br>Mês: %{{x}}<br>Realizado: %{{y:.1f}}%<extra></extra>"
        ))
        
        # 2. A Linha da Meta (Transversal cruzando todos os meses)
        fig.add_trace(go.Scatter(
            x=meses_ordenados,
            y=[meta] * len(meses_ordenados),
            name=f"Meta {pos}",
            mode='lines',
            line=dict(color=cor, width=2, dash='dot'),
            showlegend=False, # Oculto na legenda para não poluir, pois a cor já indica a posição
            hoverinfo='skip'  # O mouse não precisa focar na linha, apenas nas barras
        ))

    # 3. Layout Moderno
    fig.update_layout(
        title=dict(
            text=f"<b>{titulo}</b>",
            font=dict(size=18, color='#FAFAFA', family="sans-serif"),
            x=0.01
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#A0AEC0', family="sans-serif"),
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.05,
            xanchor="right", x=1,
            bgcolor='rgba(255,255,255,0.05)',
            bordercolor='rgba(255,255,255,0.1)',
            borderwidth=1,
            font=dict(size=12, color="white")
        ),
        margin=dict(l=20, r=20, t=80, b=20),
        barmode='group', # Agrupa as barras do mesmo mês lado a lado
        hovermode="x unified",
        xaxis=dict(
            showgrid=False,
            linecolor='rgba(255,255,255,0.1)',
            tickfont=dict(size=12, color='white', family="Arial Black")
        ),
        yaxis=dict(
            title='',
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            gridwidth=1,
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.2)'
        )
    )
    
    # Arredondamento estético nas pontas das barras
    try:
        fig.update_traces(marker_cornerradius=4, selector=dict(type='bar'))
    except ValueError:
        pass

    return fig
