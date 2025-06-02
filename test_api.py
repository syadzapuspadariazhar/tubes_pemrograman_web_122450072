#!/usr/bin/env python3
"""
Simple test script to verify POST functionality
"""
import requests
import json

def test_post_category():
    url = "http://localhost:6543/api/categories"
    data = {"nama": "Test Category"}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        print(f"Testing POST to {url}")
        print(f"Data: {data}")
        print(f"Headers: {headers}")
        
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("✅ POST request successful!")
            return True
        else:
            print(f"❌ POST request failed with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_get_categories():
    url = "http://localhost:6543/api/categories"
    
    try:
        print(f"Testing GET to {url}")
        response = requests.get(url, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ GET request successful!")
            return True
        else:
            print(f"❌ GET request failed with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Backend API ===")
    
    print("\n1. Testing GET /api/categories")
    test_get_categories()
    
    print("\n2. Testing POST /api/categories")
    test_post_category()
