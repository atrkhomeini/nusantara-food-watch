# 🎨 NUSANTARA FOOD WATCH - DESIGN SYSTEM
# Single Source of Truth untuk semua developers
# Updated: Custom color scheme + Google Fonts + Icon paths

"""
IMPORTANT: All developers MUST use these constants!
DO NOT hardcode colors, fonts, or spacing in your pages.
Always import from this file.

Usage:
    from web.design_system import COLORS, FONTS, SPACING, ICONS
"""

import os

# ============================================================================
# 1. COLOR PALETTE (CUSTOM YELLOW-OLIVE THEME)
# ============================================================================

COLORS = {
    # Primary Colors (Yellow Theme)
    'primary': '#FDDA24',           # Bright yellow - main brand color
    'primary_dark': '#B59E25',      # Darker yellow for accents
    'primary_light': '#FEE66D',     # Light yellow for highlights
    
    # Secondary Colors
    'secondary': '#B59E25',         # Olive yellow
    'secondary_dark': '#8B7A1C',    # Darker olive
    'secondary_light': '#D4C450',   # Light olive
    
    # Status Colors
    'success': '#8CB525',           # Olive green - price down, good
    'success_light': '#A8D030',     # Light olive green
    'success_dark': '#6E911D',      # Dark olive green
    
    'warning': '#F8A22D',           # Orange - watch, moderate
    'warning_light': '#FABC5E',     # Light orange
    'warning_dark': '#E08A1A',      # Dark orange
    
    'danger': '#EF3340',            # Red - price up, alert
    'danger_light': '#F36670',      # Light red
    'danger_dark': '#C92733',       # Dark red
    
    'info': '#3B82F6',              # Blue - information
    'info_light': '#60A5FA',        # Light blue
    'info_dark': '#2563EB',         # Dark blue
    
    # Neutral Colors
    'neutral': '#E5E5E5',           # For text/icons - stable prices
    'neutral_light': '#F5F5F5',     # Very light gray
    'neutral_dark': '#A3A3A3',      # Dark gray
    
    # Background Colors (Dark Theme)
    'bg_main': '#1A1A1A',           # Main background (darker)
    'bg_card': '#262626',           # Card background
    'bg_hover': '#333333',          # Hover state
    'bg_dark': '#0A0A0A',           # Even darker for contrast
    
    # Text Colors (Adjusted for Dark Theme)
    'text_primary': '#FFFFFF',      # White text for dark bg
    'text_secondary': '#E5E5E5',    # Light gray text
    'text_muted': '#A3A3A3',        # Muted gray text
    'text_dark': '#1A1A1A',         # Dark text (for light backgrounds)
    
    # Border Colors
    'border': '#333333',            # Subtle border on dark
    'border_dark': '#262626',       # Darker border
    'border_focus': '#FDDA24',      # Yellow focus border
}


# ============================================================================
# 2. TYPOGRAPHY (GOOGLE FONTS)
# ============================================================================

FONTS = {
    # Google Font Families
    'family': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    'family_display': "'Poppins', 'Inter', sans-serif",  # For headings
    'family_mono': "'Fira Code', 'Courier New', monospace",
    
    # Google Fonts Import URLs
    'google_fonts_url': 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&family=Fira+Code:wght@400;500&display=swap',
    
    # Font Sizes
    'xs': '0.75rem',    # 12px
    'sm': '0.875rem',   # 14px
    'base': '1rem',     # 16px
    'lg': '1.125rem',   # 18px
    'xl': '1.25rem',    # 20px
    '2xl': '1.5rem',    # 24px
    '3xl': '1.875rem',  # 30px
    '4xl': '2.25rem',   # 36px
    '5xl': '3rem',      # 48px
    
    # Font Weights
    'weight_normal': 400,
    'weight_medium': 500,
    'weight_semibold': 600,
    'weight_bold': 700,
    'weight_extrabold': 800,
    
    # Line Heights
    'leading_tight': 1.25,
    'leading_normal': 1.5,
    'leading_relaxed': 1.75,
}


# ============================================================================
# 3. SPACING
# ============================================================================

SPACING = {
    'xs': '0.25rem',   # 4px
    'sm': '0.5rem',    # 8px
    'md': '1rem',      # 16px
    'lg': '1.5rem',    # 24px
    'xl': '2rem',      # 32px
    '2xl': '3rem',     # 48px
    '3xl': '4rem',     # 64px
    '4xl': '6rem',     # 96px
}


# ============================================================================
# 4. BORDER RADIUS
# ============================================================================

RADIUS = {
    'sm': '0.25rem',   # 4px
    'md': '0.5rem',    # 8px
    'lg': '0.75rem',   # 12px
    'xl': '1rem',      # 16px
    '2xl': '1.5rem',   # 24px
    'full': '9999px',  # Fully rounded
}


# ============================================================================
# 5. SHADOWS (Adjusted for Dark Theme)
# ============================================================================

