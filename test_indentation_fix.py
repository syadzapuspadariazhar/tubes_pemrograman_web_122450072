#!/usr/bin/env python3
"""
Quick test to verify indentation fix
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=== Testing Indentation Fix ===")
print("Attempting to import app module...")

try:
    from app import main
    print("✅ SUCCESS: app.main imported without IndentationError")
    
    # Test creating WSGI app
    print("Testing WSGI app creation...")
    settings = {'sqlalchemy.url': 'sqlite:///backend/budget.db'}
    app = main({}, **settings)
    print("✅ SUCCESS: WSGI app created successfully")
    print("🎉 INDENTATION ERROR FIXED!")
    
except IndentationError as e:
    print(f"❌ IndentationError still exists: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()

print("=== Test Complete ===")
input("Press Enter to continue...")
