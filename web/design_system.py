# 🎨 NUSANTARA FOOD WATCH - DESIGN SYSTEM (FINAL VERSION)
# Updated: Inline SVG support for UI icons

"""
Usage:
    from web.design_system import COLORS, FONTS, get_svg_icon
"""

import os

# ============================================================================
# 1. COLOR PALETTE
# ============================================================================

COLORS = {
    'primary': '#FDDA24',
    'primary_dark': '#B59E25',
    'primary_light': '#FEE66D',
    
    'secondary': '#B59E25',
    'secondary_dark': '#8B7A1C',
    'secondary_light': '#D4C450',
    
    'success': '#8CB525',
    'success_light': '#A8D030',
    'success_dark': '#6E911D',
    
    'warning': '#F8A22D',
    'warning_light': '#FABC5E',
    'warning_dark': '#E08A1A',
    
    'danger': '#EF3340',
    'danger_light': '#F36670',
    'danger_dark': '#C92733',
    
    'info': '#3B82F6',
    'info_light': '#60A5FA',
    'info_dark': '#2563EB',
    
    'neutral': '#E5E5E5',
    'neutral_light': '#F5F5F5',
    'neutral_dark': '#A3A3A3',
    
    'bg_main': '#1A1A1A',
    'bg_card': '#262626',
    'bg_hover': '#333333',
    'bg_dark': '#0A0A0A',
    
    'text_primary': '#FFFFFF',
    'text_secondary': '#E5E5E5',
    'text_muted': '#A3A3A3',
    'text_dark': '#1A1A1A',
    
    'border': '#333333',
    'border_dark': '#262626',
    'border_focus': '#FDDA24',
}

# ============================================================================
# 2. TYPOGRAPHY (GOOGLE FONTS)
# ============================================================================

FONTS = {
    'family': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    'family_display': "'Poppins', 'Inter', sans-serif",
    'family_mono': "'Fira Code', 'Courier New', monospace",
    'google_fonts_url': 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&family=Fira+Code:wght@400;500&display=swap',
    
    'xs': '0.75rem', 'sm': '0.875rem', 'base': '1rem', 'lg': '1.125rem',
    'xl': '1.25rem', '2xl': '1.5rem', '3xl': '1.875rem', '4xl': '2.25rem', '5xl': '3rem',
    
    'weight_normal': 400, 'weight_medium': 500, 'weight_semibold': 600,
    'weight_bold': 700, 'weight_extrabold': 800,
    
    'leading_tight': 1.25, 'leading_normal': 1.5, 'leading_relaxed': 1.75,
}

# ============================================================================
# 3. SPACING & LAYOUT
# ============================================================================

SPACING = {
    'xs': '0.25rem', 'sm': '0.5rem', 'md': '1rem', 'lg': '1.5rem',
    'xl': '2rem', '2xl': '3rem', '3xl': '4rem', '4xl': '6rem',
}

RADIUS = {
    'sm': '0.25rem', 'md': '0.5rem', 'lg': '0.75rem',
    'xl': '1rem', '2xl': '1.5rem', 'full': '9999px',
}

SHADOWS = {
    'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.3)',
    'md': '0 1px 3px 0 rgba(0, 0, 0, 0.4)',
    'lg': '0 4px 6px -1px rgba(0, 0, 0, 0.5)',
    'xl': '0 10px 15px -3px rgba(0, 0, 0, 0.6)',
    '2xl': '0 25px 50px -12px rgba(0, 0, 0, 0.7)',
    'glow_primary': '0 0 20px rgba(253, 218, 36, 0.3)',
    'glow_success': '0 0 20px rgba(140, 181, 37, 0.3)',
    'glow_danger': '0 0 20px rgba(239, 51, 64, 0.3)',
}

BREAKPOINTS = {
    'mobile': '640px', 'tablet': '768px', 'desktop': '1024px',
    'wide': '1280px', 'ultrawide': '1536px',
}

# ============================================================================
# 4. SVG ICONS (INLINE)
# ============================================================================

