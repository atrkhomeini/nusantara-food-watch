"""
Database Handler untuk Nusantara Food Watch
Save scraped data ke PostgreSQL (Supabase/Neon)

Renamed from db_handler.py to avoid import conflicts
"""

import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
import logging
from typing import List, Dict
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NusantaraDatabase:
    """
    Handler untuk menyimpan data ke PostgreSQL
    
    Environment variables yang dibutuhkan:
    - DATABASE_URL atau
    - DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
    """
    
    def __init__(self, database_url: str = None):
        """
        Initialize database connection
        
        Args:
            database_url: PostgreSQL connection string
                         Format: postgresql://user:password@host:port/database
        """
        self.database_url = database_url or os.getenv('DATABASE_URL')
        
        if not self.database_url:
            # Build from individual env vars
            self.database_url = self._build_connection_string()
        
        self.conn = None
    
    def _build_connection_string(self) -> str:
        """Build connection string dari env variables"""
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        database = os.getenv('DB_NAME', 'nusantara-food-watch')
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD', '')
        
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(self.database_url)
            logger.info("✅ Database connected")
            return self.conn
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def create_tables(self):
        """Create necessary tables if not exist"""
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS harga_pangan (
            id SERIAL PRIMARY KEY,
            provinsi VARCHAR(100) NOT NULL,
            tanggal DATE NOT NULL,
            harga NUMERIC(10, 2),
            commodity_category VARCHAR(50),
            report_type VARCHAR(20) DEFAULT 'daily',
            market_type_id INTEGER DEFAULT 1,
            market_type_name VARCHAR(50),
            market_type_short VARCHAR(20),
            scraped_at TIMESTAMP DEFAULT NOW(),
            source VARCHAR(50) DEFAULT 'PIHPS/BI',
            
            -- Prevent duplicate entries
            UNIQUE(provinsi, tanggal, commodity_category, report_type, market_type_id)
        );
        
        -- Create indexes for better query performance
        CREATE INDEX IF NOT EXISTS idx_tanggal ON harga_pangan(tanggal);
        CREATE INDEX IF NOT EXISTS idx_provinsi ON harga_pangan(provinsi);
        CREATE INDEX IF NOT EXISTS idx_harga ON harga_pangan(harga);
        CREATE INDEX IF NOT EXISTS idx_market_type ON harga_pangan(market_type_id);
        CREATE INDEX IF NOT EXISTS idx_scraped_at ON harga_pangan(scraped_at);
        
        -- Create view for latest prices per market type
        CREATE OR REPLACE VIEW latest_prices AS
        SELECT DISTINCT ON (provinsi, commodity_category, market_type_id)
            provinsi,
            tanggal,
            harga,
            commodity_category,
            market_type_id,
            market_type_name,
            scraped_at
        FROM harga_pangan
        ORDER BY provinsi, commodity_category, market_type_id, tanggal DESC;
        
        -- Create view for supply chain margins
        CREATE OR REPLACE VIEW supply_chain_margins AS
        WITH market_prices AS (
            SELECT 
                provinsi,
                tanggal,
                commodity_category,
                MAX(CASE WHEN market_type_id = 4 THEN harga END) as harga_produsen,
                MAX(CASE WHEN market_type_id = 3 THEN harga END) as harga_grosir,
                MAX(CASE WHEN market_type_id = 1 THEN harga END) as harga_tradisional,
                MAX(CASE WHEN market_type_id = 2 THEN harga END) as harga_modern
            FROM harga_pangan
            GROUP BY provinsi, tanggal, commodity_category
        )
        SELECT 
            provinsi,
            tanggal,
            commodity_category,
            harga_produsen,
            harga_grosir,
            harga_tradisional,
            harga_modern,
            -- Calculate margins
            CASE WHEN harga_produsen > 0 THEN 
                ((harga_grosir - harga_produsen) / harga_produsen * 100) 
            END as margin_produsen_grosir,
            CASE WHEN harga_grosir > 0 THEN 
                ((harga_tradisional - harga_grosir) / harga_grosir * 100) 
            END as margin_grosir_tradisional,
            CASE WHEN harga_tradisional > 0 THEN 
                ((harga_modern - harga_tradisional) / harga_tradisional * 100) 
            END as margin_tradisional_modern,
            CASE WHEN harga_produsen > 0 THEN 
                ((harga_modern - harga_produsen) / harga_produsen * 100) 
            END as margin_total
        FROM market_prices
        WHERE harga_produsen IS NOT NULL OR harga_grosir IS NOT NULL;
        
        -- Create view for price trends (7 days) per market type
        CREATE OR REPLACE VIEW price_trends_7d AS
        SELECT 
            provinsi,
            commodity_category,
            market_type_id,
            market_type_name,
            AVG(harga) as avg_price_7d,
            MIN(harga) as min_price_7d,
            MAX(harga) as max_price_7d,
            STDDEV(harga) as stddev_price_7d,
            COUNT(*) as days_count
        FROM harga_pangan
        WHERE tanggal >= CURRENT_DATE - INTERVAL '7 days'
        GROUP BY provinsi, commodity_category, market_type_id, market_type_name;
        """
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(create_table_sql)
                self.conn.commit()
                logger.info("✅ Tables created successfully")
        except Exception as e:
            logger.error(f"❌ Failed to create tables: {e}")
            self.conn.rollback()
            raise
    
    def insert_data(self, df: pd.DataFrame, on_conflict: str = 'ignore'):
        """
        Insert data from DataFrame to database
        
        Args:
            df: DataFrame dengan kolom: provinsi, tanggal, harga, commodity_category
            on_conflict: 'ignore' (skip duplicates) atau 'update' (overwrite)
        """
        
        if df.empty:
            logger.warning("⚠️ DataFrame kosong, tidak ada data untuk diinsert")
            return 0
        
        # Prepare data
        df = df.copy()
        df['scraped_at'] = datetime.now()
        df['source'] = 'PIHPS/BI'
        
        # Ensure report_type exists
        if 'report_type' not in df.columns:
            df['report_type'] = 'daily'
        
        # Ensure market_type fields exist
        if 'market_type_id' not in df.columns:
            df['market_type_id'] = 1  # Default: Pasar Tradisional
        if 'market_type_name' not in df.columns:
            df['market_type_name'] = 'Pasar Tradisional'
        if 'market_type_short' not in df.columns:
            df['market_type_short'] = 'traditional'
        
        # Convert tanggal to string format
        df['tanggal'] = pd.to_datetime(df['tanggal']).dt.strftime('%Y-%m-%d')
        
        # Prepare SQL
        if on_conflict == 'ignore':
            sql = """
            INSERT INTO harga_pangan (
                provinsi, tanggal, harga, commodity_category, report_type,
                market_type_id, market_type_name, market_type_short,
                scraped_at, source
            )
            VALUES %s
            ON CONFLICT (provinsi, tanggal, commodity_category, report_type, market_type_id) DO NOTHING
            """
        else:  # update
            sql = """
            INSERT INTO harga_pangan (
                provinsi, tanggal, harga, commodity_category, report_type,
                market_type_id, market_type_name, market_type_short,
                scraped_at, source
            )
            VALUES %s
            ON CONFLICT (provinsi, tanggal, commodity_category, report_type, market_type_id) 
            DO UPDATE SET 
                harga = EXCLUDED.harga,
                scraped_at = EXCLUDED.scraped_at
            """
        
        # Execute bulk insert
        try:
            with self.conn.cursor() as cursor:
                # Prepare values
                values = [
                    (
                        row['provinsi'],
                        row['tanggal'],
                        row['harga'],
                        row.get('commodity_category', 'cat_1'),
                        row.get('report_type', 'daily'),
                        row.get('market_type_id', 1),
                        row.get('market_type_name', 'Pasar Tradisional'),
                        row.get('market_type_short', 'traditional'),
                        row['scraped_at'],
                        row['source']
                    )
                    for _, row in df.iterrows()
                    if pd.notna(row['harga'])  # Skip rows with null harga
                ]
                
                if not values:
                    logger.warning("⚠️ Semua data harga null, skip insert")
                    return 0
                
                # Bulk insert
                execute_values(cursor, sql, values)
                self.conn.commit()
                
                inserted_count = cursor.rowcount
                logger.info(f"✅ Inserted {inserted_count} rows to database")
                
                return inserted_count
                
        except Exception as e:
            logger.error(f"❌ Failed to insert data: {e}")
            self.conn.rollback()
            raise
    
    def get_latest_date(self) -> str:
        """Get latest date in database"""
        
        sql = "SELECT MAX(tanggal) FROM harga_pangan"
        
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
            COUNT(DISTINCT provinsi) as total_provinces,
            COUNT(DISTINCT tanggal) as total_dates,
            MIN(tanggal) as earliest_date,
            MAX(tanggal) as latest_date,
            AVG(harga) as avg_price,
            MIN(harga) as min_price,
            MAX(harga) as max_price
        FROM harga_pangan
        """
        
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                
                return {
                    'total_records': result[0],
                    'total_provinces': result[1],
                    'total_dates': result[2],
                    'earliest_date': result[3],
                    'latest_date': result[4],
                    'avg_price': float(result[5]) if result[5] else 0,
                    'min_price': float(result[6]) if result[6] else 0,
                    'max_price': float(result[7]) if result[7] else 0
                }
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            return {}


# For backward compatibility
DatabaseHandler = NusantaraDatabase


def main():
    """
    Main function untuk scraping dan save ke database
    """
    
    print("=" * 60)
    print("🇮🇩 NUSANTARA FOOD WATCH - Database Test")
    print("=" * 60)
    
    # Initialize
    db = NusantaraDatabase()
    
    try:
        # Connect to database
        print("\n📊 Connecting to database...")
        db.connect()
        
        # Create tables if not exist
        print("🏗️ Creating tables...")
        db.create_tables()
        
        print("\n✅ Database ready!")
        print("\nNext step:")
        print("  python production_scraper.py --mode full")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    main()