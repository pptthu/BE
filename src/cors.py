from flask_cors import CORS

def init_cors(app):
    CORS(app, resources={r"/*": {"origins": app.config.get("CORS_ORIGINS")}})
