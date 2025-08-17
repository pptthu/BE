# src/api/controllers/pod_controller.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from marshmallow import ValidationError

from services.pod_service import PodService
from infrastructure.repositories.pod_repository import PodRepository
from api.schemas.pod import PodCreateRequestSchema, PodUpdateRequestSchema, PodResponseSchema

bp = Blueprint('pods', __name__, url_prefix='/pods')

pod_service = PodService(PodRepository())

create_schema = PodCreateRequestSchema()
update_schema = PodUpdateRequestSchema()
response_schema = PodResponseSchema()


@bp.route('/', methods=['GET'])
def list_pods():
    pods = pod_service.list_pods()
    return jsonify(response_schema.dump(pods, many=True)), 200


@bp.route('/<int:pod_id>', methods=['GET'])
def get_pod(pod_id):
    pod = pod_service.get_pod(pod_id)
    if not pod:
        return jsonify({'message': 'Pod not found'}), 404
    return jsonify(response_schema.dump(pod)), 200


@bp.route('/', methods=['POST'])
def create_pod():
    data = request.get_json() or {}
    try:
        payload = create_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    now = datetime.utcnow()
    pod = pod_service.create_pod(
        name=payload['name'],
        location_id=payload['location_id'],
        price=payload['price'],
        status=payload['status'],
        created_at=now,
        updated_at=now
    )
    return jsonify(response_schema.dump(pod)), 201


@bp.route('/<int:pod_id>', methods=['PUT'])
def update_pod(pod_id):
    data = request.get_json() or {}
    try:
        payload = update_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    current = pod_service.get_pod(pod_id)
    if not current:
        return jsonify({'message': 'Pod not found'}), 404

    now = datetime.utcnow()
    pod = pod_service.update_pod(
        pod_id=pod_id,
        name=payload.get('name', current.name),
        location_id=payload.get('location_id', current.location_id),
        price=payload.get('price', current.price),
        status=payload.get('status', current.status),
        created_at=current.created_at,   # giữ nguyên created_at
        updated_at=now
    )
    return jsonify(response_schema.dump(pod)), 200


@bp.route('/<int:pod_id>', methods=['DELETE'])
def delete_pod(pod_id):
    pod_service.delete_pod(pod_id)
    return '', 204
