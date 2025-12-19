"""
Nusantara Food Watch Dashboard
Main application entry point
"""
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from web.design_system import get_google_fonts_link, COLORS

# Initialize Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_folder='assets'  # ← ADD THIS for CSS/icons
)

# Inject Google Fonts
app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {get_google_fonts_link()}
        {{%metas%}}
        {{%css%}}
    </head>
    <body style="background-color: {COLORS['bg_main']}; margin: 0; padding: 0;">
        {{%app_entry%}}
        {{%config%}}
        {{%scripts%}}
        {{%renderer%}}
    </body>
</html>
'''

# App layout with URL routing (DEFINE FIRST!)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# THEN register routes (AFTER layout)
from web.index import register_routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)