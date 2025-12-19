"""
Detail Commodities Page
Shows comprehensive analysis for single commodity
"""
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
from web.design_system import (
    COLORS, FONTS, SPACING, RADIUS, SHADOWS,
    COMPONENT_STYLES, CHART_STYLES,
    get_icon_path, get_svg_icon,
    format_currency, format_percent
)
from analysis.processing.commodity_details import (
    get_commodity_info,
    get_national_average,
    get_price_trend,
    get_top_provinces,
    get_quality_breakdown
)


def layout(commodity_id):
    """
    Detail page layout for specific commodity
    
    Args:
        commodity_id (str): Commodity ID from URL
    """
    # Get commodity info
    commodity = get_commodity_info(commodity_id)
    
    if not commodity:
        return html.Div([
            html.H1("Commodity not found"),
            html.A("Back to home", href="/")
        ])
    
    return html.Div([
        # Breadcrumb
        create_breadcrumb(commodity),
        
        # Header section
        create_header(commodity),
        
        # Key metrics
        html.Div(id='detail-metrics', **{'data-commodity-id': commodity_id}),
        
        # Price trend chart
        html.Div(id='detail-trend-chart', **{'data-commodity-id': commodity_id}),
        
        # Two column layout
        html.Div([
            # Left: Quality breakdown
            html.Div(
                id='detail-quality-chart',
                style={'flex': '1', 'marginRight': SPACING['lg']}
            ),
            
            # Right: Province ranking
            html.Div(
                id='detail-province-ranking',
                style={'flex': '1'}
            ),
        ], style={'display': 'flex', 'gap': SPACING['lg'], 'marginTop': SPACING['xl']}),
        
    ], style={
        'backgroundColor': COLORS['bg_main'],
        'minHeight': '100vh',
        'padding': SPACING['xl'],
        'maxWidth': '1400px',
        'margin': '0 auto',
    })


def create_breadcrumb(commodity):
    """Create breadcrumb navigation"""
    return html.Div([
        html.A("Home", href="/", style={'color': COLORS['text_secondary']}),
        html.Span(" / ", style={'color': COLORS['text_muted'], 'margin': f"0 {SPACING['xs']}"}),
        html.Span("Detail Komoditas", style={'color': COLORS['text_secondary']}),
        html.Span(" / ", style={'color': COLORS['text_muted'], 'margin': f"0 {SPACING['xs']}"}),
        html.Span(commodity['name'], style={'color': COLORS['primary']}),
    ], style={'marginBottom': SPACING['lg']})


def create_header(commodity):
    """Create page header"""
    return html.Div([
        html.Img(
            src=get_icon_path('commodities', commodity['icon']),
            style={'width': '64px', 'height': '64px', 'marginRight': SPACING['md']}
        ),
        html.Div([
            html.H1(
                commodity['name'],
                style={
                    **COMPONENT_STYLES['heading_1'],
                    'marginBottom': SPACING['xs']
                }
            ),
            html.P(
                "Analisis lengkap harga dan tren",
                style={'color': COLORS['text_secondary'], 'fontSize': FONTS['lg']}
            ),
        ]),
    ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': SPACING['2xl']})


# ============================================================================
# CALLBACKS
# ============================================================================

@callback(
    Output('detail-metrics', 'children'),
    Input('detail-metrics', 'data-commodity-id')
)
def update_metrics(commodity_id):
    """Update key metrics cards"""
    data = get_national_average(commodity_id)
    
    if not data:
        return html.Div("No data available")
    
    # Create metric cards
    cards = [
        create_metric_card(
            "Harga Nasional",
            format_currency(data['avg_price']),
            subtitle=f"Per {data['date']}"
        ),
        create_metric_card(
            "Volatilitas",
            "Sedang",
            subtitle="7 hari terakhir"
        ),
        create_metric_card(
            "Tren",
            "Stabil",
            subtitle="Perubahan mingguan"
        ),
    ]
    
    return html.Div(
        cards,
        style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
            'gap': SPACING['lg'],
            'marginBottom': SPACING['xl'],
        }
    )


def create_metric_card(title, value, subtitle=None):
    """Create metric card"""
    return html.Div([
        html.Div(title, style={'fontSize': FONTS['sm'], 'color': COLORS['text_secondary'], 'marginBottom': SPACING['xs']}),
        html.Div(value, style={'fontSize': FONTS['3xl'], 'fontWeight': FONTS['weight_bold'], 'color': COLORS['primary'], 'marginBottom': SPACING['xs']}),
        html.Div(subtitle, style={'fontSize': FONTS['xs'], 'color': COLORS['text_muted']}) if subtitle else None,
    ], style={**COMPONENT_STYLES['card']})


@callback(
    Output('detail-trend-chart', 'children'),
    Input('detail-trend-chart', 'data-commodity-id')
)
def update_trend_chart(commodity_id):
    """Update price trend chart"""
    df = get_price_trend(commodity_id, days=30)
    
    if df.empty:
        return html.Div("No trend data")
    
    # Create line chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['avg_price'],
        mode='lines+markers',
        name='Harga Rata-rata',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=6),
        hovertemplate='<b>%{x}</b><br>Rp %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Tren Harga 30 Hari Terakhir',
        xaxis_title='Tanggal',
        yaxis_title='Harga (Rp/kg)',
        **CHART_STYLES['layout']
    )
    
    return html.Div([
        dcc.Graph(figure=fig)
    ], style={**COMPONENT_STYLES['card']})


