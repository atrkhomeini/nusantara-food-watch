-- ============================================================================
-- COMPLETE PRE-MIGRATION CLEANUP SCRIPT
-- ============================================================================
-- Purpose: Clean up existing database objects before normalized schema migration
-- Run this FIRST, then run migration_01, migration_02, migration_03
-- ============================================================================

-- ============================================================================
-- STEP 1: DROP OLD VIEWS
-- ============================================================================
-- Views from Sprint 1/2 that use denormalized schema (harga_pangan)
-- These will be recreated in migration_01 with normalized schema (fact_prices + JOINs)

DROP VIEW IF EXISTS latest_prices CASCADE;
DROP VIEW IF EXISTS supply_chain_margins CASCADE;
DROP VIEW IF EXISTS price_trends_7d CASCADE;
DROP VIEW IF EXISTS price_trends_30d CASCADE;

-- Verify views are dropped
SELECT 'VIEWS REMAINING:' as status;
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'VIEW'
ORDER BY table_name;

-- Expected: Should show 0 rows or only other views (not the 4 above)

-- ============================================================================
-- STEP 2: CHECK FOR PARTIAL INDEXES
-- ============================================================================
-- Check if there are any partial indexes (indexes with WHERE clause)
-- These might use non-immutable functions like CURRENT_DATE

SELECT 'PARTIAL INDEXES:' as status;
SELECT 
    tablename, 
    indexname, 
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND indexdef ILIKE '%WHERE%'
ORDER BY tablename, indexname;

-- Expected: Should show 0 rows (no partial indexes)
-- If you see any, run: DROP INDEX IF EXISTS index_name;

-- ============================================================================
-- STEP 3: CHECK FOR TIME-BASED FUNCTION INDEXES
-- ============================================================================
-- Check if any indexes use CURRENT_DATE, NOW(), or similar functions

SELECT 'TIME-BASED INDEXES:' as status;
SELECT 
    tablename, 
    indexname, 
    indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND (indexdef ILIKE '%CURRENT_DATE%' 
       OR indexdef ILIKE '%NOW()%'
       OR indexdef ILIKE '%CURRENT_TIMESTAMP%')
ORDER BY tablename, indexname;

-- Expected: Should show 0 rows
-- If you see any, run: DROP INDEX IF EXISTS index_name;

-- ============================================================================
-- STEP 4: CHECK FOR EXISTING NORMALIZED TABLES
-- ============================================================================
-- Check if normalized tables already exist from previous migration attempts

SELECT 'NORMALIZED TABLES:' as status;
SELECT tablename
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename IN (
    'dim_provinces',
    'dim_commodities', 
    'dim_subcategories',
    'dim_market_types',
    'fact_prices'
  )
ORDER BY tablename;

-- Expected: Should show 0 rows (no normalized tables yet)
-- If you see tables, you have two options:
--   Option A: Keep them and skip migration_01 (not recommended - structure might be different)
--   Option B: Drop them and start fresh (recommended)

-- To drop existing normalized tables (if they exist):
-- Uncomment these lines if needed:

-- DROP TABLE IF EXISTS fact_prices CASCADE;
-- DROP TABLE IF EXISTS dim_subcategories CASCADE;
-- DROP TABLE IF EXISTS dim_commodities CASCADE;
-- DROP TABLE IF EXISTS dim_provinces CASCADE;
-- DROP TABLE IF EXISTS dim_market_types CASCADE;

-- ============================================================================
-- STEP 5: VERIFY OLD TABLE EXISTS
-- ============================================================================
-- Confirm that harga_pangan table exists (we'll migrate data from this)

SELECT 'SOURCE TABLE CHECK:' as status;
SELECT 
    tablename,
    (SELECT COUNT(*) FROM harga_pangan) as row_count
FROM pg_tables
WHERE schemaname = 'public'
  AND tablename = 'harga_pangan';

-- Expected: Should show 1 row with harga_pangan and row count
-- If harga_pangan doesn't exist, you can't migrate!

-- ============================================================================
-- STEP 6: BACKUP REMINDER
-- ============================================================================

SELECT '⚠️  BACKUP REMINDER ⚠️' as reminder;
SELECT 'Before proceeding with migration_01, make sure you have:' as instruction;
SELECT '1. Database backup from Supabase Dashboard → Database → Backups' as step_1;
SELECT '2. Local export of harga_pangan table (optional but recommended)' as step_2;
SELECT '3. Git commit of all your code changes' as step_3;

-- ============================================================================
-- CLEANUP COMPLETE!
-- ============================================================================
-- Summary of what was cleaned:
--   ✓ Dropped old views (will be recreated with JOINs)
--   ✓ Verified no partial indexes
--   ✓ Verified no time-based function indexes
--   ✓ Checked for conflicting normalized tables
--   ✓ Confirmed source table exists
--
-- You're now ready to run:
--   1. migration_01_create_normalized_schema.sql
--   2. migration_02_seed_dimensions.sql
--   3. python migration_03_migrate_data.py
-- ============================================================================

SELECT '✅ PRE-MIGRATION CLEANUP COMPLETE!' as status;
SELECT 'Ready to run migration_01_create_normalized_schema.sql' as next_step;