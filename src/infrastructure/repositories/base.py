from typing import Type, TypeVar, Generic, Optional, Dict, Any, Callable, List
from sqlalchemy.orm import Query
from src.infrastructure.databases.extensions import db
T = TypeVar("T")
class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]): self.model = model
    def get(self, _id:int)->Optional[T]: return self.model.query.get(_id)
    def first(self, **filters)->Optional[T]: return self.model.query.filter_by(**filters).first()
    def list(self, filters:Dict[str,Any]=None, order_by:Callable[[Query],Query]=None, limit:int=None, offset:int=None)->List[T]:
        q = self.model.query
        if filters: q = q.filter_by(**filters)
        if order_by: q = order_by(q)
        if offset is not None: q = q.offset(offset)
        if limit is not None: q = q.limit(limit)
        return q.all()
    def create(self, **fields)->T:
        obj = self.model(**fields); db.session.add(obj); db.session.commit(); return obj
    def update(self, _id:int, **fields)->Optional[T]:
        obj = self.get(_id)
        if not obj: return None
        for k,v in fields.items(): setattr(obj,k,v)
        db.session.commit(); return obj
    def delete(self, _id:int)->bool:
        obj = self.get(_id)
        if not obj: return False
        db.session.delete(obj); db.session.commit(); return True
