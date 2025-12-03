-- ============================================================================
-- NUSANTARA FOOD WATCH - DATABASE NORMALIZATION
-- Migration 02: Seed Dimension Tables
-- ============================================================================
--
-- This script populates the dimension tables with master data:
-- - 35 Indonesian provinces
-- - 10 food commodities
-- - ~25 subcategories (quality levels)
-- - 4 market types
--
-- Run this AFTER creating the schema (migration_01)
-- Run this BEFORE migrating data (migration_03)
-- ============================================================================

BEGIN;

-- ============================================================================
-- SEED: dim_provinces (35 Indonesian Provinces)
-- ============================================================================

INSERT INTO dim_provinces (province_code, province_name, region) VALUES
-- Sumatra
('11', 'Aceh', 'Sumatra'),
('12', 'Sumatera Utara', 'Sumatra'),
('13', 'Sumatera Barat', 'Sumatra'),
('14', 'Riau', 'Sumatra'),
('15', 'Jambi', 'Sumatra'),
('16', 'Sumatera Selatan', 'Sumatra'),
('17', 'Bengkulu', 'Sumatra'),
('18', 'Lampung', 'Sumatra'),
('19', 'Kepulauan Bangka Belitung', 'Sumatra'),
('21', 'Kepulauan Riau', 'Sumatra'),

-- Java
('31', 'DKI Jakarta', 'Java'),
('32', 'Jawa Barat', 'Java'),
('33', 'Jawa Tengah', 'Java'),
('34', 'DI Yogyakarta', 'Java'),
('35', 'Jawa Timur', 'Java'),
('36', 'Banten', 'Java'),

-- Kalimantan
('61', 'Kalimantan Barat', 'Kalimantan'),
('62', 'Kalimantan Tengah', 'Kalimantan'),
('63', 'Kalimantan Selatan', 'Kalimantan'),
('64', 'Kalimantan Timur', 'Kalimantan'),
('65', 'Kalimantan Utara', 'Kalimantan'),

-- Sulawesi
('71', 'Sulawesi Utara', 'Sulawesi'),
('72', 'Sulawesi Tengah', 'Sulawesi'),
('73', 'Sulawesi Selatan', 'Sulawesi'),
('74', 'Sulawesi Tenggara', 'Sulawesi'),
('75', 'Gorontalo', 'Sulawesi'),
('76', 'Sulawesi Barat', 'Sulawesi'),

-- Nusa Tenggara
('51', 'Bali', 'Nusa Tenggara'),
('52', 'Nusa Tenggara Barat', 'Nusa Tenggara'),
('53', 'Nusa Tenggara Timur', 'Nusa Tenggara'),

-- Maluku
('81', 'Maluku', 'Maluku'),
('82', 'Maluku Utara', 'Maluku'),

-- Papua
('91', 'Papua Barat', 'Papua'),
('92', 'Papua', 'Papua'),
('93', 'Papua Tengah', 'Papua'),
('94', 'Papua Pegunungan', 'Papua'),
('95', 'Papua Selatan', 'Papua')

ON CONFLICT (province_code) DO UPDATE SET
    province_name = EXCLUDED.province_name,
    region = EXCLUDED.region,
    updated_at = NOW();

-- ============================================================================
-- SEED: dim_commodities (10 Main Commodities)
-- ============================================================================

INSERT INTO dim_commodities (category_code, commodity_name, commodity_name_en, unit, description, is_staple) VALUES
('cat_1', 'Beras', 'Rice', 'kg', 'Staple food - Indonesian rice', true),
('cat_2', 'Daging Ayam', 'Chicken Meat', 'kg', 'Fresh chicken meat', true),
('cat_3', 'Daging Sapi', 'Beef', 'kg', 'Fresh beef', true),
('cat_4', 'Telur Ayam', 'Chicken Eggs', 'kg', 'Fresh chicken eggs', true),
('cat_5', 'Bawang Merah', 'Shallots', 'kg', 'Red onions/shallots', true),
('cat_6', 'Bawang Putih', 'Garlic', 'kg', 'Fresh garlic', true),
('cat_7', 'Cabai Merah', 'Red Chili', 'kg', 'Red chili peppers', true),
('cat_8', 'Cabai Rawit', 'Bird''s Eye Chili', 'kg', 'Small hot chili peppers', true),
('cat_9', 'Minyak Goreng', 'Cooking Oil', 'liter', 'Vegetable cooking oil', true),
('cat_10', 'Gula Pasir', 'Sugar', 'kg', 'Granulated white sugar', true)

