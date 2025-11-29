# Nusantara Food Watch

**Dashboard Intelijen Harga Pangan Indonesia - Real-time & Otomatis**

---

## Deskripsi

**Nusantara Food Watch** adalah sistem monitoring harga pangan strategis di Indonesia secara real-time. Data diambil dari PIHPS (Pusat Informasi Harga Pangan Strategis) Bank Indonesia.

### Fitur Utama

- Scraping Otomatis via GitHub Actions (daily at 6 AM)
- Multi-Commodity Support (10 komoditas)
- Multi-Market Analysis (4 tipe pasar)
- Historical Data (8 tahun ke belakang)
- Email Notifications (success/failure alerts)
- Supply Chain Margin Analysis
- API-Based (HTTP requests, no Selenium)
- Data Transformation (wide to long format)

---

## Arsitektur

```
┌─────────────────┐
│  PIHPS/BI API   │  ← Data source
└────────┬────────┘
         │ HTTPS GET (GitHub Actions)
┌────────▼────────┐
│ Python Scraper  │  ← Automated daily
└────────┬────────┘
         │ Transform & Load
┌────────▼────────┐
│  PostgreSQL DB  │  ← Supabase
└────────┬────────┘
         │ Query & Analyze
┌────────▼────────┐
│ Streamlit App   │  ← Dashboard
└─────────────────┘
```

---

## Project Structure

```
nusantara_food/
├── .github/workflows/
│   └── daily_scraper.yml         # GitHub Actions automation
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
├── src/
│   ├── scraper/
│   │   ├── app_scraper.py        # Main multi-commodity scraper
│   │   └── debug/
│   ├── data_analysis/
│   │   ├── config.py             # Centralized paths
│   │   └── utils.py              # Helper functions
│   ├── db/
│   │   └── nusantara_db.py       # Database handler
│   ├── utils/
│   │   └── notifications.py      # Email alerts
│   └── dashboard/
│       └── app.py
├── notebooks/
│   ├── 01_data_extraction.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_exploratory_analysis.ipynb
│   ├── 04_visualization.ipynb
│   └── 05_forecasting.ipynb
├── backfill_30_days.py           # Historical data backfill
├── daily_scraper.py              # Daily scraper for automation
├── requirements.txt
├── .env
└── README.md
```

---

## Roadmap

### Sprint 1 (Week 1) - COMPLETE

- [x] Investigasi API endpoints
- [x] Build scraper prototype
- [x] Test data quality
- [x] Setup database schema
- [x] Multi-commodity support (10 komoditas)
- [x] Multi-market support (4 tipe pasar)

### Sprint 2 (Week 2) - COMPLETE

- [x] Deploy scraper ke GitHub Actions
- [x] Backfill data 30 hari terakhir
- [x] Email notifications (Gmail SMTP)
- [x] Automated daily scraping at 6 AM

### Sprint 3 (Week 3) - IN PROGRESS

- [ ] Build Streamlit dashboard
- [ ] Price disparity map (heatmap)
- [ ] Anomaly detection (price spikes)
- [ ] Time series charts
- [ ] Supply chain margin visualization

### Sprint 4 (Week 4)

- [ ] UI polishing
- [ ] Deploy to Hugging Face Spaces
- [ ] Write comprehensive documentation
- [ ] Prepare demo/presentation

---

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/atrkhomeini/nusantara-food-watch.git
cd nusantara-food-watch
```

### 2. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy template
cp .env.example .env

# Edit .env with your credentials:
# - DATABASE_URL (Supabase)
# - EMAIL_ADDRESS (Gmail)
# - EMAIL_APP_PASSWORD (Gmail app password)
# - ALERT_EMAIL (where to receive alerts)
```

### 4. Setup Data Folders

```bash
python setup_analysis.py
```

### 5. Test Connection

```bash
# Test database
python -c "from src.db.nusantara_db import NusantaraDatabase; db = NusantaraDatabase(); db.connect(); print('Connected!')"

# Test email
python -m src.utils.notifications
```

### 6. Run Backfill (First Time)

