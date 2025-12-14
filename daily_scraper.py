"""
COMPLETE DAILY SCRAPER - Categories + Subcategories
Scrapes BOTH category-level AND subcategory-level data

This ensures complete coverage:
- Categories (cat_*): For aggregated analysis
- Subcategories (com_*): For quality-level detail

Usage:
    python daily_scraper_complete.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import logging
import time
import pandas as pd

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / 'src' / 'scraper'))
sys.path.insert(0, str(project_root))

from src.scraper.app_scraper import EnhancedMultiCommodityScraper
from src.db.nusantara_db import NusantaraDatabaseNormalized

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# CATEGORIES (10 commodities - aggregated)
CATEGORIES = {
    'cat_1': {'commodity_id': 1, 'name': 'Beras'},
    'cat_2': {'commodity_id': 2, 'name': 'Daging Ayam'},
    'cat_3': {'commodity_id': 3, 'name': 'Daging Sapi'},
    'cat_4': {'commodity_id': 4, 'name': 'Telur Ayam'},
    'cat_5': {'commodity_id': 5, 'name': 'Bawang Merah'},
    'cat_6': {'commodity_id': 6, 'name': 'Bawang Putih'},
    'cat_7': {'commodity_id': 7, 'name': 'Cabai Merah'},
    'cat_8': {'commodity_id': 8, 'name': 'Cabai Rawit'},
    'cat_9': {'commodity_id': 9, 'name': 'Minyak Goreng'},
    'cat_10': {'commodity_id': 10, 'name': 'Gula Pasir'},
}

# SUBCATEGORIES (21 subcommodities - quality-level detail)
SUBCATEGORIES = {
    'com_1': {'commodity_id': 1, 'name': 'Beras Kualitas Bawah I', 'quality': 'Low'},
    'com_2': {'commodity_id': 1, 'name': 'Beras Kualitas Bawah II', 'quality': 'Low'},
    'com_3': {'commodity_id': 1, 'name': 'Beras Kualitas Medium I', 'quality': 'Medium'},
    'com_4': {'commodity_id': 1, 'name': 'Beras Kualitas Medium II', 'quality': 'Medium'},
    'com_5': {'commodity_id': 1, 'name': 'Beras Kualitas Super I', 'quality': 'Premium'},
    'com_6': {'commodity_id': 1, 'name': 'Beras Kualitas Super II', 'quality': 'Premium'},
    'com_7': {'commodity_id': 2, 'name': 'Daging Ayam Ras Segar', 'quality': 'Standard'},
    'com_8': {'commodity_id': 3, 'name': 'Daging Sapi Kualitas 1', 'quality': 'Premium'},
    'com_9': {'commodity_id': 3, 'name': 'Daging Sapi Kualitas 2', 'quality': 'Standard'},
    'com_10': {'commodity_id': 4, 'name': 'Telur Ayam Ras Segar', 'quality': 'Standard'},
    'com_11': {'commodity_id': 5, 'name': 'Bawang Merah Ukuran Sedang', 'quality': 'Standard'},
    'com_12': {'commodity_id': 6, 'name': 'Bawang Putih Ukuran Sedang', 'quality': 'Standard'},
    'com_13': {'commodity_id': 7, 'name': 'Cabai Merah Besar', 'quality': 'Standard'},
    'com_14': {'commodity_id': 7, 'name': 'Cabai Merah Keriting', 'quality': 'Standard'},
    'com_15': {'commodity_id': 8, 'name': 'Cabai Rawit Hijau', 'quality': 'Standard'},
    'com_16': {'commodity_id': 8, 'name': 'Cabai Rawit Merah', 'quality': 'Standard'},
    'com_17': {'commodity_id': 9, 'name': 'Minyak Goreng Curah', 'quality': 'Standard'},
    'com_18': {'commodity_id': 9, 'name': 'Minyak Goreng Kemasan Bermerk 1', 'quality': 'Premium'},
    'com_19': {'commodity_id': 9, 'name': 'Minyak Goreng Kemasan Bermerk 2', 'quality': 'Premium'},
    'com_20': {'commodity_id': 10, 'name': 'Gula Pasir Kualitas Premium', 'quality': 'Premium'},
    'com_21': {'commodity_id': 10, 'name': 'Gula Pasir Lokal', 'quality': 'Standard'},
}


def scrape_complete_daily(days_back: int = 7, market_type_id: int = 1):
    """
    Complete daily scraping - BOTH categories AND subcategories
    
    Args:
        days_back: Days to look back (7 for overlap)
        market_type_id: 1=Traditional, 2=Modern, 3=Wholesale, 4=Producer
    """
    
    start_time = datetime.now()
    
    logger.info("="*70)
    logger.info("📅 COMPLETE DAILY SCRAPER - Categories + Subcategories")
    logger.info("="*70)
    logger.info(f"Run time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    logger.info(f"Period: {start_date.date()} to {end_date.date()}")
    
    # Statistics
    stats = {
        'start_time': start_time,
        'categories_scraped': 0,
        'categories_failed': 0,
        'subcategories_scraped': 0,
        'subcategories_failed': 0,
        'total_inserted': 0,
        'errors': []
    }
    
    # Initialize
    scraper = EnhancedMultiCommodityScraper()
    db = NusantaraDatabaseNormalized()
    db.connect()
    
    # Get mappings from database
    cursor = db.conn.cursor()
    
    cursor.execute("SELECT province_id, province_name FROM dim_provinces")
    province_map = {name: id for id, name in cursor.fetchall()}
    
    cursor.execute("SELECT subcategory_id, subcategory_name FROM dim_subcategories")
    subcategory_map = {name: id for id, name in cursor.fetchall()}
    
    cursor.close()
    
    # ==================================================================
    # PART 1: SCRAPE CATEGORIES (cat_1 to cat_10)
    # ==================================================================
    
    logger.info(f"\n{'='*70}")
    logger.info(f"📦 PART 1: SCRAPING CATEGORIES ({len(CATEGORIES)} items)")
    logger.info(f"{'='*70}")
    
    for idx, (cat_id, cat_info) in enumerate(CATEGORIES.items(), 1):
        logger.info(f"\n[{idx}/{len(CATEGORIES)}] {cat_info['name']} ({cat_id})")
        
        try:
            df = scraper.scrape_commodity(
                commodity_id=cat_id,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'),
                market_type_id=market_type_id,
                tipe_laporan=1  # Daily
            )
            
            if df.empty:
                logger.info(f"   ⚠️  No data")
                stats['categories_failed'] += 1
                continue
            
            # Add metadata
            df['db_commodity_id'] = cat_info['commodity_id']
            df['subcategory_id_mapped'] = None  # Categories don't have subcategory
            
            # Insert
            inserted = insert_to_database(db, df, province_map, subcategory_map, is_category=True)
            
            stats['categories_scraped'] += 1
            stats['total_inserted'] += inserted
            
            logger.info(f"   ✅ {inserted} records inserted")
            
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")
            stats['categories_failed'] += 1
            stats['errors'].append(f"{cat_id}: {e}")
        
        time.sleep(1)
    
    # ==================================================================
    # PART 2: SCRAPE SUBCATEGORIES (com_1 to com_21)
    # ==================================================================
    
    logger.info(f"\n{'='*70}")
    logger.info(f"📦 PART 2: SCRAPING SUBCATEGORIES ({len(SUBCATEGORIES)} items)")
    logger.info(f"{'='*70}")
    
    for idx, (subcom_id, subcom_info) in enumerate(SUBCATEGORIES.items(), 1):
        logger.info(f"\n[{idx}/{len(SUBCATEGORIES)}] {subcom_info['name']} ({subcom_id})")
        
        try:
            df = scraper.scrape_commodity(
                commodity_id=subcom_id,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'),
                market_type_id=market_type_id,
                tipe_laporan=1  # Daily
            )
            
            if df.empty:
                logger.info(f"   ⚠️  No data")
                stats['subcategories_failed'] += 1
                continue
            
            # Add metadata
            df['db_commodity_id'] = subcom_info['commodity_id']
            df['subcommodity_name'] = subcom_info['name']
            df['subcategory_id_mapped'] = df['subcommodity_name'].map(subcategory_map)
            
            # Insert
            inserted = insert_to_database(db, df, province_map, subcategory_map, is_category=False)
            
            stats['subcategories_scraped'] += 1
            stats['total_inserted'] += inserted
            
            logger.info(f"   ✅ {inserted} records inserted")
            
        except Exception as e:
            logger.error(f"   ❌ Error: {e}")
            stats['subcategories_failed'] += 1
            stats['errors'].append(f"{subcom_id}: {e}")
        
        time.sleep(1)
    
    # Final stats
    stats['end_time'] = datetime.now()
    stats['duration'] = (stats['end_time'] - stats['start_time']).total_seconds()
    
    logger.info(f"\n{'='*70}")
    logger.info("📊 COMPLETE DAILY SCRAPE FINISHED")
    logger.info(f"{'='*70}")
    logger.info(f"Duration: {stats['duration']:.1f} seconds")
    logger.info(f"\nCategories:")
    logger.info(f"  ✅ Scraped: {stats['categories_scraped']}/{len(CATEGORIES)}")
    logger.info(f"  ❌ Failed: {stats['categories_failed']}")
    logger.info(f"\nSubcategories:")
    logger.info(f"  ✅ Scraped: {stats['subcategories_scraped']}/{len(SUBCATEGORIES)}")
    logger.info(f"  ❌ Failed: {stats['subcategories_failed']}")
    logger.info(f"\n💾 Total inserted: {stats['total_inserted']:,} records")
    
    if stats['errors']:
        logger.warning(f"\n⚠️  Errors ({len(stats['errors'])}):")
        for err in stats['errors'][:5]:
            logger.warning(f"   {err}")
    
    db.close()
    
    return stats


def insert_to_database(db, df, province_map, subcategory_map, is_category=False):
    """
    Insert data to database
    
    Args:
        db: Database connection
        df: DataFrame with scraped data
        province_map: Province name → ID mapping
        subcategory_map: Subcategory name → ID mapping
        is_category: True if category-level (NULL subcategory_id)
    """
    
    # Map provinces
    df['province_id'] = df['provinsi'].map(province_map)
    
    # Prepare records
    records = []
    for _, row in df.iterrows():
        if pd.isna(row['province_id']) or pd.isna(row['harga']):
            continue
        
        # Subcategory ID (NULL for categories, mapped for subcategories)
        if is_category:
            subcategory_id = None
        else:
            subcategory_id = row.get('subcategory_id_mapped')
            if pd.isna(subcategory_id):
                continue
        
        records.append((
            int(row['province_id']),
            int(row['db_commodity_id']),
            int(subcategory_id) if subcategory_id is not None else None,
            int(row['market_type_id']),
            row['tanggal'],
            float(row['harga'])
        ))
    
    if not records:
        return 0
    
    # Insert
    cursor = db.conn.cursor()
    
    insert_query = """
        INSERT INTO fact_prices 
        (province_id, commodity_id, subcategory_id, market_type_id, tanggal, harga)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """
    
    try:
        cursor.executemany(insert_query, records)
        db.conn.commit()
        inserted = cursor.rowcount
        cursor.close()
        return inserted
    
    except Exception as e:
        db.conn.rollback()
        cursor.close()
        logger.error(f"Insert error: {e}")
        return 0


def send_notification(stats):
    """Send email notification with results"""
    
    try:
        from src.utils.notifications import send_success_email, send_failure_email
        
        total_scraped = stats['categories_scraped'] + stats['subcategories_scraped']
        total_items = len(CATEGORIES) + len(SUBCATEGORIES)
        
        if stats['total_inserted'] > 0:
            send_success_email(
                subject=f"✅ Complete Daily Scrape - {stats['total_inserted']:,} records",
                body=f"""
Nusantara Food Watch - Complete Daily Scraper Report

Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Duration: {stats['duration']:.1f} seconds

Categories (Aggregated):
  ✅ Scraped: {stats['categories_scraped']}/10
  ❌ Failed: {stats['categories_failed']}

Subcategories (Quality-Level):
  ✅ Scraped: {stats['subcategories_scraped']}/21
  ❌ Failed: {stats['subcategories_failed']}

Total: {total_scraped}/{total_items} items
Database inserted: {stats['total_inserted']:,} records

Status: ✅ SUCCESS
                """
            )
        else:
            send_failure_email(f"No data inserted. Check logs.")
        
        logger.info("✅ Email notification sent")
    
    except Exception as e:
        logger.warning(f"⚠️  Could not send email: {e}")


def main():
    """Main execution"""
    
    try:
        # Run complete scrape
        stats = scrape_complete_daily(
            days_back=7,
            market_type_id=1
        )
        
        # Send notification
        send_notification(stats)
        
        # Exit
        if stats['total_inserted'] > 0:
            logger.info("\n✅ Daily scrape successful!")
            exit(0)
        else:
            logger.warning("\n⚠️ No data inserted!")
            exit(1)
    
    except Exception as e:
        logger.error(f"\n❌ Daily scrape failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()