from flask import Blueprint, jsonify
from src.infrastructure.databases import get_session
from src.infrastructure.models.location_model import LocationModel
from src.api.schemas.location_schema import LocationSchema
from src.services.location_service import LocationService

bp = Blueprint("locations", __name__, url_prefix="/locations")
schema = LocationSchema()

@bp.get("/")
def get_locations():
    session = get_session()()
    rows = session.query(LocationModel).all()
    return jsonify(schema.dump(rows, many=True)), 200

@bp.get("/<int:location_id>")
def get_location(location_id: int):
    session = get_session()()
    row = session.get(LocationModel, location_id)
    if not row:
        return jsonify({"message": "Not found"}), 404
    return jsonify(schema.dump(row)), 200
