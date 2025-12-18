# 🔄 DATA FLOW ARCHITECTURE - Complete Explanation

## **📊 THE BIG PICTURE**

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER OPENS DASHBOARD                     │
│                         (web/pages/home_consumer.py)             │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│          USER SELECTS: "Show me Beras price in Surabaya"        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (1) Dashboard needs data
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   analysis/processing/price_data.py              │
│                   ↓ Function: get_current_price()                │
│                   ↓ "I need to fetch from database"              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (2) Execute SQL query
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   analysis/queries/get_price.sql                 │
│                   SELECT harga FROM fact_prices                  │
│                   WHERE commodity='Beras' AND province='Surabaya'│
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (3) Query database
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATABASE (Supabase)                         │
│                      Returns: Rp 12,500                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (4) Return data
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   analysis/processing/price_data.py              │
│                   ↓ Process data (format, calculate change)      │
│                   ↓ Returns: {"price": 12500, "change": 2.5}    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ (5) Return processed data
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   web/pages/home_consumer.py                     │
│                   ↓ Display: Rp 12,500 ↑ +2.5%                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## **🎯 WHY SEPARATE FOLDERS?**

### **Reason 1: Separation of Concerns**

```
analysis/          ← BUSINESS LOGIC (What to do with data)
  ├── processing/  ← Data processing, calculations, ML models
  └── queries/     ← Database queries (How to get data)

web/              ← PRESENTATION LAYER (How to show data)
  └── pages/      ← UI components, layout, user interactions
```

**Benefits:**
- ✅ **Reusability:** Same processing logic used by multiple pages
- ✅ **Testability:** Test data logic separate from UI
- ✅ **Maintainability:** Change database query without touching UI
- ✅ **Team work:** Data analyst works on `analysis/`, frontend dev works on `web/`

---

### **Reason 2: Multiple Consumers**

Your data processing might be used by:
1. **Dashboard** (`web/pages/`)
2. **Jupyter notebooks** (`notebooks/`)
3. **API endpoints** (future)
4. **Reports** (`reports/`)
5. **Command-line tools**

**Example:**
```python
# All these use SAME processing logic:

# 1. Dashboard
from analysis.processing.forecast import calculate_forecast
forecast_data = calculate_forecast('Beras', days=7)

# 2. Jupyter notebook
from analysis.processing.forecast import calculate_forecast
forecast_data = calculate_forecast('Beras', days=30)  # Different timeframe

# 3. CLI tool
from analysis.processing.forecast import calculate_forecast
forecast_data = calculate_forecast('Beras', days=7)
print(forecast_data)
```

---

## **📂 FOLDER PURPOSES**

### **1. analysis/queries/** - Raw SQL

**Purpose:** Database access layer
**Contains:** SQL query files

**Why separate SQL files?**
- ✅ Easy to read and modify
- ✅ Version control for queries
- ✅ Can be optimized by database expert
- ✅ Reusable across different Python scripts

**Example:**
```sql
-- analysis/queries/get_current_price.sql

SELECT 
    c.commodity_name,
    p.province_name,
    fp.harga,
    fp.tanggal,
    LAG(fp.harga) OVER (
        PARTITION BY fp.commodity_id, fp.province_id 
        ORDER BY fp.tanggal
    ) as prev_price
FROM fact_prices fp
JOIN dim_commodities c ON fp.commodity_id = c.commodity_id
JOIN dim_provinces p ON fp.province_id = p.province_id
WHERE 
    fp.tanggal = (SELECT MAX(tanggal) FROM fact_prices)
    AND c.commodity_name = %(commodity_name)s
    AND p.province_name = %(province_name)s;
```

---

### **2. analysis/processing/** - Business Logic

**Purpose:** Data processing, calculations, transformations
**Contains:** Python functions that use SQL queries

**Why separate processing?**
- ✅ Complex logic in one place
- ✅ Easy to test (unit tests)
- ✅ Shared by multiple pages
- ✅ ML models, statistics, forecasting

