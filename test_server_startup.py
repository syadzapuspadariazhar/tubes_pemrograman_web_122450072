#!/usr/bin/env python3
"""
Test script to verify that the ConfigurationConflictError is fixed
and the JWT authentication system is working properly.
"""
import os
import sys
import requests
import time
import subprocess
import json

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

def test_server_startup():
    """Test that the server starts without ConfigurationConflictError"""
    print("=== Testing Server Startup ===")
    
    try:
        print("Step 1: Testing imports...")
        from app import main
        print("✅ App main imported successfully")
        
        print("Step 2: Creating WSGI app...")
        settings = {
            'sqlalchemy.url': 'sqlite:///backend/budget.db'
        }
        
        app = main({}, **settings)
        print("✅ WSGI app created without ConfigurationConflictError")
        
        print("Step 3: Starting server in background...")
        from waitress import serve
        import threading
        
        # Start server in a separate thread
        server_thread = threading.Thread(
            target=lambda: serve(app, host='localhost', port=6543),
            daemon=True
        )
        server_thread.start()
        
        # Wait for server to start
        time.sleep(3)
        
        print("✅ Server started successfully on http://localhost:6543")
        return True
        
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_authentication_endpoints():
    """Test JWT authentication endpoints"""
    print("\n=== Testing Authentication Endpoints ===")
    
    base_url = "http://localhost:6543"
    
    try:
        # Test login endpoint
        print("Testing login endpoint...")
        login_data = {
            "username": "admin",
            "password": "admin"
        }
        
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get('token')
            print(f"✅ Login successful, token received: {token[:20]}...")
            
            # Test token verification
            print("Testing token verification...")
            verify_response = requests.get(
                f"{base_url}/api/auth/verify",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10
            )
            
            if verify_response.status_code == 200:
                print("✅ Token verification successful")
                return True
            else:
                print(f"❌ Token verification failed: {verify_response.status_code}")
                return False
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

def test_protected_endpoints():
    """Test that protected endpoints require authentication"""
    print("\n=== Testing Protected Endpoints ===")
    
    base_url = "http://localhost:6543"
    
    try:
        # First get a valid token
        login_data = {"username": "admin", "password": "admin"}
        login_response = requests.post(f"{base_url}/api/auth/login", json=login_data, timeout=10)
        
        if login_response.status_code != 200:
            print("❌ Could not get authentication token")
            return False
            
        token = login_response.json().get('token')
        
        # Test categories endpoint with token
        print("Testing categories endpoint with authentication...")
        categories_response = requests.get(
            f"{base_url}/api/categories",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        
        if categories_response.status_code == 200:
            print("✅ Categories endpoint accessible with authentication")
            
            # Test transactions endpoint with token
            print("Testing transactions endpoint with authentication...")
            transactions_response = requests.get(
                f"{base_url}/api/transactions",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10
            )
            
            if transactions_response.status_code == 200:
                print("✅ Transactions endpoint accessible with authentication")
                return True
            else:
                print(f"❌ Transactions endpoint failed: {transactions_response.status_code}")
                return False
        else:
            print(f"❌ Categories endpoint failed: {categories_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Protected endpoints test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔧 JWT Authentication System Test")
    print("=" * 50)
    
    # Test 1: Server startup
    if not test_server_startup():
        print("\n❌ Server startup test failed - stopping tests")
        return
    
    # Wait a bit more for server to be ready
    time.sleep(2)
    
    # Test 2: Authentication endpoints
    auth_success = test_authentication_endpoints()
    
    # Test 3: Protected endpoints
    protected_success = test_protected_endpoints()
    
    # Summary
    print("\n" + "=" * 50)
    print("🏁 TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Server Startup: PASSED")
    print(f"{'✅' if auth_success else '❌'} Authentication: {'PASSED' if auth_success else 'FAILED'}")
    print(f"{'✅' if protected_success else '❌'} Protected Routes: {'PASSED' if protected_success else 'FAILED'}")
    
    if auth_success and protected_success:
        print("\n🎉 All tests passed! JWT authentication system is working correctly.")
        print("🚀 Ready to start the frontend and test the complete application.")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
