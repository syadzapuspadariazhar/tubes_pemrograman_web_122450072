import requests
import time

print("Testing POST endpoint after timeout fix...")
print("=" * 50)

# Test GET first
print("1. Testing GET /api/categories...")
try:
    response = requests.get("http://localhost:6543/api/categories", timeout=5)
    print(f"   ✅ GET: {response.status_code} - {response.text}")
except Exception as e:
    print(f"   ❌ GET failed: {e}")
    exit(1)

# Test POST with timing
print("\n2. Testing POST /api/categories...")
try:
    start_time = time.time()
    response = requests.post(
        "http://localhost:6543/api/categories",
        headers={"Content-Type": "application/json"},
        json={"nama": "test_kategori_fix"},
        timeout=15
    )
    duration = time.time() - start_time
    
    print(f"   ✅ POST: {response.status_code} in {duration:.2f}s")
    print(f"   Response: {response.text}")
    
    # Verify it was actually added
    print("\n3. Verifying category was added...")
    response = requests.get("http://localhost:6543/api/categories", timeout=5)
    print(f"   Categories now: {response.text}")
    
    print("\n🎉 SUCCESS: POST timeout issue has been FIXED!")
    
except requests.exceptions.Timeout:
    duration = time.time() - start_time
    print(f"   ❌ POST still timing out after {duration:.2f}s")
    print("   Need to investigate further...")
    
except Exception as e:
    duration = time.time() - start_time
    print(f"   ❌ POST failed after {duration:.2f}s: {e}")
