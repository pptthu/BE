from flask import Blueprint, request, jsonify
from src.infrastructure.databases import get_session
from src.infrastructure.models.todo_model import TodoModel
from src.api.schemas.todo import TodoRequestSchema, TodoResponseSchema

bp = Blueprint("todo", __name__, url_prefix="/todos")
request_schema = TodoRequestSchema()
response_schema = TodoResponseSchema()

@bp.get("/")
def list_todos():
    session = get_session()()
    todos = session.query(TodoModel).all()
    return jsonify(response_schema.dump(todos, many=True)), 200

@bp.get("/<int:todo_id>")
def get_todo(todo_id):
    session = get_session()()
    todo = session.get(TodoModel, todo_id)
    if not todo:
        return jsonify({"message": "Not found"}), 404
    return jsonify(response_schema.dump(todo)), 200

@bp.post("/")
def create_todo():
    payload = request_schema.load(request.json or {})
    session = get_session()()
    todo = TodoModel(title=payload["title"])
    session.add(todo)
    session.commit()
    return jsonify(response_schema.dump(todo)), 201
