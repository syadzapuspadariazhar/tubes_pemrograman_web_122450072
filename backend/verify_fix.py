#!/usr/bin/env python3
"""
Test script to verify category routes are working
"""
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_routes_registration():
    """Test if category routes are properly registered"""
    print("Testing route registration...")
    
    try:
        from pyramid.config import Configurator
        from app.routes import includeme as include_routes
        from app import views
        
        # Create a test configurator
        config = Configurator()
        
        # Include routes
        include_routes(config)
        
        # Scan views
        config.scan('app.views')
        
        # Get the route mapper
        mapper = config.get_routes_mapper()
        
        # Check if category routes exist
        route_names = [route.name for route in mapper.get_routes()]
        
        expected_routes = ['get_categories', 'add_category', 'update_category', 'delete_category']
        
        print(f"Found routes: {route_names}")
        
        missing_routes = [route for route in expected_routes if route not in route_names]
        
        if missing_routes:
            print(f"❌ Missing routes: {missing_routes}")
            return False
        else:
            print("✅ All category routes are registered!")
            
            # Test specific route
            route = mapper.get_route('add_category')
            if route:
                print(f"✅ add_category route found: {route.pattern}")
                print(f"   Path: {route.path}")
                return True
            else:
                print("❌ add_category route not found")
                return False
                
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_view_functions():
    """Test if view functions are properly decorated"""
    print("\nTesting view functions...")
    
    try:
        from app.views import category_api
        
        # Check if functions exist
        functions = ['get_categories', 'add_category', 'update_category', 'delete_category']
        
        for func_name in functions:
            if hasattr(category_api, func_name):
                func = getattr(category_api, func_name)
                # Check if function has view_config decoration
                if hasattr(func, '__wrapped__'):
                    print(f"✅ {func_name} is properly decorated")
                else:
                    print(f"⚠️  {func_name} might not be properly decorated")
            else:
                print(f"❌ {func_name} function not found")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Error testing view functions: {e}")
        return False

def test_imports():
    """Test if all imports work correctly"""
    print("\nTesting imports...")
    
    try:
        from app.models import DBSession, Category
        print("✅ Models imported successfully")
        
        from app.views import category_api
        print("✅ Category API imported successfully")
        
        from app import main
        print("✅ Main app function imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=== Category Routes Verification Test ===\n")
    
    # Run tests
    imports_ok = test_imports()
    views_ok = test_view_functions()
    routes_ok = test_routes_registration()
    
    print(f"\n=== Test Results ===")
    print(f"Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    print(f"View Functions: {'✅ PASS' if views_ok else '❌ FAIL'}")
    print(f"Route Registration: {'✅ PASS' if routes_ok else '❌ FAIL'}")
    
    if imports_ok and views_ok and routes_ok:
        print(f"\n🎉 ALL TESTS PASSED! Category routes should be working.")
        print(f"The POST /api/categories endpoint should now be available.")
    else:
        print(f"\n❌ Some tests failed. Check the output above for details.")
