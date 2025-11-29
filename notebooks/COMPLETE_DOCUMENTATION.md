# 📚 NUSANTARA FOOD WATCH - COMPLETE DOCUMENTATION
## Master Guide: Setup, Collaboration, Data Analysis & Deployment

**Last Updated:** 2025-11-28  
**Version:** 2.0  
**Status:** Production Ready

---

# TABLE OF CONTENTS

1. [Project Overview](#1-project-overview)
2. [Team Collaboration Setup](#2-team-collaboration-setup)
3. [GitHub Repository Setup](#3-github-repository-setup)
4. [Supabase Database Access](#4-supabase-database-access)
5. [Environment Setup](#5-environment-setup)
6. [Data Analysis Framework](#6-data-analysis-framework)
7. [Notebook Templates Guide](#7-notebook-templates-guide)
8. [Dependencies Management](#8-dependencies-management)
9. [Troubleshooting](#9-troubleshooting)
10. [Quick Reference](#10-quick-reference)

---

# 1. PROJECT OVERVIEW

## What is Nusantara Food Watch?

Real-time food price monitoring dashboard for Indonesia, tracking 10 major commodities across 35 provinces using PIHPS (Bank Indonesia) data.

**Tech Stack:**
- **Data Collection:** Python, Requests
- **Database:** PostgreSQL (Supabase)
- **Analysis:** Pandas, NumPy, Jupyter Notebooks
- **Visualization:** Matplotlib, Seaborn, Plotly
- **Dashboard:** Streamlit
- **Deployment:** Hugging Face Spaces

**Team Structure:**
- **The Builder** (Data Engineer): Data scraping, database, analysis
- **The Storyteller** (Data Analyst): Dashboard, insights, visualization

---

# 2. TEAM COLLABORATION SETUP

## 2.1 Adding Team Members to Supabase

### For Project Owner (You):

**Step 1: Access Supabase Project Settings**

```
1. Go to https://supabase.com/dashboard
2. Select your project: "nusantara-food-watch"
3. Click Settings (gear icon) in left sidebar
4. Navigate to "Database" section
```

**Step 2: Invite Team Member**

```
1. Click "Settings" → "Team"
2. Click "Invite teammate" button
3. Enter teammate's email
4. Select role:
   - Owner: Full access (use carefully!)
   - Developer: Read/write database, can deploy
   - Read-only: View only (for analysts)
```

**Recommended Role for Data Analyst:** Developer

**Step 3: Share Database Credentials**

Create a shared `.env.example` file:

```bash
# .env.example (safe to commit to GitHub)
DATABASE_URL=postgresql://[user]:[password]@[host]:5432/[database]

# Instructions:
# 1. Copy this file to .env
# 2. Replace [user], [password], [host], [database] with actual values
# 3. Get credentials from: Supabase Dashboard → Settings → Database
```

**⚠️ IMPORTANT:** Never commit `.env` with real credentials to GitHub!

---

### For Team Member (Your Friend):

**Step 1: Accept Invitation**

```
1. Check email for Supabase invitation
2. Click "Accept invitation" link
3. Create Supabase account or sign in
4. You now have access to the project!
```

**Step 2: Get Database Connection String**

```
1. Go to Supabase Dashboard
2. Select "nusantara-food-watch" project
3. Click Settings → Database
4. Scroll to "Connection string"
5. Copy the "URI" format:
   postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
```

**Step 3: Test Connection**

Create a test script `test_connection.py`:

```python
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

try:
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    print("✅ Connected to database successfully!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM harga_pangan")
    count = cursor.fetchone()[0]
    print(f"📊 Records in database: {count:,}")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Run:
```bash
python test_connection.py
```

---

## 2.2 Supabase Access Levels Explained

| Role | Database Access | Can Deploy | Can Invite | Best For |
|------|----------------|------------|-----------|----------|
| **Owner** | Full (read/write/delete) | ✅ Yes | ✅ Yes | Project lead |
| **Developer** | Full (read/write/delete) | ✅ Yes | ❌ No | Data engineers |
| **Read-only** | Read only | ❌ No | ❌ No | Analysts, viewers |

**Recommendation:**
- **Project Owner:** Owner role
- **Data Analyst Partner:** Developer role
- **Reviewers/Stakeholders:** Read-only role

---

## 2.3 Sharing Database Access Securely

### Method 1: Using Environment Variables (Recommended)

**Share this template:**

```bash
# .env.template
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DATABASE

# How to get your credentials:
# 1. Go to Supabase Dashboard
# 2. Settings → Database → Connection String
# 3. Copy URI format
# 4. Save as .env (not .env.template)
```

### Method 2: Using Supabase Connection Pooler

For better performance:

```bash
# Use connection pooler (recommended for production)
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:6543/postgres?pgbouncer=true
```

### Method 3: Read-Only Access for Analysts

Create read-only user:

```sql
-- Run this in Supabase SQL Editor
CREATE ROLE analyst_readonly WITH LOGIN PASSWORD 'secure_password_here';
GRANT CONNECT ON DATABASE postgres TO analyst_readonly;
GRANT USAGE ON SCHEMA public TO analyst_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst_readonly;
```

---

# 3. GITHUB REPOSITORY SETUP

## 3.1 Initialize Git Repository

```bash
cd D:\nusantara_food
git init
```

## 3.2 Create .gitignore

Create `.gitignore` file:

```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
*.egg
*.egg-info/
dist/
build/
*.pyc

# Virtual Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Jupyter Notebooks
.ipynb_checkpoints
*/.ipynb_checkpoints/*

# Data files (don't push large datasets)
data/raw/*
data/interim/*
data/processed/*
!data/raw/.gitkeep
!data/interim/.gitkeep
!data/processed/.gitkeep

# Output files
reports/figures/*
!reports/figures/.gitkeep

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
*.log

# Sensitive files
.env
*.key
*.pem
secrets/
credentials/

# Database dumps
*.sql
*.db
*.sqlite

# Temporary files
tmp/
temp/
*.tmp
```

**Why these folders are ignored:**

| Folder | Why Ignored | What to Commit Instead |
|--------|-------------|----------------------|
| `data/raw/*` | Large files, can be regenerated | `.gitkeep` to preserve structure |
| `data/interim/*` | Temporary analysis files | `.gitkeep` only |
| `data/processed/*` | Generated from interim | `.gitkeep` only |
| `reports/figures/*` | Generated PNG files | `.gitkeep` only |
| `.env` | **Contains passwords!** | `.env.example` template |
| `__pycache__/` | Python bytecode | Nothing (auto-generated) |

---

## 3.3 Create .gitkeep Files

Keep folder structure in Git:

```bash
# Windows
cd D:\nusantara_food

# Create .gitkeep in ignored folders
echo. > data\raw\.gitkeep
echo. > data\interim\.gitkeep
echo. > data\processed\.gitkeep
echo. > reports\figures\.gitkeep

# Linux/Mac
touch data/raw/.gitkeep
touch data/interim/.gitkeep
touch data/processed/.gitkeep
touch reports/figures/.gitkeep
```

---

## 3.4 Create README.md for GitHub

```markdown
# Nusantara Food Watch 🇮🇩

Real-time food price monitoring dashboard for Indonesia.

## Features
- 📊 Track 10 major food commodities
- 🗺️ Coverage: 35 provinces
- 📈 8 years of historical data
- 🔄 Real-time updates from Bank Indonesia (PIHPS)
- 📉 Supply chain margin analysis

## Tech Stack
- **Backend:** Python, PostgreSQL (Supabase)
- **Analysis:** Pandas, Jupyter Notebooks
- **Visualization:** Matplotlib, Seaborn, Plotly
- **Dashboard:** Streamlit
- **Deployment:** Hugging Face Spaces

## Setup

### 1. Clone Repository
\`\`\`bash
git clone https://github.com/YOUR_USERNAME/nusantara-food-watch.git
cd nusantara-food-watch
\`\`\`

### 2. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Configure Environment
\`\`\`bash
cp .env.example .env
# Edit .env with your Supabase credentials
\`\`\`

### 4. Setup Data Analysis
\`\`\`bash
python setup_analysis.py
\`\`\`

### 5. Start Jupyter
\`\`\`bash
jupyter notebook
\`\`\`

## Project Structure
\`\`\`
nusantara_food/
├── src/              # Source code
├── notebooks/        # Jupyter notebooks
├── data/             # Data files (gitignored)
├── reports/          # Analysis reports
└── requirements.txt  # Dependencies
\`\`\`

## Team
- **Data Engineer:** [Your Name]
- **Data Analyst:** [Partner Name]

## License
MIT
```

---

## 3.5 First Commit & Push to GitHub

```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Project setup with data analysis framework"

# Create repository on GitHub
# Go to github.com → New Repository → "nusantara-food-watch"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/nusantara-food-watch.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 3.6 Collaborator Setup (Your Friend)

**For team member to get started:**

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/nusantara-food-watch.git
cd nusantara-food-watch

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env with database credentials (get from Supabase)

# 5. Setup folders
python setup_analysis.py

# 6. Test database connection
python test_connection.py

# 7. Start working!
jupyter notebook
```

---

## 3.7 Git Workflow for Team

### Daily Workflow:

```bash
# 1. Pull latest changes
git pull origin main

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make changes, test, commit
git add .
git commit -m "Add: descriptive message"

# 4. Push to GitHub
git push origin feature/your-feature-name

# 5. Create Pull Request on GitHub
# Go to GitHub → Pull Requests → New PR

# 6. After review and merge
git checkout main
git pull origin main
```

### Branch Naming Convention:

```
feature/    - New features
fix/        - Bug fixes
analysis/   - Data analysis notebooks
docs/       - Documentation updates

Examples:
feature/supply-chain-analysis
fix/database-connection-timeout
analysis/rice-price-trends
docs/update-readme
```

---

# 4. SUPABASE DATABASE ACCESS

## 4.1 Database Schema

### Main Table: harga_pangan

```sql
CREATE TABLE harga_pangan (
    id SERIAL PRIMARY KEY,
    provinsi VARCHAR(100) NOT NULL,
    tanggal DATE NOT NULL,
    harga NUMERIC(10, 2),
    
    -- Commodity information
    commodity_category VARCHAR(50),
    commodity_id VARCHAR(20),
    commodity_name VARCHAR(100),
    subcategory VARCHAR(100),
    
    -- Market type information
    market_type_id INTEGER,
    market_type_name VARCHAR(50),
    market_type_short VARCHAR(20),
    
    -- Metadata
    report_type VARCHAR(20) DEFAULT 'daily',
    scraped_at TIMESTAMP DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'PIHPS/BI',
    
    -- Prevent duplicates
    UNIQUE(provinsi, tanggal, commodity_category, report_type, market_type_id, subcategory)
);
```

### Views Available:

1. **latest_prices** - Most recent prices per commodity/market
2. **supply_chain_margins** - Price margins across supply chain
3. **price_trends_7d** - 7-day price trends

---

## 4.2 Accessing Database from Python

### Using our utilities:

```python
from src.data_analysis.utils import load_data

# Simple query
df = load_data("""
    SELECT * FROM harga_pangan
    WHERE commodity_name = 'Beras'
    AND tanggal >= '2024-01-01'
""")

# Using views
df_latest = load_data("SELECT * FROM latest_prices")
df_margins = load_data("SELECT * FROM supply_chain_margins")
```

### Direct connection:

```python
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
df = pd.read_sql("SELECT * FROM harga_pangan LIMIT 100", conn)
conn.close()
```

---

## 4.3 Supabase Dashboard Features

### SQL Editor
```
1. Supabase Dashboard → SQL Editor
2. Write and run queries directly
3. Save frequently used queries
```

### Table Editor
```
1. Supabase Dashboard → Table Editor
2. View/edit data visually (like Excel)
3. Add/delete records manually
```

### Database Backups
```
1. Supabase Dashboard → Settings → Database
2. Automatic daily backups (free tier)
3. Manual backup: Database → Export → Download SQL
```

---

# 5. ENVIRONMENT SETUP

## 5.1 Python Environment

### Create Virtual Environment:

```bash
# Using venv (built-in)
cd D:\nusantara_food
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Using Conda (Alternative):

```bash
conda create -n nusantara python=3.10
conda activate nusantara
```

---

## 5.2 Environment Variables (.env)

### Create .env file:

```bash
# Database
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres

# Optional: API Keys (if needed later)
# OPENAI_API_KEY=your_key_here
# HUGGINGFACE_TOKEN=your_token_here
```

### Create .env.example (safe to commit):

```bash
# Database Connection
DATABASE_URL=postgresql://user:password@host:5432/database

# Instructions:
# 1. Copy this file to .env
# 2. Replace with actual Supabase credentials
# 3. Get from: Supabase Dashboard → Settings → Database → Connection String
```

---

# 6. DATA ANALYSIS FRAMEWORK

## 6.1 Folder Structure

```
nusantara_food/
├── data/
│   ├── raw/              # Original data backups
│   ├── interim/          # Work-in-progress analysis ⭐
│   └── processed/        # Clean, analysis-ready data ⭐
├── reports/
│   └── figures/          # Generated charts (PNG) ⭐
├── notebooks/
│   ├── 01_data_extraction.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_exploratory_analysis.ipynb
│   ├── 04_visualization.ipynb
│   └── 05_forecasting.ipynb
├── src/
│   ├── scraper/          # Data collection scripts
│   ├── data_analysis/    # Analysis utilities ⭐
│   │   ├── __init__.py
│   │   ├── config.py     # Centralized paths
│   │   └── utils.py      # Helper functions
│   ├── db/               # Database handlers
│   └── dashboard/        # Streamlit dashboard
├── .env                  # Environment variables (gitignored!)
├── .env.example          # Template (safe to commit)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 6.2 Setup Data Analysis Environment

### Step 1: Run Setup Script

```bash
cd D:\nusantara_food
python setup_analysis.py
```

This creates:
- `data/interim/` folder
- `data/processed/` folder
- `reports/figures/` folder
- `.gitkeep` files in each
- README files with instructions

### Step 2: Verify Structure

```bash
# Check folders exist
dir data\interim
dir data\processed
dir reports\figures

# Should all exist without errors
```

---

## 6.3 Centralized Configuration

### config.py - Path Management

Located at: `src/data_analysis/config.py`

```python
"""
Centralized path configuration
All notebooks use these paths
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Project root (auto-detect)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / 'data'
INTERIM_DIR = DATA_DIR / 'interim'      # Work in progress
PROCESSED_DIR = DATA_DIR / 'processed'  # Final clean data

# Reports
REPORTS_DIR = PROJECT_ROOT / 'reports'
FIGURES_DIR = REPORTS_DIR / 'figures'   # Charts/images

# Database
DATABASE_URL = os.getenv('DATABASE_URL')

# Helper functions
def get_interim_path(filename: str) -> Path:
    """Get path for interim data file"""
    return INTERIM_DIR / filename

def get_processed_path(filename: str) -> Path:
    """Get path for processed data file"""
    return PROCESSED_DIR / filename

def get_figure_path(filename: str) -> Path:
    """Get path for figure file"""
    return FIGURES_DIR / filename
```

**Usage in notebooks:**

```python
from src.data_analysis.config import INTERIM_DIR, PROCESSED_DIR, FIGURES_DIR

# Save CSV
df.to_csv(INTERIM_DIR / 'my_data.csv', index=False)

# Load CSV
df = pd.read_csv(PROCESSED_DIR / 'clean_data.csv')

# Save figure
fig.savefig(FIGURES_DIR / 'chart.png', dpi=300)
```

---

## 6.4 Utility Functions

### utils.py - Helper Functions

Located at: `src/data_analysis/utils.py`

**Key classes and functions:**

```python
# DataLoader - Database queries
from src.data_analysis.utils import DataLoader

with DataLoader() as loader:
    df = loader.get_price_history(
        commodity='cat_1',
        start_date='2024-01-01'
    )

# Quick query function
from src.data_analysis.utils import load_data

df = load_data("SELECT * FROM harga_pangan LIMIT 100")

# DataSaver - Save outputs
from src.data_analysis.utils import DataSaver, save_csv

# Save CSV
save_csv(df, 'my_data.csv', processed=False)  # → data/interim/
save_csv(df, 'final.csv', processed=True)     # → data/processed/

# Save figure
saver = DataSaver()
saver.save_figure(fig, 'chart.png', dpi=300)  # → reports/figures/

# Data quality checks
from src.data_analysis.utils import check_missing_values, detect_outliers_iqr

missing = check_missing_values(df)
outliers, lower, upper = detect_outliers_iqr(df, 'harga')
```

---

# 7. NOTEBOOK TEMPLATES GUIDE

## 7.1 Notebook Workflow

Execute in order:

```
01_data_extraction.ipynb
    ↓ (saves to data/interim/)
02_data_cleaning.ipynb
    ↓ (saves to data/processed/)
03_exploratory_analysis.ipynb
    ↓ (saves figures to reports/figures/)
04_visualization.ipynb
    ↓ (saves figures to reports/figures/)
05_forecasting.ipynb
    ↓ (saves forecasts to data/processed/)
```

---

## 7.2 Notebook 01 - Data Extraction

**Purpose:** Pull data from database

**Input:** PostgreSQL database

**Output:** CSV files in `data/interim/`

**Pre-configured:**
- ✅ Database connection
- ✅ Date range configuration
- ✅ Commodity selection
- ✅ Auto-save to interim folder

**You add:** SQL queries and extraction logic

**Example:**

```python
# Setup (already in template)
from src.data_analysis.utils import load_data, save_csv
from src.data_analysis.config import INTERIM_DIR

# Your work
df = load_data("""
    SELECT * FROM harga_pangan
    WHERE commodity_category = 'cat_1'
    AND tanggal >= '2024-01-01'
""")

# Save
save_csv(df, 'beras_2024.csv', processed=False)
# ✅ Saved to: data/interim/beras_2024.csv
```

---

## 7.3 Notebook 02 - Data Cleaning

**Purpose:** Clean and validate data

**Input:** CSV from `data/interim/`

**Output:** Clean CSV in `data/processed/`

**Pre-configured:**
- ✅ Load from interim folder
- ✅ Missing value detection
- ✅ Outlier detection (IQR method)
- ✅ Auto-save to processed folder

**You add:** Cleaning rules

**Example:**

```python
# Setup (already in template)
from src.data_analysis.utils import save_csv, detect_outliers_iqr
from src.data_analysis.config import INTERIM_DIR, PROCESSED_DIR
import pandas as pd

# Load
df = pd.read_csv(INTERIM_DIR / 'beras_2024.csv')

# Clean
df_clean = df[df['harga'].notna()]
outliers, lower, upper = detect_outliers_iqr(df_clean, 'harga')
df_clean = df_clean[~outliers]

# Save
save_csv(df_clean, 'beras_cleaned.csv', processed=True)
# ✅ Saved to: data/processed/beras_cleaned.csv
```

---

## 7.4 Notebook 03 - Exploratory Analysis

**Purpose:** Explore patterns and distributions

**Input:** Clean CSV from `data/processed/`

**Output:** Exploratory charts in `reports/figures/`

**Pre-configured:**
- ✅ Load from processed folder
- ✅ Plot style setup
- ✅ Auto-save figures

**You add:** Analysis and visualizations

**Example:**

```python
# Setup (already in template)
from src.data_analysis.utils import DataSaver, setup_plot_style
from src.data_analysis.config import PROCESSED_DIR
import matplotlib.pyplot as plt
import pandas as pd

setup_plot_style()

# Load
df = pd.read_csv(PROCESSED_DIR / 'beras_cleaned.csv')

# Analyze
summary = df.groupby('provinsi')['harga'].agg(['mean', 'std', 'min', 'max'])

# Visualize
fig, ax = plt.subplots(figsize=(12, 6))
df.groupby('tanggal')['harga'].mean().plot(ax=ax)
ax.set_title('Average Rice Price Over Time')

# Save
saver = DataSaver()
saver.save_figure(fig, 'eda_price_trend.png')
# ✅ Saved to: reports/figures/eda_price_trend.png
```

---

## 7.5 Notebook 04 - Visualization

**Purpose:** Create publication-quality charts

**Input:** Processed CSV

**Output:** Publication-ready charts

**Pre-configured:**
- ✅ High-DPI settings (300 DPI)
- ✅ Consistent color palette
- ✅ Auto-save all charts

**You add:** Custom visualizations

---

## 7.6 Notebook 05 - Forecasting

**Purpose:** Predict future trends

**Input:** Processed CSV

**Output:** Forecasts and metrics

**Pre-configured:**
- ✅ Time series utilities
- ✅ Train/test split
- ✅ Model evaluation metrics

**You add:** Model training logic

---

## 7.7 Common Notebook Structure

Every notebook follows this pattern:

```python
# ============================================
# CELL 1: Setup
# ============================================
import sys
from pathlib import Path
project_root = Path.cwd().parent
sys.path.insert(0, str(project_root))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from src.data_analysis.utils import (
    load_data, save_csv, DataSaver,
    setup_plot_style
)
from src.data_analysis.config import (
    INTERIM_DIR, PROCESSED_DIR, FIGURES_DIR
)

setup_plot_style()
%matplotlib inline

# ============================================
# CELL 2: Configuration
# ============================================
INPUT_FILE = 'my_data.csv'
OUTPUT_FILE = 'my_output.csv'

# ============================================
# CELL 3: Load Data
# ============================================
df = pd.read_csv(INTERIM_DIR / INPUT_FILE)

# ============================================
# CELLS 4-N: Your Analysis
# ============================================
# ... your work here ...

# ============================================
# FINAL CELL: Save Results
# ============================================
save_csv(df_result, OUTPUT_FILE, processed=True)
```

---

# 8. DEPENDENCIES MANAGEMENT

## 8.1 Create requirements.txt

**Complete requirements.txt:**

```txt
# Core Data Processing
pandas==2.1.3
numpy==1.26.2

# Database
psycopg2-binary==2.9.9
python-dotenv==1.0.0

# Web Scraping
requests==2.31.0
beautifulsoup4==4.12.2

# Data Analysis & Visualization
matplotlib==3.8.2
seaborn==0.13.0
plotly==5.18.0

# Jupyter & Notebooks
jupyter==1.0.0
ipykernel==6.27.1
notebook==7.0.6

# Statistical Analysis & Forecasting
statsmodels==0.14.1
scikit-learn==1.3.2
scipy==1.11.4

# Time Series (optional - uncomment if needed)
# prophet==1.1.5

# Dashboard
streamlit==1.29.0

# Utilities
openpyxl==3.1.2       # Excel file support
xlrd==2.0.1           # Old Excel format
python-dateutil==2.8.2

# Development & Testing
pytest==7.4.3
pytest-cov==4.1.0
black==23.12.0        # Code formatter
flake8==6.1.0         # Linter
```

---

## 8.2 Install Dependencies

### Fresh Installation:

```bash
# Activate virtual environment first
cd D:\nusantara_food
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install all dependencies
pip install -r requirements.txt
```

### Update Existing Installation:

```bash
# Update all packages
pip install --upgrade -r requirements.txt
```

---

## 8.3 Update requirements.txt

### After installing new packages:

```bash
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Or manually add to requirements.txt:
# package-name==1.2.3
```

### Best practice - use specific versions:

```txt
# ❌ Bad (no version)
pandas

# ⚠️ OK (minimum version)
pandas>=2.0.0

# ✅ Best (exact version)
pandas==2.1.3
```

---

## 8.4 Verify Installation

**Test script:** `test_dependencies.py`

```python
"""
Test if all dependencies are installed correctly
"""

def test_imports():
    """Test critical imports"""
    
    imports = {
        'pandas': 'Data processing',
        'numpy': 'Numerical computing',
        'matplotlib': 'Plotting',
        'seaborn': 'Statistical visualization',
        'psycopg2': 'PostgreSQL connection',
        'requests': 'HTTP requests',
        'dotenv': 'Environment variables',
        'sklearn': 'Machine learning',
        'statsmodels': 'Statistical models',
        'streamlit': 'Dashboard framework'
    }
    
    print("=" * 70)
    print("TESTING DEPENDENCIES")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for module, description in imports.items():
        try:
            __import__(module)
            print(f"✅ {module:20s} - {description}")
            passed += 1
        except ImportError as e:
            print(f"❌ {module:20s} - Failed: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("\n🎉 All dependencies installed correctly!")
    else:
        print(f"\n⚠️ {failed} dependencies missing. Run: pip install -r requirements.txt")

if __name__ == "__main__":
    test_imports()
```

Run:
```bash
python test_dependencies.py
```

---

## 8.5 Managing Dependencies for Team

### Share exact versions:

```bash
# Generate with exact versions
pip freeze > requirements.txt

# Commit to Git
git add requirements.txt
git commit -m "Update: dependencies with exact versions"
git push
```

### Team members sync:

```bash
# Pull latest
git pull

# Install exact versions
pip install -r requirements.txt
```

---

# 9. TROUBLESHOOTING

## 9.1 Import Errors

### "ModuleNotFoundError: No module named 'src'"

**Solution:**

```python
# Add to first cell of notebook
import sys
from pathlib import Path
project_root = Path.cwd().parent
sys.path.insert(0, str(project_root))
```

---

### "ImportError: cannot import name 'load_data'"

**Cause:** utils.py not in correct location

**Solution:**

```bash
# Verify file exists
dir src\data_analysis\utils.py  # Windows
ls src/data_analysis/utils.py   # Linux/Mac

# If missing, copy from outputs folder
```

---

## 9.2 Database Errors

### "psycopg2.OperationalError: could not connect"

**Causes & Solutions:**

1. **Wrong credentials:**
   ```bash
   # Check .env file
   type .env  # Windows
   cat .env   # Linux/Mac
   
   # Verify DATABASE_URL format:
   postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```

2. **Missing .env file:**
   ```bash
   # Create from template
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   
   # Edit with your credentials
   ```

3. **Firewall blocking:**
   ```bash
   # Test connection
   telnet db.xxx.supabase.co 5432
   
   # If fails, check firewall/antivirus
   ```

---

### "FATAL: password authentication failed"

**Solution:**

```bash
# Get fresh credentials from Supabase
# Dashboard → Settings → Database → Reset Password
# Update .env with new password
```

---

## 9.3 File Path Errors

### "FileNotFoundError: data/interim"

**Cause:** Folders not created

**Solution:**

```bash
python setup_analysis.py
```

Or manually:

```bash
mkdir data\interim
mkdir data\processed
mkdir reports\figures
```

---

### "PermissionError: [Errno 13] Permission denied"

**Cause:** File open in another program

**Solution:**

1. Close Excel/other programs
2. Check Jupyter isn't running the file
3. Restart Jupyter kernel

---

## 9.4 Git Issues

### "fatal: remote origin already exists"

**Solution:**

```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/USER/REPO.git
```

---

### "error: failed to push some refs"

**Cause:** Remote has changes you don't have locally

**Solution:**

```bash
# Pull first
git pull origin main --rebase

# Then push
git push origin main
```

---

### Accidentally committed .env file

**Solution:**

```bash
# Remove from Git (keep local file)
git rm --cached .env

# Add to .gitignore
echo .env >> .gitignore

# Commit
git add .gitignore
git commit -m "Fix: Remove .env from tracking"
git push

# ⚠️ IMPORTANT: The .env is still in Git history!
# For production, rotate all passwords immediately!
```

---

## 9.5 Jupyter Notebook Issues

### Kernel keeps dying

**Solutions:**

1. **Reduce data size:**
   ```python
   # Load sample instead of full dataset
   df = load_data("SELECT * FROM harga_pangan LIMIT 10000")
   ```

2. **Clear output:**
   ```
   Cell → All Output → Clear
   ```

3. **Restart kernel:**
   ```
   Kernel → Restart & Clear Output
   ```

---

### "ImportError" after installing package

**Cause:** Need to restart kernel

**Solution:**

```
Kernel → Restart
```

---

# 10. QUICK REFERENCE

## 10.1 Common Commands

### Database Operations:

```python
# Quick query
from src.data_analysis.utils import load_data
df = load_data("SELECT * FROM harga_pangan LIMIT 100")

# Load with DataLoader
from src.data_analysis.utils import DataLoader
with DataLoader() as loader:
    df = loader.get_price_history('cat_1', start_date='2024-01-01')
```

### Save Operations:

```python
from src.data_analysis.utils import save_csv, DataSaver

# Save CSV
save_csv(df, 'my_data.csv', processed=False)  # → data/interim/
save_csv(df, 'final.csv', processed=True)     # → data/processed/

# Save figure
saver = DataSaver()
saver.save_figure(fig, 'chart.png', dpi=300)  # → reports/figures/
```

### Data Quality:

```python
from src.data_analysis.utils import check_missing_values, detect_outliers_iqr

# Check missing
missing = check_missing_values(df)

# Detect outliers
outliers, lower, upper = detect_outliers_iqr(df, 'harga')
df_clean = df[~outliers]
```

---

## 10.2 File Locations

```
Project root:              D:\nusantara_food\
Config file:               src\data_analysis\config.py
Utils file:                src\data_analysis\utils.py
Interim data:              data\interim\
Processed data:            data\processed\
Figures:                   reports\figures\
Notebooks:                 notebooks\
Environment variables:     .env (gitignored!)
Requirements:              requirements.txt
```

---

## 10.3 Git Workflow

```bash
# Daily routine
git pull origin main                      # Get latest
git checkout -b feature/my-feature        # New branch
# ... make changes ...
git add .                                 # Stage
git commit -m "Add: feature description"  # Commit
git push origin feature/my-feature        # Push
# Create Pull Request on GitHub

# After merge
git checkout main
git pull origin main
```

---

## 10.4 Jupyter Shortcuts

```
Shift + Enter     - Run cell and move to next
Ctrl + Enter      - Run cell and stay
Alt + Enter       - Run cell and insert below

Esc + A           - Insert cell above
Esc + B           - Insert cell below
Esc + D + D       - Delete cell
Esc + M           - Change to Markdown
Esc + Y           - Change to Code

Kernel → Restart  - Restart Python kernel
Cell → Run All    - Run all cells
```

---

## 10.5 Critical Don'ts

❌ **Never commit `.env` to Git** - Contains passwords!  
❌ **Never commit large data files** - Use `.gitignore`  
❌ **Never commit `__pycache__`** - Auto-generated  
❌ **Never hardcode passwords** - Use environment variables  
❌ **Never push directly to main** - Use feature branches  

---

# APPENDIX A: Complete File Checklist

## Files to Download:

- [ ] setup_analysis.py
- [ ] config.py → src/data_analysis/
- [ ] utils.py → src/data_analysis/
- [ ] 01_data_extraction.ipynb → notebooks/
- [ ] 02_data_cleaning.ipynb → notebooks/
- [ ] 03_exploratory_analysis.ipynb → notebooks/
- [ ] 04_visualization.ipynb → notebooks/
- [ ] 05_forecasting.ipynb → notebooks/
- [ ] notebooks/README.md → notebooks/
- [ ] test_connection.py
- [ ] test_dependencies.py

## Files to Create:

- [ ] .env (from .env.example)
- [ ] .gitignore
- [ ] README.md (for GitHub)
- [ ] requirements.txt
- [ ] src/data_analysis/__init__.py

## Folders to Create:

- [ ] data/interim/
- [ ] data/processed/
- [ ] reports/figures/

---

# APPENDIX B: Environment Variables Template

Create `.env.example`:

```bash
# Supabase Database
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres

# How to get:
# 1. Go to https://supabase.com/dashboard
# 2. Select your project
# 3. Settings → Database → Connection String
# 4. Copy URI format
# 5. Replace [YOUR-PASSWORD] with actual password

# Instructions:
# 1. Copy this file to .env
# 2. Replace [YOUR-PASSWORD] with actual password
# 3. Never commit .env to Git!
```

---

# APPENDIX C: Team Onboarding Checklist

## For New Team Member:

### Access Setup:
- [ ] Receive Supabase invitation email
- [ ] Accept invitation and create account
- [ ] Get added to GitHub repository
- [ ] Receive `.env` credentials securely

### Environment Setup:
- [ ] Clone GitHub repository
- [ ] Create virtual environment
- [ ] Install dependencies from requirements.txt
- [ ] Create .env with database credentials
- [ ] Run setup_analysis.py
- [ ] Test database connection
- [ ] Run test_dependencies.py

### Verification:
- [ ] Can connect to Supabase database
- [ ] Can run Jupyter notebooks
- [ ] Can import src.data_analysis utilities
- [ ] Can save files to correct folders
- [ ] Can push to GitHub

### First Tasks:
- [ ] Read notebooks/README.md
- [ ] Open 01_data_extraction.ipynb
- [ ] Run test query
- [ ] Create first visualization
- [ ] Push first commit

---

**END OF DOCUMENTATION**

**Version:** 2.0  
**Last Updated:** 2025-11-28  
**Status:** Complete and Production Ready ✅

For questions or issues, check Troubleshooting section or create GitHub issue.
