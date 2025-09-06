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
