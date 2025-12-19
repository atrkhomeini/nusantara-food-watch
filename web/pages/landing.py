"""
Landing Page - User Role Selection
Author: Ersen
Fixed: Removed dangerouslySetInnerHTML (not supported in Dash)
"""
from dash import html, dcc
from web.design_system import (
    COLORS, FONTS, SPACING, RADIUS, SHADOWS,
    get_icon_path
)

def layout():
    """Landing page layout"""
    return html.Div([
        # Hero section
        create_hero_section(),
        
        # Role selection cards
        create_role_cards(),
        
        # Footer
        create_footer(),
        
    ], style={
        'backgroundColor': COLORS['bg_main'],
        'minHeight': '100vh',
        'padding': SPACING['xl'],
    })


def create_hero_section():
    """Create hero section with logo and tagline"""
    return html.Div([
        # Logo (use rice icon as logo)
        html.Img(
            src=get_icon_path('commodities', 'Beras'),
            style={
                'width': '80px',
                'height': '80px',
                'marginBottom': SPACING['md'],
            }
        ),
        
        # Title
        html.H1(
            "Nusantara Food Watch",
            style={
                'fontSize': FONTS['5xl'],
                'fontFamily': FONTS['family_display'],
                'fontWeight': FONTS['weight_bold'],
                'color': COLORS['primary'],
                'marginBottom': SPACING['sm'],
                'textAlign': 'center',
            }
        ),
        
        # Tagline
        html.P(
            "Monitor Harga Pangan Indonesia Real-Time",
            style={
                'fontSize': FONTS['xl'],
                'color': COLORS['text_secondary'],
                'textAlign': 'center',
                'marginBottom': SPACING['2xl'],
            }
        ),
        
        # Question
        html.H2(
            "Dashboard untuk siapa?",
            style={
                'fontSize': FONTS['3xl'],
                'color': COLORS['text_primary'],
                'textAlign': 'center',
                'marginBottom': SPACING['xl'],
            }
        ),
        
    ], style={
        'textAlign': 'center',
        'paddingTop': SPACING['3xl'],
        'paddingBottom': SPACING['2xl'],
    })


def create_role_cards():
    """Create role selection cards"""
    
    roles = [
        {
            'id': 'consumer',
            'title': 'Konsumen',
            'description': 'Cari harga terbaik dan tips belanja hemat',
            'icon': 'consumer',
            'link': '/consumer',
            'color': COLORS['success'],
        },
        {
            'id': 'trader',
            'title': 'Pedagang',
            'description': 'Analisis margin dan peluang bisnis',
            'icon': 'trader',
            'link': '/trader',
            'color': COLORS['warning'],
        },
        {
            'id': 'government',
            'title': 'Pemerintah',
            'description': 'Monitor stabilitas harga dan inflasi',
            'icon': 'government',
            'link': '/government',
            'color': COLORS['info'],
        },
        {
            'id': 'researcher',
            'title': 'Peneliti',
            'description': 'Akses data lengkap dan tools analisis',
            'icon': 'researcher',
            'link': '/researcher',
            'color': COLORS['primary'],
        },
    ]
    
    cards = [create_role_card(role) for role in roles]
    
    return html.Div(
        cards,
        style={
            'display': 'grid',
            'gridTemplateColumns': 'repeat(auto-fit, minmax(280px, 1fr))',
            'gap': SPACING['xl'],
            'maxWidth': '1200px',
            'margin': '0 auto',
            'padding': SPACING['xl'],
        }
    )


def create_role_card(role):
    """Create individual role card"""
    return html.A(
        html.Div([
            # Icon
            html.Img(
                src=get_icon_path('user_roles', role['id']),
                style={
                    'width': '64px',
                    'height': '64px',
                    'marginBottom': SPACING['md'],
                }
            ),
            
            # Title
            html.H3(
                role['title'],
                style={
                    'fontSize': FONTS['2xl'],
                    'fontWeight': FONTS['weight_bold'],
                    'color': role['color'],
                    'marginBottom': SPACING['sm'],
                }
            ),
            
            # Description
            html.P(
                role['description'],
                style={
                    'fontSize': FONTS['base'],
                    'color': COLORS['text_secondary'],
                    'marginBottom': SPACING['md'],
                }
            ),
            
            # Arrow icon (FIXED: Using text arrow instead of SVG)
            html.Span(
                "→",  # Unicode arrow character
                style={
                    'fontSize': FONTS['3xl'],
                    'color': role['color'],
                    'fontWeight': FONTS['weight_bold'],
                }
            ),
            
        ], style={
            'backgroundColor': COLORS['bg_card'],
            'borderRadius': RADIUS['xl'],
            'padding': SPACING['2xl'],
            'textAlign': 'center',
            'border': f"2px solid {COLORS['border']}",
            'transition': 'all 0.3s',
            'cursor': 'pointer',
            'minHeight': '280px',
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',
            'justifyContent': 'center',
        }, className='role-card'),  # For hover effect
        
        href=role['link'],
        style={'textDecoration': 'none'}
    )


def create_footer():
    """Create footer"""
    return html.Div([
        html.P(
            "Atau langsung ke dashboard lengkap →",
            style={'color': COLORS['text_muted'], 'marginBottom': SPACING['sm']}
        ),
        html.A(
            "Dashboard Lengkap",
            href="/all",
            style={
                'color': COLORS['primary'],
                'fontSize': FONTS['lg'],
                'fontWeight': FONTS['weight_semibold'],
                'textDecoration': 'none',
            }
        ),
    ], style={
        'textAlign': 'center',
        'paddingTop': SPACING['2xl'],
        'paddingBottom': SPACING['xl'],
    })