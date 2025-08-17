from flask import jsonify

def success_response(data=None, message="OK", status=200):
    return jsonify({"status": "success", "message": message, "data": data}), status

def error_response(message="Error", status=400, errors=None):
    return jsonify({"status": "error", "message": message, "errors": errors or []}), status
