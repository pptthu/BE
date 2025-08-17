# src/infrastructure/repositories/location_repository.py
from domain.models.ilocation_repository import ILocationRepository
from domain.models.location import Location
from typing import List, Optional
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.databases import Base

load_dotenv()


# =========================
# In-memory Repository
# =========================
class LocationRepository(ILocationRepository):
    """
    Repository lưu RAM (giả lập), tương tự TodoRepository.
    Dùng cho dev/demo; khi dùng DB thật, thay bằng repo dùng Session.
    """
    def __init__(self):
        self._locations: List[Location] = []
        self._id_counter: int = 1

    def add(self, location: Location) -> Location:
        location.id = self._id_counter
        self._id_counter += 1
        self._locations.append(location)
        return location

    def get_by_id(self, location_id: int) -> Optional[Location]:
        for loc in self._locations:
            if loc.id == location_id:
                return loc
        return None

    def list(self) -> List[Location]:
        return self._locations

    def update(self, location: Location) -> Location:
        for idx, loc in enumerate(self._locations):
            if loc.id == location.id:
                self._locations[idx] = location
                return location
        raise ValueError('Location not found')

    def delete(self, location_id: int) -> None:
        self._locations = [loc for loc in self._locations if loc.id != location_id]


# =========================
# SQLAlchemy ORM Model
# =========================
class LocationModel(Base):
    """
    ORM mapping cho bảng 'locations' (DB thật).
    Lưu ý: In-memory repo ở trên KHÔNG dùng model này trực tiếp.
    """
    __tablename__ = 'locations'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)      # Tên địa điểm
    address = Column(String(255), nullable=True)    # Địa chỉ (tuỳ chọn)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
