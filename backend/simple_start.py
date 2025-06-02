#!/usr/bin/env python3
"""
Simple server startup test
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("=== Starting Server Test ===")

try:
    print("Step 1: Testing imports...")
    from app import main
    print("✅ App main imported")
    
    print("Step 2: Creating app with SQLite...")
    settings = {
        'sqlalchemy.url': 'sqlite:///budget.db'
    }
    
    app = main({}, **settings)
    print("✅ WSGI app created")
    
    print("Step 3: Starting server...")
    from waitress import serve
    print("🚀 Starting server at http://localhost:6543")
    print("📡 Category API at http://localhost:6543/api/categories")
    print("Press Ctrl+C to stop")
    
    # This will block and run the server
    serve(app, host='localhost', port=6543)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