@callback(
    Output('detail-quality-chart', 'children'),
    Input('detail-metrics', 'data-commodity-id')
)
def update_quality_chart(commodity_id):
    """Update quality breakdown chart"""
    df = get_quality_breakdown(commodity_id)
    
    if df.empty:
        return html.Div([
            html.H3("Perbandingan Kualitas", style={'color': COLORS['text_primary']}),
            html.P("Data kualitas tidak tersedia", style={'color': COLORS['text_secondary']})
        ], style={**COMPONENT_STYLES['card']})
    
    # Create bar chart
    fig = go.Figure()
    
    colors = {
        'Low': COLORS['success'],
        'Medium': COLORS['warning'],
        'Premium': COLORS['danger'],
        'Standard': COLORS['neutral']
    }
    
    fig.add_trace(go.Bar(
        x=df['subcategory_name'],
        y=df['avg_price'],
        marker_color=[colors.get(q, COLORS['primary']) for q in df['quality_level']],
        text=[f"Rp {p:,.0f}" for p in df['avg_price']],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Rp %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Perbandingan Harga per Kualitas',
        xaxis_title='Kualitas',
        yaxis_title='Harga (Rp/kg)',
        **CHART_STYLES['layout']
    )
    
    return html.Div([
        dcc.Graph(figure=fig)
    ], style={**COMPONENT_STYLES['card']})


@callback(
    Output('detail-province-ranking', 'children'),
    Input('detail-metrics', 'data-commodity-id')
)
def update_province_ranking(commodity_id):
    """Update province ranking"""
    df_cheap = get_top_provinces(commodity_id, limit=5, order='ASC')
    df_expensive = get_top_provinces(commodity_id, limit=5, order='DESC')
    
    if df_cheap.empty:
        return html.Div("No province data")
    
    return html.Div([
        html.H3("Ranking Provinsi", style={'color': COLORS['text_primary'], 'marginBottom': SPACING['md']}),
        
        # Cheapest
        html.Div([
            html.H4("✅ Termurah", style={'color': COLORS['success'], 'marginBottom': SPACING['sm']}),
            create_province_table(df_cheap, 'success'),
        ], style={'marginBottom': SPACING['lg']}),
        
        # Most expensive
        html.Div([
            html.H4("🚨 Termahal", style={'color': COLORS['danger'], 'marginBottom': SPACING['sm']}),
            create_province_table(df_expensive, 'danger'),
        ]),
        
    ], style={**COMPONENT_STYLES['card']})


def create_province_table(df, color_type):
    """Create province ranking table"""
    color = COLORS['success'] if color_type == 'success' else COLORS['danger']
    
    rows = []
    for idx, row in df.iterrows():
        rows.append(html.Div([
            html.Span(f"{idx + 1}.", style={'fontWeight': FONTS['weight_bold'], 'marginRight': SPACING['sm'], 'color': color}),
            html.Span(row['province_name'], style={'flex': 1, 'color': COLORS['text_primary']}),
            html.Span(format_currency(row['price']), style={'fontWeight': FONTS['weight_semibold'], 'color': color}),
        ], style={
            'display': 'flex',
            'alignItems': 'center',
            'padding': SPACING['sm'],
            'borderBottom': f"1px solid {COLORS['border']}",
        }))
    
    return html.Div(rows)