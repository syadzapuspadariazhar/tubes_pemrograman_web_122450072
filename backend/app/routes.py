def includeme(config):
    # Authentication Routes
    config.add_route('login', '/api/auth/login', request_method='POST')
    config.add_route('verify_token', '/api/auth/verify', request_method='GET')

    # Category Routes with specific HTTP methods
    config.add_route('get_categories', '/api/categories', request_method='GET')
    config.add_route('add_category', '/api/categories', request_method='POST')
    config.add_route('update_category', '/api/categories/{id}', request_method='PUT')
    config.add_route('delete_category', '/api/categories/{id}', request_method='DELETE')

    # Transaction Routes with specific HTTP methods
    config.add_route('get_transactions', '/api/transactions', request_method='GET')
    config.add_route('add_transaction', '/api/transactions', request_method='POST')
    config.add_route('update_transaction', '/api/transactions/{id}', request_method='PUT')
    config.add_route('delete_transaction', '/api/transactions/{id}', request_method='DELETE')

    # CORS preflight fallback - only for OPTIONS requests to unmatched paths
    config.add_route('cors_preflight', '/{path:.*}', request_method='OPTIONS')