**Example:**
```python
# analysis/processing/price_data.py

import pandas as pd
from pathlib import Path
from src.db.nusantara_db import get_db_connection

def get_current_price(commodity_name, province_name):
    """
    Get current price with change percentage
    
    Args:
        commodity_name (str): e.g., "Beras"
        province_name (str): e.g., "Jawa Timur"
        
    Returns:
        dict: {"price": 12500, "change_percent": 2.5, "date": "2025-12-18"}
    """
    # Load SQL query
    sql_file = Path(__file__).parent.parent / 'queries' / 'get_current_price.sql'
    with open(sql_file, 'r') as f:
        query = f.read()
    
    # Execute query
    conn = get_db_connection()
    df = pd.read_sql_query(
        query, 
        conn, 
        params={
            'commodity_name': commodity_name,
            'province_name': province_name
        }
    )
    
    # Process data
    if df.empty:
        return None
    
    row = df.iloc[0]
    current_price = row['harga']
    prev_price = row['prev_price']
    
    # Calculate change percentage
    if prev_price and prev_price > 0:
        change_percent = ((current_price - prev_price) / prev_price) * 100
    else:
        change_percent = 0
    
    return {
        'price': current_price,
        'change_percent': change_percent,
        'date': row['tanggal'].strftime('%Y-%m-%d'),
        'commodity': row['commodity_name'],
        'province': row['province_name']
    }
```

---

### **3. web/pages/** - Presentation

**Purpose:** User interface, display data
**Contains:** Dash layouts and callbacks

**Why separate pages?**
- ✅ Focus on UI/UX
- ✅ Don't mix data logic with presentation
- ✅ Easy to redesign UI without touching data logic

**Example:**
```python
# web/pages/home_consumer.py

from dash import html, dcc, Input, Output, callback
from web.design_system import COLORS, FONTS
from web.components import create_stat_card
from analysis.processing.price_data import get_current_price  # ← Import processing!

def layout():
    return html.Div([
        # Province selector
        dcc.Dropdown(
            id='consumer-province',
            options=[
                {'label': 'Jawa Timur', 'value': 'Jawa Timur'},
                {'label': 'DKI Jakarta', 'value': 'DKI Jakarta'},
            ],
            value='Jawa Timur'
        ),
        
        # Price display
        html.Div(id='price-display'),
    ])


@callback(
    Output('price-display', 'children'),
    Input('consumer-province', 'value')
)
def update_price(province):
    # Call processing layer
    data = get_current_price('Beras', province)
    
    if not data:
        return html.Div("No data available")
    
    # Focus on presentation only
    return create_stat_card(
        label=f"Harga Beras - {data['province']}",
        value=f"Rp {data['price']:,}",
        change_percent=data['change_percent'],
        icon_name='Beras',
        icon_category='commodities'
    )
```

---

## **🔄 COMPLETE WORKFLOW EXAMPLE**

### **Scenario: User wants price forecast**

#### **Step 1: User Action (web/pages/)**
```python
# User clicks "Show forecast for Beras in Surabaya for 7 days"
# Callback triggered in web/pages/home_consumer.py

@callback(
    Output('forecast-chart', 'figure'),
    Input('commodity-dropdown', 'value'),
    Input('province-dropdown', 'value'),
    Input('days-slider', 'value')
)
def update_forecast(commodity, province, days):
    # Call processing layer
    forecast_data = calculate_forecast(commodity, province, days)
    
    # Create chart (presentation only)
    fig = create_line_chart(
        forecast_data,
        x_col='date',
        y_col='predicted_price',
        title=f'Forecast {commodity} - {province}'
    )
    
    return fig
```

---

#### **Step 2: Processing Layer (analysis/processing/)**
```python
# analysis/processing/forecast.py

import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from src.db.nusantara_db import get_db_connection

def calculate_forecast(commodity_name, province_name, days=7):
    """
    Calculate price forecast using historical data
    
    Args:
        commodity_name (str): Commodity name
        province_name (str): Province name
        days (int): Number of days to forecast
        
    Returns:
        pd.DataFrame: Columns ['date', 'predicted_price', 'confidence_lower', 'confidence_upper']
    """
    
    # STEP 1: Get historical data using SQL query
    sql_file = Path(__file__).parent.parent / 'queries' / 'get_historical_prices.sql'
    with open(sql_file, 'r') as f:
        query = f.read()
    
    conn = get_db_connection()
    df_history = pd.read_sql_query(
        query,
        conn,
        params={
            'commodity_name': commodity_name,
            'province_name': province_name,
            'days_back': 30  # Get last 30 days
        }
    )
    
    # STEP 2: Clean data
    df_history = df_history.dropna()
    df_history['tanggal'] = pd.to_datetime(df_history['tanggal'])
    df_history = df_history.sort_values('tanggal')
    
    # STEP 3: Calculate forecast (simple moving average for now)
    # In production, use ARIMA, Prophet, or LSTM
    last_price = df_history['harga'].iloc[-1]
    avg_change = df_history['harga'].pct_change().mean()
    
    # Generate forecast dates
    last_date = df_history['tanggal'].max()
    forecast_dates = [last_date + timedelta(days=i) for i in range(1, days + 1)]
    
    # Predict prices
    predictions = []
    current_price = last_price
    
    for _ in range(days):
        # Simple prediction: last_price * (1 + avg_change)
        current_price = current_price * (1 + avg_change)
        predictions.append(current_price)
    
    # Create forecast dataframe
    df_forecast = pd.DataFrame({
        'date': forecast_dates,
        'predicted_price': predictions,
        'confidence_lower': [p * 0.95 for p in predictions],  # 95% confidence
        'confidence_upper': [p * 1.05 for p in predictions],
    })
    
    return df_forecast
```

