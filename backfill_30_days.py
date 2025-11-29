"""
Backfill Script for Nusantara Food Watch
Fills in missing data for the last 30 days

Usage:
    python backfill_30_days.py                    # Backfill last 30 days
    python backfill_30_days.py --days 7           # Backfill last 7 days
    python backfill_30_days.py --start 2024-01-01 --end 2024-01-31  # Custom range

This script:
1. Calculates date range (last 30 days by default)
2. Scrapes data for all commodities and market types
3. Inserts into database (skips duplicates)
4. Sends email notification on completion
"""

import sys
from pathlib import Path
import argparse
from datetime import datetime, timedelta
import time

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.scraper.app_scraper import EnhancedMultiCommodityScraper
from src.db.nusantara_db import NusantaraDatabase
from src.utils.notifications import send_backfill_complete_email, send_scrape_failure_email


def backfill_data(
    start_date: str,
    end_date: str,
    commodities: list = None,
    market_types: list = None
):
    """
    Backfill data for specified date range
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        commodities: List of commodity IDs (None = all)
        market_types: List of market type IDs (None = all)
    
    Returns:
        Total number of records inserted
    """
    
    print("=" * 70)
    print("NUSANTARA FOOD WATCH - BACKFILL SCRIPT")
    print("=" * 70)
    
    print(f"\n📅 Date Range: {start_date} to {end_date}")
    print(f"🏪 Market Types: {market_types or 'All (1-4)'}")
    print(f"🌾 Commodities: {commodities or 'All (10 categories)'}")
    
    # Initialize
    scraper = EnhancedMultiCommodityScraper()
    db = NusantaraDatabase()
    
    # Default to all market types if not specified
    if market_types is None:
        market_types = [1, 2, 3, 4]  # Traditional, Modern, Wholesale, Producer
    
    total_inserted = 0
    start_time = time.time()
    
    # Scrape for each market type
    for i, market_id in enumerate(market_types, 1):
        market_names = {
            1: "Traditional Markets (Pasar Tradisional)",
            2: "Modern Markets/Supermarkets",
            3: "Wholesalers (Pedagang Besar)",
            4: "Producers/Farmers (Produsen)"
        }
        
        print(f"\n{'=' * 70}")
        print(f"Market Type {i}/{len(market_types)}: {market_names.get(market_id, 'Unknown')}")
        print("=" * 70)
        
        try:
            # Scrape data
            print(f"\n📥 Scraping data...")
            df = scraper.scrape_all_commodities(
                start_date=start_date,
                end_date=end_date,
                market_type_id=market_id,
                tipe_laporan=1,  # Daily data
                commodities=commodities
            )
            
            if df.empty:
                print("⚠️ No data returned from API")
                continue
            
            print(f"✓ Retrieved {len(df):,} records from API")
            
            # Prepare data for database
            df['commodity_category'] = df['commodity_id']
            df['report_type'] = 'daily'
            df['market_type_id'] = market_id
            
            # Insert to database
            print(f"\n💾 Inserting to database...")
            db.connect()
            
            inserted = db.insert_data(df, on_conflict='ignore')
            
            print(f"✅ Inserted {inserted:,} new records (duplicates skipped)")
            total_inserted += inserted
            
            db.close()
            
            # Brief pause between market types to avoid rate limiting
            if i < len(market_types):
                print("\n⏸️ Pausing 2 seconds before next market type...")
                time.sleep(2)
            
        except Exception as e:
            print(f"\n❌ Error scraping market type {market_id}: {e}")
            db.close()
            continue
    
    # Calculate execution time
    end_time = time.time()
    duration = end_time - start_time
    
    # Print summary
    print("\n" + "=" * 70)
    print("BACKFILL SUMMARY")
    print("=" * 70)
    print(f"✅ Total Records Inserted: {total_inserted:,}")
    print(f"⏱️ Total Time: {int(duration // 60)}m {int(duration % 60)}s")
    print(f"📊 Average: {total_inserted / duration:.1f} records/second" if duration > 0 else "")
    print("=" * 70)
    
    return total_inserted, duration


def main():
    """
    Main function - parse arguments and run backfill
    """
    
    parser = argparse.ArgumentParser(
        description='Backfill Nusantara Food Watch data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python backfill_30_days.py                     # Last 30 days
  python backfill_30_days.py --days 7            # Last 7 days
  python backfill_30_days.py --days 90           # Last 90 days
  python backfill_30_days.py --start 2024-01-01 --end 2024-01-31
  python backfill_30_days.py --no-email          # Skip email notification
        """
    )
    
    parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to backfill (default: 30)'
    )
    
    parser.add_argument(
        '--start',
        type=str,
        help='Start date (YYYY-MM-DD). Overrides --days.'
    )
    
    parser.add_argument(
        '--end',
        type=str,
        help='End date (YYYY-MM-DD). Defaults to today.'
    )
    
    parser.add_argument(
        '--market-types',
        type=int,
        nargs='+',
        choices=[1, 2, 3, 4],
        help='Market type IDs to scrape (default: all)'
    )
    
    parser.add_argument(
        '--no-email',
        action='store_true',
        help='Skip email notification'
    )
    
    args = parser.parse_args()
    
    # Calculate date range
    if args.start and args.end:
        start_date = args.start
        end_date = args.end
    elif args.start:
        start_date = args.start
        end_date = datetime.now().strftime('%Y-%m-%d')
    else:
        end_date = datetime.now()
        start_date = (end_date - timedelta(days=args.days)).strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
    
    # Validate dates
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
        datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        print("❌ Error: Dates must be in YYYY-MM-DD format")
        sys.exit(1)
    
    # Run backfill
    try:
        total_records, duration = backfill_data(
            start_date=start_date,
            end_date=end_date,
            market_types=args.market_types
        )
        
        # Send email notification
        if not args.no_email:
            print("\n📧 Sending email notification...")
            try:
                send_backfill_complete_email(
                    total_records=total_records,
                    start_date=start_date,
                    end_date=end_date,
                    duration=duration
                )
                print("✅ Email sent successfully")
            except Exception as e:
                print(f"⚠️ Failed to send email: {e}")
        
        print("\n✅ Backfill completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Backfill interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Backfill failed: {e}")
        
        # Send failure email
        if not args.no_email:
            try:
                send_scrape_failure_email(
                    error_message=str(e),
                    error_type="Backfill Error"
                )
            except Exception as email_error:
                print(f"⚠️ Failed to send failure email: {email_error}")
        
        sys.exit(1)


if __name__ == "__main__":
    main()