#!/usr/bin/env python3
"""
Test script to start server and verify endpoints
"""
import os
import sys
import time
import threading
import requests
from waitress import serve

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def start_server():
    """Start the Pyramid server"""
    try:
        from app import main
        
        settings = {
            'sqlalchemy.url': 'sqlite:///budget.db',
            'pyramid.reload_templates': 'true',
            'pyramid.debug_authorization': 'false',
            'pyramid.debug_notfound': 'false',
            'pyramid.debug_routematch': 'false',
        }
        
        print("Creating WSGI application...")
        app = main({}, **settings)
        
        print("Starting server on http://localhost:6543...")
        serve(app, host='0.0.0.0', port=6543)
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        import traceback
        traceback.print_exc()

def test_endpoints():
    """Test the endpoints after server starts"""
    print("Waiting for server to start...")
    time.sleep(3)
    
    base_url = "http://localhost:6543"
    
    # Test GET categories
    try:
        response = requests.get(f"{base_url}/api/categories", timeout=10)
        print(f"✅ GET /api/categories: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ GET /api/categories failed: {e}")
    
    # Test POST categories
    try:
        data = {"nama": "Test Category"}
        response = requests.post(
            f"{base_url}/api/categories", 
            json=data, 
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"✅ POST /api/categories: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ POST /api/categories failed: {e}")

if __name__ == '__main__':
    # Start testing in a separate thread
    test_thread = threading.Thread(target=test_endpoints, daemon=True)
    test_thread.start()
    
    # Start server (this blocks)
    start_server()
