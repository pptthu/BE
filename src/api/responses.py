from flask import jsonify
def ok(data=None, status=200): return jsonify({"ok": True, "data": data}), status
def fail(message="Bad Request", status=400): return jsonify({"ok": False, "error": message}), status
