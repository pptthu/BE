# app.py
from flask import Flask, jsonify
from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint

from api.swagger import spec
from api.middleware import middleware
from infrastructure.databases import init_db

# ==== Import tất cả controllers (mỗi file phải có biến bp) ====
from api.controllers.auth_controller import bp as auth_bp
from api.controllers.bookings_controller import bp as bookings_bp
from api.controllers.customer_controller import bp as customers_bp
from api.controllers.locations_controller import bp as locations_bp
from api.controllers.me_controller import bp as me_bp
from api.controllers.pod_contronller import bp as pods_bp
from api.controllers.service_packages_controller import bp as service_packages_bp
from api.controllers.staffs_controller import bp as staff_bp
from api.controllers.user_controller import bp as users_bp


def create_app():
    app = Flask(__name__)
    Swagger(app)

    # ==== Đăng ký tất cả Blueprints ====
    app.register_blueprint(auth_bp)               
    app.register_blueprint(me_bp)                
    app.register_blueprint(bookings_bp)          
    app.register_blueprint(locations_bp)      
    app.register_blueprint(pods_bp)             
    app.register_blueprint(service_packages_bp)  
    app.register_blueprint(staff_bp)             
    app.register_blueprint(customers_bp)        
    app.register_blueprint(users_bp)             

    # ==== Swagger UI (/docs) ====
    SWAGGER_URL = "/docs"
    API_URL = "/swagger.json"
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Booking API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # ==== DB + Middleware ====
    init_db(app)
    middleware(app)

    # ==== Tự động add MỌI route vào OpenAPI spec ====
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint == "static":
                continue
            view_func = app.view_functions.get(rule.endpoint)
            if not view_func:
                continue
            try:
                spec.path(view=view_func)
            except Exception:
                # Route không có doc swagger block thì bỏ qua, không ảnh hưởng chạy
                pass

    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(spec.to_dict())

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=6868, debug=True)
