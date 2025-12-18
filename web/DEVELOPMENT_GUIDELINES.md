# 🚀 NUSANTARA FOOD WATCH - DEVELOPMENT GUIDELINES (UPDATED)
# Updated for: New project structure + Yellow-Olive dark theme + Icon files

## **📁 PROJECT STRUCTURE**

```
nusantara_food/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py                     # Main entry point
├── backfill_unified.py        # Historical data backfill
├── daily_scraper.py           # Daily scraper
│
├── .github/
│   └── workflows/
│       └── daily_scraper.yml  # GitHub Actions automation
│
├── data/                       # Data storage (gitignored)
│   ├── raw/                   # Raw scraped data
│   ├── interim/               # Intermediate processing
│   └── processed/             # Analysis-ready data
│
├── dump/                       # Temporary files (gitignored)
│
├── notebooks/                  # Jupyter notebooks for analysis
│   ├── 01_data_extraction.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_exploratory_analysis.ipynb
│   ├── 04_visualization.ipynb
│   ├── 05_forecasting.ipynb
│   └── COMPLETE_DOCUMENTATION.md
│
├── reports/                    # Generated reports
│   └── figures/               # Saved visualizations
│
├── src/                        # Source code modules
│   ├── __init__.py
│   │
│   ├── db/                    # Database modules
│   │   ├── __init__.py
│   │   ├── nusantara_db.py   # Database connection & queries
│   │   └── normalization/    # Migration scripts
│   │
│   ├── scraper/               # Scraping modules
│   │   ├── __init__.py
│   │   ├── pihps_scraper.py  # Core scraper
│   │   └── debug/            # Debug utilities
│   │
│   ├── data_analysis/         # Analysis modules
│   │   ├── __init__.py
│   │   ├── cleaning.py       # Data cleaning
│   │   ├── forecast.py       # Forecasting models
│   │   └── visualize.py      # Visualization helpers
│   │
│   ├── models/                # ML models (future)
│   │   └── __init__.py
│   │
│   └── utils/                 # Utility modules
│       ├── __init__.py
│       └── notifications.py  # Email notifications
│
├── analysis/                   # ⭐ NEW: Analysis scripts
│   ├── processing/            # Data processing scripts
│   │   └── *.py
│   └── queries/               # SQL queries
│       └── *.sql
│
└── web/                        # ⭐ Dashboard application
    ├── main.py                # Dash app entry point
    ├── index.py               # URL routing
    ├── design_system.py       # ⭐ SINGLE SOURCE OF TRUTH
    ├── components.py          # ⭐ Reusable components
    ├── README.md
    ├── requirements.txt
    │
    ├── assets/                # Static assets
    │   ├── style/            # CSS files
    │   │   └── custom.css
    │   └── icons/            # ⭐ Icon files (PNG/SVG)
    │       ├── rice.png
    │       ├── chicken.png
    │       ├── arrow-up.png
    │       └── ... (see ICON_LIST.md)
    │
    ├── pages/                 # Page modules
    │   ├── __init__.py
    │   ├── landing.py         # Landing page
    │   ├── home_consumer.py   # Consumer homepage
    │   ├── home_government.py # Government homepage
    │   ├── home_trader.py     # Trader homepage
    │   ├── home_researcher.py # Researcher homepage
    │   ├── all_user.py        # Shared pages
    │   └── about_page.py      # About page
    │
    └── utils/                 # Dashboard utilities
        ├── __init__.py
        ├── config.py          # Configuration
        └── helpers.py         # Helper functions
```

---

## **🎨 DESIGN SYSTEM (Yellow-Olive Dark Theme)**

### **Color Palette:**

```python
# Primary Colors
'primary': '#FDDA24'           # Bright yellow
'primary_dark': '#B59E25'      # Dark yellow

# Status Colors
'success': '#8CB525'           # Olive green (good)
'warning': '#F8A22D'           # Orange (watch)
'danger': '#EF3340'            # Red (alert)

# Backgrounds (Dark Theme)
'bg_main': '#1A1A1A'           # Main background
'bg_card': '#262626'           # Card background
'bg_hover': '#333333'          # Hover state

# Text (Light on Dark)
'text_primary': '#FFFFFF'      # White text
'text_secondary': '#E5E5E5'    # Gray text
```

### **Typography (Google Fonts):**

```python
# Font Families
'family': 'Inter'              # Body text
'family_display': 'Poppins'    # Headings
'family_mono': 'Fira Code'     # Code

# Import in HTML:
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=swap" rel="stylesheet">
```

### **Icons (File-based):**

```python
# Location: web/assets/icons/
# Format: PNG or SVG

# Usage:
from web.design_system import get_icon_path

icon_path = get_icon_path('commodities', 'Beras')
# Returns: '/assets/icons/rice.png'

html.Img(src=icon_path, style={'width': '32px'})
```

---

## **📋 CODING STANDARDS**

