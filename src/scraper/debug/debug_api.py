"""
Debug Script - Check PIHPS API Responses
This will show us what the API actually returns
"""

import requests
from datetime import datetime, timedelta
import json

# PIHPS API endpoints
BASE_URL = "https://www.bi.go.id/hargapangan/WebSite/TabelHarga"

def check_api_response(price_type_id=1, days_back=30):
    """
    Check what API returns for different market types
    """
    
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    
    print(f"\n{'='*70}")
    print(f"Testing API with:")
    print(f"  price_type_id: {price_type_id}")
    print(f"  start_date: {start_date}")
    print(f"  end_date: {end_date}")
    print(f"{'='*70}\n")
    
    # Try the endpoint
    url = f"{BASE_URL}/GetHargaHarian"
    
    params = {
        'filter_id': price_type_id,
        'katpangan_id': 'cat_1',
        'provinsi_id': '',  # Empty = all provinces
        'tanggal_awal': start_date,
        'tanggal_akhir': end_date,
        'tipe_laporan': 1  # 1=Harian
    }
    
    print(f"URL: {url}")
    print(f"Params: {json.dumps(params, indent=2)}\n")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Referer': 'https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalKomoditas'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Response Length: {len(response.text)} chars\n")
        
        # Show first 500 chars
        print("First 500 characters of response:")
        print("-" * 70)
        print(response.text[:500])
        print("-" * 70)
        
        # Try to parse as JSON
        try:
            data = response.json()
            print("\n✅ Valid JSON!")
            print(f"Response type: {type(data)}")
            
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
            elif isinstance(data, list):
                print(f"List length: {len(data)}")
                if data:
                    print(f"First item: {data[0]}")
        except json.JSONDecodeError as e:
            print(f"\n❌ NOT valid JSON!")
            print(f"JSON Error: {e}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")


def test_all_endpoints():
    """
    Test different API endpoints that might exist
    """
    
    endpoints = [
        'GetHargaHarian',
        'GetHargaMingguan', 
        'GetHargaBulanan',
        'GetHargaGrafis',
        'GetDataHarga',
        'GetHargaPangan'
    ]
    
    print("\n" + "="*70)
    print("TESTING DIFFERENT ENDPOINTS")
    print("="*70)
    
    for endpoint in endpoints:
        url = f"{BASE_URL}/{endpoint}"
        
        print(f"\nTrying: {url}")
        
        try:
            response = requests.get(
                url,
                params={
                    'filter_id': 1,
                    'katpangan_id': 'cat_1',
                    'provinsi_id': '',
                    'tanggal_awal': '2025-11-01',
                    'tanggal_akhir': '2025-11-28'
                },
                headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Accept': 'application/json'
                },
                timeout=10
            )
            
            print(f"  Status: {response.status_code}")
            print(f"  Length: {len(response.text)} chars")
            
            # Check if looks like JSON
            if response.text.strip().startswith('{') or response.text.strip().startswith('['):
                print(f"  ✅ Looks like JSON")
                try:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        print(f"  ✅ Has data: {len(data)} items")
                    elif isinstance(data, dict):
                        print(f"  ✅ Dict with keys: {list(data.keys())}")
                except:
                    pass
            else:
                print(f"  ❌ Doesn't look like JSON")
                print(f"  First 100 chars: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ Failed: {e}")


def test_market_type_endpoints():
    """
    Test if different market types need different endpoints
    """
    
    print("\n" + "="*70)
    print("TESTING MARKET-SPECIFIC ENDPOINTS")
    print("="*70)
    
    market_configs = [
        {
            'name': 'Pasar Tradisional',
            'referer': 'https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalKomoditas',
            'price_type_id': 1
        },
        {
            'name': 'Pasar Modern',
            'referer': 'https://www.bi.go.id/hargapangan/TabelHarga/PasarModernKomoditas',
            'price_type_id': 2
        },
        {
            'name': 'Pedagang Besar',
            'referer': 'https://www.bi.go.id/hargapangan/TabelHarga/PedagangBesarKomoditas',
            'price_type_id': 3
        },
        {
            'name': 'Produsen',
            'referer': 'https://www.bi.go.id/hargapangan/TabelHarga/ProdusenKomoditas',
            'price_type_id': 4
        }
    ]
    
    for config in market_configs:
        print(f"\n{config['name']}:")
        print(f"  Referer: {config['referer']}")
        print(f"  price_type_id: {config['price_type_id']}")
        
        url = f"{BASE_URL}/GetHargaHarian"
        
        try:
            response = requests.get(
                url,
                params={
                    'filter_id': config['price_type_id'],
                    'katpangan_id': 'cat_1',
                    'provinsi_id': '31',  # DKI Jakarta
                    'tanggal_awal': '2025-11-01',
                    'tanggal_akhir': '2025-11-28'
                },
                headers={
                    'User-Agent': 'Mozilla/5.0',
                    'Accept': 'application/json',
                    'Referer': config['referer']
                },
                timeout=10
            )
            
            print(f"  Status: {response.status_code}")
            print(f"  Length: {len(response.text)} chars")
            
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"  ✅ Has {len(data)} records")
                    if data:
                        print(f"  Sample: {str(data[0])[:100]}")
                else:
                    print(f"  Type: {type(data)}")
            except:
                print(f"  ❌ Not valid JSON")
                print(f"  First 200 chars: {response.text[:200]}")
                
        except Exception as e:
            print(f"  ❌ Failed: {e}")


if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           PIHPS API DEBUG TOOL                               ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    # Test 1: Check basic response
    print("\n📋 TEST 1: Check basic API response")
    check_api_response(price_type_id=1, days_back=7)
    
    # Test 2: Test different endpoints
    print("\n📋 TEST 2: Test different endpoint names")
    test_all_endpoints()
    
    # Test 3: Test market-specific configs
    print("\n📋 TEST 3: Test each market type")
    test_market_type_endpoints()
    
    print("\n" + "="*70)
    print("✅ DEBUG COMPLETE")
    print("="*70)