"""
Find Correct PIHPS API Endpoint
Tests both GET and POST methods with different URL patterns
"""

import requests
import json

def test_url_patterns():
    """
    Test different URL patterns
    """
    
    base_patterns = [
        "https://www.bi.go.id/hargapangan/TabelHarga/GetHargaHarian",
        "https://www.bi.go.id/hargapangan/api/TabelHarga/GetHargaHarian",
        "https://www.bi.go.id/hargapangan/Api/GetHargaHarian",
        "https://www.bi.go.id/id-id/hargapangan/api/GetHargaHarian",
        "https://www.bi.go.id/hargapangan/Services/GetHargaHarian",
    ]
    
    params = {
        'filter_id': 1,
        'provinsi_id': '31',  # Jakarta
        'tanggal_awal': '2025-11-01',
        'tanggal_akhir': '2025-11-28',
        'katpangan_id': 'cat_1'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalKomoditas'
    }
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           FINDING CORRECT API ENDPOINT                       ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    for url in base_patterns:
        print(f"\n{'='*70}")
        print(f"Testing: {url}")
        print('='*70)
        
        # Test GET
        print("\n📋 Method: GET")
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            print(f"  Length: {len(response.text)} chars")
            
            if response.status_code == 200 and len(response.text) > 10:
                print(f"  ✅ POTENTIAL MATCH!")
                print(f"  First 200 chars: {response.text[:200]}")
                
                try:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        print(f"  ✅✅ SUCCESS! Got {len(data)} records")
                        print(f"  Sample: {data[0]}")
                        return url, 'GET', params
                except:
                    pass
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        # Test POST (with params as form data)
        print("\n📋 Method: POST (form data)")
        try:
            response = requests.post(url, data=params, headers=headers, timeout=10)
            print(f"  Status: {response.status_code}")
            print(f"  Length: {len(response.text)} chars")
            
            if response.status_code == 200 and len(response.text) > 10:
                print(f"  ✅ POTENTIAL MATCH!")
                print(f"  First 200 chars: {response.text[:200]}")
                
                try:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        print(f"  ✅✅ SUCCESS! Got {len(data)} records")
                        print(f"  Sample: {data[0]}")
                        return url, 'POST', params
                except:
                    pass
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        # Test POST (with params as JSON)
        print("\n📋 Method: POST (JSON)")
        try:
            headers_json = headers.copy()
            headers_json['Content-Type'] = 'application/json'
            
            response = requests.post(url, json=params, headers=headers_json, timeout=10)
            print(f"  Status: {response.status_code}")
            print(f"  Length: {len(response.text)} chars")
            
            if response.status_code == 200 and len(response.text) > 10:
                print(f"  ✅ POTENTIAL MATCH!")
                print(f"  First 200 chars: {response.text[:200]}")
                
                try:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        print(f"  ✅✅ SUCCESS! Got {len(data)} records")
                        print(f"  Sample: {data[0]}")
                        return url, 'POST-JSON', params
                except:
                    pass
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n❌ No working endpoint found!")
    return None, None, None


def test_page_source_patterns():
    """
    Check if data is embedded in page source (not AJAX)
    """
    
    print("\n\n╔══════════════════════════════════════════════════════════════╗")
    print("║        CHECKING IF DATA IN PAGE SOURCE (NOT AJAX)           ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    url = "https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalKomoditas"
    
    try:
        response = requests.get(url, timeout=10)
        
        # Look for common data patterns
        patterns = [
            'var data =',
            'window.data =',
            'chartData =',
            'tableData =',
            'priceData =',
            'hargaData ='
        ]
        
        for pattern in patterns:
            if pattern in response.text:
                # Find the data
                start = response.text.find(pattern)
                snippet = response.text[start:start+500]
                print(f"✅ Found pattern: {pattern}")
                print(f"Snippet: {snippet}")
                print()
        
        # Look for script tags with JSON
        if '<script' in response.text and 'JSON.parse' in response.text:
            print("✅ Found JSON.parse in script - data might be embedded")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    # Test API endpoints
    result = test_url_patterns()
    
    if result[0]:
        print("\n\n" + "="*70)
        print("✅✅ FOUND WORKING ENDPOINT!")
        print("="*70)
        print(f"URL: {result[0]}")
        print(f"Method: {result[1]}")
        print(f"Params: {json.dumps(result[2], indent=2)}")
    else:
        # Try checking page source
        test_page_source_patterns()
        
        print("\n\n" + "="*70)
        print("⚠️ NO API ENDPOINT FOUND")
        print("="*70)
        print("\nPossible reasons:")
        print("1. Data is rendered server-side (in HTML)")
        print("2. API requires authentication/session")
        print("3. API uses different parameter names")
        print("4. Need to inspect browser Network tab manually")
        print("\n📋 NEXT STEP:")
        print("1. Open: https://www.bi.go.id/hargapangan/TabelHarga/PasarTradisionalKomoditas")
        print("2. Press F12 → Network tab → XHR filter")
        print("3. Select province and dates, click submit")
        print("4. Look for requests - copy the URL!")