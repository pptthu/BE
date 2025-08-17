from flask import Flask
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from src.config import Config
from src.app_logging import setup_logging
from src.api.middleware import register_middleware
from src.api.routes import register_routes
from src.infrastructure.databases import init_db

def create_app():
    logger = setup_logging()
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Dùng config/template mới
    Swagger(app, config=Config.SWAGGER_CONFIG, template=Config.SWAGGER_TEMPLATE)

    JWTManager(app)
    init_db()
    register_middleware(app)
    register_routes(app)

    @app.get("/")
    def root():
        return {"name": "POD Booking System API", "version": "1.0.0"}

    logger.info("App initialized")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
