# 🧩 NUSANTARA FOOD WATCH - COMPONENT LIBRARY (UPDATED)
# Reusable Dash Components with Yellow-Olive Dark Theme

"""
IMPORTANT: Use these components untuk consistency!
Updated for: Dark theme + Yellow-Olive colors + Icon files

Usage:
    from web.components import StatCard, PriceChart, FilterBar
"""

from dash import html, dcc
import plotly.graph_objects as go
from web.design_system import (
    COLORS, FONTS, SPACING, RADIUS, SHADOWS,
    COMPONENT_STYLES, CHART_STYLES, ICONS,
    get_icon_path, get_trend_color, get_trend_icon,
    format_currency, format_percent
)


# ============================================================================
# 1. STAT CARD COMPONENT (Dark Theme)
# ============================================================================

def create_stat_card(label, value, change_percent=None, icon_name=None, icon_category='commodities', color=None):
    """
    Create a statistic card with dark theme
    
    Args:
        label (str): Card label
        value (str): Main value to display
        change_percent (float, optional): Percentage change
        icon_name (str, optional): Icon name from ICONS dict
        icon_category (str): Icon category ('commodities', 'user_roles', etc.)
        color (str, optional): Custom background color
    
    Returns:
        html.Div: Stat card component
    
    Example:
        create_stat_card(
            "Harga Beras", 
            "Rp 12,500", 
            change_percent=2.5, 
            icon_name="Beras",
            icon_category="commodities"
        )
    """
    
    # Determine color based on change
    if color is None and change_percent is not None:
        color = get_trend_color(change_percent)
    elif color is None:
        color = COLORS['primary']
    
    # Build icon element (image instead of emoji)
    icon_element = None
    if icon_name:
        icon_path = get_icon_path(icon_category, icon_name)
        icon_element = html.Img(
            src=icon_path,
            style={
                'width': '48px',
                'height': '48px',
                'marginBottom': SPACING['sm'],
                'filter': 'brightness(1.2)',  # Brighten icons on dark bg
            }
        )
    
    # Build change indicator
    change_element = None
    if change_percent is not None:
        trend_icon_path = get_trend_icon(change_percent)
        change_text = format_percent(change_percent)
        change_element = html.Div(
            [
                html.Img(
                    src=trend_icon_path,
                    style={'width': '16px', 'height': '16px', 'marginRight': '4px'}
                ),
                html.Span(change_text),
            ],
            style={
                'fontSize': FONTS['sm'],
                'color': get_trend_color(change_percent),
                'marginTop': SPACING['xs'],
                'display': 'flex',
                'alignItems': 'center',
            }
        )
    
    return html.Div(
        [
            # Icon (if provided)
            icon_element,
            
            # Value
            html.Div(
                value,
                style={
                    'fontSize': FONTS['3xl'],
                    'fontWeight': FONTS['weight_bold'],
                    'color': COLORS['text_dark'],  # Dark text on colored bg
                    'marginBottom': SPACING['xs'],
                }
            ),
            
            # Label
            html.Div(
                label,
                style={
                    'fontSize': FONTS['sm'],
                    'color': COLORS['text_dark'],
                    'opacity': 0.9,
                }
            ),
            
            # Change indicator
            change_element,
        ],
        style={
            'backgroundColor': color,
            'borderRadius': COMPONENT_STYLES['card']['borderRadius'],
            'padding': SPACING['lg'],
            'boxShadow': SHADOWS['lg'],
            'minHeight': '160px',
            'transition': 'transform 0.2s, box-shadow 0.2s',
            'cursor': 'pointer',
        },
        className='stat-card',  # For CSS hover effects
    )


# ============================================================================
# 2. FILTER BAR COMPONENT (Dark Theme)
# ============================================================================

def create_filter_bar(filters):
    """
    Create a horizontal filter bar with dark theme
    
    Args:
        filters (list): List of dcc components (Dropdown, DatePicker, etc.)
    
    Returns:
        html.Div: Filter bar component
    """
    return html.Div(
        filters,
        style={
            **COMPONENT_STYLES['card'],
            'display': 'flex',
            'gap': SPACING['md'],
            'flexWrap': 'wrap',
            'alignItems': 'center',
        }
    )


# ============================================================================
# 3. CARD CONTAINER COMPONENT (Dark Theme)
# ============================================================================

