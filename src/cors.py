from flask_cors import CORS
def setup_cors(app):
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)
