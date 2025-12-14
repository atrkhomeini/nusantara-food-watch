"""
POPULATE SUBCATEGORY DATABASE
Insert scraped subcategory data into fact_prices with proper subcategory_id foreign keys
"""

import sys
from pathlib import Path
import pandas as pd
import logging

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.db.nusantara_db import NusantaraDatabaseNormalized

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def populate_database(csv_file: str, batch_size: int = 500):
    """
    Insert subcategory data from CSV into database
    
    Args:
        csv_file: Path to CSV from backfill script
        batch_size: Number of records per batch insert
    """
    
    logger.info("="*70)
    logger.info("📥 POPULATING DATABASE WITH SUBCATEGORY DATA")
    logger.info("="*70)
    
    # Load CSV
    logger.info(f"📂 Loading: {csv_file}")
    df = pd.read_csv(csv_file)
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    
    logger.info(f"✅ Loaded {len(df):,} records")
    # Detect column name
    name_col = 'subcommodity_name' if 'subcommodity_name' in df.columns else 'subcategory_name'
    
    logger.info(f"   Subcommodities: {df[name_col].nunique()}")
    logger.info(f"   Provinces: {df['provinsi'].nunique()}")
    logger.info(f"   Date range: {df['tanggal'].min().date()} to {df['tanggal'].max().date()}")
    
    # Connect to database
    logger.info("\n🔌 Connecting to database...")
    db = NusantaraDatabaseNormalized()
    db.connect()  # This establishes db.conn
    
    # Get mappings
    logger.info("\n🗺️  Loading dimension mappings...")
    
    # Province mapping
    logger.info("   Loading province mappings...")
    province_query = "SELECT province_id, province_name FROM dim_provinces"
    df_provinces = pd.read_sql(province_query, db.conn)
    province_map = dict(zip(df_provinces['province_name'], df_provinces['province_id']))
    df['province_id'] = df['provinsi'].map(province_map)
    
    # Subcategory mapping
    logger.info("   Loading subcategory mappings...")
    subcategory_query = "SELECT subcategory_id, subcategory_name FROM dim_subcategories"
    df_subcats = pd.read_sql(subcategory_query, db.conn)
    subcategory_map = dict(zip(df_subcats['subcategory_name'], df_subcats['subcategory_id']))
    
    # Handle both 'subcommodity_name' (from backfill) and 'subcategory_name' columns
    if 'subcommodity_name' in df.columns:
        df['db_subcategory_id'] = df['subcommodity_name'].map(subcategory_map)
    elif 'subcategory_name' in df.columns:
        df['db_subcategory_id'] = df['subcategory_name'].map(subcategory_map)
    else:
        logger.error("❌ Neither 'subcommodity_name' nor 'subcategory_name' found in CSV!")
        return 0
    
    # Market type is already in the data
    df['market_type_id'] = df['market_type_id'].astype(int)
    
    # Commodity ID is already in the data (db_commodity_id)
    
    # Check for unmapped values
    logger.info("\n🔍 Checking data quality...")
    
    missing_provinces = df[df['province_id'].isna()]
    missing_subcategories = df[df['db_subcategory_id'].isna()]
    missing_prices = df[df['harga'].isna()]
    
    if not missing_provinces.empty:
        logger.warning(f"⚠️  {len(missing_provinces)} records with unmapped provinces")
        logger.warning(f"   Provinces: {missing_provinces['provinsi'].unique()[:5]}")
    
    if not missing_subcategories.empty:
        logger.warning(f"⚠️  {len(missing_subcategories)} records with unmapped subcategories")
        name_col = 'subcommodity_name' if 'subcommodity_name' in missing_subcategories.columns else 'subcategory_name'
        if name_col in missing_subcategories.columns:
            logger.warning(f"   Subcommodities: {missing_subcategories[name_col].unique()[:5]}")
    
    if not missing_prices.empty:
        logger.warning(f"⚠️  {len(missing_prices)} records with NULL prices")
    
    # Filter to only valid records
    df_valid = df[
        df['province_id'].notna() & 
        df['db_commodity_id'].notna() &
        df['db_subcategory_id'].notna() &
        df['market_type_id'].notna() &
        df['harga'].notna()
    ].copy()
    
    logger.info(f"\n✅ Valid records: {len(df_valid):,} / {len(df):,}")
    
    if df_valid.empty:
        logger.error("❌ No valid records to insert!")
        return 0
    
    # Prepare for database insertion
    logger.info("\n💾 Inserting into database...")
    logger.info("   This may take a few minutes...")
    
    # Check what constraint exists
    logger.info("\n🔍 Checking database constraints...")
    cursor_check = db.conn.cursor()
    cursor_check.execute("""
        SELECT pg_get_constraintdef(oid) 
        FROM pg_constraint
        WHERE conrelid = 'fact_prices'::regclass 
        AND contype IN ('p', 'u')
        LIMIT 1
    """)
    
    constraint_result = cursor_check.fetchone()
    if constraint_result:
        logger.info(f"   Found constraint: {constraint_result[0]}")
    cursor_check.close()
    
    # Try insert with most common constraint pattern
    # If this fails, we'll try without ON CONFLICT
    insert_query = """
        INSERT INTO fact_prices 
        (province_id, commodity_id, subcategory_id, market_type_id, tanggal, harga)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    # We'll use ON CONFLICT DO NOTHING if it fails
    insert_query_with_conflict = insert_query + """
        ON CONFLICT DO NOTHING
    """
    
    try:
        total_inserted = 0
        total_batches = (len(df_valid) + batch_size - 1) // batch_size
        
        cursor = db.conn.cursor()
        use_conflict_handling = True
        
        for i in range(0, len(df_valid), batch_size):
            batch = df_valid.iloc[i:i+batch_size]
            batch_num = (i // batch_size) + 1
            
            # Prepare batch data
            records = []
            for _, row in batch.iterrows():
                records.append((
                    int(row['province_id']),
                    int(row['db_commodity_id']),
                    int(row['db_subcategory_id']),
                    int(row['market_type_id']),
                    row['tanggal'],
                    float(row['harga'])
                ))
            
            # Try insert
            try:
                if use_conflict_handling:
                    cursor.executemany(insert_query_with_conflict, records)
                else:
                    cursor.executemany(insert_query, records)
                
                db.conn.commit()
                total_inserted += cursor.rowcount
                logger.info(f"   Batch {batch_num}/{total_batches}: {cursor.rowcount} records inserted")
                
            except Exception as batch_error:
                # If ON CONFLICT fails, try without it
                if use_conflict_handling and 'constraint' in str(batch_error).lower():
                    logger.warning(f"   ⚠️  ON CONFLICT failed, trying without...")
                    use_conflict_handling = False
                    db.conn.rollback()
                    
                    # Retry this batch
                    cursor.executemany(insert_query, records)
                    db.conn.commit()
                    total_inserted += cursor.rowcount
                    logger.info(f"   Batch {batch_num}/{total_batches}: {cursor.rowcount} records inserted")
                else:
                    raise
        
        cursor.close()
        
        logger.info("\n" + "="*70)
        logger.info("✅ DATABASE POPULATION COMPLETE")
        logger.info("="*70)
        logger.info(f"Inserted/Updated: {total_inserted:,} records")
        name_col = 'subcommodity_name' if 'subcommodity_name' in df_valid.columns else 'subcategory_name'
        logger.info(f"Subcommodities: {df_valid[name_col].nunique()}")
        logger.info(f"Provinces: {df_valid['provinsi'].nunique()}")
        logger.info(f"Date range: {df_valid['tanggal'].min().date()} to {df_valid['tanggal'].max().date()}")
        
        # Verify in database
        logger.info("\n🔍 Verifying in database...")
        verify_query = """
            SELECT 
                COUNT(*) as total,
                COUNT(DISTINCT subcategory_id) as subcategories,
                COUNT(CASE WHEN subcategory_id IS NOT NULL THEN 1 END) as with_subcategory
            FROM fact_prices
        """
        
        result = pd.read_sql(verify_query, db.conn)
        logger.info(f"\n📊 Database Statistics:")
        logger.info(f"   Total records: {result['total'].iloc[0]:,}")
        logger.info(f"   With subcategory: {result['with_subcategory'].iloc[0]:,}")
        logger.info(f"   Unique subcategories: {result['subcategories'].iloc[0]}")
        
        return total_inserted
    
    except Exception as e:
        logger.error(f"\n❌ Database error: {e}")
        import traceback
        traceback.print_exc()
        return 0


def main():
    """
    Run database population
    """
    
    print("\n" + "="*70)
    print("POPULATE SUBCATEGORY DATA TO DATABASE")
    print("="*70)
    
    # Find CSV files
    csv_files = sorted(Path('.').glob('subcategory_backfill_*.csv'))
    
    if not csv_files:
        print("\n❌ No backfill CSV files found!")
        print("   Please run backfill_subcategory_complete.py first")
        return
    
    print(f"\nFound {len(csv_files)} CSV file(s):")
    for i, f in enumerate(csv_files, 1):
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"{i}. {f.name} ({size_mb:.1f} MB)")
    
    if len(csv_files) == 1:
        choice = '1'
    else:
        choice = input(f"\nSelect file (1-{len(csv_files)}): ").strip()
    
    try:
        idx = int(choice) - 1
        csv_file = csv_files[idx]
        
        print(f"\n📂 Selected: {csv_file.name}")
        confirm = input("Proceed with database insertion? (y/n): ")
        
        if confirm.lower() == 'y':
            inserted = populate_database(str(csv_file))
            
            if inserted > 0:
                print("\n" + "="*70)
                print("✅ SUCCESS!")
                print("="*70)
                print(f"Inserted/Updated {inserted:,} records")
                print("\n💡 Next steps:")
                print("1. Verify data in database")
                print("2. Update analysis queries to use subcategories")
                print("3. Create quality comparison visualizations")
                print("4. Build enhanced dashboard")
            else:
                print("\n❌ No records inserted")
        else:
            print("\n❌ Cancelled")
    
    except (ValueError, IndexError):
        print("\n❌ Invalid selection")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()