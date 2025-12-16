"""
UNIFIED BACKFILL SCRIPT - Categories + Subcategories
Combines backfill_30_days.py and backfill_subcategory.py into one complete solution

This script:
1. Scrapes BOTH categories (cat_*) AND subcategories (com_*)
2. Supports custom date ranges
3. Inserts directly to database (no CSV)
4. Sends email notifications
5. Handles all market types

Usage:
    python backfill_unified.py                          # Last 30 days, both types
    python backfill_unified.py --days 90                # Last 90 days
    python backfill_unified.py --start 2024-01-01 --end 2024-12-31
    python backfill_unified.py --categories-only        # Only categories
    python backfill_unified.py --subcategories-only     # Only subcategories
"""

import sys
from pathlib import Path
import argparse
from datetime import datetime, timedelta
import time
import logging

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

# SUBCATEGORIES (21 subcommodities - quality-level)
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


def backfill_unified(
    start_date: str,
    end_date: str,
    market_types: list = None,
    scrape_categories: bool = True,
    scrape_subcategories: bool = True,
    tipe_laporan: int = 1
):
    """
    Unified backfill - categories AND subcategories
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        market_types: List of market IDs (None = [1] Traditional only)
        scrape_categories: Scrape category-level data
        scrape_subcategories: Scrape subcategory-level data
        tipe_laporan: 1=Daily, 3=Monthly
    """
    
    start_time = datetime.now()
    
    logger.info("="*70)
    logger.info("🔄 UNIFIED BACKFILL - Categories + Subcategories")
    logger.info("="*70)
    logger.info(f"📅 Date range: {start_date} to {end_date}")
    logger.info(f"🏪 Market types: {market_types or [1]}")
    logger.info(f"📊 Report type: {'Daily' if tipe_laporan == 1 else 'Monthly'}")
    logger.info(f"📦 Categories: {'✅ Yes' if scrape_categories else '❌ No'}")
    logger.info(f"📦 Subcategories: {'✅ Yes' if scrape_subcategories else '❌ No'}")
    
    if market_types is None:
        market_types = [1]  # Default: Traditional market only
    
    # Initialize
    scraper = EnhancedMultiCommodityScraper()
    db = NusantaraDatabaseNormalized()
    db.connect()
    
    # Get mappings
    cursor = db.conn.cursor()
    cursor.execute("SELECT province_id, province_name FROM dim_provinces")
    province_map = {name: id for id, name in cursor.fetchall()}
    
    cursor.execute("SELECT subcategory_id, subcategory_name FROM dim_subcategories")
    subcategory_map = {name: id for id, name in cursor.fetchall()}
    cursor.close()
    
    # Statistics
    stats = {
        'categories_scraped': 0,
        'categories_failed': 0,
        'subcategories_scraped': 0,
        'subcategories_failed': 0,
        'total_inserted': 0,
        'errors': []
    }
    
    # Process each market type
    for market_idx, market_id in enumerate(market_types, 1):
        market_names = {
            1: "Traditional Markets",
            2: "Modern Markets/Supermarkets",
            3: "Wholesalers",
            4: "Producers/Farmers"
        }
        
        logger.info(f"\n{'='*70}")
        logger.info(f"🏪 MARKET TYPE {market_idx}/{len(market_types)}: {market_names.get(market_id, 'Unknown')}")
        logger.info(f"{'='*70}")
        
        # ============================================================
        # PART 1: CATEGORIES
        # ============================================================
        
        if scrape_categories:
            logger.info(f"\n📦 PART 1: SCRAPING CATEGORIES ({len(CATEGORIES)} items)")
            
            for idx, (cat_id, cat_info) in enumerate(CATEGORIES.items(), 1):
                logger.info(f"\n[{idx}/10] {cat_info['name']} ({cat_id})")
                
                try:
                    # Check connection
                    try:
                        cursor_test = db.conn.cursor()
                        cursor_test.execute("SELECT 1")
                        cursor_test.close()
                    except:
                        logger.warning("   🔄 Reconnecting...")
                        db.close()
                        db = NusantaraDatabaseNormalized()
                        db.connect()
                        cursor = db.conn.cursor()
                        cursor.execute("SELECT province_id, province_name FROM dim_provinces")
                        province_map = {name: id for id, name in cursor.fetchall()}
                        cursor.execute("SELECT subcategory_id, subcategory_name FROM dim_subcategories")
                        subcategory_map = {name: id for id, name in cursor.fetchall()}
                        cursor.close()
                        logger.info("   ✅ Reconnected")
                    
                    df = scraper.scrape_commodity(
                        commodity_id=cat_id,
                        start_date=start_date,
                        end_date=end_date,
                        market_type_id=market_id,
                        tipe_laporan=tipe_laporan
                    )
                    
                    if df.empty:
                        logger.info("   ⚠️  No data")
                        stats['categories_failed'] += 1
                        continue
                    
                    # Add metadata
                    df['db_commodity_id'] = cat_info['commodity_id']
                    
                    # Insert
                    inserted = insert_to_db(db, df, province_map, subcategory_map, is_category=True)
                    
                    stats['categories_scraped'] += 1
                    stats['total_inserted'] += inserted
                    
                    logger.info(f"   ✅ {inserted} records")
                    
                except Exception as e:
                    logger.error(f"   ❌ Error: {e}")
                    stats['categories_failed'] += 1
                    stats['errors'].append(f"{cat_id}: {e}")
                
                time.sleep(1)
        
        # ============================================================
        # PART 2: SUBCATEGORIES
        # ============================================================
        
        if scrape_subcategories:
            logger.info(f"\n📦 PART 2: SCRAPING SUBCATEGORIES ({len(SUBCATEGORIES)} items)")
            
            for idx, (subcom_id, subcom_info) in enumerate(SUBCATEGORIES.items(), 1):
                logger.info(f"\n[{idx}/21] {subcom_info['name']} ({subcom_id})")
                
                try:
                    # Check connection before each scrape
                    try:
                        cursor_test = db.conn.cursor()
                        cursor_test.execute("SELECT 1")
                        cursor_test.close()
                    except:
                        logger.warning("   🔄 Database connection lost, reconnecting...")
                        db.close()
                        db = NusantaraDatabaseNormalized()
                        db.connect()
                        
                        # Reload mappings
                        cursor = db.conn.cursor()
                        cursor.execute("SELECT province_id, province_name FROM dim_provinces")
                        province_map = {name: id for id, name in cursor.fetchall()}
                        cursor.execute("SELECT subcategory_id, subcategory_name FROM dim_subcategories")
                        subcategory_map = {name: id for id, name in cursor.fetchall()}
                        cursor.close()
                        logger.info("   ✅ Reconnected successfully")
                    
                    df = scraper.scrape_commodity(
                        commodity_id=subcom_id,
                        start_date=start_date,
                        end_date=end_date,
                        market_type_id=market_id,
                        tipe_laporan=tipe_laporan
                    )
                    
                    if df.empty:
                        logger.info("   ⚠️  No data")
                        stats['subcategories_failed'] += 1
                        continue
                    
                    # Add metadata
                    df['db_commodity_id'] = subcom_info['commodity_id']
                    df['subcommodity_name'] = subcom_info['name']
                    
                    # Insert
                    inserted = insert_to_db(db, df, province_map, subcategory_map, is_category=False)
                    
                    stats['subcategories_scraped'] += 1
                    stats['total_inserted'] += inserted
                    
                    logger.info(f"   ✅ {inserted} records")
                    
                except Exception as e:
                    logger.error(f"   ❌ Error: {e}")
                    stats['subcategories_failed'] += 1
                    stats['errors'].append(f"{subcom_id}: {e}")
                
                time.sleep(1)
    
    # Final stats
    duration = (datetime.now() - start_time).total_seconds()
    
    logger.info(f"\n{'='*70}")
    logger.info("✅ UNIFIED BACKFILL COMPLETE")
    logger.info(f"{'='*70}")
    logger.info(f"⏱️  Duration: {int(duration//60)}m {int(duration%60)}s")
    logger.info(f"\nCategories:")
    logger.info(f"  ✅ Scraped: {stats['categories_scraped']}/10")
    logger.info(f"  ❌ Failed: {stats['categories_failed']}")
    logger.info(f"\nSubcategories:")
    logger.info(f"  ✅ Scraped: {stats['subcategories_scraped']}/21")
    logger.info(f"  ❌ Failed: {stats['subcategories_failed']}")
    logger.info(f"\n💾 Total inserted: {stats['total_inserted']:,} records")
    
    if stats['errors']:
        logger.warning(f"\n⚠️  Errors: {len(stats['errors'])}")
        for err in stats['errors'][:5]:
            logger.warning(f"   {err}")
    
    db.close()
    
    return stats, duration


