WITH latest_date AS (
    SELECT MAX(tanggal) as max_date 
    FROM fact_prices
),
latest_prices AS (
    SELECT 
        p.province_id,
        p.province_name,
        p.region,
        c.commodity_id,
        c.commodity_name,
        fp.harga,
        fp.tanggal
    FROM fact_prices fp
    JOIN dim_provinces p ON fp.province_id = p.province_id
    JOIN dim_commodities c ON fp.commodity_id = c.commodity_id
    CROSS JOIN latest_date ld
    WHERE fp.tanggal = ld.max_date
      AND fp.market_type_id = 1  -- Traditional market
      AND fp.subcategory_id IS NULL  -- General quality
),
national_avg AS (
    SELECT 
        commodity_id,
        AVG(harga) as avg_price
    FROM latest_prices
    GROUP BY commodity_id
)
SELECT 
    lp.province_name,
    lp.region,
    lp.commodity_name,
    lp.harga,
    na.avg_price as national_avg,
    ROUND(((lp.harga - na.avg_price) / na.avg_price) * 100, 2) as deviation_pct,
    lp.tanggal
FROM latest_prices lp
JOIN national_avg na ON lp.commodity_id = na.commodity_id
ORDER BY lp.commodity_name, lp.harga DESC;