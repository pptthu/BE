from flask import Flask
from flask_cors import CORS

def register_middleware(app: Flask):
    # CORS for local dev; tighten in production
    CORS(app, resources={r"/*": {"origins": "*"}})
    return app
