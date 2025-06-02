import requests
import json
import time

print("Testing POST endpoint with detailed timing...")
start_time = time.time()

try:
    print("Making POST request...")
    response = requests.post(
        "http://localhost:6543/api/categories",
        headers={"Content-Type": "application/json"},
        json={"nama": "test kategori"},
        timeout=30  # Increased timeout
    )
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"✅ POST completed in {duration:.2f} seconds")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
except requests.exceptions.Timeout:
    end_time = time.time()
    duration = end_time - start_time
    print(f"❌ Request timed out after {duration:.2f} seconds")
    
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection error: {e}")
    
except Exception as e:
    end_time = time.time()
    duration = end_time - start_time
    print(f"❌ Error after {duration:.2f} seconds: {e}")

print("\nTesting GET endpoint for comparison...")
try:
    start_time = time.time()
    response = requests.get("http://localhost:6543/api/categories", timeout=10)
    end_time = time.time()
    duration = end_time - start_time
    print(f"✅ GET completed in {duration:.2f} seconds")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ GET Error: {e}")
