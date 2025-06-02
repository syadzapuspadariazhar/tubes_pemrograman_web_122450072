#!/usr/bin/env python3
"""
Alternative server startup that creates a proper WSGI application
"""
import os
from pyramid.config import Configurator
from waitress import serve

def create_app():
    """Create and configure the Pyramid application"""
    # Set up basic settings
    settings = {
        'sqlalchemy.url': 'sqlite:///budget.db',
        'pyramid.reload_templates': 'true',
        'pyramid.debug_authorization': 'false',
        'pyramid.debug_notfound': 'false',
        'pyramid.debug_routematch': 'false',
        'pyramid.default_locale_name': 'en'
    }
    
    # Import main function and create app
    from app import main
    app = main({}, **settings)
    
    return app

def start_server():
    """Start the server"""
    print("🚀 Starting Budget Tracking Backend Server")
    print("📍 Server will be available at: http://localhost:6543")
    print("📋 API endpoints at: http://localhost:6543/api/")
    print("🔧 Press Ctrl+C to stop")
    print("=" * 60)
    
    try:
        app = create_app()
        print("✅ Application created successfully")
        serve(app, host='0.0.0.0', port=6543)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_server()
