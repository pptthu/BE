# src/api/controllers/location_controller.py
from flask import Blueprint, request, jsonify
from datetime import datetime

from services.location_service import LocationService
from infrastructure.repositories.location_repository import LocationRepository
from api.schemas.location import LocationRequestSchema, LocationResponseSchema

bp = Blueprint('locations', __name__, url_prefix='/locations')

# Khởi tạo service và repository (memory / giả lập)
location_service = LocationService(LocationRepository())

request_schema = LocationRequestSchema()
response_schema = LocationResponseSchema()


#  CÁC CHỨC NĂNG (API ENDPOINTS) 

@bp.route('/', methods=['GET'])
def list_locations():
    """
    Lấy danh sách tất cả Location (READ ALL)
    - GET /locations/
    - Trả về list tất cả các location hiện có
    """
    locations = location_service.list_locations()
    return jsonify(response_schema.dump(locations, many=True)), 200


@bp.route('/<int:location_id>', methods=['GET'])
def get_location(location_id):
    """
    Lấy chi tiết 1 Location theo ID (READ ONE)
    - GET /locations/<id>
    - Trả về thông tin location nếu có, 404 nếu không tìm thấy
    """
    location = location_service.get_location(location_id)
    if not location:
        return jsonify({'message': 'Location not found'}), 404
    return jsonify(response_schema.dump(location)), 200


@bp.route('/', methods=['POST'])
def create_location():
    """
     Tạo mới Location (CREATE)
    - POST /locations/
    - Nhận dữ liệu JSON (name, address, ...)
    - Validate schema trước khi thêm
    - Trả về Location mới tạo
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    now = datetime.utcnow()
    location = location_service.create_location(
        name=data['name'],
        address=data['address'],
        created_at=now,
        updated_at=now
    )
    return jsonify(response_schema.dump(location)), 201


@bp.route('/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    """
    Cập nhật Location (UPDATE)
    - PUT /locations/<id>
    - Nhận dữ liệu JSON (name, address, ...)
    - Validate schema trước khi update
    - Trả về Location đã cập nhật
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    location = location_service.update_location(
        location_id=location_id,
        name=data['name'],
        address=data['address'],
        created_at=datetime.utcnow(),   # theo khung Todo
        updated_at=datetime.utcnow()
    )
    return jsonify(response_schema.dump(location)), 200


@bp.route('/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    """
    Xoá Location (DELETE)
    - DELETE /locations/<id>
    - Xoá location theo ID
    - Trả về HTTP 204 (No Content) nếu thành công
    """
    location_service.delete_location(location_id)
    return '', 204
