from .base_repository import BaseRepository
from src.infrastructure.models.todo_model import TodoModel

class TodoRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, TodoModel)
