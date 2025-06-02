#!/usr/bin/env python3
"""
Simple server startup script that properly initializes the Pyramid app
"""
from pyramid.paster import get_app
from waitress import serve
import os

def start_server():
    """Start the server using the development.ini configuration"""
    print("Starting budget tracking backend server...")
    
    # Get the app using Pyramid's configuration
    app = get_app('development.ini')
    
    print("✅ Application loaded successfully")
    print("🚀 Starting server on http://localhost:6543")
    print("📋 API endpoints available at http://localhost:6543/api/")
    print("🔧 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the server
    serve(app, host='0.0.0.0', port=6543)

if __name__ == "__main__":
    start_server()
