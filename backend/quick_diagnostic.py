#!/usr/bin/env python3
"""
Quick diagnostic script to test POST endpoint timing
"""
import sys
import time
import subprocess
import signal
import os

def test_server_response():
    print("=" * 50)
    print("BACKEND SERVER DIAGNOSTIC TEST")
    print("=" * 50)
    
    # Test if server is responding to GET first
    print("\n1. Testing GET /api/categories...")
    try:
        import requests
        start = time.time()
        response = requests.get("http://localhost:6543/api/categories", timeout=5)
        duration = time.time() - start
        print(f"   ✅ GET successful in {duration:.2f}s - Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ GET failed: {e}")
        return False
    
    # Test POST with timeout monitoring
    print("\n2. Testing POST /api/categories...")
    try:
        start = time.time()
        response = requests.post(
            "http://localhost:6543/api/categories",
            headers={"Content-Type": "application/json"},
            json={"nama": "diagnostic_test"},
            timeout=10
        )
        duration = time.time() - start
        print(f"   ✅ POST successful in {duration:.2f}s - Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return True
        
    except requests.exceptions.Timeout:
        duration = time.time() - start
        print(f"   ❌ POST timed out after {duration:.2f}s")
        print("   This indicates the server is hanging during POST processing")
        return False
        
    except Exception as e:
        duration = time.time() - start
        print(f"   ❌ POST failed after {duration:.2f}s: {e}")
        return False

if __name__ == "__main__":
    success = test_server_response()
    
    if not success:
        print("\n" + "=" * 50)
        print("DIAGNOSIS: Server POST endpoint is hanging")
        print("RECOMMENDATION: Restart server and check logs")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("DIAGNOSIS: Server is working correctly")
        print("=" * 50)
