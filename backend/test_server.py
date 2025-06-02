#!/usr/bin/env python3
import requests
import json

def test_category_post():
    url = "http://localhost:6543/api/categories"
    headers = {'Content-Type': 'application/json'}
    data = {'nama': 'Test Category from Script'}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server. Is it running on port 6543?")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing POST /api/categories endpoint...")
    test_category_post()
