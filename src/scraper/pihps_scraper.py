"""
PIHPS Scraper - Nusantara Food Watch
Scraper untuk data harga pangan dari BI/PIHPS
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PIHPSScraper:
    """
    Scraper untuk website PIHPS (Pusat Informasi Harga Pangan Strategis)
    
    Base URL: https://www.bi.go.id/hargapangan/
    """
    
    BASE_URL = "https://www.bi.go.id/hargapangan/WebSite/TabelHarga"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'X-Requested-With': 'XMLHttpRequest',  # ← ADD THIS LINE!
            'Referer': 'https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalKomoditas',
        })
    
    def get_provinces(self) -> List[Dict]:
        """
        Ambil daftar provinsi dari endpoint GetRefProvince
        
        Returns:
            List of dict dengan struktur:
            [
                {"id": "1", "name": "Aceh"},
                {"id": "2", "name": "Sumatera Utara"},
                ...
            ]
        """
        url = f"{self.BASE_URL}/GetRefProvince"
        
        try:
            # Add cache-busting timestamp
            params = {'_': int(time.time() * 1000)}
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✅ Berhasil ambil {len(data)} provinsi")
            return data
            
        except Exception as e:
            logger.error(f"❌ Gagal ambil daftar provinsi: {e}")
            return []
    
    def get_commodities(self) -> List[Dict]:
        """
        Ambil daftar komoditas dari endpoint GetRefCommodityAndCategory
        
        Returns:
            List of dict dengan kategori dan komoditas
        """
        url = f"{self.BASE_URL}/GetRefCommodityAndCategory"
        
        try:
            params = {'_': int(time.time() * 1000)}
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✅ Berhasil ambil data komoditas")
            return data
            
        except Exception as e:
            logger.error(f"❌ Gagal ambil daftar komoditas: {e}")
            return []
    
    def get_harga_data(
        self,
        price_type_id: int = 1,
        commodity_cat_id: str = "cat_1",
        province_id: str = "",
        start_date: str = None,
        end_date: str = None
    ) -> Dict:
        """
        Ambil data harga dari endpoint GetGridDataKomoditas
        
        Args:
            price_type_id: 1=Pasar Tradisional, 2=Pasar Modern (?)
            commodity_cat_id: Kategori komoditas (cat_1, cat_2, dll)
            province_id: ID provinsi (kosong = semua provinsi)
            start_date: Tanggal mulai (format: YYYY-MM-DD)
            end_date: Tanggal akhir (format: YYYY-MM-DD)
        
        Returns:
            Dict dengan key 'data' berisi list provinsi dan harganya
        """
        url = f"{self.BASE_URL}/GetGridDataKomoditas"
        
        # Default date range: 7 hari terakhir
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        params = {
            'price_type_id': price_type_id,
            'commodity_cat_id': commodity_cat_id,
            'province_id': province_id,
            'regency_id': '',
            'showKota': 'false',
            'showPasar': 'false',
            'tipe_laporan': '1',
            'start_date': start_date,
            'end_date': end_date,
            '_': int(time.time() * 1000)
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"✅ Berhasil ambil data harga ({start_date} s/d {end_date})")
            return data
            
        except Exception as e:
            logger.error(f"❌ Gagal ambil data harga: {e}")
            return {"data": []}
    
    # Add this method to PIHPSScraper class
    def debug_api_response(self, commodity_cat_id: str = "cat_1"):
        """
        Debug helper to see raw API response
        """
        url = f"{self.BASE_URL}/GetGridDataKomoditas"
        
        # Recent 3 days
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
        
        params = {
            'price_type_id': 1,
            'commodity_cat_id': commodity_cat_id,
            'province_id': '31',  # DKI Jakarta
            'regency_id': '',
            'showKota': 'false',
            'showPasar': 'false',
            'tipe_laporan': '1',
            'start_date': start_date,
            'end_date': end_date,
            '_': int(time.time() * 1000)
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Save to file for inspection
            with open('api_response_debug.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print("✅ API response saved to: api_response_debug.json")
            print("\n📋 Response structure preview:")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])  # First 2000 chars
            
            return data
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def transform_to_long_format(self, raw_data: Dict) -> pd.DataFrame:
        """
        Transform data dari wide format ke long format
        
        Wide format (dari API):
        {
            "name": "Aceh",
            "19/11/2025": "14,500",
            "20/11/2025": "14,500"
        }
        
        Long format (untuk database):
        | provinsi | tanggal    | harga |
        | Aceh     | 2025-11-19 | 14500 |
        | Aceh     | 2025-11-20 | 14500 |
        """
        
        if not raw_data.get('data'):
            logger.warning("⚠️ Data kosong, skip transform")
            return pd.DataFrame()
        
        all_rows = []
        
        for item in raw_data['data']:
            provinsi = item.get('name', '')
            level = item.get('level', 0)
            
            # Skip agregat nasional (level 0)
            if level == 0:
                continue
            
            # Extract semua kolom tanggal (yang formatnya DD/MM/YYYY)
            for key, value in item.items():
                if '/' in key:  # Ini adalah kolom tanggal
                    try:
                        # Parse tanggal dari format DD/MM/YYYY
                        tanggal = datetime.strptime(key, '%d/%m/%Y').date()
                        
                        # Clean harga (remove koma, convert ke float)
                        if value == '-' or value == '':
                            harga = None
                        else:
                            harga = float(value.replace(',', ''))
                        
                        all_rows.append({
                            'provinsi': provinsi,
                            'tanggal': tanggal,
                            'harga': harga
                        })
                    
                    except Exception as e:
                        logger.warning(f"⚠️ Gagal parse {provinsi} - {key}: {e}")
                        continue
        
        df = pd.DataFrame(all_rows)
        
        if not df.empty:
            logger.info(f"✅ Transform berhasil: {len(df)} rows")
        
        return df
    
    def scrape_all_provinces(
        self,
        days_back: int = 7,
        commodity_cat_id: str = "cat_1"
    ) -> pd.DataFrame:
        """
        Scrape semua provinsi untuk periode tertentu
        
        Args:
            days_back: Berapa hari ke belakang dari hari ini
            commodity_cat_id: Kategori komoditas
        
        Returns:
            DataFrame dengan kolom: provinsi, tanggal, harga
        """
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        logger.info(f"🚀 Mulai scraping: {start_date} s/d {end_date}")
        
        # Ambil data (province_id kosong = semua provinsi)
        raw_data = self.get_harga_data(
            price_type_id=1,
            commodity_cat_id=commodity_cat_id,
            province_id="",
            start_date=start_date,
            end_date=end_date
        )
        
        # Transform ke long format
        df = self.transform_to_long_format(raw_data)
        
        if not df.empty:
            # Add metadata
            df['scraped_at'] = datetime.now()
            df['commodity_category'] = commodity_cat_id
            df['source'] = 'PIHPS/BI'
            
            logger.info(f"✅ Scraping selesai: {len(df)} records")
        
        return df
    
    def save_to_csv(self, df: pd.DataFrame, filename: str = None):
        """Save DataFrame ke CSV"""
        
        if df.empty:
            logger.warning("⚠️ DataFrame kosong, tidak ada yang disave")
            return
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'harga_pangan_{timestamp}.csv'
        
        df.to_csv(filename, index=False)
        logger.info(f"💾 Data disimpan ke: {filename}")


def main():
    """
    Contoh penggunaan scraper
    """
    
    print("=" * 60)
    print("🇮🇩 NUSANTARA FOOD WATCH - PIHPS Scraper")
    print("=" * 60)
    
    scraper = PIHPSScraper()
    
    # Test 1: Ambil daftar provinsi
    print("\n📍 Test 1: Ambil daftar provinsi...")
    provinces = scraper.get_provinces()
    if provinces:
        print(f"   Jumlah provinsi: {len(provinces)}")
        print(f"   Contoh: {provinces[0] if provinces else 'N/A'}")
    
    # Test 2: Ambil daftar komoditas
    print("\n🌾 Test 2: Ambil daftar komoditas...")
    commodities = scraper.get_commodities()
    if commodities:
        print(f"   Data komoditas berhasil diambil")
    
    # Test 3: Scrape data 7 hari terakhir
    print("\n📊 Test 3: Scrape data harga 7 hari terakhir...")
    df = scraper.scrape_all_provinces(days_back=7)
    
    if not df.empty:
        print("\n✅ Preview Data:")
        print(df.head(10))
        print(f"\n📈 Total records: {len(df)}")
        print(f"📅 Tanggal range: {df['tanggal'].min()} s/d {df['tanggal'].max()}")
        print(f"🗺️ Jumlah provinsi: {df['provinsi'].nunique()}")
        
        # Save to CSV
        scraper.save_to_csv(df)
    
    print("\n" + "=" * 60)
    print("✅ Scraping selesai!")
    print("=" * 60)


if __name__ == "__main__":
    scraper = PIHPSScraper()
    
    # Debug: See raw API response
    print("\n🔍 DEBUG: Checking API response structure...")
    scraper.debug_api_response(commodity_cat_id="cat_1")