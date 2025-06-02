#!/usr/bin/env python3
"""
Simple server start script to test our fixes
"""
import sys
import os
from waitress import serve

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import main
    print("App imported successfully")
    
    # Create the WSGI application
    settings = {
        'sqlalchemy.url': 'sqlite:///budget.db',
        'pyramid.reload_templates': 'true',
        'pyramid.debug_authorization': 'false',
        'pyramid.debug_notfound': 'false',
        'pyramid.debug_routematch': 'false',
        'pyramid.default_locale_name': 'en',
        'tm.attempts': '3'
    }
    
    app = main({}, **settings)
    print("WSGI app created successfully")
    
    # Start the server
    print("Starting server on http://localhost:6543")
    serve(app, host='0.0.0.0', port=6543)
    
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