SVG_ICONS = {
    'arrow-up': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25Zm.53 5.47a.75.75 0 0 0-1.06 0l-3 3a.75.75 0 1 0 1.06 1.06l1.72-1.72v5.69a.75.75 0 0 0 1.5 0v-5.69l1.72 1.72a.75.75 0 1 0 1.06-1.06l-3-3Z" clip-rule="evenodd" />
</svg>''',
    
    'arrow-down': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25Zm-.53 14.03a.75.75 0 0 0 1.06 0l3-3a.75.75 0 1 0-1.06-1.06l-1.72 1.72V8.25a.75.75 0 0 0-1.5 0v5.69l-1.72-1.72a.75.75 0 0 0-1.06 1.06l3 3Z" clip-rule="evenodd" />
</svg>''',
    
    'arrow-right': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25Zm4.28 10.28a.75.75 0 0 0 0-1.06l-3-3a.75.75 0 1 0-1.06 1.06l1.72 1.72H8.25a.75.75 0 0 0 0 1.5h5.69l-1.72 1.72a.75.75 0 1 0 1.06 1.06l3-3Z" clip-rule="evenodd" />
</svg>''',
    
    'arrow-left': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25Zm-4.28 9.22a.75.75 0 0 0 0 1.06l3 3a.75.75 0 1 0 1.06-1.06l-1.72-1.72h5.69a.75.75 0 0 0 0-1.5h-5.69l1.72-1.72a.75.75 0 0 0-1.06-1.06l-3 3Z" clip-rule="evenodd" />
</svg>''',
    
    'menu': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path fill-rule="evenodd" d="M3 6.75A.75.75 0 0 1 3.75 6h16.5a.75.75 0 0 1 0 1.5H3.75A.75.75 0 0 1 3 6.75ZM3 12a.75.75 0 0 1 .75-.75h16.5a.75.75 0 0 1 0 1.5H3.75A.75.75 0 0 1 3 12Zm0 5.25a.75.75 0 0 1 .75-.75h16.5a.75.75 0 0 1 0 1.5H3.75a.75.75 0 0 1-.75-.75Z" clip-rule="evenodd" />
</svg>''',
    
    'close': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25Zm-1.72 6.97a.75.75 0 1 0-1.06 1.06L10.94 12l-1.72 1.72a.75.75 0 1 0 1.06 1.06L12 13.06l1.72 1.72a.75.75 0 1 0 1.06-1.06L13.06 12l1.72-1.72a.75.75 0 1 0-1.06-1.06L12 10.94l-1.72-1.72Z" clip-rule="evenodd" />
</svg>''',
    
    'search': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M8.25 10.875a2.625 2.625 0 1 1 5.25 0 2.625 2.625 0 0 1-5.25 0Z" />
  <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25Zm-1.125 4.5a4.125 4.125 0 1 0 2.338 7.524l2.007 2.006a.75.75 0 1 0 1.06-1.06l-2.006-2.007a4.125 4.125 0 0 0-3.399-6.463Z" clip-rule="evenodd" />
</svg>''',
    
    'filter': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M6 12a.75.75 0 0 1-.75-.75v-7.5a.75.75 0 1 1 1.5 0v7.5A.75.75 0 0 1 6 12ZM18 12a.75.75 0 0 1-.75-.75v-7.5a.75.75 0 0 1 1.5 0v7.5A.75.75 0 0 1 18 12ZM6.75 20.25v-1.5a.75.75 0 0 0-1.5 0v1.5a.75.75 0 0 0 1.5 0ZM18.75 18.75v1.5a.75.75 0 0 1-1.5 0v-1.5a.75.75 0 0 1 1.5 0ZM12.75 5.25v-1.5a.75.75 0 0 0-1.5 0v1.5a.75.75 0 0 0 1.5 0ZM12 21a.75.75 0 0 1-.75-.75v-7.5a.75.75 0 0 1 1.5 0v7.5A.75.75 0 0 1 12 21ZM3.75 15a2.25 2.25 0 1 0 4.5 0 2.25 2.25 0 0 0-4.5 0ZM12 11.25a2.25 2.25 0 1 1 0-4.5 2.25 2.25 0 0 1 0 4.5ZM15.75 15a2.25 2.25 0 1 0 4.5 0 2.25 2.25 0 0 0-4.5 0Z" />
</svg>''',
    
    'upload': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M11.47 1.72a.75.75 0 0 1 1.06 0l3 3a.75.75 0 0 1-1.06 1.06l-1.72-1.72V7.5h-1.5V4.06L9.53 5.78a.75.75 0 0 1-1.06-1.06l3-3ZM11.25 7.5V15a.75.75 0 0 0 1.5 0V7.5h3.75a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-9a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h3.75Z" />
</svg>''',
    
    'download': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 1.5a.75.75 0 0 1 .75.75V7.5h-1.5V2.25A.75.75 0 0 1 12 1.5ZM11.25 7.5v5.69l-1.72-1.72a.75.75 0 0 0-1.06 1.06l3 3a.75.75 0 0 0 1.06 0l3-3a.75.75 0 1 0-1.06-1.06l-1.72 1.72V7.5h3.75a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-9a3 3 0 0 1-3-3v-9a3 3 0 0 1 3-3h3.75Z" />
</svg>''',
    
    'calendar': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="M12 11.993a.75.75 0 0 0-.75.75v.006c0 .414.336.75.75.75h.006a.75.75 0 0 0 .75-.75v-.006a.75.75 0 0 0-.75-.75H12ZM12 16.494a.75.75 0 0 0-.75.75v.005c0 .414.335.75.75.75h.005a.75.75 0 0 0 .75-.75v-.005a.75.75 0 0 0-.75-.75H12ZM8.999 17.244a.75.75 0 0 1 .75-.75h.006a.75.75 0 0 1 .75.75v.006a.75.75 0 0 1-.75.75h-.006a.75.75 0 0 1-.75-.75v-.006ZM7.499 16.494a.75.75 0 0 0-.75.75v.005c0 .414.336.75.75.75h.005a.75.75 0 0 0 .75-.75v-.005a.75.75 0 0 0-.75-.75H7.5ZM13.499 14.997a.75.75 0 0 1 .75-.75h.006a.75.75 0 0 1 .75.75v.005a.75.75 0 0 1-.75.75h-.006a.75.75 0 0 1-.75-.75v-.005ZM14.25 16.494a.75.75 0 0 0-.75.75v.006c0 .414.335.75.75.75h.005a.75.75 0 0 0 .75-.75v-.006a.75.75 0 0 0-.75-.75h-.005ZM15.75 14.995a.75.75 0 0 1 .75-.75h.005a.75.75 0 0 1 .75.75v.006a.75.75 0 0 1-.75.75H16.5a.75.75 0 0 1-.75-.75v-.006ZM13.498 12.743a.75.75 0 0 1 .75-.75h2.25a.75.75 0 1 1 0 1.5h-2.25a.75.75 0 0 1-.75-.75ZM6.748 14.993a.75.75 0 0 1 .75-.75h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1-.75-.75Z" />
  <path fill-rule="evenodd" d="M18 2.993a.75.75 0 0 0-1.5 0v1.5h-9V2.994a.75.75 0 1 0-1.5 0v1.497h-.752a3 3 0 0 0-3 3v11.252a3 3 0 0 0 3 3h13.5a3 3 0 0 0 3-3V7.492a3 3 0 0 0-3-3H18V2.993ZM3.748 18.743v-7.5a1.5 1.5 0 0 1 1.5-1.5h13.5a1.5 1.5 0 0 1 1.5 1.5v7.5a1.5 1.5 0 0 1-1.5 1.5h-13.5a1.5 1.5 0 0 1-1.5-1.5Z" clip-rule="evenodd" />
</svg>''',
    
    'location': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path fill-rule="evenodd" d="m11.54 22.351.07.04.028.016a.76.76 0 0 0 .723 0l.028-.015.071-.041a16.975 16.975 0 0 0 1.144-.742 19.58 19.58 0 0 0 2.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 0 0-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 0 0 2.682 2.282 16.975 16.975 0 0 0 1.145.742ZM12 13.5a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" clip-rule="evenodd" />
</svg>''',
    
    'settings': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path fill-rule="evenodd" d="M11.078 2.25c-.917 0-1.699.663-1.85 1.567L9.05 4.889c-.02.12-.115.26-.297.348a7.493 7.493 0 0 0-.986.57c-.166.115-.334.126-.45.083L6.3 5.508a1.875 1.875 0 0 0-2.282.819l-.922 1.597a1.875 1.875 0 0 0 .432 2.385l.84.692c.095.078.17.229.154.43a7.598 7.598 0 0 0 0 1.139c.015.2-.059.352-.153.43l-.841.692a1.875 1.875 0 0 0-.432 2.385l.922 1.597a1.875 1.875 0 0 0 2.282.818l1.019-.382c.115-.043.283-.031.45.082.312.214.641.405.985.57.182.088.277.228.297.35l.178 1.071c.151.904.933 1.567 1.85 1.567h1.844c.916 0 1.699-.663 1.85-1.567l.178-1.072c.02-.12.114-.26.297-.349.344-.165.673-.356.985-.57.167-.114.335-.125.45-.082l1.02.382a1.875 1.875 0 0 0 2.28-.819l.923-1.597a1.875 1.875 0 0 0-.432-2.385l-.84-.692c-.095-.078-.17-.229-.154-.43a7.614 7.614 0 0 0 0-1.139c-.016-.2.059-.352.153-.43l.84-.692c.708-.582.891-1.59.433-2.385l-.922-1.597a1.875 1.875 0 0 0-2.282-.818l-1.02.382c-.114.043-.282.031-.449-.083a7.49 7.49 0 0 0-.985-.57c-.183-.087-.277-.227-.297-.348l-.179-1.072a1.875 1.875 0 0 0-1.85-1.567h-1.843ZM12 15.75a3.75 3.75 0 1 0 0-7.5 3.75 3.75 0 0 0 0 7.5Z" clip-rule="evenodd" />
</svg>''',
    
    'user': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path fill-rule="evenodd" d="M18.685 19.097A9.723 9.723 0 0 0 21.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 0 0 3.065 7.097A9.716 9.716 0 0 0 12 21.75a9.716 9.716 0 0 0 6.685-2.653Zm-12.54-1.285A7.486 7.486 0 0 1 12 15a7.486 7.486 0 0 1 5.855 2.812A8.224 8.224 0 0 1 12 20.25a8.224 8.224 0 0 1-5.855-2.438ZM15.75 9a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0Z" clip-rule="evenodd" />
</svg>''',
    
    'logout': '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path fill-rule="evenodd" d="M16.5 3.75a1.5 1.5 0 0 1 1.5 1.5v13.5a1.5 1.5 0 0 1-1.5 1.5h-6a1.5 1.5 0 0 1-1.5-1.5V15a.75.75 0 0 0-1.5 0v3.75a3 3 0 0 0 3 3h6a3 3 0 0 0 3-3V5.25a3 3 0 0 0-3-3h-6a3 3 0 0 0-3 3V9A.75.75 0 1 0 9 9V5.25a1.5 1.5 0 0 1 1.5-1.5h6ZM5.78 8.47a.75.75 0 0 0-1.06 0l-3 3a.75.75 0 0 0 0 1.06l3 3a.75.75 0 0 0 1.06-1.06l-1.72-1.72H15a.75.75 0 0 0 0-1.5H4.06l1.72-1.72a.75.75 0 0 0 0-1.06Z" clip-rule="evenodd" />
</svg>''',
}

def get_svg_icon(icon_name, color=None, size='24px'):
    """
    Get SVG icon as HTML string with custom color and size
    
    Args:
        icon_name (str): Icon name from SVG_ICONS
        color (str): CSS color (default: currentColor)
        size (str): Icon size (default: '24px')
    
    Returns:
        str: SVG HTML string
    
    Example:
        >>> svg = get_svg_icon('arrow-up', color='#FDDA24', size='32px')
        >>> html.Div(dangerously_allow_html={'__html': svg})
    """
    svg = SVG_ICONS.get(icon_name, SVG_ICONS.get('menu'))  # Default to menu
    
    # Add style attributes
    style = f'width: {size}; height: {size};'
    if color and color != 'currentColor':
        style += f' color: {color};'
    
    # Insert style into SVG
    svg = svg.replace('<svg', f'<svg style="{style}"')
    
    return svg

# ============================================================================
# 5. ICON PATHS (PNG FILES)
# ============================================================================

ICONS = {
    'base_path': '/assets/icons/',  # ← CHANGE THIS!
    
    'commodities': {
        'Beras': 'commodities/rice.png',  # ← ADD subfolder!
        'Daging Ayam': 'commodities/chicken.png',
        'Daging Sapi': 'commodities/beef.png',
        'Telur Ayam': 'commodities/egg.png',
        'Bawang Merah': 'commodities/onion-red.png',
        'Bawang Putih': 'commodities/garlic.png',
        'Cabai Merah': 'commodities/chili-red.png',
        'Cabai Rawit': 'commodities/chili-green.png',
        'Minyak Goreng': 'commodities/oil.png',
        'Gula Pasir': 'commodities/sugar.png',
    },
    
    'user_roles': {
        'government': 'roles/role-government.png',  # ← ADD subfolder!
        'consumer': 'roles/role-consumer.png',
        'trader': 'roles/role-trader.png',
        'researcher': 'roles/role-researcher.png',
    },
}

def get_icon_path(category, name):
    """Get full path for PNG icon"""
    base = ICONS['base_path']
    filename = ICONS.get(category, {}).get(name, 'default.png')
    return f"{base}{filename}"

# ============================================================================
# 6. UTILITY FUNCTIONS
# ============================================================================

def format_currency(value):
    """Format as Rupiah"""
    return f"Rp {value:,.0f}"

def format_percent(value):
    """Format as percentage"""
    return f"{value:+.1f}%"

def get_trend_color(change_percent):
    """Get color based on price change"""
    if change_percent > 5:
        return COLORS['danger']
    elif change_percent > 0:
        return COLORS['warning']
    elif change_percent < -5:
        return COLORS['success']
    else:
        return COLORS['neutral']

def get_trend_icon_svg(change_percent):
    """Get trend icon SVG"""
    if change_percent > 1:
        return get_svg_icon('arrow-up', COLORS['danger'])
    elif change_percent < -1:
        return get_svg_icon('arrow-down', COLORS['success'])
    else:
        return get_svg_icon('arrow-right', COLORS['neutral'])

def get_google_fonts_link():
    """Get Google Fonts HTML link"""
    return f'<link href="{FONTS["google_fonts_url"]}" rel="stylesheet">'

# Component styles (same as before)
COMPONENT_STYLES = {
    'card': {
        'backgroundColor': COLORS['bg_card'],
        'borderRadius': RADIUS['lg'],
        'padding': SPACING['lg'],
        'boxShadow': SHADOWS['md'],
        'marginBottom': SPACING['lg'],
        'border': f"1px solid {COLORS['border']}",
    },
    'button_primary': {
        'backgroundColor': COLORS['primary'],
        'color': COLORS['text_dark'],
        'border': 'none',
        'borderRadius': RADIUS['md'],
        'padding': f"{SPACING['sm']} {SPACING['lg']}",
        'fontSize': FONTS['base'],
        'fontWeight': FONTS['weight_semibold'],
        'cursor': 'pointer',
        'transition': 'all 0.2s',
    },
    'heading_1': {
        'fontSize': FONTS['4xl'],
        'fontFamily': FONTS['family_display'],
        'fontWeight': FONTS['weight_bold'],
        'color': COLORS['text_primary'],
        'marginBottom': SPACING['md'],
    },
}

CHART_STYLES = {
    'layout': {
        'template': 'plotly_dark',
        'font': {'family': FONTS['family'], 'size': 14, 'color': COLORS['text_primary']},
        'paper_bgcolor': COLORS['bg_card'],
        'plot_bgcolor': COLORS['bg_main'],
        'hovermode': 'x unified',
        'margin': {'l': 60, 'r': 40, 't': 60, 'b': 60},
    },
    'line_colors': [COLORS['primary'], COLORS['success'], COLORS['warning'], COLORS['info'], COLORS['danger']],
}

__all__ = ['COLORS', 'FONTS', 'SPACING', 'RADIUS', 'SHADOWS', 'COMPONENT_STYLES', 'CHART_STYLES',
           'get_svg_icon', 'get_icon_path', 'format_currency', 'format_percent', 'get_trend_color',
           'get_trend_icon_svg', 'get_google_fonts_link']