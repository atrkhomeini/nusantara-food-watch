# 📱 EXAMPLE: Consumer Homepage with Price Forecast
# Use this as REFERENCE template for your pages!

"""
Page: Consumer Homepage
Features:
- Location-based pricing
- Today's tips (actionable insights)
- Price cards for main commodities
- Daily price forecast (NEW!) ⭐
- Quality comparison chart
"""

from dash import html, dcc, Input, Output, callback
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

from design_system import CHART_STYLES, COLORS, FONTS, SPACING, COMPONENT_STYLES, ICONS
from components import (
    create_stat_card, 
    create_card, 
    create_filter_bar, 
    create_insight_box,
    create_loading,
    create_line_chart,
    create_bar_chart,
)


# ============================================================================
# 1. PAGE LAYOUT
# ============================================================================

def layout():
    """
    Consumer homepage layout
    Returns: html.Div
    """
    return html.Div([
        # Location selector
        create_location_bar(),
        
        # Main content area
        html.Div([
            # Today's tips section
            create_tips_section(),
            
            # Price cards grid
            create_price_cards_grid(),
            
            # NEW: Daily Price Forecast ⭐
            create_forecast_section(),
            
            # Quality comparison
            create_quality_section(),
            
        ], style={'padding': SPACING['xl'], 'maxWidth': '1400px', 'margin': '0 auto'}),
        
    ], style={'backgroundColor': COLORS['bg_main'], 'minHeight': '100vh'})


# ============================================================================
# 2. LOCATION BAR
# ============================================================================

def create_location_bar():
    """Location selection bar"""
    return html.Div(
        [
            html.Div([
                html.Span('📍', style={'fontSize': FONTS['xl'], 'marginRight': SPACING['sm']}),
                html.Span('Lokasi Anda:', style={'marginRight': SPACING['sm'], 'fontWeight': FONTS['weight_semibold']}),
            ]),
            dcc.Dropdown(
                id='consumer-location',
                options=[
                    {'label': '🇮🇩 Nasional', 'value': 'national'},
                    {'label': 'DKI Jakarta', 'value': 'jakarta'},
                    {'label': 'Jawa Barat', 'value': 'jabar'},
                    {'label': 'Jawa Timur', 'value': 'jatim'},
                    {'label': 'Surabaya', 'value': 'surabaya'},
                    # Add all provinces...
                ],
                value='surabaya',
                style={'width': '300px'},
            ),
        ],
        style={
            **COMPONENT_STYLES['card'],
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'space-between',
            'marginBottom': SPACING['lg'],
        }
    )


# ============================================================================
# 3. TODAY'S TIPS SECTION
# ============================================================================

def create_tips_section():
    """Actionable tips based on price movements"""
    return html.Div([
        html.H2('💡 Tips Belanja Hari Ini', style=COMPONENT_STYLES['heading_2']),
        
        html.Div(id='consumer-tips-container', children=[
            # These will be populated by callback
            create_insight_box("✅ BELI SEKARANG: Ayam (turun 3%, harga bagus!)", 'success'),
            create_insight_box("⏳ TUNGGU 1-2 MINGGU: Cabai (naik 15%, prediksi akan turun)", 'warning'),
            create_insight_box("➡️ HARGA STABIL: Beras, Telur (aman beli kapan saja)", 'info'),
        ]),
        
    ], style={'marginBottom': SPACING['xl']})


# ============================================================================
# 4. PRICE CARDS GRID
# ============================================================================

def create_price_cards_grid():
    """Grid of commodity price cards"""
    return html.Div([
        html.H2('🛒 Harga Hari Ini', style=COMPONENT_STYLES['heading_2']),
        
        html.Div(
            id='consumer-price-cards',
            children=[
                # Sample cards - will be populated by callback
                create_stat_card(
                    label='per kg',
                    value='Rp 11,500',
                    change_percent=0,
                    icon='🍚 Beras',
                ),
                create_stat_card(
                    label='per kg',
                    value='Rp 34,000',
                    change_percent=-3.0,
                    icon='🍗 Ayam',
                ),
                create_stat_card(
                    label='per butir',
                    value='Rp 2,200',
                    change_percent=2.0,
                    icon='🥚 Telur',
                ),
                create_stat_card(
                    label='per kg',
                    value='Rp 45,000',
                    change_percent=15.0,
                    icon='🌶️ Cabai',
                ),
            ],
            style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(250px, 1fr))',
                'gap': SPACING['lg'],
            }
        ),
        
    ], style={'marginBottom': SPACING['xl']})


