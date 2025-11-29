"""
Email Notification Module for Nusantara Food Watch
Sends alerts on scraper success/failure

Setup Instructions:
1. Use Gmail account for sending
2. Enable 2-Factor Authentication on Gmail
3. Generate App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: Mail
   - Select device: Other (Custom name) → "Nusantara Food Watch"
   - Copy the 16-character password
4. Add to .env:
   EMAIL_ADDRESS=your-email@gmail.com
   EMAIL_APP_PASSWORD=your-16-char-app-password
   ALERT_EMAIL=recipient@email.com

For GitHub Actions:
1. Go to Repository → Settings → Secrets and variables → Actions
2. Add secrets:
   - EMAIL_ADDRESS
   - EMAIL_APP_PASSWORD
   - ALERT_EMAIL
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# SMTP Configuration for Gmail
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  # TLS port


def send_email_alert(
    subject: str,
    body: str,
    is_html: bool = False,
    is_error: bool = False
) -> bool:
    """
    Send email alert using Gmail
    
    Args:
        subject: Email subject
        body: Email body content
        is_html: Whether body is HTML formatted
        is_error: True for error emails (adds [ERROR] prefix)
    
    Returns:
        True if sent successfully, False otherwise
    """
    
    # Get credentials from environment
    sender_email = os.getenv('EMAIL_ADDRESS')
    sender_password = os.getenv('EMAIL_APP_PASSWORD')
    receiver_email = os.getenv('ALERT_EMAIL')
    
    # Validate credentials
    if not all([sender_email, sender_password, receiver_email]):
        print("⚠️ Email credentials not configured!")
        print("Missing:")
        if not sender_email:
            print("  - EMAIL_ADDRESS")
        if not sender_password:
            print("  - EMAIL_APP_PASSWORD")
        if not receiver_email:
            print("  - ALERT_EMAIL")
        return False
    
    # Add prefix to subject
    prefix = "[ERROR] " if is_error else "[INFO] "
    full_subject = f"{prefix}Nusantara Food Watch - {subject}"
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = full_subject
    
    # Attach body
    mime_type = 'html' if is_html else 'plain'
    msg.attach(MIMEText(body, mime_type))
    
    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade to secure connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"✅ Email sent successfully to {receiver_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Email authentication failed!")
        print("Check:")
        print("  1. EMAIL_ADDRESS is correct")
        print("  2. EMAIL_APP_PASSWORD is app password (not regular password)")
        print("  3. 2FA is enabled on Gmail")
        return False
        
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error sending email: {e}")
        return False


def send_scrape_success_email(
    records_count: int,
    commodities_count: int = 10,
    provinces_count: int = 35,
    market_types: int = 4,
    execution_time: Optional[float] = None
) -> bool:
    """
    Send success notification after successful scrape
    
    Args:
        records_count: Number of records inserted
        commodities_count: Number of commodities scraped
        provinces_count: Number of provinces
        market_types: Number of market types
        execution_time: Execution time in seconds (optional)
    
    Returns:
        True if sent successfully
    """
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Plain text version
    body = f"""
Nusantara Food Watch - Scraper Success Report
{'=' * 60}

Timestamp: {timestamp}

SUMMARY
-------
Status: ✅ Success
Records Inserted: {records_count:,}
Commodities: {commodities_count}
Provinces: {provinces_count}
Market Types: {market_types}
"""
    
    if execution_time:
        minutes = int(execution_time // 60)
        seconds = int(execution_time % 60)
        body += f"Execution Time: {minutes}m {seconds}s\n"
    
    body += """

DATA COVERAGE
-------------
- Traditional Markets (Pasar Tradisional)
- Modern Markets/Supermarkets
- Wholesalers (Pedagang Besar)
- Producers/Farmers (Produsen)

NEXT STEPS
----------
✓ Data available in database
✓ Ready for analysis
✓ Dashboard will auto-update

---
This is an automated message from Nusantara Food Watch scraper.
Project: github.com/YOUR_USERNAME/nusantara-food-watch
"""
    
    subject = f"Daily Scrape Success - {records_count:,} records"
    
    return send_email_alert(subject, body, is_html=False, is_error=False)


def send_scrape_failure_email(
    error_message: str,
    error_type: str = "Unknown Error",
    traceback_info: Optional[str] = None
) -> bool:
    """
    Send failure notification when scraper fails
    
    Args:
        error_message: Error message
        error_type: Type of error
        traceback_info: Full traceback (optional)
    
    Returns:
        True if sent successfully
    """
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    body = f"""
Nusantara Food Watch - Scraper Failure Alert
{'=' * 60}

⚠️ SCRAPER FAILED - ACTION REQUIRED ⚠️

Timestamp: {timestamp}

ERROR DETAILS
-------------
Type: {error_type}
Message: {error_message}

"""
    
    if traceback_info:
        body += f"""
FULL TRACEBACK
--------------
{traceback_info}

