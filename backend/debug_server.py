import logging
import sys
from app import main
from waitress import serve

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def start_server():
    try:
        logger.info("Starting Pyramid server...")
        
        # Settings from development.ini
        settings = {
            'sqlalchemy.url': 'sqlite:///budget.db',
            'pyramid.reload_templates': 'true',
            'pyramid.debug_authorization': 'false',
            'pyramid.debug_notfound': 'false',
            'pyramid.debug_routematch': 'false',
        }
        
        logger.info("Creating WSGI application...")
        app = main({}, **settings)
        
        logger.info("Server starting on http://localhost:6543")
        logger.info("Category endpoints should be available at /api/categories")
        
        # Start the server
        serve(app, host='0.0.0.0', port=6543)
        
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    start_server()
