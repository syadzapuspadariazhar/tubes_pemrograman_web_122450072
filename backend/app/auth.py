import datetime
import json
import jwt
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPUnauthorized, HTTPBadRequest

# Simple in-memory user storage (in production, use a proper database)
USERS = {
    'admin': {
        'password': 'admin123',
        'name': 'Administrator',
        'email': 'admin@budget.app'
    },
    'demo': {
        'password': 'demo123',
        'name': 'Demo User',
        'email': 'demo@budget.app'
    }
}
JWT_SECRET = 'your-secret-key-budget-app-2024'

@view_config(route_name='login', renderer='json')
def login_view(request):
    """Handle user login"""
    try:
        # Parse request body
        if hasattr(request, 'json_body'):
            data = request.json_body
        else:
            data = json.loads(request.body.decode('utf-8'))

        username = data.get('username', '').strip()
        password = data.get('password', '').strip()

        if not username or not password:
            return HTTPBadRequest(json_body={
                'error': 'Username dan password harus diisi'
            })

        # Check user credentials
        user = USERS.get(username)
        if not user or user['password'] != password:
            return HTTPUnauthorized(json_body={
                'error': 'Username atau password salah'
            })

        # Create JWT token
        payload = {
            'username': username,
            'name': user['name'],
            'email': user['email'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

        return {
            'token': token,
            'user': {
                'username': username,
                'name': user['name'],
                'email': user['email']
            }
        }

    except Exception as e:
        print(f"Login error: {e}")
        return HTTPBadRequest(json_body={
            'error': 'Terjadi kesalahan saat login'
        })

@view_config(route_name='verify_token', renderer='json')
def verify_token_view(request):
    """Verify JWT token"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return HTTPUnauthorized(json_body={
                'valid': False,
                'error': 'Token tidak ditemukan'
            })

        token = auth_header.split(' ')[1]

        # Verify token
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            return {
                'valid': True,
                'user': {
                    'username': payload['username'],
                    'name': payload['name'],
                    'email': payload['email']
                }
            }
        except jwt.ExpiredSignatureError:
            return HTTPUnauthorized(json_body={
                'valid': False,
                'error': 'Token sudah kadaluarsa'
            })
        except jwt.InvalidTokenError:
            return HTTPUnauthorized(json_body={
                'valid': False,
                'error': 'Token tidak valid'
            })

    except Exception as e:
        print(f"Token verification error: {e}")
        return HTTPUnauthorized(json_body={
            'valid': False,
            'error': 'Terjadi kesalahan saat verifikasi token'
        })