### **1. Always Import Design System**

```python
# ✅ CORRECT
from web.design_system import COLORS, FONTS, SPACING
from web.components import create_stat_card, create_card

def my_component():
    return html.Div(
        "Hello",
        style={'color': COLORS['primary']}  # Yellow
    )

# ❌ WRONG
def my_component():
    return html.Div(
        "Hello",
        style={'color': '#FDDA24'}  # Hardcoded!
    )
```

---

### **2. Use File-based Icons**

```python
# ✅ CORRECT
from web.design_system import get_icon_path

icon = html.Img(
    src=get_icon_path('commodities', 'Beras'),
    style={'width': '32px', 'height': '32px'}
)

# ❌ WRONG
icon = html.Span('🍚')  # Emoji not supported anymore
```

---

### **3. Dark Theme Styling**

```python
# ✅ CORRECT - Light text on dark background
html.Div(
    "Content",
    style={
        'backgroundColor': COLORS['bg_card'],  # Dark
        'color': COLORS['text_primary'],       # Light text
    }
)

# ❌ WRONG - Dark text on dark background
html.Div(
    "Content",
    style={
        'backgroundColor': COLORS['bg_card'],
        'color': '#000000',  # Can't read!
    }
)
```

---

### **4. File Structure for Pages**

Every page file should follow this structure:

```python
"""
Page: Consumer Homepage
Author: [Your Name]
Description: Homepage for consumer role with forecast
Updated: YYYY-MM-DD
"""

from dash import html, dcc, Input, Output, callback
from web.design_system import COLORS, FONTS, SPACING
from web.components import create_stat_card, create_card
from analysis.processing.price_data import get_current_prices  # ⭐ NEW path


# ============================================================================
# 1. LAYOUT DEFINITION
# ============================================================================

def layout():
    """Main layout"""
    return html.Div([
        create_header(),
        create_content(),
    ], style={'backgroundColor': COLORS['bg_main']})  # Dark background


# ============================================================================
# 2. COMPONENT FUNCTIONS
# ============================================================================

def create_header():
    """Create page header"""
    return html.Div(
        html.H1("Consumer Dashboard", style=COMPONENT_STYLES['heading_1']),
        style={'padding': SPACING['xl']}
    )


def create_content():
    """Create main content"""
    return html.Div([
        create_stat_card(
            label="Harga Beras",
            value="Rp 12,500",
            change_percent=2.5,
            icon_name="Beras",           # ⭐ Use icon name
            icon_category="commodities"
        ),
    ])


# ============================================================================
# 3. CALLBACKS
# ============================================================================

@callback(
    Output('chart', 'figure'),
    Input('dropdown', 'value')
)
def update_chart(value):
    """Update chart callback"""
    pass
```

---

## **🖼️ ICON MANAGEMENT**

### **Required Icons (Place in `web/assets/icons/`):**

See `ICON_LIST.md` for complete list.

**Categories:**
1. **Commodities** (rice.png, chicken.png, etc.)
2. **User Roles** (role-consumer.png, role-trader.png, etc.)
3. **Status** (arrow-up.png, arrow-down.png, alert.png, etc.)
4. **UI** (menu.png, search.png, download.png, etc.)

**Icon Guidelines:**
- Format: PNG or SVG
- Size: 256x256px or 512x512px
- Style: Flat, modern, consistent
- Colors: Monochrome or yellow-olive theme
- Background: Transparent

