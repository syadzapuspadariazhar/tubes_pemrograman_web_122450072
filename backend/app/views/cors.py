from pyramid.view import view_config
from pyramid.response import Response

@view_config(route_name='cors_preflight')
def cors_preflight_handler(request):
    """Global fallback CORS handler for all OPTIONS requests"""
    response = Response(status=200)
    response.headers.update({
        "Access-Control-Allow-Origin": "http://localhost:3000",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With, Accept",
        "Access-Control-Max-Age": "86400",
        "Content-Length": "0"
    })
    return response