SHADOWS = {
    'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.3)',
    'md': '0 1px 3px 0 rgba(0, 0, 0, 0.4)',
    'lg': '0 4px 6px -1px rgba(0, 0, 0, 0.5)',
    'xl': '0 10px 15px -3px rgba(0, 0, 0, 0.6)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.7)',
    
    # Glow effects for dark theme
    'glow_primary': f'0 0 20px rgba(253, 218, 36, 0.3)',
    'glow_success': f'0 0 20px rgba(140, 181, 37, 0.3)',
    'glow_danger': f'0 0 20px rgba(239, 51, 64, 0.3)',
}


# ============================================================================
# 6. BREAKPOINTS (Responsive)
# ============================================================================

BREAKPOINTS = {
    'mobile': '640px',
    'tablet': '768px',
    'desktop': '1024px',
    'wide': '1280px',
    'ultrawide': '1536px',
}


# ============================================================================
# 7. ICON PATHS (From web/assets/icons/)
# ============================================================================

ICONS = {
    # Base path for icons
    'base_path': '/assets/icons/',
    
    # Commodities (PNG/SVG files)
    'commodities': {
        'Beras': 'rice.png',
        'Daging Ayam': 'chicken.png',
        'Daging Sapi': 'beef.png',
        'Telur Ayam': 'egg.png',
        'Bawang Merah': 'onion-red.png',
        'Bawang Putih': 'garlic.png',
        'Cabai Merah': 'chili-red.png',
        'Cabai Rawit': 'chili-green.png',
        'Minyak Goreng': 'oil.png',
        'Gula Pasir': 'sugar.png',
    },
    
    # User roles
    'user_roles': {
        'government': 'role-government.png',
        'consumer': 'role-consumer.png',
        'trader': 'role-trader.png',
        'researcher': 'role-researcher.png',
    },
    
    # Status icons
    'status': {
        'up': 'arrow-up.png',
        'down': 'arrow-down.png',
        'stable': 'arrow-right.png',
        'alert': 'alert.png',
        'warning': 'warning.png',
        'success': 'success.png',
        'info': 'info.png',
    },
    
    # UI icons
    'ui': {
        'menu': 'menu.png',
        'close': 'close.png',
        'search': 'search.png',
        'filter': 'filter.png',
        'download': 'download.png',
        'upload': 'upload.png',
        'calendar': 'calendar.png',
        'location': 'location.png',
        'settings': 'settings.png',
    },
}


# ============================================================================
# 8. COMPONENT STYLES (Base Styles for Common Components)
# ============================================================================

COMPONENT_STYLES = {
    # Card Style (Dark theme)
    'card': {
        'backgroundColor': COLORS['bg_card'],
        'borderRadius': RADIUS['lg'],
        'padding': SPACING['lg'],
        'boxShadow': SHADOWS['md'],
        'marginBottom': SPACING['lg'],
        'border': f"1px solid {COLORS['border']}",
    },
    
    # Button Primary (Yellow)
    'button_primary': {
        'backgroundColor': COLORS['primary'],
        'color': COLORS['text_dark'],  # Dark text on yellow
        'border': 'none',
        'borderRadius': RADIUS['md'],
        'padding': f"{SPACING['sm']} {SPACING['lg']}",
        'fontSize': FONTS['base'],
        'fontWeight': FONTS['weight_semibold'],
        'cursor': 'pointer',
        'transition': 'all 0.2s',
        'boxShadow': SHADOWS['glow_primary'],
    },
    
    # Button Secondary
    'button_secondary': {
        'backgroundColor': 'transparent',
        'color': COLORS['primary'],
        'border': f"2px solid {COLORS['primary']}",
        'borderRadius': RADIUS['md'],
        'padding': f"{SPACING['sm']} {SPACING['lg']}",
        'fontSize': FONTS['base'],
        'fontWeight': FONTS['weight_semibold'],
        'cursor': 'pointer',
        'transition': 'all 0.2s',
    },
    
    # Input/Dropdown Style (Dark theme)
    'input': {
        'backgroundColor': COLORS['bg_hover'],
        'color': COLORS['text_primary'],
        'border': f"2px solid {COLORS['border']}",
        'borderRadius': RADIUS['md'],
        'padding': SPACING['sm'],
        'fontSize': FONTS['base'],
        'minHeight': '45px',
    },
    
    # Heading Styles (Light text on dark)
    'heading_1': {
        'fontSize': FONTS['4xl'],
        'fontFamily': FONTS['family_display'],
        'fontWeight': FONTS['weight_bold'],
        'color': COLORS['text_primary'],
        'marginBottom': SPACING['md'],
    },
    
    'heading_2': {
        'fontSize': FONTS['3xl'],
        'fontFamily': FONTS['family_display'],
        'fontWeight': FONTS['weight_semibold'],
        'color': COLORS['text_primary'],
        'marginBottom': SPACING['sm'],
    },
    
    'heading_3': {
        'fontSize': FONTS['2xl'],
        'fontFamily': FONTS['family_display'],
        'fontWeight': FONTS['weight_semibold'],
        'color': COLORS['text_primary'],
        'marginBottom': SPACING['sm'],
    },
}


