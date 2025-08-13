#!/usr/bin/env python3
"""
Script to test the /ventas/analisis/{negocio_id} endpoint
"""

import requests
import json
from datetime import date, timedelta

# Configuration
BASE_URL = "http://127.0.0.1:8000"
TEST_EMAIL = "ismaeldimenza@hotmail.com"
TEST_PASSWORD = "ismael38772433"

def test_analisis_endpoint():
    """Test the sales analysis endpoint"""
    
    print("🧪 TESTING /ventas/analisis/{negocio_id} ENDPOINT")
    print("=" * 60)
    
    # 1. Login to get token
    print("\n1. 🔐 Login to get authentication token")
    try:
        login_data = {
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        response = requests.post(f"{BASE_URL}/users/login", data=login_data)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            print(f"✅ Login successful")
            print(f"✅ Token obtained: {access_token[:20]}...")
        else:
            print(f"❌ Error in login: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False
    
    # Headers with token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 2. Get user's businesses to find a negocio_id
    print("\n2. 🏪 Get user businesses")
    try:
        response = requests.get(f"{BASE_URL}/businesses/me", headers=headers)
        if response.status_code == 200:
            businesses = response.json()
            print(f"✅ Found {len(businesses)} businesses")
            if not businesses:
                print("❌ No businesses found for user")
                return False
            
            # Use the first business for testing
            negocio_id = businesses[0]["id"]
            negocio_nombre = businesses[0]["nombre"]
            print(f"✅ Testing with business: {negocio_nombre} (ID: {negocio_id})")
        else:
            print(f"❌ Error getting businesses: {response.status_code}")
            print(f"   {response.text}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False
    
    # 3. Test the analysis endpoint with different date ranges
    print(f"\n3. 📊 Testing analysis endpoint with negocio_id: {negocio_id}")
    
    # Test cases with different date ranges
    test_cases = [
        {
            "name": "Last 7 days",
            "fecha_inicio": (date.today() - timedelta(days=7)).isoformat(),
            "fecha_fin": date.today().isoformat()
        },
        {
            "name": "Last 30 days",
            "fecha_inicio": (date.today() - timedelta(days=30)).isoformat(),
            "fecha_fin": date.today().isoformat()
        },
        {
            "name": "This month",
            "fecha_inicio": date.today().replace(day=1).isoformat(),
            "fecha_fin": date.today().isoformat()
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n3.{i} Testing {test_case['name']} ({test_case['fecha_inicio']} to {test_case['fecha_fin']})")
        try:
            # Make the API call
            url = f"{BASE_URL}/ventas/analisis/{negocio_id}"
            params = {
                "fecha_inicio": test_case["fecha_inicio"],
                "fecha_fin": test_case["fecha_fin"]
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            print(f"    Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("    ✅ Success! Response structure:")
                print(f"       - fecha_inicio: {data.get('fecha_inicio')}")
                print(f"       - fecha_fin: {data.get('fecha_fin')}")
                print(f"       - total_ventas: {data.get('total_ventas', 0)}")
                print(f"       - total_productos_vendidos: {data.get('total_productos_vendidos', 0)}")
                print(f"       - margen_ganancia_total: {data.get('margen_ganancia_total', 0)}")
                print(f"       - ventas_por_dia: {len(data.get('ventas_por_dia', []))} entries")
                print(f"       - productos_mas_vendidos: {len(data.get('productos_mas_vendidos', []))} entries")
                print(f"       - categorias_mas_vendidas: {len(data.get('categorias_mas_vendidas', []))} entries")
                
                # Show sample data if available
                if data.get('productos_mas_vendidos'):
                    print("    📦 Top selling products:")
                    for j, producto in enumerate(data['productos_mas_vendidos'][:3], 1):
                        print(f"       {j}. {producto.get('nombre')} - Qty: {producto.get('cantidad')} - Total: ${producto.get('total', 0)}")
                        
            elif response.status_code == 422:
                print("    ❌ 422 Unprocessable Entity - Parameter validation error")
                error_detail = response.json()
                print(f"    Error details: {json.dumps(error_detail, indent=6)}")
            else:
                print(f"    ❌ Error: {response.status_code}")
                print(f"    Response: {response.text}")
                
        except Exception as e:
            print(f"    ❌ Connection error: {e}")
    
    # 4. Test with invalid parameters to trigger 422
    print(f"\n4. 🚨 Testing with invalid parameters (should return 422)")
    try:
        invalid_cases = [
            {
                "name": "Invalid date format",
                "fecha_inicio": "2023-13-01",  # Invalid month
                "fecha_fin": date.today().isoformat()
            },
            {
                "name": "Future start date > end date",
                "fecha_inicio": (date.today() + timedelta(days=1)).isoformat(),
                "fecha_fin": date.today().isoformat()
            }
        ]
        
        for case in invalid_cases:
            print(f"\n   Testing: {case['name']}")
            response = requests.get(
                f"{BASE_URL}/ventas/analisis/{negocio_id}",
                headers=headers,
                params={
                    "fecha_inicio": case["fecha_inicio"],
                    "fecha_fin": case["fecha_fin"]
                }
            )
            print(f"   Status Code: {response.status_code}")
            if response.status_code == 422:
                print("   ✅ Correctly returned 422 for invalid parameters")
            elif response.status_code == 400:
                print("   ✅ Correctly returned 400 for invalid date range")
            else:
                print(f"   ⚠️ Unexpected status: {response.status_code}")
                
    except Exception as e:
        print(f"    ❌ Connection error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 ENDPOINT TESTING COMPLETED")
    return True

if __name__ == "__main__":
    success = test_analisis_endpoint()
    exit(0 if success else 1)
