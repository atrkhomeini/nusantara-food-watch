"""
ENHANCED PIHPS SCRAPER - Multi-Commodity + Monthly Data
Supports all 10 food commodities with monthly aggregation
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from nusantara_db import NusantaraDatabase
import time
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EnhancedMultiCommodityScraper:
    """
    Enhanced scraper with multi-commodity support
    """
    
    BASE_URL = "https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetGridDataKomoditas"
    
    # Complete commodity list from PIHPS
    COMMODITIES = {
        'cat_1': {
            'name': 'Beras',
            'subcategories': [
                'Beras Kualitas Bawah I',
                'Beras Kualitas Bawah II', 
                'Beras Kualitas Medium I',
                'Beras Kualitas Medium II',
                'Beras Kualitas Super I',
                'Beras Kualitas Super II'
            ]
        },
        'cat_2': {
            'name': 'Daging Ayam',
            'subcategories': ['Daging Ayam Ras Segar']
        },
        'cat_3': {
            'name': 'Daging Sapi',
            'subcategories': [
                'Daging Sapi Kualitas 1',
                'Daging Sapi Kualitas 2'
            ]
        },
        'cat_4': {
            'name': 'Telur Ayam',
            'subcategories': ['Telur Ayam Ras Segar']
        },
        'cat_5': {
            'name': 'Bawang Merah',
            'subcategories': ['Bawang Merah Ukuran Sedang']
        },
        'cat_6': {
            'name': 'Bawang Putih',
            'subcategories': ['Bawang Putih Ukuran Sedang']
        },
        'cat_7': {
            'name': 'Cabai Merah',
            'subcategories': [
                'Cabai Merah Besar',
                'Cabai Merah Keriting'
            ]
        },
        'cat_8': {
            'name': 'Cabai Rawit',
            'subcategories': [
                'Cabai Rawit Hijau',
                'Cabai Rawit Merah'
            ]
        },
        'cat_9': {
            'name': 'Minyak Goreng',
            'subcategories': [
                'Minyak Goreng Curah',
                'Minyak Goreng Kemasan Bermerk 1',
                'Minyak Goreng Kemasan Bermerk 2'
            ]
        },
        'cat_10': {
            'name': 'Gula Pasir',
            'subcategories': [
                'Gula Pasir Kualitas Premium',
                'Gula Pasir Lokal'
            ]
        }
    }
    
    MARKET_TYPES = {
        1: "Pasar Tradisional",
        2: "Pasar Modern",
        3: "Pedagang Besar",
        4: "Produsen"
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalDaerah'
        })
    
    def clean_price(self, price_str):
        """Convert Indonesian number format to float"""
        if not price_str or price_str == '-':
            return None
        try:
            return float(price_str.replace(',', ''))
        except:
            return None
    
    def transform_wide_to_long(self, data, commodity_id, commodity_name):
        """
        Transform WIDE format to LONG format with commodity info
        
        Handles both formats:
        - Daily: "20/11/2025" 
        - Monthly: "Aug 2025", "Sep 2025"
        """
        
        if not data:
            logger.warning("No data to transform")
            return pd.DataFrame()
        
        logger.info(f"Transforming {len(data)} rows...")
        
        rows = []
        
        # Month name to number mapping
        month_map = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
            'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
            'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        
        for idx, item in enumerate(data):
            province_name = item.get('name')
            level = item.get('level', 1)
            row_no = item.get('no', '')
            
            # Debug first few rows
            if idx < 3:
                logger.info(f"  Row {idx}: name='{province_name}', level={level}, no='{row_no}'")
            
            # Skip aggregate row (level 0 or name contains "Semua")
            if level == 0 or 'Semua' in str(province_name):
                logger.info(f"  Skipping aggregate row: {province_name}")
                continue
            
            # Extract all columns that look like dates
            date_cols = []
            for key in item.keys():
                if key in ['no', 'name', 'level']:
                    continue
                
                # Check if daily format (DD/MM/YYYY)
                if '/' in str(key):
                    date_cols.append(('daily', key))
                # Check if monthly format (MMM YYYY)
                elif any(month in str(key) for month in month_map.keys()):
                    date_cols.append(('monthly', key))
            
            if idx == 1:  # Show for first province
                logger.info(f"  Found {len(date_cols)} date columns")
                if date_cols:
                    logger.info(f"  Sample: {date_cols[:3]}")
            
            # Process each date column
            for date_type, date_key in date_cols:
                value = item.get(date_key)
                
                # Parse date based on format
                try:
                    if date_type == 'daily':
                        # Daily: "20/11/2025" → "2025-11-20"
                        day, month, year = str(date_key).split('/')
                        tanggal = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    
                    elif date_type == 'monthly':
                        # Monthly: "Aug 2025" → "2025-08-01"
                        parts = str(date_key).split()
                        if len(parts) == 2:
                            month_name, year = parts
                            month_num = month_map.get(month_name, '01')
                            # Use first day of month for monthly data
                            tanggal = f"{year}-{month_num}-01"
                        else:
                            continue
                    else:
                        continue
                
                except Exception as e:
                    if idx < 3:
                        logger.warning(f"  Failed to parse date '{date_key}': {e}")
                    continue
                
                # Clean price
                harga = self.clean_price(value)
                
                if harga is not None:
                    rows.append({
                        'provinsi': province_name,
                        'tanggal': tanggal,
                        'harga': harga,
                        'commodity_id': commodity_id,
                        'commodity_name': commodity_name,
                        'subcategory': None
                    })
        
        if not rows:
            logger.warning(f"❌ No valid rows extracted! Check data structure.")
            # Debug: show one full item
            if data:
                logger.info(f"Sample item keys: {list(data[1].keys()) if len(data) > 1 else list(data[0].keys())}")
            return pd.DataFrame()
        
        df = pd.DataFrame(rows)
        logger.info(f"✅ Extracted {len(df)} price records")
        
        return df
    
    def scrape_commodity(
        self,
        commodity_id: str,
        start_date: str,
        end_date: str,
        market_type_id: int = 1,
        tipe_laporan: int = 3  # 3=Monthly (default)
    ):
        """
        Scrape specific commodity for date range
        """
        
        commodity_info = self.COMMODITIES.get(commodity_id, {'name': commodity_id})
        commodity_name = commodity_info['name']
        market_name = self.MARKET_TYPES.get(market_type_id, "Unknown")
        
        report_types = {1: 'Harian', 2: 'Mingguan', 3: 'Bulanan'}
        
        logger.info(f"\n{'='*70}")
        logger.info(f"🛒 Commodity: {commodity_name} ({commodity_id})")
        logger.info(f"🏪 Market: {market_name}")
        logger.info(f"📅 Period: {start_date} to {end_date}")
        logger.info(f"📊 Type: {report_types.get(tipe_laporan, 'Unknown')}")
        logger.info(f"{'='*70}")
        
        params = {
            'price_type_id': market_type_id,
            'comcat_id': commodity_id,
            'province_id': '',
            'regency_id': '',
            'showKota': 'false',
            'showPasar': 'false',
            'tipe_laporan': tipe_laporan,
            'start_date': start_date,
            'end_date': end_date
        }
        
        try:
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"❌ HTTP {response.status_code}")
                return pd.DataFrame()
            
            result = response.json()
            
            if 'data' not in result or not result['data']:
                logger.warning(f"⚠️ No data for {commodity_name}")
                return pd.DataFrame()
            
            data = result['data']
            logger.info(f"✅ Received {len(data)} rows")
            
            # Transform
            df = self.transform_wide_to_long(data, commodity_id, commodity_name)
            
            if df.empty:
                logger.warning(f"⚠️ No valid data after transformation")
                return df
            
            # Add metadata
            df['market_type_id'] = market_type_id
            df['market_type_name'] = market_name
            df['report_type'] = report_types.get(tipe_laporan, 'daily').lower()
            
            logger.info(f"✅ Transformed to {len(df)} records")
            logger.info(f"   Provinces: {df['provinsi'].nunique()}")
            logger.info(f"   Date range: {df['tanggal'].min()} to {df['tanggal'].max()}")
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def scrape_all_commodities(
        self,
        start_date: str,
        end_date: str,
        market_type_id: int = 1,
        tipe_laporan: int = 3,
        commodities: list = None
    ):
        """
        Scrape all (or selected) commodities
        """
        
        if commodities is None:
            commodities = list(self.COMMODITIES.keys())
        
        logger.info(f"\n{'='*70}")
        logger.info(f"🛒 SCRAPING {len(commodities)} COMMODITIES")
        logger.info(f"{'='*70}")
        
        all_data = []
        
        for i, commodity_id in enumerate(commodities, 1):
            logger.info(f"\n[{i}/{len(commodities)}] Processing {commodity_id}...")
            
            df = self.scrape_commodity(
                commodity_id=commodity_id,
                start_date=start_date,
                end_date=end_date,
                market_type_id=market_type_id,
                tipe_laporan=tipe_laporan
            )
            
            if not df.empty:
                all_data.append(df)
            
            # Rate limiting
            time.sleep(2)
        
        if not all_data:
            logger.warning("⚠️ No data collected")
            return pd.DataFrame()
        
        df_combined = pd.concat(all_data, ignore_index=True)
        
        logger.info(f"\n{'='*70}")
        logger.info(f"✅ COMBINED RESULTS")
        logger.info(f"{'='*70}")
        logger.info(f"Total records: {len(df_combined):,}")
        logger.info(f"Commodities: {df_combined['commodity_name'].nunique()}")
        logger.info(f"Provinces: {df_combined['provinsi'].nunique()}")
        
        return df_combined
    
    def scrape_monthly_historical(
        self,
        years_back: int = 8,
        market_type_id: int = 1,
        commodities: list = None
    ):
        """
        Scrape monthly historical data for multiple commodities
        """
        
        logger.info(f"\n{'='*70}")
        logger.info(f"📅 MONTHLY HISTORICAL SCRAPE ({years_back} years)")
        logger.info(f"{'='*70}")
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years_back * 365)
        
        all_data = []
        
        # Break into 1-year chunks
        current_start = start_date
        chunk_days = 365
        
        while current_start < end_date:
            current_end = min(current_start + timedelta(days=chunk_days), end_date)
            
            logger.info(f"\n📦 Chunk: {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}")
            
            df = self.scrape_all_commodities(
                start_date=current_start.strftime('%Y-%m-%d'),
                end_date=current_end.strftime('%Y-%m-%d'),
                market_type_id=market_type_id,
                tipe_laporan=3,  # Monthly
                commodities=commodities
            )
            
            if not df.empty:
                all_data.append(df)
            
            current_start = current_end + timedelta(days=1)
            
            # Rate limiting between chunks
            time.sleep(5)
        
        if not all_data:
            return pd.DataFrame()
        
        df_combined = pd.concat(all_data, ignore_index=True)
        
        logger.info(f"\n✅ Total historical records: {len(df_combined):,}")
        
        return df_combined


def main():
    """
    Main scraping workflow - Monthly Multi-Commodity
    """
    
    logger.info("╔══════════════════════════════════════════════════════════════╗")
    logger.info("║   MULTI-COMMODITY MONTHLY SCRAPER - NUSANTARA FOOD WATCH    ║")
    logger.info("╚══════════════════════════════════════════════════════════════╝")
    
    scraper = EnhancedMultiCommodityScraper()
    db = NusantaraDatabase()
    
    # PHASE 1: Quick test (last 3 months, 3 commodities)
    logger.info("\n📋 PHASE 1: QUICK TEST")
    logger.info("  • Last 6 months")
    logger.info("  • 3 commodities (Beras, Daging Ayam, Minyak Goreng)")
    logger.info("  • Monthly data")
    logger.info("  • 1 market type (Pasar Tradisional)")
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')  # 6 months
    
    df_test = scraper.scrape_all_commodities(
        start_date=start_date,
        end_date=end_date,
        market_type_id=1,
        tipe_laporan=3,  # MONTHLY (now fixed!)
        commodities=['cat_1', 'cat_2', 'cat_9']  # Beras, Ayam, Minyak
    )
    
    if df_test.empty:
        logger.error("❌ TEST FAILED")
        return
    
    logger.info(f"\n✅ TEST SUCCESSFUL - {len(df_test):,} records")
    
    # Show sample
    logger.info(f"\nSample data:")
    logger.info(df_test.head(10).to_string())
    
    # Save test data
    try:
        db.connect()
        db.create_tables()
        
        # Clean commodity_category for database
        df_test['commodity_category'] = df_test['commodity_id']
        
        inserted = db.insert_data(df_test, on_conflict='ignore')
        logger.info(f"\n✅ Saved {inserted} test records to database")
        
        db.close()
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
        return
    
    # PHASE 2: User confirmation for full scrape
    logger.info("\n" + "="*70)
    logger.info("✅ TEST COMPLETE!")
    logger.info("="*70)
    logger.info("\nReady for FULL SCRAPE:")
    logger.info("  • ALL 10 commodities")
    logger.info("  • 8 years historical (monthly)")
    logger.info("  • 4 market types")
    logger.info("  • Estimated records: 100,000+")
    logger.info("  • Estimated time: 2-3 hours")
    
    proceed = input("\nProceed with full scrape? (yes/no): ").strip().lower()
    
    if proceed not in ['yes', 'y']:
        logger.info("\n⏸️ Stopped by user")
        logger.info("\nYou can always run this script again later!")
        logger.info("\nTo test more commodities:")
        logger.info("  Modify commodities=['cat_1', 'cat_2', ...] in the script")
        return
    
    # PHASE 3: Full scrape
    logger.info("\n📋 PHASE 2: FULL HISTORICAL SCRAPE")
    
    for market_id, market_name in scraper.MARKET_TYPES.items():
        logger.info(f"\n\n{'='*70}")
        logger.info(f"🏪 MARKET TYPE {market_id}/4: {market_name}")
        logger.info(f"{'='*70}")
        
        df_full = scraper.scrape_monthly_historical(
            years_back=8,
            market_type_id=market_id,
            commodities=None  # All commodities
        )
        
        if not df_full.empty:
            try:
                db.connect()
                
                # Clean for database
                df_full['commodity_category'] = df_full['commodity_id']
                
                inserted = db.insert_data(df_full, on_conflict='ignore')
                logger.info(f"\n✅ Saved {inserted:,} records for {market_name}")
                
                db.close()
            except Exception as e:
                logger.error(f"❌ Database error: {e}")
        
        # Rate limiting between market types
        time.sleep(10)
    
    # FINAL STATS
    logger.info("\n\n" + "="*70)
    logger.info("✅ FULL SCRAPE COMPLETED!")
    logger.info("="*70)
    
    try:
        db.connect()
        stats = db.get_stats()
        
        logger.info(f"\n📊 FINAL DATABASE STATISTICS:")
        logger.info(f"  Total records: {stats.get('total_records', 0):,}")
        logger.info(f"  Provinces: {stats.get('total_provinces', 0)}")
        logger.info(f"  Date range: {stats.get('earliest_date')} to {stats.get('latest_date')}")
        
        # Per commodity
        query = """
        SELECT commodity_category, COUNT(*) as count
        FROM harga_pangan
        GROUP BY commodity_category
        ORDER BY count DESC
        """
        df_summary = pd.read_sql(query, db.conn)
        logger.info(f"\n📊 Records per commodity:")
        logger.info(f"\n{df_summary.to_string(index=False)}")
        
        db.close()
        
    except Exception as e:
        logger.error(f"❌ Error getting stats: {e}")
    
    logger.info("\n🎉 SUCCESS! Multi-commodity monthly data ready!")
    logger.info("\nNext steps:")
    logger.info("  1. Analyze price trends across commodities")
    logger.info("  2. Compare supply chain margins")
    logger.info("  3. Build comprehensive dashboard")


if __name__ == "__main__":
    main()