# ============================================================================
# 5. PRICE FORECAST SECTION ⭐ NEW!
# ============================================================================

def create_forecast_section():
    """
    NEW: Daily price forecast section
    Shows what will happen tomorrow with consumer-friendly insights
    """
    return html.Div([
        create_card(
            children=[
                # Commodity selector for forecast
                html.Div([
                    html.Label('Pilih Komoditas:', style={'marginRight': SPACING['sm']}),
                    dcc.Dropdown(
                        id='consumer-forecast-commodity',
                        options=[
                            {'label': f"{ICONS['commodities'][c]} {c}", 'value': i}
                            for i, c in enumerate(['Beras', 'Daging Ayam', 'Telur Ayam', 'Cabai Merah'], 1)
                        ],
                        value=1,  # Beras
                        clearable=False,
                        style={'width': '300px'},
                    ),
                ], style={'marginBottom': SPACING['md']}),
                
                # Forecast chart
                create_loading(
                    'consumer-forecast-chart',
                    dcc.Graph(id='consumer-forecast-chart')
                ),
                
                # Insight box below chart
                html.Div(id='consumer-forecast-insight'),
            ],
            title='📈 Prediksi Harga Besok',
            subtitle='Berdasarkan pola harga 30 hari terakhir'
        ),
        
    ], style={'marginBottom': SPACING['xl']})


# ============================================================================
# 6. QUALITY COMPARISON SECTION
# ============================================================================

def create_quality_section():
    """Quality price comparison - worth it or not?"""
    return html.Div([
        create_card(
            children=[
                # Commodity selector
                html.Div([
                    html.Label('Pilih Komoditas:', style={'marginRight': SPACING['sm']}),
                    dcc.Dropdown(
                        id='consumer-quality-commodity',
                        options=[
                            {'label': f"{ICONS['commodities']['Beras']} Beras", 'value': 1},
                            {'label': f"{ICONS['commodities']['Minyak Goreng']} Minyak Goreng", 'value': 9},
                            {'label': f"{ICONS['commodities']['Gula Pasir']} Gula Pasir", 'value': 10},
                        ],
                        value=1,
                        clearable=False,
                        style={'width': '300px'},
                    ),
                ], style={'marginBottom': SPACING['md']}),
                
                # Quality chart
                create_loading(
                    'consumer-quality-chart',
                    dcc.Graph(id='consumer-quality-chart')
                ),
                
                # Worth it recommendation
                html.Div(id='consumer-quality-insight'),
            ],
            title='🏆 Worth It or Not?',
            subtitle='Perbandingan harga per kualitas'
        ),
        
    ], style={'marginBottom': SPACING['xl']})


# ============================================================================
# 7. CALLBACKS
# ============================================================================

