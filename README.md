# Nusantara Food Watch - PIHPS Scraper

**Dashboard Intelijen Harga Pangan Indonesia - Real-time & Otomatis**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Deskripsi

**Nusantara Food Watch** adalah sistem scraping dan dashboard untuk memantau harga pangan strategis di Indonesia secara real-time. Data diambil dari **PIHPS (Pusat Informasi Harga Pangan Strategis)** Bank Indonesia.

### ✨ Fitur Utama

- ✅ **Scraping Otomatis**: Ambil data harga dari 34 provinsi Indonesia
- ✅ **API-Based**: Tidak butuh Selenium, hanya HTTP requests (cepat & ringan)
- ✅ **Data Transformation**: Convert wide format → long format untuk database
- ✅ **Error Handling**: Robust handling untuk missing data
- ✅ **Scheduled Jobs**: Support untuk GitHub Actions/Cron
- ✅ **CSV Export**: Save data untuk analisa lebih lanjut

---

## 🏗️ Arsitektur

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

## 📈 Roadmap

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

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📝 License

MIT License - lihat [LICENSE](LICENSE) file

---

## 👥 Team

**Project Manager:** [Ayat Tulloh Rahulloh Khomeini]

- **The Builder** (Data Engineer): Handling scraping & database
- **The Storyteller** (Data Analyst): Dashboard & insights

**Data Analyst:** [Naufal Makarim A]

- **The Storyteller** (Data Analyst): Dashboard & Insights

---

## 📧 Contact

- Email: dkhomeini79@gmail.com
- GitHub: [@atrkhomeini](https://github.com/atrkhomeini)
- Project Link: [Nusantara Food Watch](https://github.com/atrkhomeini/nusantara-food-watch)

---

## 🙏 Acknowledgments

- Data source: [PIHPS Bank Indonesia](https://www.bi.go.id/hargapangan/)
- Kementerian Pertanian RI
- Komunitas data science Indonesia

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/atrkhomeini/nusantara-food-watch?style=social)
![GitHub forks](https://img.shields.io/github/forks/atrkhomeini/nusantara-food-watch?style=social)
![GitHub issues](https://img.shields.io/github/issues/atrkhomeini/nusantara-food-watch)

---

**Made with ❤️ for Indonesia**