**Where to find:**
- [Flaticon](https://www.flaticon.com/)
- [Noun Project](https://thenounproject.com/)
- [Font Awesome](https://fontawesome.com/) (export as PNG)
- [Material Icons](https://fonts.google.com/icons)

---

## **🔄 GIT WORKFLOW**

### **Branch Naming:**

```
feature/consumer-homepage       # New feature
fix/chart-dark-theme           # Bug fix
refactor/update-icons          # Code refactor
docs/update-readme             # Documentation
style/apply-yellow-theme       # Styling
```

### **Commit Messages:**

```bash
feat: add price forecast to consumer homepage
fix: correct icon paths in stat cards
refactor: migrate to file-based icons
docs: update icon list
style: apply yellow-olive dark theme
```

---

## **📊 DATA ANALYSIS WORKFLOW**

### **Processing Scripts (analysis/processing/):**

```python
# analysis/processing/price_forecast.py

def calculate_forecast(commodity_id, days=7):
    """
    Calculate price forecast
    
    Args:
        commodity_id (int): Commodity ID
        days (int): Forecast days
        
    Returns:
        pd.DataFrame: Forecast data
    """
    # Query from database
    # Apply forecasting model
    # Return results
    pass
```

### **SQL Queries (analysis/queries/):**

```sql
-- analysis/queries/get_latest_prices.sql

SELECT 
    c.commodity_name,
    p.province_name,
    fp.harga,
    fp.tanggal
FROM fact_prices fp
JOIN dim_commodities c ON fp.commodity_id = c.commodity_id
JOIN dim_provinces p ON fp.province_id = p.province_id
WHERE fp.tanggal = (SELECT MAX(tanggal) FROM fact_prices)
ORDER BY c.commodity_name, p.province_name;
```

### **Usage in Dashboard:**

```python
# web/pages/home_consumer.py

from analysis.processing.price_forecast import calculate_forecast
from analysis.queries import get_latest_prices  # Load SQL query

@callback(...)
def update_forecast(...):
    df = calculate_forecast(commodity_id, days=7)
    return create_line_chart(df, 'date', 'price')
```

---

## **🚀 DEVELOPMENT WORKFLOW**

### **Step 1: Setup Environment**

```bash
# Clone repo
git clone <repo-url>
cd nusantara_food

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r web/requirements.txt

# Download icons (see ICON_LIST.md)
# Place in web/assets/icons/
```

---

### **Step 2: Development Cycle**

```bash
# 1. Create feature branch
git checkout -b feature/consumer-homepage

# 2. Make changes
# - Follow design_system.py
# - Use components.py
# - Use file-based icons

# 3. Test dashboard
cd web
python main.py
# Open http://localhost:8050

# 4. Test with dark theme
# Verify contrast, icon visibility

# 5. Commit and push
git add .
git commit -m "feat: add consumer homepage"
git push origin feature/consumer-homepage

# 6. Create Pull Request
```

---

## **✅ PRE-COMMIT CHECKLIST**

Before committing, verify:

```
[ ] All colors from design_system.py (no hardcoded #FDDA24)
[ ] All icons from web/assets/icons/ (no emoji text)
[ ] Dark theme: Light text on dark background
[ ] Google Fonts loaded in HTML
[ ] No console.log or print statements
[ ] Tested in dark mode
[ ] Icons visible and properly sized
[ ] Tested locally (app runs without errors)
[ ] No merge conflicts
```

---

## **🎨 DARK THEME BEST PRACTICES**

### **1. Text Contrast:**

```python
# ✅ CORRECT
html.Div(
    "Text",
    style={
        'backgroundColor': COLORS['bg_main'],    # #1A1A1A
        'color': COLORS['text_primary']          # #FFFFFF
    }
)

# ❌ WRONG - Low contrast
html.Div(
    "Text",
    style={
        'backgroundColor': COLORS['bg_main'],    # #1A1A1A
        'color': COLORS['text_secondary']        # #E5E5E5 - harder to read
    }
)
```

### **2. Card Elevation:**

```python
# Create depth with subtle borders
style={
    'backgroundColor': COLORS['bg_card'],        # #262626
    'border': f"1px solid {COLORS['border']}",  # #333333
    'boxShadow': SHADOWS['lg'],
}
```

### **3. Interactive Elements:**

```python
# Hover states
':hover': {
    'backgroundColor': COLORS['bg_hover'],  # #333333
    'transform': 'translateY(-2px)',
    'boxShadow': SHADOWS['xl'],
}
```

---

## **🐛 DEBUGGING TIPS**

### **1. Icon Not Showing?**

```python
# Check path
print(get_icon_path('commodities', 'Beras'))
# Should print: /assets/icons/rice.png

# Verify file exists
import os
exists = os.path.exists('web/assets/icons/rice.png')
print(f"Icon exists: {exists}")
```

### **2. Dark Theme Issues?**

```python
# Check text color
style = {'color': COLORS['text_primary']}
print(style)  # Should be #FFFFFF

# Verify background
bg = COLORS['bg_main']
print(bg)  # Should be #1A1A1A
```

### **3. Google Fonts Not Loading?**

```python
# In web/main.py
from web.design_system import get_google_fonts_link

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
    </body>
</html>
'''
```

---

## **💡 TIPS FOR SUCCESS**

### **Tip 1: Icon Consistency**

All icons should be same style (flat, outlined, solid, etc.)

### **Tip 2: Dark Theme Testing**

Test in different lighting conditions:
- Bright room
- Dark room
- Different screen brightness

### **Tip 3: Color Accessibility**

Use WCAG contrast checker for text:
- Yellow (#FDDA24) on dark (#1A1A1A) = ✅ Good contrast
- Gray (#E5E5E5) on dark = ✅ Good

### **Tip 4: Icon Sources**

Download all icons from same source for consistency!

---

## **📞 NEED HELP?**

**Design questions:** Check `web/design_system.py`
**Component questions:** Check `web/components.py`
**Icon questions:** See `ICON_LIST.md`
**Code questions:** Ask in team chat

---

## **🎉 YOU'RE READY!**

With updated structure:
- ✅ Yellow-Olive dark theme
- ✅ Google Fonts (Inter, Poppins)
- ✅ File-based icons
- ✅ Proper project organization
- ✅ Analysis scripts separated

**Happy coding!** 🚀