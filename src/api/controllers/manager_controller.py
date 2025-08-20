from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.infrastructure.databases.extensions import db
from src.api.middleware import roles_required
from src.infrastructure.models.location_model import Location
from src.infrastructure.models.pod_model import POD

bp = Blueprint("manager", __name__)

@bp.get("/manager/locations")
@jwt_required()
@roles_required("manager", "admin")
def list_locations():
    items = Location.query.order_by(Location.id.asc()).all()
    return jsonify([{"id": i.id, "name": i.name, "address": i.address} for i in items])

@bp.post("/manager/locations")
@jwt_required()
@roles_required("manager", "admin")
def create_location():
    data = request.get_json() or {}
    loc = Location(name=data.get("name"), address=data.get("address"))
    db.session.add(loc); db.session.commit()
    return jsonify({"id": loc.id}), 201

@bp.put("/manager/locations/<int:loc_id>")
@jwt_required()
@roles_required("manager", "admin")
def update_location(loc_id):
    loc = Location.query.get_or_404(loc_id)
    data = request.get_json() or {}
    loc.name = data.get("name", loc.name)
    loc.address = data.get("address", loc.address)
    db.session.commit()
    return jsonify({"id": loc.id})

@bp.delete("/manager/locations/<int:loc_id>")
@jwt_required()
@roles_required("manager", "admin")
def delete_location(loc_id):
    loc = Location.query.get_or_404(loc_id)
    db.session.delete(loc); db.session.commit()
    return jsonify({"deleted": True})

@bp.get("/manager/pods")
@jwt_required()
@roles_required("manager", "admin")
def list_pods():
    items = POD.query.order_by(POD.id.asc()).all()
    return jsonify([{
        "id": p.id, "name": p.name, "price": float(p.price),
        "status": p.status, "location_id": p.location_id
    } for p in items])

@bp.post("/manager/pods")
@jwt_required()
@roles_required("manager", "admin")
def create_pod():
    data = request.get_json() or {}
    pod = POD(
        name=data.get("name"),
        price=data.get("price"),
        status=data.get("status", "active"),
        location_id=data.get("location_id"),
    )
    db.session.add(pod); db.session.commit()
    return jsonify({"id": pod.id}), 201

@bp.put("/manager/pods/<int:pod_id>")
@jwt_required()
@roles_required("manager", "admin")
def update_pod(pod_id):
    pod = POD.query.get_or_404(pod_id)
    data = request.get_json() or {}
    pod.name = data.get("name", pod.name)
    if "price" in data: pod.price = data["price"]
    pod.status = data.get("status", pod.status)
    if "location_id" in data: pod.location_id = data["location_id"]
    db.session.commit()
    return jsonify({"id": pod.id})

@bp.delete("/manager/pods/<int:pod_id>")
@jwt_required()
@roles_required("manager", "admin")
def delete_pod(pod_id):
    pod = POD.query.get_or_404(pod_id)
    db.session.delete(pod); db.session.commit()
    return jsonify({"deleted": True})
