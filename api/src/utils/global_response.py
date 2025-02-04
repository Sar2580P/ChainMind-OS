from flask import  jsonify

def success_response(data , message):
    return jsonify({
        'data': data,
        'message': message,
        'status_code': 200
    })

def error_response(message, status_code):
    return jsonify({
        'message': message,
        'status_code': status_code
    })

def not_found_response(path):
    return jsonify({
        'message': 'Not Found: ' + path,
        'status_code': 404
    })

def bad_request_response():
    return jsonify({
        'message': 'Bad Request',
        'status_code': 400
    })

def unauthorized_response():
    return jsonify({
        'message': 'Unauthorized',
        'status_code': 401
    })

def internal_server_error_response(message):
    return jsonify({
        'message': 'Internal Server Error' + message,
        'status_code': 500
    })