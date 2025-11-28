# Nusantara Food Watch - PIHPS Scraper

**Dashboard Intelijen Harga Pangan Indonesia - Real-time & Otomatis**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Deskripsi

**Nusantara Food Watch** adalah sistem scraping dan dashboard untuk memantau harga pangan strategis di Indonesia secara real-time. Data diambil dari **PIHPS (Pusat Informasi Harga Pangan Strategis)** Bank Indonesia.

### Fitur Utama

- ✅ **Scraping Otomatis**: Ambil data harga dari 34 provinsi Indonesia
- ✅ **API-Based**: Tidak butuh Selenium, hanya HTTP requests (cepat & ringan)
- ✅ **Data Transformation**: Convert wide format → long format untuk database
- ✅ **Error Handling**: Robust handling untuk missing data
- ✅ **Scheduled Jobs**: Support untuk GitHub Actions/Cron
- ✅ **CSV Export**: Save data untuk analisa lebih lanjut

---

## Arsitektur

```
┌─────────────────┐
│  PIHPS/BI API   │  ← Data source
└────────┬────────┘
         │ HTTPS GET
┌────────▼────────┐
│ Python Scraper  │  ← pihps_scraper.py
└────────┬────────┘
         │ Transform
┌────────▼────────┐
│  PostgreSQL DB  │  ← Supabase/Neon
└────────┬────────┘
         │ Query
┌────────▼────────┐
│ Streamlit App   │  ← Dashboard
└─────────────────┘
```
---

## Project Structure

```
nusantara_food/
├── dump/
│   └── __init__.py
├── data/
│   ├── raw
│   ├── interim
│   └── processed
├── src/
│   ├── scraper/
│   │   ├── debug/
│   │   │   ├── debug_api.py
│   │   │   ├── debug_monthly.py
│   │   │   └── find_endpoint.py
│   │   ├── pihps_scraper.py
│   │   └── app_scraper.py
│   ├── data_analysis/
│   │   ├── cleaning.py
│   │   ├── visualize.py
│   │   ├── forecast.py
│   │   └── app_analysis.py
│   ├── models/
│   │   └── __init__.py
│   ├── .streamlit
│   ├── dashboard/
│   │   ├── docs/
│   │   │   └── README
│   │   ├── .streamlit
│   │   ├── app.py
│   │   ├── setup.py
│   │   ├── test.py
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── deploy_to_hf/
│   │       ├── .streamlit
│   │       ├── src/
│   │       │   └── __init__.py
│   │       ├── app.py
│   │       ├── README
│   │       └── requirements.txt
│   └── db/
│       ├── test_db_setup.py
│       └── nusantara_db.py
├── notebooks/
│   ├── cleaning.ipynb
│   ├── visualize.ipynb
│   └── forecast.ipynb
├── .gitignore
├── README
├── requirements.txt
├── main.py
└── .env
```

---

## Roadmap

### Sprint 1 (Week 1) ✅
- [x] Investigasi API endpoints
- [x] Build scraper prototype
- [x] Test data quality
- [x] Setup database schema

### Sprint 2 (Week 2)
- [ ] Deploy scraper ke GitHub Actions
- [ ] Backfill data 30 hari terakhir
- [ ] Error notification (Telegram/Email)
- [ ] Build basic Streamlit UI

### Sprint 3 (Week 3)
- [ ] Disparity map (peta panas)
- [ ] Anomaly detection (harga naik >10%)
- [ ] Time series chart
- [ ] Add narasi/insight

### Sprint 4 (Week 4)
- [ ] UI polishing
- [ ] Deploy ke Hugging Face Spaces
- [ ] Write comprehensive README
- [ ] Prepare demo/presentation

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

## License

MIT License - lihat [LICENSE](LICENSE) file

---

## Team

**Project Manager:** [Ayat Tulloh Rahulloh Khomeini]

- **The Builder** (Data Engineer): Handling scraping & database
- **The Storyteller** (Data Analyst): Dashboard & insights

**Data Analyst:** [Naufal Makarim A]

- **The Storyteller** (Data Analyst): Dashboard & Insights

---

## Contact

- Email: dkhomeini79@gmail.com
- GitHub: [@atrkhomeini](https://github.com/atrkhomeini)
- Project Link: [Nusantara Food Watch](https://github.com/atrkhomeini/nusantara-food-watch)

---

## Acknowledgments

- Data source: [PIHPS Bank Indonesia](https://www.bi.go.id/hargapangan/)
- Kementerian Pertanian RI
- Komunitas data science Indonesia

---

## Project Stats

![GitHub stars](https://img.shields.io/github/stars/atrkhomeini/nusantara-food-watch?style=social)
![GitHub forks](https://img.shields.io/github/forks/atrkhomeini/nusantara-food-watch?style=social)
![GitHub issues](https://img.shields.io/github/issues/atrkhomeini/nusantara-food-watch)

---

**Made with ❤️ for Indonesia**