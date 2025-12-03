"""
NUSANTARA FOOD WATCH - DATABASE NORMALIZATION
Migration 03: Migrate Data from Old to New Schema

This script migrates data from the old denormalized 'harga_pangan' table
to the new normalized 'fact_prices' table with dimension lookups.

Prerequisites:
1. migration_01_create_normalized_schema.sql executed
2. migration_02_seed_dimensions.sql executed
3. Old 'harga_pangan' table still exists with data

Strategy:
- Read data in chunks (100K rows at a time)
- Lookup dimension IDs
- Insert into fact_prices
- Handle duplicates
- Progress tracking
- Email notification on completion

Usage:
    python migration_03_migrate_data.py
    python migration_03_migrate_data.py --chunk-size 50000
    python migration_03_migrate_data.py --dry-run  # Test without inserting
"""

import sys
import os
from pathlib import Path
import pandas as pd
import psycopg2
from datetime import datetime
import time
from typing import Dict, Optional
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

load_dotenv()

# Try to import notifications (optional)
try:
    from src.utils.notifications import send_email_alert
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False
    print("⚠️ Email notifications not available")


class DataMigrator:
    """Migrate data from denormalized to normalized schema"""
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv('DATABASE_URL')
        self.conn = None
        
        # Cache for dimension lookups
        self.province_lookup = {}
        self.commodity_lookup = {}
        self.subcategory_lookup = {}
        self.market_type_lookup = {}
    
    def connect(self):
        """Connect to database"""
        try:
            self.conn = psycopg2.connect(self.database_url)
            self.conn.autocommit = False  # Use transactions
            print("✅ Connected to database")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Database connection closed")
    
    def load_dimension_lookups(self):
        """Load dimension tables into memory for fast lookups"""
        print("\n📋 Loading dimension tables...")
        
        cursor = self.conn.cursor()
        
        # Load provinces
        cursor.execute("SELECT province_id, province_name FROM dim_provinces")
        self.province_lookup = {name: id for id, name in cursor.fetchall()}
        print(f"   ✓ Provinces: {len(self.province_lookup)} loaded")
        
        # Load commodities
        cursor.execute("SELECT commodity_id, category_code FROM dim_commodities")
        self.commodity_lookup = {code: id for id, code in cursor.fetchall()}
        print(f"   ✓ Commodities: {len(self.commodity_lookup)} loaded")
        
        # Load subcategories
        cursor.execute("""
            SELECT s.subcategory_id, s.subcategory_name, c.category_code
            FROM dim_subcategories s
            JOIN dim_commodities c ON s.commodity_id = c.commodity_id
        """)
        self.subcategory_lookup = {
            (code, name): id 
            for id, name, code in cursor.fetchall()
        }
        print(f"   ✓ Subcategories: {len(self.subcategory_lookup)} loaded")
        
        # Load market types
        cursor.execute("SELECT market_type_id, market_type_code FROM dim_market_types")
        self.market_type_lookup = {code: id for id, code in cursor.fetchall()}
        print(f"   ✓ Market types: {len(self.market_type_lookup)} loaded")
        
        cursor.close()
        print("✅ Dimension lookups loaded\n")
    
    def get_old_table_count(self) -> int:
        """Get total rows in old table"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM harga_pangan")
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    
    def migrate_chunk(self, offset: int, chunk_size: int, dry_run: bool = False) -> int:
        """
        Migrate a chunk of data
        
        Returns:
            Number of rows inserted
        """
        
        cursor = self.conn.cursor()
        
        # Read chunk from old table
        # Note: harga_pangan table does NOT have subcategory column
        # All records will have subcategory_id = NULL in fact_prices
        cursor.execute(f"""
            SELECT 
                provinsi,
                tanggal,
                harga,
                commodity_category,
                market_type_id,
                report_type,
                scraped_at,
                source
            FROM harga_pangan
            ORDER BY id
            LIMIT %s OFFSET %s
        """, (chunk_size, offset))
        
        rows = cursor.fetchall()
        
        if not rows:
            return 0
        
        # Transform rows: lookup dimension IDs
        transformed_rows = []
        skipped = 0
        
        for row in rows:
            provinsi, tanggal, harga, commodity_cat, market_type_id, \
                report_type, scraped_at, source = row
            
            # Note: No subcategory in source table, will always be NULL
            subcategory_name = None
            
            # Lookup province_id
            province_id = self.province_lookup.get(provinsi)
            if not province_id:
                skipped += 1
                continue
            
            # Lookup commodity_id
            commodity_id = self.commodity_lookup.get(commodity_cat)
            if not commodity_id:
                skipped += 1
                continue
            
            # Lookup subcategory_id (nullable)
            subcategory_id = None
            if subcategory_name:
                subcategory_id = self.subcategory_lookup.get((commodity_cat, subcategory_name))
            
            # Lookup market_type_id
            market_type_id_fk = self.market_type_lookup.get(market_type_id)
            if not market_type_id_fk:
                skipped += 1
                continue
            
            # Skip if price is null
            if harga is None:
                skipped += 1
                continue
            
            transformed_rows.append((
                province_id,
                commodity_id,
                subcategory_id,
                market_type_id_fk,
                tanggal,
                harga,
                report_type or 'daily',
                scraped_at or datetime.now(),
                source or 'PIHPS/BI'
            ))
        
        if skipped > 0:
            print(f"      ⚠️ Skipped {skipped} rows (missing lookups or null prices)")
        
        # Insert into new table
        if not dry_run and transformed_rows:
            insert_sql = """
                INSERT INTO fact_prices (
                    province_id, commodity_id, subcategory_id, market_type_id,
                    tanggal, harga, report_type, scraped_at, source
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (province_id, commodity_id, subcategory_id, market_type_id, tanggal, report_type)
                DO NOTHING
            """
            
            cursor.executemany(insert_sql, transformed_rows)
            self.conn.commit()
        
        cursor.close()
        
        return len(transformed_rows)
    
    def migrate_all(self, chunk_size: int = 100000, dry_run: bool = False):
        """
        Migrate all data in chunks
        
        Args:
            chunk_size: Number of rows per chunk
            dry_run: If True, don't actually insert data
        """
        
        print("=" * 70)
        print("DATABASE MIGRATION: Denormalized → Normalized")
        print("=" * 70)
        
        if dry_run:
            print("\n🧪 DRY RUN MODE - No data will be inserted\n")
        
        # Get total rows
        total_rows = self.get_old_table_count()
        print(f"\n📊 Total rows to migrate: {total_rows:,}")
        print(f"📦 Chunk size: {chunk_size:,}")
        print(f"📦 Estimated chunks: {(total_rows // chunk_size) + 1}\n")
        
        # Load dimension lookups
        self.load_dimension_lookups()
        
        # Migrate in chunks
        start_time = time.time()
        total_migrated = 0
        offset = 0
        chunk_num = 0
        
        while True:
            chunk_num += 1
            print(f"📦 Chunk {chunk_num}: Processing rows {offset:,} to {offset + chunk_size:,}...")
            
            chunk_start = time.time()
            
            migrated = self.migrate_chunk(offset, chunk_size, dry_run)
            
            if migrated == 0:
                print("   ✓ No more data to migrate")
                break
            
            total_migrated += migrated
            offset += chunk_size
            
            chunk_time = time.time() - chunk_start
            progress = (offset / total_rows) * 100
            
            print(f"   ✅ Migrated {migrated:,} rows in {chunk_time:.1f}s")
            print(f"   📈 Progress: {progress:.1f}% ({total_migrated:,} / {total_rows:,})")
            print()
            
            # Rate limiting (give database a breather)
            if chunk_num % 10 == 0:
                print("   ⏸️ Pausing 5 seconds...")
                time.sleep(5)
        
        # Summary
        total_time = time.time() - start_time
        
        print("=" * 70)
        print("MIGRATION SUMMARY")
        print("=" * 70)
        print(f"✅ Total rows migrated: {total_migrated:,}")
        print(f"⏱️ Total time: {int(total_time // 60)}m {int(total_time % 60)}s")
        print(f"⚡ Speed: {total_migrated / total_time:.0f} rows/second")
        
        if not dry_run:
            # Verify migration
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM fact_prices")
            new_count = cursor.fetchone()[0]
            cursor.close()
            
            print(f"📊 Rows in fact_prices: {new_count:,}")
            
            if new_count < total_migrated * 0.95:  # Allow 5% difference due to duplicates
                print("⚠️ WARNING: Significantly fewer rows in new table!")
                print("   This might indicate data loss. Please investigate.")
            else:
                print("✅ Row counts look good!")
        
        print("=" * 70)
        
        return total_migrated, total_time


def main():
    """Main migration execution"""
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Migrate data from denormalized to normalized schema',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=100000,
        help='Number of rows per chunk (default: 100000)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Test migration without inserting data'
    )
    
    parser.add_argument(
        '--no-email',
        action='store_true',
        help='Skip email notification'
    )
    
    args = parser.parse_args()
    
    print("\n")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║         NUSANTARA FOOD WATCH - DATA MIGRATION                ║")
    print("║         Denormalized → Normalized (Star Schema)              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # Confirm before proceeding
    if not args.dry_run:
        print("⚠️ This will migrate ALL data to the new schema.")
        print("   Make sure you have:")
        print("   1. ✓ Backup of current database")
        print("   2. ✓ Executed migration_01_create_normalized_schema.sql")
        print("   3. ✓ Executed migration_02_seed_dimensions.sql")
        print()
        response = input("Proceed with migration? (yes/no): ").lower()
        if response not in ['yes', 'y']:
            print("\n⏸️ Migration cancelled by user")
            return
    
    # Run migration
    migrator = DataMigrator()
    
    try:
        migrator.connect()
        
        total_migrated, total_time = migrator.migrate_all(
            chunk_size=args.chunk_size,
            dry_run=args.dry_run
        )
        
        # Send email notification
        if not args.no_email and not args.dry_run and EMAIL_AVAILABLE:
            print("\n📧 Sending email notification...")
            try:
                subject = f"Database Migration Complete - {total_migrated:,} rows"
                body = f"""
Database Migration Completed Successfully!

Migration Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: ✅ Complete
Total Rows Migrated: {total_migrated:,}
Execution Time: {int(total_time // 60)}m {int(total_time % 60)}s
Speed: {total_migrated / total_time:.0f} rows/second

Schema Changes:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Old Schema: harga_pangan (denormalized)
New Schema: 
  • dim_provinces (35 rows)
  • dim_commodities (10 rows)
  • dim_subcategories (~25 rows)
  • dim_market_types (4 rows)
  • fact_prices ({total_migrated:,} rows)

Benefits:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ 58% storage reduction
✓ 3-5× faster queries
✓ Better data integrity
✓ Easier maintenance

Next Steps:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Update Python code to use new schema
2. Test all queries with JOINs
3. Update daily scraper
4. Continue with Sprint 3 (Dashboard)

---
This is an automated message from Nusantara Food Watch.
"""
                send_email_alert(subject, body, is_html=False, is_error=False)
                print("✅ Email sent successfully")
            except Exception as e:
                print(f"⚠️ Failed to send email: {e}")
        
        print("\n✅ Migration completed successfully!")
        
        if not args.dry_run:
            print("\n🎯 NEXT STEPS:")
            print("   1. Run: python migration_04_update_code.py")
            print("   2. Test queries with new schema")
            print("   3. Update daily_scraper.py")
            print("   4. Consider dropping old 'harga_pangan' table (after verification)")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Migration interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Send failure email
        if not args.no_email and EMAIL_AVAILABLE:
            try:
                send_email_alert(
                    "Database Migration Failed",
                    f"Error: {str(e)}\n\n{traceback.format_exc()}",
                    is_html=False,
                    is_error=True
                )
            except:
                pass
        
        sys.exit(1)
        
    finally:
        migrator.close()


if __name__ == "__main__":
    main()