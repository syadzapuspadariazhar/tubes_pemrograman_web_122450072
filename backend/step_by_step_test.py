import os
import sys

# Ensure we're in the right directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
sys.path.insert(0, script_dir)

print(f"Working directory: {os.getcwd()}")
print(f"Python path includes: {script_dir}")

# Test step by step
try:
    print("\n1. Testing basic imports...")
    from pyramid.config import Configurator
    print("   ✅ Pyramid imported")
    
    from sqlalchemy import create_engine
    print("   ✅ SQLAlchemy imported")
    
    print("\n2. Testing app imports...")
    from app import main
    print("   ✅ App main imported")
    
    from app.models import DBSession, Category
    print("   ✅ Models imported")
    
    print("\n3. Testing database connection...")
    engine = create_engine('sqlite:///budget.db', echo=True)
    print(f"   ✅ Database engine created: {engine}")
    
    print("\n4. Creating app...")
    settings = {'sqlalchemy.url': 'sqlite:///budget.db'}
    app = main({}, **settings)
    print("   ✅ WSGI app created successfully")
    
    print("\n5. Testing manual HTTP server...")
    from wsgiref.simple_server import make_server
    
    print("   Starting HTTP server on localhost:6543...")
    server = make_server('localhost', 6543, app)
    print("   ✅ Server created successfully")
    print("   🌐 Server available at http://localhost:6543")
    print("   📡 Category API at /api/categories")
    print("   Press Ctrl+C to stop...")
    
    server.serve_forever()
    
except KeyboardInterrupt:
    print("\n   Server stopped by user")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")