def create_card(children, title=None, subtitle=None, icon_name=None, icon_category='ui'):
    """
    Create a card container with dark theme
    
    Args:
        children: Card content
        title (str, optional): Card title
        subtitle (str, optional): Card subtitle
        icon_name (str, optional): Icon for title
        icon_category (str): Icon category
    
    Returns:
        html.Div: Card component
    """
    header = []
    
    if title:
        title_content = [html.Span(title)]
        
        # Add icon if provided
        if icon_name:
            icon_path = get_icon_path(icon_category, icon_name)
            title_content.insert(0, html.Img(
                src=icon_path,
                style={
                    'width': '32px',
                    'height': '32px',
                    'marginRight': SPACING['sm'],
                    'verticalAlign': 'middle',
                }
            ))
        
        header.append(
            html.H3(
                title_content,
                style={
                    **COMPONENT_STYLES['heading_3'],
                    'display': 'flex',
                    'alignItems': 'center',
                }
            )
        )
    
    if subtitle:
        header.append(
            html.P(
                subtitle,
                style={
                    'fontSize': FONTS['sm'],
                    'color': COLORS['text_secondary'],
                    'marginTop': SPACING['xs'],
                    'marginBottom': SPACING['md'],
                }
            )
        )
    
    return html.Div(
        header + ([children] if not isinstance(children, list) else children),
        style=COMPONENT_STYLES['card']
    )


# ============================================================================
# 4. INSIGHT BOX COMPONENT (Dark Theme)
# ============================================================================

def create_insight_box(text, insight_type='info'):
    """
    Create an insight/tip box with dark theme
    
    Args:
        text (str): Insight text
        insight_type (str): Type ('info', 'success', 'warning', 'danger')
    
    Returns:
        html.Div: Insight box component
    """
    
    type_config = {
        'info': {
            'icon': get_icon_path('status', 'info'),
            'bg': COLORS['info'],
            'border': COLORS['info'],
        },
        'success': {
            'icon': get_icon_path('status', 'success'),
            'bg': COLORS['success'],
            'border': COLORS['success'],
        },
        'warning': {
            'icon': get_icon_path('status', 'warning'),
            'bg': COLORS['warning'],
            'border': COLORS['warning'],
        },
        'danger': {
            'icon': get_icon_path('status', 'alert'),
            'bg': COLORS['danger'],
            'border': COLORS['danger'],
        },
    }
    
    config = type_config.get(insight_type, type_config['info'])
    
    return html.Div(
        [
            html.Img(
                src=config['icon'],
                style={
                    'width': '24px',
                    'height': '24px',
                    'marginRight': SPACING['sm'],
                }
            ),
            html.Span(text, style={'flex': 1}),
        ],
        style={
            'backgroundColor': f"{config['bg']}20",  # 20% opacity
            'borderLeft': f"4px solid {config['border']}",
            'borderRadius': RADIUS['md'],
            'padding': SPACING['md'],
            'marginBottom': SPACING['md'],
            'display': 'flex',
            'alignItems': 'center',
            'fontSize': FONTS['base'],
            'color': COLORS['text_primary'],
        }
    )


# ============================================================================
# 5. LOADING COMPONENT
# ============================================================================

def create_loading(component_id, children=None):
    """
    Wrap component with loading state
    
    Args:
        component_id (str): Component ID
        children: Component to wrap
    
    Returns:
        dcc.Loading: Loading wrapper
    """
    return dcc.Loading(
        id=f"loading-{component_id}",
        type="circle",
        color=COLORS['primary'],  # Yellow spinner
        children=children if children else html.Div(id=component_id),
    )


# ============================================================================
# 6. TABLE COMPONENT (Dark Theme)
# ============================================================================

def create_table(headers, rows, max_height='400px'):
    """
    Create a styled table with dark theme
    
    Args:
        headers (list): List of header strings
        rows (list): List of row data
        max_height (str): Maximum table height
    
    Returns:
        html.Div: Table component
    """
    return html.Div(
        html.Table(
            [
                # Header
                html.Thead(
                    html.Tr([
                        html.Th(
                            header,
                            style={
                                'padding': SPACING['sm'],
                                'textAlign': 'left',
                                'borderBottom': f"2px solid {COLORS['primary']}",
                                'fontWeight': FONTS['weight_semibold'],
                                'color': COLORS['text_primary'],
                                'backgroundColor': COLORS['bg_hover'],
                            }
                        ) for header in headers
                    ])
                ),
                
                # Body
                html.Tbody([
                    html.Tr(
                        [
                            html.Td(
                                cell,
                                style={
                                    'padding': SPACING['sm'],
                                    'borderBottom': f"1px solid {COLORS['border']}",
                                    'color': COLORS['text_secondary'],
                                }
                            ) for cell in row
                        ],
                        style={
                            'transition': 'background-color 0.2s',
                        },
                        className='table-row',  # For hover effect
                    ) for row in rows
                ])
            ],
            style={'width': '100%', 'borderCollapse': 'collapse'}
        ),
        style={
            'maxHeight': max_height,
            'overflowY': 'auto',
            'borderRadius': RADIUS['md'],
        }
    )


