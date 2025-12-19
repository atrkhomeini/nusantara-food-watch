"""
Commodity detail processing functions
"""
import pandas as pd
from pathlib import Path
from src.db.nusantara_db import get_db_connection


def get_commodity_info(commodity_id):
    """
    Get commodity basic information
    
    Args:
        commodity_id (int): Commodity ID (1-10)
        
    Returns:
        dict: {'id': 1, 'name': 'Beras', 'icon': 'rice.png'}
    """
    commodities = {
        1: {'id': 1, 'name': 'Beras', 'icon': 'Beras'},
        2: {'id': 2, 'name': 'Daging Ayam', 'icon': 'Daging Ayam'},
        3: {'id': 3, 'name': 'Daging Sapi', 'icon': 'Daging Sapi'},
        4: {'id': 4, 'name': 'Telur Ayam', 'icon': 'Telur Ayam'},
        5: {'id': 5, 'name': 'Bawang Merah', 'icon': 'Bawang Merah'},
        6: {'id': 6, 'name': 'Bawang Putih', 'icon': 'Bawang Putih'},
        7: {'id': 7, 'name': 'Cabai Merah', 'icon': 'Cabai Merah'},
        8: {'id': 8, 'name': 'Cabai Rawit', 'icon': 'Cabai Rawit'},
        9: {'id': 9, 'name': 'Minyak Goreng', 'icon': 'Minyak Goreng'},
        10: {'id': 10, 'name': 'Gula Pasir', 'icon': 'Gula Pasir'},
    }
    return commodities.get(int(commodity_id))


def get_national_average(commodity_id):
    """Get national average price for commodity"""
    query = """
    SELECT 
        AVG(fp.harga) as avg_price,
        MAX(fp.tanggal) as latest_date
    FROM fact_prices fp
    WHERE 
        fp.commodity_id = %(commodity_id)s
        AND fp.subcategory_id IS NULL
        AND fp.tanggal >= CURRENT_DATE - INTERVAL '7 days'
    """
    
    conn = get_db_connection()
    df = pd.read_sql_query(query, conn, params={'commodity_id': commodity_id})
    
    if df.empty:
        return None
    
    return {
        'avg_price': float(df['avg_price'].iloc[0]),
        'date': df['latest_date'].iloc[0].strftime('%Y-%m-%d')
    }


def get_price_trend(commodity_id, days=30):
    """Get price trend for last N days"""
    query = """
    SELECT 
        fp.tanggal as date,
        AVG(fp.harga) as avg_price
    FROM fact_prices fp
    WHERE 
        fp.commodity_id = %(commodity_id)s
        AND fp.subcategory_id IS NULL
        AND fp.tanggal >= CURRENT_DATE - INTERVAL '%(days)s days'
    GROUP BY fp.tanggal
    ORDER BY fp.tanggal ASC
    """
    
    conn = get_db_connection()
    df = pd.read_sql_query(
        query, 
        conn, 
        params={'commodity_id': commodity_id, 'days': days}
    )
    
    return df


def get_top_provinces(commodity_id, limit=10, order='ASC'):
    """Get cheapest/most expensive provinces"""
    query = f"""
    WITH latest_prices AS (
        SELECT 
            p.province_name,
            fp.harga as price,
            fp.tanggal as date,
            ROW_NUMBER() OVER (PARTITION BY fp.province_id ORDER BY fp.tanggal DESC) as rn
        FROM fact_prices fp
        JOIN dim_provinces p ON fp.province_id = p.province_id
        WHERE 
            fp.commodity_id = %(commodity_id)s
            AND fp.subcategory_id IS NULL
            AND fp.tanggal >= CURRENT_DATE - INTERVAL '7 days'
    )
    SELECT 
        province_name,
        price,
        date
    FROM latest_prices
    WHERE rn = 1
    ORDER BY price {order}
    LIMIT %(limit)s
    """
    
    conn = get_db_connection()
    df = pd.read_sql_query(
        query,
        conn,
        params={'commodity_id': commodity_id, 'limit': limit}
    )
    
    return df


def get_quality_breakdown(commodity_id):
    """Get price breakdown by quality level"""
    query = """
    WITH latest_prices AS (
        SELECT 
            s.quality_level,
            s.subcategory_name,
            AVG(fp.harga) as avg_price,
            COUNT(*) as data_points
        FROM fact_prices fp
        JOIN dim_subcategories s ON fp.subcategory_id = s.subcategory_id
        WHERE 
            fp.commodity_id = %(commodity_id)s
            AND fp.subcategory_id IS NOT NULL
            AND fp.tanggal >= CURRENT_DATE - INTERVAL '7 days'
        GROUP BY s.quality_level, s.subcategory_name
    )
    SELECT * FROM latest_prices
    ORDER BY avg_price ASC
    """
    
    conn = get_db_connection()
    df = pd.read_sql_query(query, conn, params={'commodity_id': commodity_id})
    
    return df