-- ============================================================================
-- PRICE TREND ANALYSIS - LAST 30 DAYS (FIXED)
-- ============================================================================

WITH latest_data AS (
    -- Find the actual latest date in database
    SELECT MAX(tanggal) as max_date
    FROM fact_prices
),
date_range AS (
    -- Get last 30 days based on actual latest date
    SELECT 
        max_date - INTERVAL '30 days' as start_date,
        max_date as end_date
    FROM latest_data
),
daily_prices AS (
    SELECT 
        fp.tanggal,
        p.province_name,
        c.commodity_name,
        c.category_code,
        AVG(fp.harga) as avg_price,
        COUNT(*) as data_points
    FROM fact_prices fp
    JOIN dim_provinces p ON fp.province_id = p.province_id
    JOIN dim_commodities c ON fp.commodity_id = c.commodity_id
    JOIN dim_market_types mt ON fp.market_type_id = mt.market_type_id
    CROSS JOIN date_range dr
    WHERE 
        fp.tanggal >= dr.start_date
        AND fp.tanggal <= dr.end_date
        AND mt.market_type_code = 1  -- Traditional market
        -- Province filter (uncomment to use)
        -- AND p.province_name = 'DKI Jakarta'
    GROUP BY fp.tanggal, p.province_name, c.commodity_name, c.category_code
),
price_stats AS (
    SELECT 
        province_name,
        commodity_name,
        category_code,
        COUNT(DISTINCT tanggal) as days_with_data,
        MIN(tanggal) as first_date,
        MAX(tanggal) as last_date,
        
        -- Price at start and end
        (ARRAY_AGG(avg_price ORDER BY tanggal ASC))[1] as price_start,
        (ARRAY_AGG(avg_price ORDER BY tanggal DESC))[1] as price_end,
        
        -- Statistics
        AVG(avg_price) as avg_price_30d,
        MIN(avg_price) as min_price_30d,
        MAX(avg_price) as max_price_30d,
        STDDEV(avg_price) as stddev_price_30d,
        
        -- Coefficient of Variation (volatility)
        CASE 
            WHEN AVG(avg_price) > 0 THEN
                ROUND((STDDEV(avg_price) / AVG(avg_price) * 100)::numeric, 2)
        END as cv_pct
        
    FROM daily_prices
    GROUP BY province_name, commodity_name, category_code
),
trend_analysis AS (
    SELECT 
        ps.*,
        
        -- Absolute change
        price_end - price_start as change_abs,
        
        -- Percentage change
        CASE 
            WHEN price_start > 0 THEN
                ROUND(((price_end - price_start) / price_start * 100)::numeric, 2)
        END as change_pct,
        
        -- Trend direction
        CASE 
            WHEN price_end > price_start * 1.05 THEN 'Rising (>5%)'
            WHEN price_end < price_start * 0.95 THEN 'Falling (>5%)'
            ELSE 'Stable (±5%)'
        END as trend_direction,
        
        -- Volatility classification
        CASE 
            WHEN ps.cv_pct >= 20 THEN 'High Volatility'
            WHEN ps.cv_pct >= 10 THEN 'Medium Volatility'
            WHEN ps.cv_pct >= 5 THEN 'Low Volatility'
            ELSE 'Very Stable'
        END as volatility_level
        
    FROM price_stats ps
    WHERE days_with_data >= 5  -- At least 5 days of data
)
SELECT 
    province_name,
    commodity_name,
    category_code,
    
    -- Date range
    first_date,
    last_date,
    days_with_data,
    
    -- Prices
    ROUND(price_start::numeric, 2) as price_start,
    ROUND(price_end::numeric, 2) as price_end,
    ROUND(avg_price_30d::numeric, 2) as avg_price_30d,
    ROUND(min_price_30d::numeric, 2) as min_price_30d,
    ROUND(max_price_30d::numeric, 2) as max_price_30d,
    
    -- Changes
    ROUND(change_abs::numeric, 2) as change_abs,
    change_pct,
    trend_direction,
    
    -- Volatility
    ROUND(stddev_price_30d::numeric, 2) as stddev_price,
    cv_pct as volatility_cv,
    volatility_level,
    
    -- Price range
    ROUND((max_price_30d - min_price_30d)::numeric, 2) as price_range_30d,
    ROUND(((max_price_30d - min_price_30d) / avg_price_30d * 100)::numeric, 2) as range_pct

FROM trend_analysis
ORDER BY 
    province_name,
    ABS(change_pct) DESC NULLS LAST;