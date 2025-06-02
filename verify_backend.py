#!/usr/bin/env python3
"""
Quick verification script to check if the authentication system is working
"""
import requests
import time

def check_server():
    """Check if server is running"""
    try:
        response = requests.get('http://localhost:6543/api/categories', timeout=5)
        print(f"✅ Server is running! Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running on port 6543")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

def test_authentication():
    """Test the authentication endpoints"""
    print("\n🔐 Testing Authentication...")
    
    # Test login
    login_data = {"username": "admin", "password": "admin123"}
    try:
        response = requests.post('http://localhost:6543/api/auth/login', 
                               json=login_data, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print(f"✅ Login successful! Token: {token[:20]}...")
            
            # Test token verification
            headers = {"Authorization": f"Bearer {token}"}
            verify_response = requests.get('http://localhost:6543/api/auth/verify', 
                                         headers=headers, timeout=5)
            
            if verify_response.status_code == 200:
                print("✅ Token verification successful!")
                return True
            else:
                print(f"❌ Token verification failed: {verify_response.status_code}")
                return False
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Quick Backend Verification\n")
    
    # Check if server is running
    server_ok = check_server()
    
    if server_ok:
        # Test authentication
        auth_ok = test_authentication()
        
        print("\n" + "="*40)
        print("📊 VERIFICATION RESULTS:")
        print(f"Server Status: {'✅ RUNNING' if server_ok else '❌ DOWN'}")
        print(f"Authentication: {'✅ WORKING' if auth_ok else '❌ FAILED'}")
        
        if server_ok and auth_ok:
            print("\n🎉 Backend is ready for use!")
            print("📝 Next steps:")
            print("   1. Start frontend: cd frontend && npm start")
            print("   2. Open browser: http://localhost:3000")
            print("   3. Login with: admin / admin123")
        else:
            print("\n⚠️  Backend has issues - check server logs")
    else:
        print("\n❌ Server is not running. Start it with:")
        print("   cd backend && .\\env\\Scripts\\activate && python start_server_fixed.py")