@callback(
    Output('consumer-forecast-chart', 'figure'),
    Output('consumer-forecast-insight', 'children'),
    Input('consumer-forecast-commodity', 'value'),
    Input('consumer-location', 'value')
)
def update_forecast(commodity_id, location):
    """
    Update daily price forecast chart
    Shows: Today + next 7 days prediction
    """
    
    # TODO: Replace with actual data query
    # df = get_price_forecast(commodity_id, location, days=7)
    
    # SAMPLE DATA for demonstration
    dates = pd.date_range(start=datetime.now(), periods=8, freq='D')
    df = pd.DataFrame({
        'date': dates,
        'actual': [12500, 12550, 12600, 12650, None, None, None, None],
        'predicted': [None, None, None, 12650, 12700, 12800, 12850, 12900],
        'lower_bound': [None, None, None, 12550, 12600, 12700, 12750, 12800],
        'upper_bound': [None, None, None, 12750, 12800, 12900, 12950, 13000],
    })
    
    # Create figure
    fig = go.Figure()
    
    # Actual prices (past)
    fig.add_trace(go.Scatter(
        x=df['date'][:4],
        y=df['actual'][:4],
        mode='lines+markers',
        name='Harga Aktual',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=8),
    ))
    
    # Predicted prices (future)
    fig.add_trace(go.Scatter(
        x=df['date'][3:],
        y=df['predicted'][3:],
        mode='lines+markers',
        name='Prediksi',
        line=dict(color=COLORS['warning'], width=3, dash='dash'),
        marker=dict(size=8, symbol='diamond'),
    ))
    
    # Confidence interval
    fig.add_trace(go.Scatter(
        x=df['date'][3:],
        y=df['upper_bound'][3:],
        mode='lines',
        name='Confidence Upper',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip',
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'][3:],
        y=df['lower_bound'][3:],
        mode='lines',
        name='Confidence Lower',
        fill='tonexty',
        fillcolor='rgba(245, 158, 11, 0.2)',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip',
    ))
    
    # Layout
    fig.update_layout(
        title='Prediksi Harga 7 Hari Ke Depan',
        xaxis_title='Tanggal',
        yaxis_title='Harga (Rp/kg)',
        hovermode='x unified',
        **CHART_STYLES['layout'],
    )
    
    # Generate insight
    tomorrow_price = df['predicted'].iloc[4]
    today_price = df['actual'].iloc[3]
    change = ((tomorrow_price - today_price) / today_price) * 100
    
    if change > 2:
        insight = create_insight_box(
            f"📈 Harga diprediksi NAIK {change:.1f}% besok. Pertimbangkan beli hari ini untuk hemat!",
            'warning'
        )
    elif change < -2:
        insight = create_insight_box(
            f"📉 Harga diprediksi TURUN {abs(change):.1f}% besok. Tunggu besok untuk harga lebih baik!",
            'success'
        )
    else:
        insight = create_insight_box(
            f"➡️ Harga relatif STABIL (perubahan {change:+.1f}%). Aman beli kapan saja.",
            'info'
        )
    
    return fig, insight


@callback(
    Output('consumer-quality-chart', 'figure'),
    Output('consumer-quality-insight', 'children'),
    Input('consumer-quality-commodity', 'value'),
    Input('consumer-location', 'value')
)
def update_quality(commodity_id, location):
    """
    Update quality comparison chart
    Shows: Low vs Medium vs Premium pricing
    """
    
    # TODO: Replace with actual data query
    # df = get_quality_breakdown(commodity_id, location)
    
    # SAMPLE DATA
    df = pd.DataFrame({
        'quality': ['Low', 'Medium', 'Premium'],
        'price': [11000, 12500, 13000],
        'percentage': [100, 113.6, 118.2],
    })
    
    # Create bar chart
    fig = go.Figure(data=[
        go.Bar(
            x=df['quality'],
            y=df['price'],
            text=[f"Rp {p:,.0f}<br>(+{pct-100:.1f}%)" if pct > 100 else f"Rp {p:,.0f}" 
                  for p, pct in zip(df['price'], df['percentage'])],
            textposition='auto',
            marker_color=[
                COLORS['success'],
                COLORS['warning'],
                COLORS['danger'],
            ],
        )
    ])
    
    fig.update_layout(
        title='Perbandingan Harga per Kualitas',
        xaxis_title='Kualitas',
        yaxis_title='Harga (Rp/kg)',
        **CHART_STYLES['layout'],
    )
    
    # Generate recommendation
    premium_price = df[df['quality'] == 'Premium']['price'].iloc[0]
    low_price = df[df['quality'] == 'Low']['price'].iloc[0]
    gap_percent = ((premium_price - low_price) / low_price) * 100
    
    if gap_percent < 15:
        insight = create_insight_box(
            f"⭐ Premium hanya {gap_percent:.1f}% lebih mahal! WORTH IT untuk kualitas lebih baik.",
            'success'
        )
    elif gap_percent < 25:
        insight = create_insight_box(
            f"💰 Premium {gap_percent:.1f}% lebih mahal. Medium quality adalah pilihan terbaik!",
            'info'
        )
    else:
        insight = create_insight_box(
            f"💸 Premium {gap_percent:.1f}% lebih mahal. Pertimbangkan Low/Medium untuk hemat.",
            'warning'
        )
    
    return fig, insight


# ============================================================================
# 8. EXPORT
# ============================================================================

# This will be imported by index.py for routing
__all__ = ['layout']