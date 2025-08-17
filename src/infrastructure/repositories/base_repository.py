from typing import Type, Any, List, Optional
from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, session: Session, model: Type[Any]):
        self.session = session
        self.model = model

    def get(self, _id: int) -> Optional[Any]:
        return self.session.get(self.model, _id)

    def list(self) -> List[Any]:
        return self.session.query(self.model).all()

    def create(self, **kwargs) -> Any:
        obj = self.model(**kwargs)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, _id: int) -> bool:
        obj = self.get(_id)
        if not obj:
            return False
        self.session.delete(obj)
        self.session.commit()
        return True