# ============================================================================
# 9. CHART STYLES (Plotly Chart Configurations)
# ============================================================================

CHART_STYLES = {
    # Default Chart Layout (Dark theme)
    'layout': {
        'template': 'plotly_dark',
        'font': {
            'family': FONTS['family'],
            'size': 14,
            'color': COLORS['text_primary'],
        },
        'paper_bgcolor': COLORS['bg_card'],
        'plot_bgcolor': COLORS['bg_main'],
        'hovermode': 'x unified',
        'margin': {'l': 60, 'r': 40, 't': 60, 'b': 60},
    },
    
    # Line Chart Colors (Yellow-Olive theme)
    'line_colors': [
        COLORS['primary'],      # Yellow
        COLORS['success'],      # Olive green
        COLORS['warning'],      # Orange
        COLORS['info'],         # Blue
        COLORS['danger'],       # Red
        COLORS['secondary'],    # Olive yellow
    ],
    
    # Bar Chart Colors by Quality
    'bar_colors': {
        'Low': COLORS['success'],       # Green = cheap = good
        'Medium': COLORS['warning'],    # Orange = medium
        'Premium': COLORS['danger'],    # Red = expensive
        'Standard': COLORS['neutral'],  # Gray = standard
    },
}


# ============================================================================
# 10. UTILITY FUNCTIONS
# ============================================================================

def get_icon_path(category, name):
    """
    Get full path for icon file
    
    Args:
        category (str): Icon category ('commodities', 'user_roles', 'status', 'ui')
        name (str): Icon name
    
    Returns:
        str: Full path to icon
    
    Example:
        get_icon_path('commodities', 'Beras')  # → '/assets/icons/rice.png'
    """
    base = ICONS['base_path']
    filename = ICONS.get(category, {}).get(name, 'default.png')
    return f"{base}{filename}"


def get_trend_color(change_percent):
    """Get color based on price change percentage"""
    if change_percent > 5:
        return COLORS['danger']
    elif change_percent > 0:
        return COLORS['warning']
    elif change_percent < -5:
        return COLORS['success']
    else:
        return COLORS['neutral']


def get_trend_icon(change_percent):
    """Get icon path based on price change"""
    if change_percent > 1:
        return get_icon_path('status', 'up')
    elif change_percent < -1:
        return get_icon_path('status', 'down')
    else:
        return get_icon_path('status', 'stable')


def format_currency(value):
    """Format number as Indonesian Rupiah"""
    return f"Rp {value:,.0f}"


def format_percent(value):
    """Format number as percentage"""
    return f"{value:+.1f}%"


# ============================================================================
# 11. GOOGLE FONTS LINK (For HTML Head)
# ============================================================================

def get_google_fonts_link():
    """
    Get Google Fonts link tag for HTML head
    
    Returns:
        str: HTML link tag for Google Fonts
    
    Usage in Dash:
        app.index_string = f'''
        <!DOCTYPE html>
        <html>
            <head>
                {get_google_fonts_link()}
                {{%metas%}}
                {{%css%}}
            </head>
            <body>
                {{%app_entry%}}
                {{%config%}}
                {{%scripts%}}
                {{%renderer%}}
            </body>
        </html>
        '''
    """
    return f'<link href="{FONTS["google_fonts_url"]}" rel="stylesheet">'


# ============================================================================
# 12. VALIDATION
# ============================================================================

def validate_design_system():
    """Run this to verify all constants are properly defined"""
    errors = []
    
    # Check colors
    required_colors = ['primary', 'success', 'danger', 'warning', 'bg_main', 'bg_card', 'text_primary']
    for color in required_colors:
        if color not in COLORS:
            errors.append(f"Missing required color: {color}")
    
    # Check fonts
    required_fonts = ['family', 'base', 'weight_normal', 'google_fonts_url']
    for font in required_fonts:
        if font not in FONTS:
            errors.append(f"Missing required font: {font}")
    
    # Check icon paths exist (will need actual files)
    if not os.path.exists('web/assets/icons'):
        errors.append("Warning: web/assets/icons directory not found")
    
    if errors:
        print("❌ Design System Validation Failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ Design System Validation Passed!")
        print(f"✅ Color scheme: Yellow-Olive theme")
        print(f"✅ Theme: Dark mode")
        print(f"✅ Fonts: Google Fonts (Inter, Poppins, Fira Code)")
        print(f"✅ Icons: File-based from /assets/icons/")
        return True


# ============================================================================
# 13. EXPORT
# ============================================================================

__all__ = [
    'COLORS',
    'FONTS',
    'SPACING',
    'RADIUS',
    'SHADOWS',
    'BREAKPOINTS',
    'ICONS',
    'COMPONENT_STYLES',
    'CHART_STYLES',
    'get_icon_path',
    'get_trend_color',
    'get_trend_icon',
    'format_currency',
    'format_percent',
    'get_google_fonts_link',
]


# Run validation when imported
if __name__ == "__main__":
    validate_design_system()