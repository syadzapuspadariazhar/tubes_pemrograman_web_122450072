import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

print("=== Manual Debug Session ===")

try:
    print("1. Testing imports...")
    from app import main
    print("   ✅ Main app imported")
    
    from app.models import DBSession, Category
    print("   ✅ Models imported")
    
    from app.views import category_api
    print("   ✅ Category API imported")
    
    print("\n2. Testing app creation...")
    settings = {
        'sqlalchemy.url': 'sqlite:///budget.db',
        'pyramid.reload_templates': 'true',
        'pyramid.debug_authorization': 'false',
        'pyramid.debug_notfound': 'false',
        'pyramid.debug_routematch': 'false',
    }
    
    app = main({}, **settings)
    print("   ✅ WSGI app created successfully")
    
    print("\n3. Testing route registration...")
    from pyramid.config import Configurator
    config = Configurator(settings=settings)
    config.include('app.routes')
    config.scan('app.views')
    
    mapper = config.get_routes_mapper()
    routes = [(route.name, route.pattern, route.path) for route in mapper.get_routes()]
    
    print("   Registered routes:")
    for name, pattern, path in routes:
        if 'categor' in name.lower():
            print(f"   ✅ {name}: {pattern} -> {path}")
    
    print("\n4. Testing manual server start...")
    from waitress import serve
    print("   Starting server on port 6543...")
    print("   🌐 Server should be accessible at http://localhost:6543")
    print("   📡 Category endpoints at /api/categories")
    print("   Press Ctrl+C to stop server")
    
    serve(app, host='localhost', port=6543)
    
except KeyboardInterrupt:
    print("\n   Server stopped by user")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