def insert_to_db(db, df, province_map, subcategory_map, is_category=False):
    """Insert data to database"""
    
    import pandas as pd
    
    logger.info(f"   🔍 DEBUG: DataFrame has {len(df)} rows")
    logger.info(f"   🔍 DEBUG: Columns: {list(df.columns)}")
    logger.info(f"   🔍 DEBUG: is_category={is_category}")
    
    # Map province names to IDs
    df['province_id'] = df['provinsi'].map(province_map)
    
    # Debug: Check province mapping
    unmapped_provinces = df[df['province_id'].isna()]['provinsi'].unique()
    if len(unmapped_provinces) > 0:
        logger.warning(f"   ⚠️  Unmapped provinces: {unmapped_provinces[:5]}")
    
    records = []
    skipped = 0
    skip_reasons = {'no_province': 0, 'no_price': 0, 'no_subcat_name': 0, 'unmapped_subcat': 0}
    
    for idx, row in df.iterrows():
        # Skip if missing required data
        if pd.isna(row['province_id']):
            skip_reasons['no_province'] += 1
            skipped += 1
            continue
        
        if pd.isna(row['harga']):
            skip_reasons['no_price'] += 1
            skipped += 1
            continue
        
        # Determine subcategory ID
        if is_category:
            # Categories don't have subcategory
            subcategory_id = None
        else:
            # Subcategories: get ID from name
            # Use bracket notation for pandas Series, not .get()
            if 'subcommodity_name' not in df.columns:
                logger.error(f"   ❌ Column 'subcommodity_name' not in DataFrame!")
                logger.error(f"   Available columns: {list(df.columns)}")
                skip_reasons['no_subcat_name'] += len(df)
                break
            
            subcat_name = row['subcommodity_name']
            
            if idx < 3:  # Debug first 3 rows
                logger.info(f"   🔍 Row {idx}: subcommodity_name='{subcat_name}'")
            
            if pd.isna(subcat_name) or subcat_name is None or subcat_name == '':
                if idx < 3:
                    logger.warning(f"   ⚠️  Row {idx}: Missing subcommodity_name")
                skip_reasons['no_subcat_name'] += 1
                skipped += 1
                continue
            
            subcategory_id = subcategory_map.get(str(subcat_name))  # Convert to string
            
            if idx < 3:
                logger.info(f"   🔍 Row {idx}: Mapped to subcategory_id={subcategory_id}")
            
            if subcategory_id is None:
                if idx < 3:
                    logger.warning(f"   ⚠️  Row {idx}: Unmapped subcategory '{subcat_name}'")
                    logger.info(f"   🔍 Available subcategories: {list(subcategory_map.keys())[:5]}")
                skip_reasons['unmapped_subcat'] += 1
                skipped += 1
                continue
        
        records.append((
            int(row['province_id']),
            int(row['db_commodity_id']),
            int(subcategory_id) if subcategory_id is not None else None,
            int(row['market_type_id']),
            row['tanggal'],
            float(row['harga'])
        ))
    
    logger.info(f"   📊 Prepared {len(records)} records for insert")
    
    if skipped > 0:
        logger.info(f"   ⚠️  Skipped {skipped} records:")
        for reason, count in skip_reasons.items():
            if count > 0:
                logger.info(f"      - {reason}: {count}")
    
    if not records:
        logger.warning(f"   ❌ No valid records to insert!")
        return 0
    
    cursor = db.conn.cursor()
    
    insert_query = """
        INSERT INTO fact_prices 
        (province_id, commodity_id, subcategory_id, market_type_id, tanggal, harga)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """
    
    # Process in batches to avoid timeout
    batch_size = 500
    total_inserted = 0
    
    try:
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            
            cursor.executemany(insert_query, batch)
            db.conn.commit()
            total_inserted += cursor.rowcount
            
            if (i + batch_size) % 2000 == 0:  # Progress every 2000 records
                logger.info(f"      Progress: {i+batch_size}/{len(records)} processed...")
        
        cursor.close()
        
        logger.info(f"   💾 Database insert: {total_inserted} rows affected")
        
        return total_inserted
        
    except Exception as e:
        db.conn.rollback()
        cursor.close()
        logger.error(f"   ❌ Insert error: {e}")
        import traceback
        traceback.print_exc()
        return 0


