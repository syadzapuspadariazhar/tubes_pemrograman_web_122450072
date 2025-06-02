#!/usr/bin/env python3
"""
Test script to verify the login functionality works
"""
import requests
import json

BASE_URL = "http://localhost:6543"

def test_login():
    """Test the login endpoint"""
    print("🧪 Testing login functionality...")
    
    # Test login with valid credentials
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", 
                               json=login_data,
                               headers={"Content-Type": "application/json"})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                print("✅ Login successful! Token received.")
                return data["token"]
            else:
                print("❌ Login response missing token")
                return None
        else:
            print(f"❌ Login failed with status {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server. Is it running on port 6543?")
        return None
    except Exception as e:
        print(f"❌ Error during login test: {e}")
        return None

def test_verify_token(token):
    """Test token verification"""
    if not token:
        print("⏭️  Skipping token verification (no token)")
        return False
        
    print("\n🧪 Testing token verification...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/auth/verify",
                              headers={"Authorization": f"Bearer {token}"})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Token verification successful!")
            return True
        else:
            print(f"❌ Token verification failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during token verification: {e}")
        return False

def test_protected_endpoint(token):
    """Test accessing a protected endpoint"""
    if not token:
        print("⏭️  Skipping protected endpoint test (no token)")
        return False
        
    print("\n🧪 Testing protected endpoint access...")
    
    try:
        # Test categories endpoint
        response = requests.get(f"{BASE_URL}/api/categories",
                              headers={"Authorization": f"Bearer {token}"})
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Protected endpoint access successful!")
            return True
        else:
            print(f"❌ Protected endpoint access failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error during protected endpoint test: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting authentication system test...\n")
    
    # Test login
    token = test_login()
    
    # Test token verification
    verify_success = test_verify_token(token)
    
    # Test protected endpoint
    protected_success = test_protected_endpoint(token)
    
    print("\n" + "="*50)
    print("📊 TEST SUMMARY:")
    print(f"Login: {'✅ PASS' if token else '❌ FAIL'}")
    print(f"Token Verification: {'✅ PASS' if verify_success else '❌ FAIL'}")  
    print(f"Protected Access: {'✅ PASS' if protected_success else '❌ FAIL'}")
    
    if token and verify_success and protected_success:
        print("🎉 All authentication tests PASSED!")
    else:
        print("⚠️  Some authentication tests FAILED!")
        print("Make sure the backend server is running and try again.")