# ============================================================================
# 7. CHART HELPERS (Dark Theme)
# ============================================================================

def create_line_chart(df, x_col, y_col, title='', labels=None, color=None):
    """
    Create a standardized line chart with dark theme
    
    Args:
        df: DataFrame
        x_col (str): X-axis column
        y_col (str): Y-axis column
        title (str): Chart title
        labels (dict): Custom labels
        color (str): Line color (default: primary yellow)
    
    Returns:
        plotly.graph_objects.Figure
    """
    import plotly.express as px
    
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=title,
        labels=labels or {},
    )
    
    # Apply yellow theme styling
    fig.update_traces(
        line_color=color or COLORS['primary'],
        line_width=3,
    )
    
    fig.update_layout(**CHART_STYLES['layout'])
    
    return fig


def create_bar_chart(df, x_col, y_col, title='', labels=None, color_col=None):
    """
    Create a standardized bar chart with dark theme
    
    Args:
        df: DataFrame
        x_col (str): X-axis column
        y_col (str): Y-axis column
        title (str): Chart title
        labels (dict): Custom labels
        color_col (str): Column for color mapping
    
    Returns:
        plotly.graph_objects.Figure
    """
    import plotly.express as px
    
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title,
        labels=labels or {},
        color=color_col,
        color_discrete_map=CHART_STYLES['bar_colors'] if color_col else None,
    )
    
    # Apply dark theme
    fig.update_layout(**CHART_STYLES['layout'])
    
    # Yellow bars if no color mapping
    if not color_col:
        fig.update_traces(marker_color=COLORS['primary'])
    
    return fig


# ============================================================================
# 8. NAVIGATION BAR (Dark Theme with Yellow Accent)
# ============================================================================

def create_navbar(active_page, user_role='consumer'):
    """
    Create navigation bar with dark theme
    
    Args:
        active_page (str): Current page
        user_role (str): User role
    
    Returns:
        html.Div: Navigation bar
    """
    role_icon_path = get_icon_path('user_roles', user_role)
    
    nav_items = [
        {'label': 'Home', 'href': '/'},
        {'label': 'Analisis', 'href': '/analisis'},
        {'label': 'Data', 'href': '/data'},
        {'label': 'About', 'href': '/about'},
    ]
    
    return html.Div(
        [
            # Logo
            html.Div(
                [
                    html.Img(
                        src=get_icon_path('commodities', 'Beras'),  # Use rice icon as logo
                        style={'width': '32px', 'height': '32px', 'marginRight': SPACING['sm']}
                    ),
                    html.Span('Nusantara Food Watch', style={'fontSize': FONTS['xl'], 'fontWeight': FONTS['weight_bold']}),
                ],
                style={'display': 'flex', 'alignItems': 'center', 'color': COLORS['primary']}
            ),
            
            # Nav items
            html.Div(
                [
                    html.A(
                        item['label'],
                        href=item['href'],
                        style={
                            'color': COLORS['primary'] if item['href'] == active_page else COLORS['text_secondary'],
                            'textDecoration': 'none',
                            'padding': f"{SPACING['sm']} {SPACING['md']}",
                            'borderRadius': RADIUS['md'],
                            'backgroundColor': COLORS['bg_hover'] if item['href'] == active_page else 'transparent',
                            'transition': 'all 0.2s',
                            'fontWeight': FONTS['weight_medium'],
                        }
                    ) for item in nav_items
                ],
                style={'display': 'flex', 'gap': SPACING['sm']}
            ),
            
            # User role indicator
            html.Div(
                [
                    html.Img(
                        src=role_icon_path,
                        style={'width': '24px', 'height': '24px', 'marginRight': SPACING['xs']}
                    ),
                    html.Span(user_role.title()),
                ],
                style={
                    'display': 'flex',
                    'alignItems': 'center',
                    'color': COLORS['text_secondary'],
                    'fontSize': FONTS['sm'],
                }
            ),
        ],
        style={
            'backgroundColor': COLORS['bg_card'],
            'padding': SPACING['lg'],
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'boxShadow': SHADOWS['lg'],
            'borderBottom': f"2px solid {COLORS['primary']}",
        }
    )


# ============================================================================
# 9. EXPORT
# ============================================================================

__all__ = [
    'create_stat_card',
    'create_filter_bar',
    'create_card',
    'create_insight_box',
    'create_loading',
    'create_table',
    'create_line_chart',
    'create_bar_chart',
    'create_navbar',
]