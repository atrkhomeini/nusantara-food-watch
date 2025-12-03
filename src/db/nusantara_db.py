"""
Database Handler for Normalized Schema
Nusantara Food Watch - Star Schema Version

This replaces src/db/nusantara_db.py for the normalized database.
Handles inserts into fact_prices with dimension lookups.
"""

import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import logging
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NusantaraDatabaseNormalized:
    """
    Database handler for normalized star schema
    
    New structure:
    - dim_provinces (35 rows)
    - dim_commodities (10 rows)
    - dim_subcategories (~25 rows)
    - dim_market_types (4 rows)
    - fact_prices (main data)
    """
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv('DATABASE_URL')
        self.conn = None
        
        # Cache for dimension lookups
        self._province_cache = {}
        self._commodity_cache = {}
        self._subcategory_cache = {}
        self._market_type_cache = {}
        self._cache_loaded = False
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(self.database_url)
            logger.info("✅ Database connected (normalized schema)")
            
            # Load dimension caches
            if not self._cache_loaded:
                self._load_dimension_caches()
            
            return self.conn
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def _load_dimension_caches(self):
        """Load dimension tables into memory for fast lookups"""
        if not self.conn:
            raise Exception("Not connected to database")
        
        cursor = self.conn.cursor()
        
        try:
            # Load provinces
            cursor.execute("SELECT province_id, province_name FROM dim_provinces")
            self._province_cache = {name: id for id, name in cursor.fetchall()}
            
            # Load commodities
            cursor.execute("SELECT commodity_id, category_code FROM dim_commodities")
            self._commodity_cache = {code: id for id, code in cursor.fetchall()}
            
            # Load subcategories (keyed by commodity_code + subcategory_name)
            cursor.execute("""
                SELECT s.subcategory_id, s.subcategory_name, c.category_code
                FROM dim_subcategories s
                JOIN dim_commodities c ON s.commodity_id = c.commodity_id
            """)
            self._subcategory_cache = {
                (code, name): id 
                for id, name, code in cursor.fetchall()
            }
            
            # Load market types (by market_type_code from PIHPS)
            cursor.execute("SELECT market_type_id, market_type_code FROM dim_market_types")
            self._market_type_cache = {code: id for id, code in cursor.fetchall()}
            
            self._cache_loaded = True
            logger.info("✅ Dimension caches loaded")
            
        except Exception as e:
            logger.error(f"❌ Failed to load dimension caches: {e}")
            raise
        finally:
            cursor.close()
    
    def _lookup_province_id(self, province_name: str) -> Optional[int]:
        """Lookup province_id from province_name"""
        return self._province_cache.get(province_name)
    
    def _lookup_commodity_id(self, category_code: str) -> Optional[int]:
        """Lookup commodity_id from category_code (e.g., 'cat_1')"""
        return self._commodity_cache.get(category_code)
    
    def _lookup_subcategory_id(self, category_code: str, subcategory_name: str) -> Optional[int]:
        """Lookup subcategory_id from category_code + subcategory_name"""
        return self._subcategory_cache.get((category_code, subcategory_name))
    
    def _lookup_market_type_id(self, market_type_code: int) -> Optional[int]:
        """Lookup market_type_id from market_type_code (1-4)"""
        return self._market_type_cache.get(market_type_code)
    
    def insert_data(self, df: pd.DataFrame, on_conflict: str = 'ignore') -> int:
        """
        Insert data from DataFrame to fact_prices
        
        Args:
            df: DataFrame with columns: provinsi, tanggal, harga, commodity_category, 
                market_type_id, subcategory (optional)
            on_conflict: 'ignore' (skip duplicates) or 'update' (overwrite)
        
        Returns:
            Number of rows inserted
        """
        
        if df.empty:
            logger.warning("⚠️ DataFrame empty, no data to insert")
            return 0
        
        # Ensure connection and caches are loaded
        if not self.conn:
            self.connect()
        
        # Prepare data
        df = df.copy()
        df['scraped_at'] = datetime.now()
        df['source'] = df.get('source', 'PIHPS/BI')
        df['report_type'] = df.get('report_type', 'daily')
        
        # Convert tanggal to string format
        df['tanggal'] = pd.to_datetime(df['tanggal']).dt.strftime('%Y-%m-%d')
        
        # Transform: lookup dimension IDs
        transformed_rows = []
        skipped = 0
        
        for _, row in df.iterrows():
            # Skip if price is null
            if pd.isna(row['harga']):
                skipped += 1
                continue
            
            # Lookup province_id
            province_id = self._lookup_province_id(row['provinsi'])
            if not province_id:
                logger.warning(f"⚠️ Province not found: {row['provinsi']}")
                skipped += 1
                continue
            
            # Lookup commodity_id
            commodity_id = self._lookup_commodity_id(row.get('commodity_category', row.get('commodity_id', 'cat_1')))
            if not commodity_id:
                logger.warning(f"⚠️ Commodity not found: {row.get('commodity_category')}")
                skipped += 1
                continue
            
            # Lookup subcategory_id (optional)
            subcategory_id = None
            if 'subcategory' in row and pd.notna(row['subcategory']):
                subcategory_id = self._lookup_subcategory_id(
                    row.get('commodity_category', row.get('commodity_id')),
                    row['subcategory']
                )
            
            # Lookup market_type_id
            market_type_code = row.get('market_type_id', 1)
            market_type_id = self._lookup_market_type_id(market_type_code)
            if not market_type_id:
                logger.warning(f"⚠️ Market type not found: {market_type_code}")
                skipped += 1
                continue
            
            transformed_rows.append((
                province_id,
                commodity_id,
                subcategory_id,
                market_type_id,
                row['tanggal'],
                float(row['harga']),
                row.get('report_type', 'daily'),
                row['scraped_at'],
                row.get('source', 'PIHPS/BI')
            ))
        
        if skipped > 0:
            logger.warning(f"⚠️ Skipped {skipped} rows (missing lookups or null prices)")
        
        if not transformed_rows:
            logger.warning("⚠️ No valid rows to insert after transformation")
            return 0
        
        # Prepare SQL
        if on_conflict == 'ignore':
            sql = """
                INSERT INTO fact_prices (
                    province_id, commodity_id, subcategory_id, market_type_id,
                    tanggal, harga, report_type, scraped_at, source
                )
                VALUES %s
                ON CONFLICT (province_id, commodity_id, subcategory_id, market_type_id, tanggal, report_type)
                DO NOTHING
            """
        else:  # update
            sql = """
                INSERT INTO fact_prices (
                    province_id, commodity_id, subcategory_id, market_type_id,
                    tanggal, harga, report_type, scraped_at, source
                )
                VALUES %s
                ON CONFLICT (province_id, commodity_id, subcategory_id, market_type_id, tanggal, report_type)
                DO UPDATE SET 
                    harga = EXCLUDED.harga,
                    scraped_at = EXCLUDED.scraped_at
            """
        
        # Execute bulk insert
        try:
            with self.conn.cursor() as cursor:
                execute_values(cursor, sql, transformed_rows)
                self.conn.commit()
                
                inserted_count = cursor.rowcount
                logger.info(f"✅ Inserted {inserted_count} rows to fact_prices")
                
                return inserted_count
                
        except Exception as e:
            logger.error(f"❌ Failed to insert data: {e}")
            self.conn.rollback()
            raise
    
    def get_latest_date(self) -> Optional[str]:
        """Get latest date in fact_prices"""
        sql = "SELECT MAX(tanggal) FROM fact_prices"
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                
                if result and result[0]:
                    return result[0].strftime('%Y-%m-%d')
                else:
                    return None
        except Exception as e:
            logger.error(f"❌ Failed to get latest date: {e}")
            return None
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        sql = """
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT province_id) as total_provinces,
                COUNT(DISTINCT commodity_id) as total_commodities,
                COUNT(DISTINCT market_type_id) as total_market_types,
                MIN(tanggal) as earliest_date,
                MAX(tanggal) as latest_date,
                AVG(harga) as avg_price,
                MIN(harga) as min_price,
                MAX(harga) as max_price
            FROM fact_prices
        """
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                
                return {
                    'total_records': result[0],
                    'total_provinces': result[1],
                    'total_commodities': result[2],
                    'total_market_types': result[3],
                    'earliest_date': result[4],
                    'latest_date': result[5],
                    'avg_price': float(result[6]) if result[6] else 0,
                    'min_price': float(result[7]) if result[7] else 0,
                    'max_price': float(result[8]) if result[8] else 0
                }
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {}


# Alias for backward compatibility
NusantaraDatabase = NusantaraDatabaseNormalized


def main():
    """Test the normalized database handler"""
    
    print("=" * 70)
    print("🇮🇩 NUSANTARA FOOD WATCH - Normalized Database Test")
    print("=" * 70)
    
    db = NusantaraDatabaseNormalized()
    
    try:
        # Connect
        print("\n📊 Connecting to database...")
        db.connect()
        
        # Get stats
        print("\n📊 Database statistics:")
        stats = db.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Test insert with sample data
        print("\n🧪 Testing insert with sample data...")
        test_df = pd.DataFrame({
            'provinsi': ['DKI Jakarta', 'Jawa Barat'],
            'tanggal': [datetime.now().date()] * 2,
            'harga': [15000, 14500],
            'commodity_category': ['cat_1'] * 2,
            'market_type_id': [1, 1],
            'report_type': ['daily'] * 2
        })
        
        inserted = db.insert_data(test_df, on_conflict='ignore')
        print(f"✅ Test insert: {inserted} rows")
        
        print("\n✅ Normalized database handler working correctly!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
    
    finally:
        db.close()
    
    print("\n" + "=" * 70)
    print("✅ Test complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()