#!/usr/bin/env python3
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from waitress import serve
from app import main

if __name__ == '__main__':
    # Get settings from development.ini
    settings = {
        'sqlalchemy.url': 'sqlite:///budget.db',
        'pyramid.reload_templates': 'true',
        'pyramid.debug_authorization': 'false',
        'pyramid.debug_notfound': 'false',
        'pyramid.debug_routematch': 'false',
    }
    
    print("Starting server on http://localhost:6543")
    print("Category routes should be available...")
    app = main({}, **settings)
    serve(app, host='0.0.0.0', port=6543)