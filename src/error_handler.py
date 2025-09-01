from flask import Blueprint, jsonify


errors = Blueprint("errors", __name__)


@errors.app_errorhandler(Exception)
def handle_error(e):
return jsonify({"error": str(e)}), 500