def get_error_response(**kwargs):
    return {
        'message': kwargs.get('message') or 'Something went wrong',
        'error_code': kwargs.get('error_code') or 0,
        'error': kwargs.get('error') or ''
    }
