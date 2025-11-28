"""
Database Setup Test & Verification Script
Run this after setting up your database to ensure everything works
"""

import sys
import os

def test_env_file():
    """Test if .env file exists and has DATABASE_URL"""
    print("\n" + "="*70)
    print("TEST 1: Environment Variables")
    print("="*70)
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("\nAction required:")
        print("1. Copy .env.example to .env")
        print("2. Add your DATABASE_URL")
        return False
    
    print("✅ .env file exists")
    
    # Try to load
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.getenv('DATABASE_URL')
        
        if not database_url:
            print("❌ DATABASE_URL not found in .env")
            print("\nAction required:")
            print("Add this line to .env:")
            print("DATABASE_URL=postgresql://user:password@host:5432/database")
            return False
        
        print("✅ DATABASE_URL found")
        
        # Validate format
        if not database_url.startswith('postgresql://'):
            print("⚠️ DATABASE_URL should start with 'postgresql://'")
            return False
        
        print("✅ DATABASE_URL format looks correct")
        
        # Show masked version
        masked = database_url[:15] + "***" + database_url[-20:]
        print(f"   {masked}")
        
        return True
        
    except ImportError:
        print("⚠️ python-dotenv not installed")
        print("Run: pip install python-dotenv")
        return True  # Continue anyway
    
    except Exception as e:
        print(f"❌ Error reading .env: {e}")
        return False


def test_dependencies():
    """Test if required packages are installed"""
    print("\n" + "="*70)
    print("TEST 2: Dependencies")
    print("="*70)
    
    required = {
        'psycopg2': 'psycopg2-binary',
        'pandas': 'pandas',
        'requests': 'requests'
    }
    
    all_installed = True
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"✅ {module} installed")
        except ImportError:
            print(f"❌ {module} not installed")
            print(f"   Run: pip install {package}")
            all_installed = False
    
    return all_installed


def test_database_connection():
    """Test connection to database"""
    print("\n" + "="*70)
    print("TEST 3: Database Connection")
    print("="*70)
    
    try:
        from nusantara_db import NusantaraDatabase as DatabaseHandler
        
        db = DatabaseHandler()
        print("✅ DatabaseHandler initialized")
        
        # Try to connect
        print("Connecting to database...")
        conn = db.connect()
        print("✅ Connection successful!")
        
        # Test query
        print("Running test query...")
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL version: {version[:50]}...")
        
        cursor.close()
        db.close()
        print("✅ Connection closed properly")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure db_handler.py is in the same directory")
        return False
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nPossible issues:")
        print("1. DATABASE_URL is incorrect")
        print("2. Database server is down")
        print("3. Network/firewall blocking connection")
        print("4. Password is wrong")
        return False


def test_create_tables():
    """Test creating tables"""
    print("\n" + "="*70)
    print("TEST 4: Create Tables")
    print("="*70)
    
    try:
        from nusantara_db import NusantaraDatabase as DatabaseHandler
        
        db = DatabaseHandler()
        db.connect()
        
        print("Creating tables...")
        db.create_tables()
        print("✅ Tables created successfully!")
        
        # List tables
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print(f"\nTables found: {len(tables)}")
        for table in tables:
            print(f"  • {table[0]}")
        
        # List views
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        views = cursor.fetchall()
        
        if views:
            print(f"\nViews found: {len(views)}")
            for view in views:
                print(f"  • {view[0]}")
        
        cursor.close()
        db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False


def test_insert_data():
    """Test inserting sample data"""
    print("\n" + "="*70)
    print("TEST 5: Insert Sample Data")
    print("="*70)
    
    try:
        from nusantara_db import NusantaraDatabase as DatabaseHandler
        import pandas as pd
        from datetime import datetime
        
        # Create test data
        df = pd.DataFrame({
            'provinsi': ['DKI Jakarta', 'Jawa Barat', 'Jawa Tengah'],
            'tanggal': [datetime.now().date()] * 3,
            'harga': [15000, 14500, 14000],
            'commodity_category': ['cat_1'] * 3,
            'report_type': ['daily'] * 3
        })
        
        print(f"Test data prepared: {len(df)} records")
        
        db = DatabaseHandler()
        db.connect()
        
        print("Inserting data...")
        inserted = db.insert_data(df)
        print(f"✅ Inserted {inserted} records")
        
        # Get stats
        print("\nDatabase statistics:")
        stats = db.get_stats()
        for key, value in stats.items():
            print(f"  • {key}: {value}")
        
        db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to insert data: {e}")
        return False


def test_query_data():
    """Test querying data"""
    print("\n" + "="*70)
    print("TEST 6: Query Data")
    print("="*70)
    
    try:
        from nusantara_db import NusantaraDatabase as DatabaseHandler
        import pandas as pd
        
        db = DatabaseHandler()
        db.connect()
        
        print("Running query: SELECT * FROM harga_pangan LIMIT 5;")
        df = pd.read_sql("SELECT * FROM harga_pangan LIMIT 5;", db.conn)
        
        print(f"✅ Query successful! Retrieved {len(df)} rows")
        
        if len(df) > 0:
            print("\nSample data:")
            print(df.to_string())
        else:
            print("\n⚠️ No data in table yet (this is OK for first setup)")
        
        db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Query failed: {e}")
        return False


def cleanup_test_data():
    """Optional: Remove test data"""
    print("\n" + "="*70)
    print("CLEANUP: Remove Test Data")
    print("="*70)
    
    response = input("\nDo you want to remove test data? (y/n): ").lower()
    
    if response != 'y':
        print("Keeping test data")
        return
    
    try:
        from nusantara_db import NusantaraDatabase as DatabaseHandler
        
        db = DatabaseHandler()
        db.connect()
        
        cursor = db.conn.cursor()
        cursor.execute("DELETE FROM harga_pangan WHERE report_type = 'daily';")
        db.conn.commit()
        
        deleted = cursor.rowcount
        print(f"✅ Deleted {deleted} test records")
        
        cursor.close()
        db.close()
        
    except Exception as e:
        print(f"❌ Cleanup failed: {e}")


def main():
    """Run all tests"""
    
    print("\n")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║       DATABASE SETUP TEST & VERIFICATION                         ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    
    results = {}
    
    # Run tests
    results['env'] = test_env_file()
    results['deps'] = test_dependencies()
    
    if results['env'] and results['deps']:
        results['connection'] = test_database_connection()
        
        if results['connection']:
            results['tables'] = test_create_tables()
            results['insert'] = test_insert_data()
            results['query'] = test_query_data()
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    test_names = {
        'env': 'Environment Variables',
        'deps': 'Dependencies',
        'connection': 'Database Connection',
        'tables': 'Create Tables',
        'insert': 'Insert Data',
        'query': 'Query Data'
    }
    
    for key, name in test_names.items():
        if key in results:
            status = "✅ PASS" if results[key] else "❌ FAIL"
            print(f"{status} - {name}")
        else:
            print(f"⏭️  SKIP - {name} (previous test failed)")
    
    # Overall verdict
    print("\n" + "="*70)
    
    if all(results.values()):
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Your database is ready for scraping!")
        print("\nNext step:")
        print("  python production_scraper.py --mode full")
        
        # Optional cleanup
        if results.get('insert'):
            cleanup_test_data()
        
    else:
        print("⚠️ SOME TESTS FAILED")
        print("\nPlease fix the issues above before proceeding.")
        print("\nCommon solutions:")
        print("1. Check .env file has correct DATABASE_URL")
        print("2. Verify database is running (check Supabase dashboard)")
        print("3. Test connection manually with psql")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()