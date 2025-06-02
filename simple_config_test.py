#!/usr/bin/env python3
"""
Simple test to verify ConfigurationConflictError is fixed
"""
import os
import sys

# Add backend directory to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

print("=== Testing Configuration Fix ===")

try:
    print("Step 1: Testing app imports...")
    from app import main
    print("✅ App main imported")
    
    print("Step 2: Creating WSGI app...")
    settings = {
        'sqlalchemy.url': 'sqlite:///backend/budget.db'
    }
    
    app = main({}, **settings)
    print("✅ WSGI app created successfully")
    print("✅ No ConfigurationConflictError detected!")
    print("")
    print("🎉 SUCCESS: The duplicate view registration issue has been FIXED!")
    print("🚀 The server can now start without conflicts.")
    print("")
    print("Next steps:")
    print("1. Start the backend server: cd backend && python simple_start.py")
    print("2. Start the frontend: npm start (in frontend directory)")
    print("3. Test the complete authentication flow")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
print("\n=== Test Complete ===")
