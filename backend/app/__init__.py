from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.httpexceptions import HTTPServiceUnavailable
from .models import DBSession, Base, init_db
from sqlalchemy import engine_from_config
import logging

logger = logging.getLogger('app')

def main(global_config, **settings):
    # Initialize the database with better error handling
    if not init_db(settings):
        logger.error("Failed to initialize the database. Application might not function correctly.")    # Configure the Pyramid application
    config = Configurator(settings=settings)
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)
    
    # Include transaction manager for proper database session handling
    # config.include('pyramid_tm')  # Temporarily disabled to fix timeout issue
    
    config.include('app.routes')
    
    # Scan views for route configuration including authentication
    config.scan('app.views')
    config.scan('app.auth')  # Scan only auth.py to avoid duplicate registrations
    
    logger.info("Pyramid application configured successfully and views scanned.")
    
    return config.make_wsgi_app()

def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With, Accept"
        })
    event.request.add_response_callback(cors_headers)
