import requests
import json

# Test the POST endpoint
url = "http://localhost:6543/api/categories"
headers = {"Content-Type": "application/json"}
data = {
    "nama": "Test Category"
}

print("Testing POST /api/categories endpoint...")
print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print("-" * 50)

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS: POST request worked!")
    else:
        print(f"\n❌ FAILED: Expected 200, got {response.status_code}")
        # Try to parse error message
        try:
            error_data = response.json()
            print(f"Error details: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Raw response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ CONNECTION ERROR: Server is not running or not accessible")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")

# Also test GET to see existing categories
print("\n" + "="*50)
print("Testing GET /api/categories endpoint...")

try:
    response = requests.get("http://localhost:6543/api/categories")
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS: GET request worked!")
    else:
        print(f"\n❌ FAILED: Expected 200, got {response.status_code}")
        
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
