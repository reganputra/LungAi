from flask import jsonify


def success_response(data=None, message=None):
    """Create standardized success response"""
    response = {'status': 'success'}
    if message:
        response['message'] = message
    if data:
        response.update(data)
    return jsonify(response)


def error_response(message, status_code=400):
    """Create standardized error response"""
    return jsonify({
        'status': 'error',
        'message': message
    }), status_code
