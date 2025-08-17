# src/api/controllers/service_packages_controller.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from services.service_package_service import ServicePackageService
from infrastructure.repositories.service_package_repository import ServicePackageRepository
from api.schemas.service_package import (
    ServicePackageCreateSchema,
    ServicePackageUpdateSchema,
    ServicePackageResponseSchema,
)

bp = Blueprint("service_packages", __name__, url_prefix="/service-packages")

# Khởi tạo service và repository (in-memory / chưa nối DB thật)
service_package_service = ServicePackageService(ServicePackageRepository())

create_schema = ServicePackageCreateSchema()
update_schema = ServicePackageUpdateSchema()
response_schema = ServicePackageResponseSchema()


@bp.route("/", methods=["GET"])
def list_service_packages():
    """
    Lấy danh sách tất cả service packages
    GET /service-packages
    """
    items = service_package_service.list_packages()
    return jsonify(response_schema.dump(items, many=True)), 200


@bp.route("/<int:pkg_id>", methods=["GET"])
def get_service_package(pkg_id: int):
    """
    Lấy chi tiết 1 service package
    GET /service-packages/<id>
    """
    pkg = service_package_service.get_package(pkg_id)
    if not pkg:
        return jsonify({"message": "Service package not found"}), 404
    return jsonify(response_schema.dump(pkg)), 200


@bp.route("/", methods=["POST"])
def create_service_package():
    """
    Tạo service package mới
    POST /service-packages
    Body theo ServicePackageCreateSchema:
    {
      "name": "...",
      "description": "...",
      "price": 50000.0
    }
    """
    data = request.get_json() or {}
    try:
        payload = create_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    now = datetime.utcnow()
    pkg = service_package_service.create_package(
        name=payload["name"],
        description=payload.get("description"),
        price=payload["price"],
        created_at=now,
        updated_at=now,
    )
    return jsonify(response_schema.dump(pkg)), 201


@bp.route("/<int:pkg_id>", methods=["PUT"])
def update_service_package(pkg_id: int):
    """
    Cập nhật đầy đủ service package
    PUT /service-packages/<id>
    Body theo ServicePackageUpdateSchema
    """
    data = request.get_json() or {}
    try:
        payload = update_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    current = service_package_service.get_package(pkg_id)
    if not current:
        return jsonify({"message": "Service package not found"}), 404

    now = datetime.utcnow()
    pkg = service_package_service.update_package(
        package_id=pkg_id,
        name=payload.get("name", current.name),
        description=payload.get("description", getattr(current, "description", None)),
        price=payload.get("price", current.price),
        created_at=current.created_at,  # giữ nguyên created_at
        updated_at=now,
    )
    return jsonify(response_schema.dump(pkg)), 200


@bp.route("/<int:pkg_id>", methods=["DELETE"])
def delete_service_package(pkg_id: int):
    """
    Xoá service package
    DELETE /service-packages/<id>
    """
    ok = service_package_service.delete_package(pkg_id)
    if not ok:
        return jsonify({"message": "Service package not found"}), 404
    return "", 204