---

#### **Step 3: Query Layer (analysis/queries/)**
```sql
-- analysis/queries/get_historical_prices.sql

SELECT 
    fp.tanggal,
    fp.harga,
    c.commodity_name,
    p.province_name
FROM fact_prices fp
JOIN dim_commodities c ON fp.commodity_id = c.commodity_id
JOIN dim_provinces p ON fp.province_id = p.province_id
WHERE 
    c.commodity_name = %(commodity_name)s
    AND p.province_name = %(province_name)s
    AND fp.tanggal >= CURRENT_DATE - INTERVAL '%(days_back)s days'
    AND fp.subcategory_id IS NULL  -- Category level only
ORDER BY fp.tanggal DESC;
```

---

#### **Step 4: Database (Supabase)**
```
Returns: 30 rows of historical price data
[
  {tanggal: '2025-12-18', harga: 12500, ...},
  {tanggal: '2025-12-17', harga: 12450, ...},
  ...
]
```

---

#### **Step 5: Back to Dashboard**
```python
# web/pages/home_consumer.py receives forecast_data

df_forecast:
   date        | predicted_price | confidence_lower | confidence_upper
---------------|-----------------|------------------|------------------
   2025-12-19 | 12550          | 11923           | 13178
   2025-12-20 | 12600          | 11970           | 13230
   ...

# Display as chart
fig = create_line_chart(df_forecast, 'date', 'predicted_price')
return fig
```

---

## **🎯 KEY BENEFITS**

### **Benefit 1: Reusability**

**Same processing, different presentations:**

```python
# analysis/processing/price_data.py
def get_top_provinces(commodity_name, limit=5):
    """Get provinces with highest/lowest prices"""
    # Complex SQL query + processing
    return result

# USED BY:

# 1. Consumer page - Show cheapest provinces
from analysis.processing.price_data import get_top_provinces
cheapest = get_top_provinces('Beras', limit=5)

# 2. Trader page - Show arbitrage opportunities  
from analysis.processing.price_data import get_top_provinces
expensive = get_top_provinces('Beras', limit=5, order='DESC')

# 3. Government page - Regional comparison
from analysis.processing.price_data import get_top_provinces
all_provinces = get_top_provinces('Beras', limit=None)
```

---

### **Benefit 2: Independent Development**

```
Data Analyst:               Frontend Developer:
├── Works on                ├── Works on
│   analysis/processing/    │   web/pages/
│   analysis/queries/       │   web/components/
│                           │
├── Creates:                ├── Creates:
│   get_forecast()         │   ForecastChart component
│   calculate_margin()     │   MarginCalculator page
│   get_trends()           │   TrendVisualization
│                           │
└── Returns:                └── Displays:
    Clean data structure        Beautiful UI
```

**They can work in parallel!** 🎉

---

### **Benefit 3: Easy Testing**

```python
# Test processing WITHOUT running dashboard

# tests/test_price_data.py
from analysis.processing.price_data import get_current_price

def test_get_current_price():
    result = get_current_price('Beras', 'Jawa Timur')
    
    assert result is not None
    assert 'price' in result
    assert 'change_percent' in result
    assert result['price'] > 0
    
# Run tests
pytest tests/test_price_data.py

# No need to open browser or test UI!
```

---

### **Benefit 4: Multiple Use Cases**

```python
# Same processing used everywhere:

# 1. Dashboard
from analysis.processing.price_data import get_current_price

# 2. Jupyter Notebook
from analysis.processing.price_data import get_current_price
price = get_current_price('Beras', 'Jawa Timur')
# Analyze in notebook

# 3. API endpoint (future)
@app.route('/api/price')
def api_price():
    from analysis.processing.price_data import get_current_price
    result = get_current_price(request.args['commodity'], request.args['province'])
    return jsonify(result)

# 4. CLI tool
if __name__ == '__main__':
    from analysis.processing.price_data import get_current_price
    result = get_current_price('Beras', 'Jawa Timur')
    print(f"Current price: Rp {result['price']:,}")
```

