"""
Debug Monthly Data Response
Check what the API actually returns for monthly data
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "https://www.bi.go.id/hargapangan/WebSite/TabelHarga/GetGridDataKomoditas"

def debug_monthly_response():
    """
    Debug: Show raw response for monthly data
    """
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
    
    print("=" * 70)
    print("DEBUG: Monthly Data Response")
    print("=" * 70)
    
    # Test parameters
    test_cases = [
        {
            'name': 'Monthly - Beras',
            'params': {
                'price_type_id': 1,
                'comcat_id': 'cat_1',
                'province_id': '',
                'regency_id': '',
                'showKota': 'false',
                'showPasar': 'false',
                'tipe_laporan': 3,  # MONTHLY
                'start_date': start_date,
                'end_date': end_date
            }
        },
        {
            'name': 'Daily - Beras (working)',
            'params': {
                'price_type_id': 1,
                'comcat_id': 'cat_1',
                'province_id': '',
                'regency_id': '',
                'showKota': 'false',
                'showPasar': 'false',
                'tipe_laporan': 1,  # DAILY
                'start_date': '2025-11-20',
                'end_date': '2025-11-28'
            }
        }
    ]
    
    for test in test_cases:
        print(f"\n{'='*70}")
        print(f"TEST: {test['name']}")
        print(f"{'='*70}")
        print(f"\nParameters:")
        print(json.dumps(test['params'], indent=2))
        
        try:
            response = requests.get(
                BASE_URL,
                params=test['params'],
                headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Accept': 'application/json'
                },
                timeout=30
            )
            
            print(f"\nStatus: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                if 'data' in result:
                    data = result['data']
                    print(f"Rows returned: {len(data)}")
                    
                    if data:
                        # Show first row structure
                        print(f"\nFirst row structure:")
                        print(json.dumps(data[0], indent=2))
                        
                        # Show all keys in first row
                        print(f"\nAll keys in first row:")
                        for key in data[0].keys():
                            value = data[0][key]
                            print(f"  '{key}': {value} ({type(value).__name__})")
                        
                        # Count date columns
                        date_cols = [k for k in data[0].keys() if '/' in str(k)]
                        print(f"\nDate columns found: {len(date_cols)}")
                        print(f"Date columns: {date_cols[:5]}...")  # Show first 5
                        
                        # Show second row (province)
                        if len(data) > 1:
                            print(f"\nSecond row (should be Aceh):")
                            print(f"  name: {data[1].get('name')}")
                            print(f"  level: {data[1].get('level')}")
                            # Show one price
                            for key in data[1].keys():
                                if '/' in str(key):
                                    print(f"  {key}: {data[1][key]}")
                                    break
                    else:
                        print("❌ Empty data array")
                else:
                    print("❌ No 'data' key in response")
                    print(f"Response keys: {list(result.keys())}")
            else:
                print(f"❌ HTTP Error")
                print(f"Response: {response.text[:200]}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*70)
    print("DEBUG COMPLETE")
    print("="*70)


if __name__ == "__main__":
    debug_monthly_response()