def send_notification(stats, duration, start_date, end_date):
    """Send email notification"""
    
    try:
        from src.utils.notifications import send_backfill_complete_email
        
        send_backfill_complete_email(
            total_records=stats['total_inserted'],
            start_date=start_date,
            end_date=end_date,
            duration=duration
        )
        logger.info("✅ Email notification sent")
    except Exception as e:
        logger.warning(f"⚠️  Email failed: {e}")


def main():
    """Main execution with argument parsing"""
    
    parser = argparse.ArgumentParser(
        description='Unified backfill for categories and subcategories',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python backfill_unified.py                              # Last 30 days, both types
  python backfill_unified.py --days 90                    # Last 90 days
  python backfill_unified.py --days 365                   # Last year
  python backfill_unified.py --start 2024-01-01 --end 2024-12-31
  python backfill_unified.py --categories-only            # Categories only
  python backfill_unified.py --subcategories-only         # Subcategories only
  python backfill_unified.py --market-types 1 2           # Traditional + Modern
  python backfill_unified.py --monthly                    # Use monthly data
  python backfill_unified.py --no-email                   # Skip notification
        """
    )
    
    parser.add_argument('--days', type=int, default=30, help='Days to backfill (default: 30)')
    parser.add_argument('--start', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--market-types', type=int, nargs='+', choices=[1,2,3,4], help='Market types')
    parser.add_argument('--categories-only', action='store_true', help='Only categories')
    parser.add_argument('--subcategories-only', action='store_true', help='Only subcategories')
    parser.add_argument('--monthly', action='store_true', help='Use monthly data (tipe_laporan=3)')
    parser.add_argument('--no-email', action='store_true', help='Skip email')
    
    args = parser.parse_args()
    
    # Calculate dates
    if args.start and args.end:
        start_date = args.start
        end_date = args.end
    elif args.start:
        start_date = args.start
        end_date = datetime.now().strftime('%Y-%m-%d')
    else:
        end_date = datetime.now()
        start_date = (end_date - timedelta(days=args.days)).strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
    
    # Validate
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD")
        sys.exit(1)
    
    # Determine what to scrape
    scrape_cats = not args.subcategories_only
    scrape_subcats = not args.categories_only
    
    # Run backfill
    try:
        stats, duration = backfill_unified(
            start_date=start_date,
            end_date=end_date,
            market_types=args.market_types,
            scrape_categories=scrape_cats,
            scrape_subcategories=scrape_subcats,
            tipe_laporan=3 if args.monthly else 1
        )
        
        # Send notification
        if not args.no_email:
            send_notification(stats, duration, start_date, end_date)
        
        logger.info("\n✅ Backfill completed successfully!")
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️  Interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"\n❌ Backfill failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 