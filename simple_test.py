import requests
import json

print("Testing POST /api/categories with correct field name...")

try:
    response = requests.post(
        "http://localhost:6543/api/categories",
        headers={"Content-Type": "application/json"},
        json={"nama": "Kategori Test"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ SUCCESS: Categories can be added via POST!")
    else:
        print(f"❌ Error {response.status_code}")
        try:
            error_details = response.json()
            print(f"Details: {json.dumps(error_details, indent=2)}")
        except:
            pass
            
except Exception as e:
    print(f"❌ Exception: {e}")

print("\n" + "="*50)
print("Testing GET /api/categories...")

try:
    response = requests.get("http://localhost:6543/api/categories")
    print(f"Status: {response.status_code}")
    print(f"Categories: {response.text}")
except Exception as e:
    print(f"❌ Exception: {e}")