---

## **📋 FILE ORGANIZATION EXAMPLE**

### **Complete Structure:**

```
analysis/
├── processing/              # Business logic
│   ├── __init__.py
│   ├── price_data.py       # Price-related functions
│   │   ├── get_current_price()
│   │   ├── get_top_provinces()
│   │   └── calculate_price_change()
│   │
│   ├── forecast.py         # Forecasting functions
│   │   ├── calculate_forecast()
│   │   ├── predict_trend()
│   │   └── calculate_confidence_interval()
│   │
│   ├── margin.py           # Margin calculations
│   │   ├── calculate_supply_chain_margin()
│   │   ├── get_arbitrage_opportunities()
│   │   └── calculate_profit_potential()
│   │
│   └── statistics.py       # Statistical analysis
│       ├── calculate_volatility()
│       ├── get_price_distribution()
│       └── calculate_inflation()
│
└── queries/                 # SQL queries
    ├── get_current_price.sql
    ├── get_historical_prices.sql
    ├── get_top_provinces.sql
    ├── get_supply_chain_breakdown.sql
    └── get_price_trends.sql

web/
└── pages/                   # Presentation layer
    ├── home_consumer.py    # Uses: price_data.py, forecast.py
    ├── home_trader.py      # Uses: margin.py, forecast.py
    ├── home_government.py  # Uses: statistics.py, price_data.py
    └── home_researcher.py  # Uses: ALL processing modules
```

---

## **💡 REAL WORLD ANALOGY**

Think of it like a restaurant:

```
analysis/queries/          = RECIPE BOOK
                             "How to cook each dish"

analysis/processing/       = KITCHEN
                             "Chefs prepare the food"

web/pages/                 = DINING ROOM
                             "Waiters present food beautifully to customers"
```

**Flow:**
1. Customer orders: "I want Nasi Goreng" (User clicks dashboard)
2. Waiter takes order: web/pages/ receives input
3. Kitchen prepares: analysis/processing/ cooks the data
4. Chef follows recipe: analysis/queries/ (SQL)
5. Waiter serves: web/pages/ displays result

---

## **✅ QUICK DECISION GUIDE**

### **When to use analysis/processing/:**

```
✅ Calculations (price change %, volatility, etc.)
✅ Data transformations (wide → long format)
✅ ML models (forecasting, clustering)
✅ Business logic (margin calculation, arbitrage detection)
✅ Aggregations (averages, sums, rankings)
```

### **When to use analysis/queries/:**

```
✅ Database queries (SELECT, JOIN, WHERE)
✅ Complex SQL (window functions, CTEs)
✅ Data extraction from database
✅ Stored procedures (if using)
```

### **When to use web/pages/:**

```
✅ User interface (buttons, dropdowns, charts)
✅ Layout and styling
✅ User interactions (clicks, selections)
✅ Display logic (show/hide, formatting)
✅ Callbacks (input → output)
```

---

## **🎓 SUMMARY**

### **The Three Layers:**

```
┌──────────────────────────────────────────┐
│         web/pages/                       │  PRESENTATION
│         "How it LOOKS"                   │  (UI, Layout, Styling)
└────────────────┬─────────────────────────┘
                 │ import from
                 ▼
┌──────────────────────────────────────────┐
│         analysis/processing/             │  BUSINESS LOGIC
│         "What to DO with data"           │  (Calculations, ML)
└────────────────┬─────────────────────────┘
                 │ loads & executes
                 ▼
┌──────────────────────────────────────────┐
│         analysis/queries/                │  DATA ACCESS
│         "How to GET data"                │  (SQL queries)
└────────────────┬─────────────────────────┘
                 │ queries
                 ▼
┌──────────────────────────────────────────┐
│         DATABASE                         │  DATA STORAGE
│         (Supabase PostgreSQL)            │
└──────────────────────────────────────────┘
```

---

### **Why This Architecture?**

✅ **Separation of Concerns** - Each layer has one job
✅ **Reusability** - Same logic used by multiple pages
✅ **Testability** - Test data logic independently
✅ **Maintainability** - Change database without touching UI
✅ **Scalability** - Add new pages without duplicating logic
✅ **Team Collaboration** - Different devs work on different layers

---

**Does this clear up the confusion?** 🎯

Intinya:
- `analysis/queries/` = Cara ambil data dari database (SQL)
- `analysis/processing/` = Cara olah data (Python functions)
- `web/pages/` = Cara tampilkan data (Dash UI)

Mau saya kasih contoh konkret lainnya? 😊