"""
    
    body += """
RECOMMENDED ACTIONS
-------------------
1. Check GitHub Actions logs
2. Verify database connection
3. Check PIHPS API status
4. Review error message above
5. Fix issue and re-run manually if needed

MANUAL RE-RUN
-------------
To manually trigger scraper:
1. Go to: github.com/YOUR_USERNAME/nusantara-food-watch/actions
2. Select "Daily Food Price Scraper"
3. Click "Run workflow"

---
This is an automated alert from Nusantara Food Watch scraper.
Please respond ASAP to minimize data gaps.
"""
    
    subject = f"Scraper Failed - {error_type}"
    
    return send_email_alert(subject, body, is_html=False, is_error=True)


def send_backfill_complete_email(
    total_records: int,
    start_date: str,
    end_date: str,
    duration: Optional[float] = None
) -> bool:
    """
    Send notification after backfill completes
    
    Args:
        total_records: Total records backfilled
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        duration: Execution time in seconds
    
    Returns:
        True if sent successfully
    """
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    body = f"""
Nusantara Food Watch - Backfill Complete
{'=' * 60}

Timestamp: {timestamp}

BACKFILL SUMMARY
----------------
Status: ✅ Complete
Total Records: {total_records:,}
Date Range: {start_date} to {end_date}
"""
    
    if duration:
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        body += f"Duration: {minutes}m {seconds}s\n"
    
    body += """

WHAT'S NEXT
-----------
✓ Historical data loaded
✓ Database ready for analysis
✓ Can start building dashboard
✓ Daily scraper will maintain data going forward

---
This is an automated message from Nusantara Food Watch.
"""
    
    subject = f"Backfill Complete - {total_records:,} records loaded"
    
    return send_email_alert(subject, body, is_html=False, is_error=False)


def send_test_email() -> bool:
    """
    Send test email to verify configuration
    
    Returns:
        True if sent successfully
    """
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    body = f"""
Nusantara Food Watch - Test Email
{'=' * 60}

This is a test email to verify email notifications are working correctly.

Timestamp: {timestamp}

If you're receiving this, your email configuration is correct!

Configuration Details:
- Sender: {os.getenv('EMAIL_ADDRESS', 'NOT SET')}
- Receiver: {os.getenv('ALERT_EMAIL', 'NOT SET')}
- SMTP Server: {SMTP_SERVER}:{SMTP_PORT}

Next Steps:
✓ Email notifications configured
✓ Ready for automated scraping
✓ Will receive alerts on success/failure

---
Test completed successfully.
"""
    
    subject = "Test Email - Configuration Verified"
    
    return send_email_alert(subject, body, is_html=False, is_error=False)


# Convenience functions for backward compatibility
def send_success_email(records_count: int = 0) -> bool:
    """Quick success email (for GitHub Actions)"""
    return send_scrape_success_email(records_count or 1000)


def send_failure_email(error_message: str) -> bool:
    """Quick failure email (for GitHub Actions)"""
    return send_scrape_failure_email(error_message)


if __name__ == "__main__":
    """
    Test email configuration
    Usage: python -m src.utils.notifications
    """
    print("=" * 70)
    print("EMAIL CONFIGURATION TEST")
    print("=" * 70)
    
    # Check environment variables
    print("\n1. Checking environment variables...")
    email_address = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_APP_PASSWORD')
    alert_email = os.getenv('ALERT_EMAIL')
    
    if email_address:
        print(f"   ✓ EMAIL_ADDRESS: {email_address}")
    else:
        print("   ✗ EMAIL_ADDRESS: NOT SET")
    
    if email_password:
        print(f"   ✓ EMAIL_APP_PASSWORD: {'*' * 16}")
    else:
        print("   ✗ EMAIL_APP_PASSWORD: NOT SET")
    
    if alert_email:
        print(f"   ✓ ALERT_EMAIL: {alert_email}")
    else:
        print("   ✗ ALERT_EMAIL: NOT SET")
    
    if not all([email_address, email_password, alert_email]):
        print("\n❌ Configuration incomplete!")
        print("\nAdd to .env file:")
        print("EMAIL_ADDRESS=your-email@gmail.com")
        print("EMAIL_APP_PASSWORD=your-16-char-app-password")
        print("ALERT_EMAIL=recipient@email.com")
        exit(1)
    
    # Send test email
    print("\n2. Sending test email...")
    success = send_test_email()
    
    if success:
        print("\n" + "=" * 70)
        print("✅ EMAIL CONFIGURATION SUCCESSFUL!")
        print("=" * 70)
        print(f"\nTest email sent to: {alert_email}")
        print("Check your inbox!")
    else:
        print("\n" + "=" * 70)
        print("❌ EMAIL CONFIGURATION FAILED!")
        print("=" * 70)
        print("\nPlease check:")
        print("1. Gmail 2FA is enabled")
        print("2. App password is correct (16 characters)")
        print("3. Email addresses are valid")