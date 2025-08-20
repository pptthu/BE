from flask import jsonify

def ok(data=None, **kwargs):
    body = {"data": data}
    body.update(kwargs)
    return jsonify(body)

def err(message: str, code: str = "error", status: int = 400):
    return jsonify({"error": code, "message": message}), status
