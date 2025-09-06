<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> origin/main
from flask import Blueprint, request, g
from ..middleware import auth_required, roles_required
from ...services.manager_service import ManagerService
from ..responses import ok

bp = Blueprint("manager", __name__)

@bp.get("/manager/locations")
@auth_required
@roles_required("MANAGER", "ADMIN")
def list_locations():
    svc = ManagerService(g.db)
    return ok(svc.list_locations())

@bp.post("/manager/locations")
@auth_required
@roles_required("MANAGER", "ADMIN")
def create_location():
    data = request.get_json(silent=True) or {}
    svc = ManagerService(g.db)
    loc = svc.create_location(data.get("name"), data.get("address"))
    return ok(loc, 201)

@bp.put("/manager/locations/<int:loc_id>")
@auth_required
@roles_required("MANAGER", "ADMIN")
def update_location(loc_id: int):
    data = request.get_json(silent=True) or {}
    svc = ManagerService(g.db)
    loc = svc.update_location(loc_id, data.get("name"), data.get("address"))
    return ok(loc)

@bp.delete("/manager/locations/<int:loc_id>")
@auth_required
@roles_required("MANAGER", "ADMIN")
def delete_location(loc_id: int):
    svc = ManagerService(g.db)
    svc.delete_location(loc_id)
    return ok(True)

@bp.get("/manager/pods")
@auth_required
@roles_required("MANAGER", "ADMIN")
def list_pods_mng():
    svc = ManagerService(g.db)
    return ok(svc.list_pods())

@bp.post("/manager/pods")
@auth_required
@roles_required("MANAGER", "ADMIN")
def create_pod():
    data = request.get_json(silent=True) or {}
    svc = ManagerService(g.db)
    pod = svc.create_pod(
        name=data.get("name"),
        price=data.get("price"),
        location_id=data.get("location_id"),
        status=data.get("status", "AVAILABLE"),
    )
    return ok(pod, 201)

@bp.put("/manager/pods/<int:pod_id>")
@auth_required
@roles_required("MANAGER", "ADMIN")
def update_pod(pod_id: int):
    data = request.get_json(silent=True) or {}
    svc = ManagerService(g.db)
    pod = svc.update_pod(
        pod_id,
        name=data.get("name"),
        price=data.get("price"),
        location_id=data.get("location_id"),
        status=data.get("status"),
    )
    return ok(pod)

@bp.delete("/manager/pods/<int:pod_id>")
@auth_required
@roles_required("MANAGER", "ADMIN")
def delete_pod(pod_id: int):
    svc = ManagerService(g.db)
    svc.delete_pod(pod_id)
    return ok(True)
<<<<<<< HEAD
=======
=======
from flask import Blueprint, request, jsonify
from services.location_service import LocationService
from services.pod_service import PodService
from schemas.location_schema import LocationRequestSchema, LocationResponseSchema
from schemas.pod_schema import PodRequestSchema, PodResponseSchema

manager_bp = Blueprint("manager", __name__, url_prefix="/manager")

location_service = LocationService()
pod_service = PodService()

location_request_schema = LocationRequestSchema()
location_response_schema = LocationResponseSchema()
pod_request_schema = PodRequestSchema()
pod_response_schema = PodResponseSchema()

@manager_bp.route("/locations", methods=["GET"])
def list_locations():
    locations = location_service.list_locations()
    return jsonify(location_response_schema.dump(locations, many=True))

@manager_bp.route("/locations", methods=["POST"])
def create_location():
    data = location_request_schema.load(request.json)
    location = location_service.create_location(data)
    return jsonify(location_response_schema.dump(location)), 201

@manager_bp.route("/locations/<int:location_id>", methods=["PUT"])
def update_location(location_id):
    data = location_request_schema.load(request.json)
    location = location_service.update_location(location_id, data)
    if not location:
        return jsonify({"error": "Location not found"}), 404
    return jsonify(location_response_schema.dump(location))

@manager_bp.route("/locations/<int:location_id>", methods=["DELETE"])
def delete_location(location_id):
    location_service.delete_location(location_id)
    return jsonify({"message": "Location deleted"}), 200

@manager_bp.route("/pods", methods=["GET"])
def list_pods():
    pods = pod_service.list_pods()
    return jsonify(pod_response_schema.dump(pods, many=True))

@manager_bp.route("/pods", methods=["POST"])
def create_pod():
    data = pod_request_schema.load(request.json)
    pod = pod_service.create_pod(data)
    return jsonify(pod_response_schema.dump(pod)), 201

@manager_bp.route("/pods/<int:pod_id>", methods=["PUT"])
def update_pod(pod_id):
    data = pod_request_schema.load(request.json)
    pod = pod_service.update_pod(pod_id, data)
    if not pod:
        return jsonify({"error": "Pod not found"}), 404
    return jsonify(pod_response_schema.dump(pod))

@manager_bp.route("/pods/<int:pod_id>", methods=["DELETE"])
def delete_pod(pod_id):
    pod_service.delete_pod(pod_id)
    return jsonify({"message": "Pod deleted"}), 200
>>>>>>> origin/main
>>>>>>> origin/main
