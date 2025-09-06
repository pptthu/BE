<<<<<<< HEAD
from flask import jsonify
from .domain.exceptions import AppError

def register_error_handlers(app):
    @app.errorhandler(AppError)
    def _app_error(e: AppError):
        return jsonify({"ok": False, "error": str(e)}), getattr(e, "status_code", 400)

    @app.errorhandler(404)
    def _404(e):
        return jsonify({"ok": False, "error": "Not found"}), 404

    @app.errorhandler(Exception)
    def _500(e):
        return jsonify({"ok": False, "error": str(e)}), 500
=======
from flask import jsonify
from .domain.exceptions import AppError

def register_error_handlers(app):
    @app.errorhandler(AppError)
    def _app_error(e: AppError):
        return jsonify({"ok": False, "error": str(e)}), getattr(e, "status_code", 400)

    @app.errorhandler(404)
    def _404(e):
        return jsonify({"ok": False, "error": "Not found"}), 404

    @app.errorhandler(Exception)
    def _500(e):
        return jsonify({"ok": False, "error": str(e)}), 500
>>>>>>> origin/main
