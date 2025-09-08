import os
from flask import Flask, g
from .config import load_config
from .app_logging import setup_logging
from .cors import setup_cors
from .error_handler import register_error_handlers
from .infrastructure.databases.mssql import init_mssql, get_session
from .api.routes import register_routes

def create_app():
    setup_logging("INFO")
    app = Flask(__name__, static_folder=os.path.join(os.getcwd(), "static"))
    cfg = load_config()
    app.config.update(cfg)

    setup_cors(app)
    init_mssql(app)
    register_error_handlers(app)

    @app.before_request
    def _before():
        g.db = get_session()

    @app.teardown_request
    def _teardown(exc):
        db = getattr(g, "db", None)
        if db is not None:
            if exc:
                db.rollback()
            db.close()

    register_routes(app)
    return app