ON CONFLICT (category_code) DO UPDATE SET
    commodity_name = EXCLUDED.commodity_name,
    commodity_name_en = EXCLUDED.commodity_name_en,
    unit = EXCLUDED.unit,
    description = EXCLUDED.description,
    is_staple = EXCLUDED.is_staple,
    updated_at = NOW();

-- ============================================================================
-- SEED: dim_subcategories (Quality Levels & Varieties)
-- ============================================================================

-- Get commodity IDs for foreign keys
WITH commodity_ids AS (
    SELECT commodity_id, category_code FROM dim_commodities
)

INSERT INTO dim_subcategories (commodity_id, subcategory_name, subcategory_name_en, quality_level, sort_order)
SELECT 
    c.commodity_id,
    sub.name,
    sub.name_en,
    sub.quality,
    sub.sort_order
FROM commodity_ids c
CROSS JOIN LATERAL (
    VALUES
    -- Beras (cat_1) - 6 types
    ('Beras Kualitas Bawah I', 'Low Quality Rice I', 'Low', 1),
    ('Beras Kualitas Bawah II', 'Low Quality Rice II', 'Low', 2),
    ('Beras Kualitas Medium I', 'Medium Quality Rice I', 'Medium', 3),
    ('Beras Kualitas Medium II', 'Medium Quality Rice II', 'Medium', 4),
    ('Beras Kualitas Super I', 'Premium Quality Rice I', 'Premium', 5),
    ('Beras Kualitas Super II', 'Premium Quality Rice II', 'Premium', 6)
) AS sub(name, name_en, quality, sort_order)
WHERE c.category_code = 'cat_1'

UNION ALL

-- Daging Ayam (cat_2) - 1 type
SELECT c.commodity_id, 'Daging Ayam Ras Segar', 'Fresh Broiler Chicken', 'Standard', 1
FROM commodity_ids c WHERE c.category_code = 'cat_2'

UNION ALL

-- Daging Sapi (cat_3) - 2 qualities
SELECT c.commodity_id, sub.name, sub.name_en, sub.quality, sub.sort_order
FROM commodity_ids c
CROSS JOIN LATERAL (
    VALUES
    ('Daging Sapi Kualitas 1', 'Beef Quality 1', 'Premium', 1),
    ('Daging Sapi Kualitas 2', 'Beef Quality 2', 'Standard', 2)
) AS sub(name, name_en, quality, sort_order)
WHERE c.category_code = 'cat_3'

UNION ALL

-- Telur Ayam (cat_4) - 1 type
SELECT c.commodity_id, 'Telur Ayam Ras Segar', 'Fresh Chicken Eggs', 'Standard', 1
FROM commodity_ids c WHERE c.category_code = 'cat_4'

UNION ALL

-- Bawang Merah (cat_5) - 1 type
SELECT c.commodity_id, 'Bawang Merah Ukuran Sedang', 'Medium Size Shallots', 'Standard', 1
FROM commodity_ids c WHERE c.category_code = 'cat_5'

UNION ALL

-- Bawang Putih (cat_6) - 1 type
SELECT c.commodity_id, 'Bawang Putih Ukuran Sedang', 'Medium Size Garlic', 'Standard', 1
FROM commodity_ids c WHERE c.category_code = 'cat_6'

UNION ALL

-- Cabai Merah (cat_7) - 2 types
SELECT c.commodity_id, sub.name, sub.name_en, sub.quality, sub.sort_order
FROM commodity_ids c
CROSS JOIN LATERAL (
    VALUES
    ('Cabai Merah Besar', 'Large Red Chili', 'Standard', 1),
    ('Cabai Merah Keriting', 'Curly Red Chili', 'Standard', 2)
) AS sub(name, name_en, quality, sort_order)
WHERE c.category_code = 'cat_7'

UNION ALL

-- Cabai Rawit (cat_8) - 2 types
SELECT c.commodity_id, sub.name, sub.name_en, sub.quality, sub.sort_order
FROM commodity_ids c
CROSS JOIN LATERAL (
    VALUES
    ('Cabai Rawit Hijau', 'Green Bird''s Eye Chili', 'Standard', 1),
    ('Cabai Rawit Merah', 'Red Bird''s Eye Chili', 'Standard', 2)
) AS sub(name, name_en, quality, sort_order)
WHERE c.category_code = 'cat_8'

UNION ALL

