"""
URL Routing for Nusantara Food Watch Dashboard
Handles all page navigation
"""
from dash import html
from dash.dependencies import Input, Output

def register_routes(app):
    """Register all page routes"""
    
    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def display_page(pathname):
        """
        Route URL paths to appropriate pages
        
        Routes:
        - / → Landing page (role selection)
        - /consumer → Consumer homepage
        - /trader → Trader homepage
        - /government → Government homepage
        - /researcher → Researcher homepage
        - /all → All features dashboard
        - /detail/<commodity_id> → Commodity detail page
        """
        
        # Import pages (lazy loading to avoid circular imports)
        try:
            from web.pages import landing
        except ImportError:
            return html.Div([
                html.H1("Error: pages module not found"),
                html.P("Make sure web/pages/__init__.py exists")
            ])
        
        # Root - Landing page
        if pathname == '/' or pathname is None:
            return landing.layout()
        
        # Researcher page
        elif pathname == '/researcher':
            try:
                from web.pages import home_researcher
                return home_researcher.layout()
            except ImportError:
                return create_404_page(pathname, "Researcher page not implemented yet")
        
        # Detail commodity page
        elif pathname.startswith('/detail/'):
            try:
                # Extract commodity_id from URL
                commodity_id = pathname.split('/')[-1]
                
                # Validate commodity_id is a number
                try:
                    commodity_id = int(commodity_id)
                    if commodity_id < 1 or commodity_id > 10:
                        raise ValueError("Invalid commodity ID")
                except ValueError:
                    return create_404_page(pathname, f"Invalid commodity ID: {commodity_id}")
                
                # Load detail page
                from web.pages import detail_commodity
                return detail_commodity.layout(commodity_id)
                
            except ImportError as e:
                return create_404_page(pathname, f"Detail commodity page not implemented yet. Error: {str(e)}")
        
        # Consumer page
        elif pathname == '/consumer':
            try:
                from web.pages import home_consumer
                return home_consumer.layout()
            except ImportError:
                return create_404_page(pathname, "Consumer page not implemented yet")
        
        # Trader page
        elif pathname == '/trader':
            try:
                from web.pages import home_trader
                return home_trader.layout()
            except ImportError:
                return create_404_page(pathname, "Trader page not implemented yet")
        
        # Government page
        elif pathname == '/government':
            try:
                from web.pages import home_government
                return home_government.layout()
            except ImportError:
                return create_404_page(pathname, "Government page not implemented yet")
        
        # All features dashboard
        elif pathname == '/all':
            return create_all_dashboard_page()
        
        # 404 - Page not found
        else:
            return create_404_page(pathname)


def create_404_page(pathname, message=None):
    """Create 404 error page"""
    from web.design_system import COLORS, FONTS, SPACING
    
    return html.Div([
        html.Div([
            html.H1(
                "404 - Page Not Found",
                style={
                    'color': COLORS['danger'],
                    'fontSize': FONTS['4xl'],
                    'marginBottom': SPACING['md']
                }
            ),
            html.P(
                f"The page '{pathname}' does not exist.",
                style={
                    'color': COLORS['text_secondary'],
                    'fontSize': FONTS['lg'],
                    'marginBottom': SPACING['lg']
                }
            ),
            html.P(
                message or "Please check the URL and try again.",
                style={
                    'color': COLORS['text_muted'],
                    'fontSize': FONTS['base'],
                    'marginBottom': SPACING['xl']
                }
            ),
            html.A(
                "← Back to Home",
                href="/",
                style={
                    'color': COLORS['primary'],
                    'fontSize': FONTS['lg'],
                    'textDecoration': 'none',
                    'fontWeight': 600
                }
            ),
        ], style={
            'textAlign': 'center',
            'padding': SPACING['4xl'],
            'maxWidth': '600px',
            'margin': '0 auto',
            'marginTop': SPACING['4xl']
        })
    ], style={
        'backgroundColor': COLORS['bg_main'],
        'minHeight': '100vh',
        'color': COLORS['text_primary']
    })


def create_all_dashboard_page():
    """
    Create 'All Features' dashboard page
    Quick access to all commodities
    """
    from web.design_system import COLORS, FONTS, SPACING, RADIUS, get_icon_path
    
    commodities = [
        {'id': 1, 'name': 'Beras', 'icon': 'Beras'},
        {'id': 2, 'name': 'Daging Ayam', 'icon': 'Daging Ayam'},
        {'id': 3, 'name': 'Daging Sapi', 'icon': 'Daging Sapi'},
        {'id': 4, 'name': 'Telur Ayam', 'icon': 'Telur Ayam'},
        {'id': 5, 'name': 'Bawang Merah', 'icon': 'Bawang Merah'},
        {'id': 6, 'name': 'Bawang Putih', 'icon': 'Bawang Putih'},
        {'id': 7, 'name': 'Cabai Merah', 'icon': 'Cabai Merah'},
        {'id': 8, 'name': 'Cabai Rawit', 'icon': 'Cabai Rawit'},
        {'id': 9, 'name': 'Minyak Goreng', 'icon': 'Minyak Goreng'},
        {'id': 10, 'name': 'Gula Pasir', 'icon': 'Gula Pasir'},
    ]
    
    # Create commodity cards
    cards = []
    for commodity in commodities:
        cards.append(
            html.A(
                html.Div([
                    html.Img(
                        src=get_icon_path('commodities', commodity['icon']),
                        style={
                            'width': '48px',
                            'height': '48px',
                            'marginBottom': SPACING['sm']
                        }
                    ),
                    html.Div(
                        commodity['name'],
                        style={
                            'fontSize': FONTS['lg'],
                            'fontWeight': 600,
                            'color': COLORS['text_primary']
                        }
                    ),
                ], style={
                    'backgroundColor': COLORS['bg_card'],
                    'borderRadius': RADIUS['lg'],
                    'padding': SPACING['lg'],
                    'textAlign': 'center',
                    'border': f"2px solid {COLORS['border']}",
                    'transition': 'all 0.3s',
                    'cursor': 'pointer',
                    'display': 'flex',
                    'flexDirection': 'column',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'minHeight': '150px',
                }, className='commodity-card'),
                href=f"/detail/{commodity['id']}",
                style={'textDecoration': 'none'}
            )
        )
    
    return html.Div([
        # Header
        html.Div([
            html.H1(
                "Dashboard Lengkap",
                style={
                    'color': COLORS['primary'],
                    'fontSize': FONTS['4xl'],
                    'marginBottom': SPACING['sm']
                }
            ),
            html.P(
                "Pilih komoditas untuk melihat detail analisis",
                style={
                    'color': COLORS['text_secondary'],
                    'fontSize': FONTS['lg'],
                    'marginBottom': SPACING['xl']
                }
            ),
            html.A(
                "← Kembali ke Role Selection",
                href="/",
                style={
                    'color': COLORS['text_muted'],
                    'fontSize': FONTS['base'],
                    'textDecoration': 'none',
                }
            ),
        ], style={
            'textAlign': 'center',
            'marginBottom': SPACING['2xl']
        }),
        
        # Commodity grid
        html.Div(
            cards,
            style={
                'display': 'grid',
                'gridTemplateColumns': 'repeat(auto-fit, minmax(200px, 1fr))',
                'gap': SPACING['lg'],
                'maxWidth': '1200px',
                'margin': '0 auto'
            }
        ),
        
    ], style={
        'backgroundColor': COLORS['bg_main'],
        'minHeight': '100vh',
        'padding': SPACING['2xl']
    })