```bash
# Backfill last 30 days
python backfill_30_days.py

# Or specific range
python backfill_30_days.py --start 2024-01-01 --end 2024-01-31
```

### 7. Start Jupyter (for analysis)

```bash
jupyter notebook
```

---

## Automated Scraping

### GitHub Actions Setup

The scraper runs automatically every day at 6:00 AM Jakarta time via GitHub Actions.

**Setup:**

1. Go to Repository Settings → Secrets and variables → Actions
2. Add secrets:
   - `DATABASE_URL`
   - `EMAIL_ADDRESS`
   - `EMAIL_APP_PASSWORD`
   - `ALERT_EMAIL`
3. Push to GitHub - workflow will activate

**Manual Trigger:**

1. Go to Actions tab
2. Select "Daily Food Price Scraper"
3. Click "Run workflow"

---

## Data Coverage

### Commodities (10)

1. Beras (6 subcategories)
2. Daging Ayam
3. Daging Sapi (2 qualities)
4. Telur Ayam
5. Bawang Merah
6. Bawang Putih
7. Cabai Merah (2 types)
8. Cabai Rawit (2 types)
9. Minyak Goreng (3 types)
10. Gula Pasir (2 types)

### Market Types (4)

1. Pasar Tradisional
2. Pasar Modern/Supermarket
3. Pedagang Besar (Wholesaler)
4. Produsen (Producer/Farmer)

### Geographic Coverage

- 35 provinces across Indonesia
- Daily and monthly data
- Historical data: 2017 - present

---

## Tech Stack

| Category | Technology |
|----------|------------|
| **Language & Core** | ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) |
| **Data Processing** | ![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/Numpy-013243?logo=numpy&logoColor=white) |
| **Modeling** | ![Statsmodels](https://img.shields.io/badge/Statsmodels-2C3E50?logo=python&logoColor=white) |
| **Visualization** | ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white) ![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white) |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?logo=postgresql&logoColor=white) ![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?logo=supabase&logoColor=white) |
| **Deployment & Ops** | ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white) ![HuggingFace](https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=black) |

---

## Usage Examples

### Manual Scraping

```python
from src.scraper.app_scraper import EnhancedMultiCommodityScraper

scraper = EnhancedMultiCommodityScraper()

# Scrape specific commodity
df = scraper.scrape_commodity(
    commodity_id='cat_1',  # Beras
    start_date='2024-01-01',
    end_date='2024-01-31',
    market_type_id=1,  # Pasar Tradisional
    tipe_laporan=3  # Monthly
)

# Scrape all commodities
df_all = scraper.scrape_all_commodities(
    start_date='2024-01-01',
    end_date='2024-01-31'
)
```

### Data Analysis

```python
from src.data_analysis.utils import load_data, save_csv

# Load from database
df = load_data("""
    SELECT * FROM harga_pangan
    WHERE commodity_category = 'cat_1'
    AND tanggal >= '2024-01-01'
""")

# Save for analysis
save_csv(df, 'beras_2024.csv', processed=False)
```

---

## Team

**Project Manager:** Ayat Tulloh Rahulloh Khomeini
- Role: The Builder (Data Engineer)
- Responsibilities: Scraping, database, automation
- Contact: dkhomeini79@gmail.com
- GitHub: [@atrkhomeini](https://github.com/atrkhomeini)

**Data Analyst:** Naufal Makarim A
- Role: The Storyteller (Data Analyst)
- Responsibilities: Dashboard, insights, visualization

---

## License

MIT License - see LICENSE file

---

## Acknowledgments

- Data source: [PIHPS Bank Indonesia](https://www.bi.go.id/hargapangan/)
- Kementerian Pertanian RI
- Komunitas data science Indonesia

---

## Contact & Links

- Email: dkhomeini79@gmail.com
- GitHub: [@atrkhomeini](https://github.com/atrkhomeini)
- Project: [Nusantara Food Watch](https://github.com/atrkhomeini/nusantara-food-watch)

---

**Made with dedication for Indonesia**