-- Minyak Goreng (cat_9) - 3 types
SELECT c.commodity_id, sub.name, sub.name_en, sub.quality, sub.sort_order
FROM commodity_ids c
CROSS JOIN LATERAL (
    VALUES
    ('Minyak Goreng Curah', 'Bulk Cooking Oil', 'Low', 1),
    ('Minyak Goreng Kemasan Bermerk 1', 'Branded Packaged Oil 1', 'Premium', 2),
    ('Minyak Goreng Kemasan Bermerk 2', 'Branded Packaged Oil 2', 'Medium', 3)
) AS sub(name, name_en, quality, sort_order)
WHERE c.category_code = 'cat_9'

UNION ALL

-- Gula Pasir (cat_10) - 2 types
SELECT c.commodity_id, sub.name, sub.name_en, sub.quality, sub.sort_order
FROM commodity_ids c
CROSS JOIN LATERAL (
    VALUES
    ('Gula Pasir Kualitas Premium', 'Premium White Sugar', 'Premium', 1),
    ('Gula Pasir Lokal', 'Local White Sugar', 'Standard', 2)
) AS sub(name, name_en, quality, sort_order)
WHERE c.category_code = 'cat_10'

ON CONFLICT (commodity_id, subcategory_name) DO UPDATE SET
    subcategory_name_en = EXCLUDED.subcategory_name_en,
    quality_level = EXCLUDED.quality_level,
    sort_order = EXCLUDED.sort_order,
    updated_at = NOW();

-- ============================================================================
-- SEED: dim_market_types (4 Market Types in Supply Chain)
-- ============================================================================

INSERT INTO dim_market_types (market_type_code, market_name, market_name_en, market_short, description, supply_chain_level) VALUES
(1, 'Pasar Tradisional', 'Traditional Market', 'traditional', 'Traditional wet markets - retail level', 1),
(2, 'Pasar Modern', 'Modern Market', 'modern', 'Supermarkets and modern retail - retail level', 2),
(3, 'Pedagang Besar', 'Wholesaler', 'wholesale', 'Wholesale distributors - middle supply chain', 3),
(4, 'Produsen', 'Producer', 'producer', 'Farmers and producers - start of supply chain', 4)

ON CONFLICT (market_type_code) DO UPDATE SET
    market_name = EXCLUDED.market_name,
    market_name_en = EXCLUDED.market_name_en,
    market_short = EXCLUDED.market_short,
    description = EXCLUDED.description,
    supply_chain_level = EXCLUDED.supply_chain_level,
    updated_at = NOW();

COMMIT;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Check counts
SELECT 'dim_provinces' as table_name, COUNT(*) as row_count, '(Expected: 35)' as expected FROM dim_provinces
UNION ALL
SELECT 'dim_commodities', COUNT(*), '(Expected: 10)' FROM dim_commodities
UNION ALL
SELECT 'dim_subcategories', COUNT(*), '(Expected: ~25)' FROM dim_subcategories
UNION ALL
SELECT 'dim_market_types', COUNT(*), '(Expected: 4)' FROM dim_market_types;

-- Preview data
SELECT 'PROVINCES:' as info;
SELECT province_code, province_name, region FROM dim_provinces ORDER BY province_code LIMIT 10;

SELECT 'COMMODITIES:' as info;
SELECT category_code, commodity_name, commodity_name_en, unit FROM dim_commodities ORDER BY category_code;

SELECT 'SUBCATEGORIES (Sample):' as info;
SELECT 
    c.commodity_name,
    s.subcategory_name,
    s.quality_level,
    s.sort_order
FROM dim_subcategories s
JOIN dim_commodities c ON s.commodity_id = c.commodity_id
ORDER BY c.category_code, s.sort_order
LIMIT 15;

SELECT 'MARKET TYPES:' as info;
SELECT 
    market_type_code,
    market_name,
    market_name_en,
    supply_chain_level,
    description
FROM dim_market_types
ORDER BY supply_chain_level DESC;

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'DIMENSION TABLES SEEDED SUCCESSFULLY!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Provinces: % rows', (SELECT COUNT(*) FROM dim_provinces);
    RAISE NOTICE 'Commodities: % rows', (SELECT COUNT(*) FROM dim_commodities);
    RAISE NOTICE 'Subcategories: % rows', (SELECT COUNT(*) FROM dim_subcategories);
    RAISE NOTICE 'Market Types: % rows', (SELECT COUNT(*) FROM dim_market_types);
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Ready for data migration!';
    RAISE NOTICE 'Next: Run migration_03_migrate_data.py';
END $$;