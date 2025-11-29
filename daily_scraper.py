"""
Daily Scraper for Nusantara Food Watch
Automated daily scraping script for GitHub Actions

This script:
1. Scrapes yesterday's data (most recent complete day)
2. Scrapes all commodities and market types
3. Inserts to database
4. Sends email notification

Usage:
    python daily_scraper.py                    # Scrape yesterday
    python daily_scraper.py --today            # Scrape today (for testing)
    python daily_scraper.py --days-back 3      # Scrape last 3 days
"""

import sys
from pathlib import Path
import argparse
from datetime import datetime, timedelta
import time
import traceback

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.scraper.app_scraper import EnhancedMultiCommodityScraper
from src.db.nusantara_db import NusantaraDatabase
from src.utils.notifications import (
    send_scrape_success_email,
    send_scrape_failure_email
)


def scrape_daily_data(
    target_date: str,
    market_types: list = None
) -> tuple:
    """
    Scrape data for a specific date
    
    Args:
        target_date: Date to scrape (YYYY-MM-DD)
        market_types: List of market type IDs (None = all)
    
    Returns:
        (total_records, execution_time)
    """
    
    print("=" * 70)
    print("NUSANTARA FOOD WATCH - DAILY SCRAPER")
    print("=" * 70)
    print(f"\n📅 Target Date: {target_date}")
    print(f"⏰ Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize
    scraper = EnhancedMultiCommodityScraper()
    db = NusantaraDatabase()
    
    # Default to all market types
    if market_types is None:
        market_types = [1, 2, 3, 4]
    
    market_names = {
        1: "Traditional Markets",
        2: "Modern Markets",
        3: "Wholesalers",
        4: "Producers/Farmers"
    }
    
    total_inserted = 0
    start_time = time.time()
    
    # Scrape each market type
    for i, market_id in enumerate(market_types, 1):
        print(f"\n{'=' * 70}")
        print(f"[{i}/{len(market_types)}] {market_names.get(market_id, f'Market {market_id}')}")
        print("=" * 70)
        
        try:
            # Scrape
            print(f"📥 Scraping data...")
            df = scraper.scrape_all_commodities(
                start_date=target_date,
                end_date=target_date,
                market_type_id=market_id,
                tipe_laporan=1,  # Daily
                commodities=None  # All commodities
            )
            
            if df.empty:
                print("⚠️ No data returned")
                continue
            
            print(f"✓ Retrieved {len(df):,} records")
            
            # Prepare for database
            df['commodity_category'] = df['commodity_id']
            df['report_type'] = 'daily'
            df['market_type_id'] = market_id
            
            # Insert
            print(f"💾 Saving to database...")
            db.connect()
            inserted = db.insert_data(df, on_conflict='update')
            db.close()
            
            print(f"✅ Inserted/Updated {inserted:,} records")
            total_inserted += inserted
            
            # Pause between requests
            if i < len(market_types):
                time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.close()
            continue
    
    execution_time = time.time() - start_time
    
    # Summary
    print("\n" + "=" * 70)
    print("SCRAPING SUMMARY")
    print("=" * 70)
    print(f"✅ Total Records: {total_inserted:,}")
    print(f"⏱️ Execution Time: {int(execution_time // 60)}m {int(execution_time % 60)}s")
    print("=" * 70)
    
    return total_inserted, execution_time


def main():
    """
    Main function
    """
    
    parser = argparse.ArgumentParser(
        description='Daily scraper for Nusantara Food Watch'
    )
    
    parser.add_argument(
        '--today',
        action='store_true',
        help='Scrape today instead of yesterday'
    )
    
    parser.add_argument(
        '--days-back',
        type=int,
        default=1,
        help='Number of days back to scrape (default: 1 = yesterday)'
    )
    
    parser.add_argument(
        '--date',
        type=str,
        help='Specific date to scrape (YYYY-MM-DD)'
    )
    
    parser.add_argument(
        '--no-email',
        action='store_true',
        help='Skip email notification'
    )
    
    args = parser.parse_args()
    
    # Determine target date
    if args.date:
        target_date = args.date
    elif args.today:
        target_date = datetime.now().strftime('%Y-%m-%d')
    else:
        days_back = args.days_back
        target_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    
    # Validate date format
    try:
        datetime.strptime(target_date, '%Y-%m-%d')
    except ValueError:
        print(f"❌ Invalid date format: {target_date}")
        print("Use YYYY-MM-DD format")
        sys.exit(1)
    
    # Run scraper
    try:
        total_records, execution_time = scrape_daily_data(target_date)
        
        # Send success email
        if not args.no_email and total_records > 0:
            print("\n📧 Sending success notification...")
            try:
                send_scrape_success_email(
                    records_count=total_records,
                    execution_time=execution_time
                )
                print("✅ Email sent")
            except Exception as e:
                print(f"⚠️ Email failed: {e}")
        
        # Check if any data was scraped
        if total_records == 0:
            print("\n⚠️ WARNING: No records inserted!")
            print("This might indicate:")
            print("  - API is down")
            print("  - Data not available yet for this date")
            print("  - Network connectivity issue")
            
            if not args.no_email:
                send_scrape_failure_email(
                    error_message="No records returned from API",
                    error_type="No Data Warning"
                )
            
            sys.exit(1)
        
        print("\n✅ Daily scrape completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Scraper interrupted")
        sys.exit(1)
        
    except Exception as e:
        error_msg = str(e)
        tb = traceback.format_exc()
        
        print(f"\n❌ Scraper failed: {error_msg}")
        print("\nFull traceback:")
        print(tb)
        
        # Send failure email
        if not args.no_email:
            print("\n📧 Sending failure notification...")
            try:
                send_scrape_failure_email(
                    error_message=error_msg,
                    error_type=type(e).__name__,
                    traceback_info=tb
                )
                print("✅ Failure email sent")
            except Exception as email_error:
                print(f"⚠️ Failed to send email: {email_error}")
        
        sys.exit(1)


if __name__ == "__main__":
    main()