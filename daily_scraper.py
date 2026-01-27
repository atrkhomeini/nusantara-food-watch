"""
COMPLETE DAILY SCRAPER - Categories + Subcategories
Scrapes BOTH category-level AND subcategory-level data
Iterates through ALL Market Types.

Usage:
    python daily_scraper.py
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
from src.utils.notifications import send_success_email, send_failure_email

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
    
    # Get Market Name for logging
    market_name = EnhancedMultiCommodityScraper.MARKET_TYPES.get(market_type_id, f"Market {market_type_id}")
    
    start_time = datetime.now()
    
    logger.info("\n" + "#"*70)
    logger.info(f"🏗️  SCRAPING MARKET: {market_name.upper()} (ID: {market_type_id})")
    logger.info("#"*70)
    
    # Date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    
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
    
    logger.info(f"📦 [{market_name}] Scraping Categories...")
    
    for idx, (cat_id, cat_info) in enumerate(CATEGORIES.items(), 1):
        try:
            df = scraper.scrape_commodity(
                commodity_id=cat_id,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'),
                market_type_id=market_type_id,
                tipe_laporan=1  # Daily
            )
            
            if df.empty:
                stats['categories_failed'] += 1
                continue
            
            # Add metadata
            df['db_commodity_id'] = cat_info['commodity_id']
            df['subcategory_id_mapped'] = None
            
            # Insert
            inserted = insert_to_database(db, df, province_map, subcategory_map, is_category=True)
            
            stats['categories_scraped'] += 1
            stats['total_inserted'] += inserted
            
            logger.info(f"   [{cat_info['name']}] ✅ {inserted} rows")
            
        except Exception as e:
            logger.error(f"   ❌ Error {cat_info['name']}: {e}")
            stats['categories_failed'] += 1
            stats['errors'].append(f"{market_name}-{cat_id}: {e}")
        
        time.sleep(1)
    
    # ==================================================================
    # PART 2: SCRAPE SUBCATEGORIES (com_1 to com_21)
    # ==================================================================
    
    logger.info(f"📦 [{market_name}] Scraping Subcategories...")
    
    for idx, (subcom_id, subcom_info) in enumerate(SUBCATEGORIES.items(), 1):
        try:
            df = scraper.scrape_commodity(
                commodity_id=subcom_id,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'),
                market_type_id=market_type_id,
                tipe_laporan=1  # Daily
            )
            
            if df.empty:
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
            
            logger.info(f"   [{subcom_info['name']}] ✅ {inserted} rows")
            
        except Exception as e:
            logger.error(f"   ❌ Error {subcom_info['name']}: {e}")
            stats['subcategories_failed'] += 1
            stats['errors'].append(f"{market_name}-{subcom_id}: {e}")
        
        time.sleep(1)
    
    db.close()
    return stats


def insert_to_database(db, df, province_map, subcategory_map, is_category=False):
    """
    Insert data to database (Same as before)
    """
    # Map provinces
    df['province_id'] = df['provinsi'].map(province_map)
    
    # Prepare records
    records = []
    for _, row in df.iterrows():
        if pd.isna(row['province_id']) or pd.isna(row['harga']):
            continue
        
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


def send_aggregated_notification(total_stats):
    """Send summary email for ALL markets"""
    
    try:
        if total_stats['total_inserted'] > 0:
            send_success_email(
                subject=f"✅ Daily Scrape Complete - {total_stats['total_inserted']:,} records",
                body=f"""
Nusantara Food Watch - Daily Scraper Report
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Duration: {total_stats['duration']:.1f} seconds

Markets Processed: {total_stats['markets_count']}

Summary:
  Total Records Inserted: {total_stats['total_inserted']:,}
  
  Categories (Across all markets):
    Scraped: {total_stats['categories_scraped']}
    Failed: {total_stats['categories_failed']}
    
  Subcategories (Across all markets):
    Scraped: {total_stats['subcategories_scraped']}
    Failed: {total_stats['subcategories_failed']}

Status: 200 - SUCCESS
                """
            )
        else:
            send_failure_email(f"Daily scrape finished but NO data was inserted from any market.")
        
        logger.info("✅ Email notification sent")
    
    except Exception as e:
        logger.warning(f"⚠️  Could not send email: {e}")


def main():
    """Main execution - Loops through ALL Market Types"""
    
    start_time_global = datetime.now()
    
    # Initialize Global Stats
    global_stats = {
        'total_inserted': 0,
        'categories_scraped': 0,
        'categories_failed': 0,
        'subcategories_scraped': 0,
        'subcategories_failed': 0,
        'markets_count': 0,
        'errors': []
    }
    
    try:
        # Get all market types from the Scraper Class
        # {1: 'Pasar Tradisional', 2: 'Pasar Modern', ...}
        market_types = EnhancedMultiCommodityScraper.MARKET_TYPES
        
        logger.info("="*70)
        logger.info(f"🚀 STARTING DAILY SCRAPE FOR {len(market_types)} MARKETS")
        logger.info("="*70)
        
        # Loop through each market
        for market_id, market_name in market_types.items():
            try:
                # Run scrape for this specific market
                stats = scrape_complete_daily(
                    days_back=7,
                    market_type_id=market_id
                )
                
                # Aggregate results
                global_stats['total_inserted'] += stats['total_inserted']
                global_stats['categories_scraped'] += stats['categories_scraped']
                global_stats['categories_failed'] += stats['categories_failed']
                global_stats['subcategories_scraped'] += stats['subcategories_scraped']
                global_stats['subcategories_failed'] += stats['subcategories_failed']
                global_stats['errors'].extend(stats['errors'])
                global_stats['markets_count'] += 1
                
            except Exception as e:
                logger.error(f"❌ Critical failure for market {market_name}: {e}")
                global_stats['errors'].append(f"CRITICAL {market_name}: {e}")
        
        # Calculate total duration
        global_stats['duration'] = (datetime.now() - start_time_global).total_seconds()
        
        # Log Final Summary
        logger.info("\n" + "="*70)
        logger.info("🏁 GLOBAL SCRAPE FINISHED")
        logger.info("="*70)
        logger.info(f"Total Markets: {global_stats['markets_count']}")
        logger.info(f"Total Inserted: {global_stats['total_inserted']:,} records")
        
        # Send one consolidated email
        send_aggregated_notification(global_stats)
        
        if global_stats['total_inserted'] > 0:
            exit(0)
        else:
            logger.warning("⚠️ No data inserted in total!")
            exit(1)
            
    except Exception as e:
        logger.error(f"\n❌ Global scrape script failed: {e}")
        import traceback
        traceback.print_exc()
        send_failure_email(f"Script crashed: {e}")
        exit(1)


if __name__ == "__main__":
    main()