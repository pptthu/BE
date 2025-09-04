from sqlalchemy.orm import Session
from ..infrastructure.repositories.location_repository import LocationRepository
from ..infrastructure.repositories.pod_repository import PODRepository
from ..infrastructure.repositories.user_repository import UserRepository
from ..infrastructure.models.location import Location
from ..infrastructure.models.pod import POD
from ..infrastructure.models.role import Role
from ..infrastructure.models.base import now_utc
from ..domain.exceptions import AppError

class ManagerService:
    def __init__(self, session: Session):
        self.db = session
        self.locations = LocationRepository(session)
        self.pods = PODRepository(session)
        self.users = UserRepository(session)

    def list_locations(self):
        items = self.locations.list()
        return [{"id": x.id, "name": x.name, "address": x.address} for x in items]

    def create_location(self, name: str, address: str):
        if not name or not address:
            raise AppError("Invalid name/address", 400)
        loc = Location(name=name, address=address, created_at=now_utc(), updated_at=now_utc())
        self.locations.add(loc)
        self.db.commit()
        return {"id": loc.id, "name": loc.name, "address": loc.address}

    def update_location(self, loc_id: int, name: str | None, address: str | None):
        loc = self.locations.get(loc_id)
        if not loc:
            raise AppError("Location not found", 404)
        if name: loc.name = name
        if address: loc.address = address
        self.db.commit()
        return {"id": loc.id, "name": loc.name, "address": loc.address}

    def delete_location(self, loc_id: int):
        loc = self.locations.get(loc_id)
        if not loc:
            return
        self.locations.delete(loc)
        self.db.commit()

    def list_pods(self):
        items = self.pods.list_all()
        return [{"id": p.id, "name": p.name, "price": float(p.price), "status": p.status, "location_id": p.location_id} for p in items]

    def create_pod(self, name: str, price, location_id: int, status: str = "AVAILABLE"):
        if not name or price is None or not location_id:
            raise AppError("Invalid pod data", 400)
        pod = POD(name=name, price=price, status=status, location_id=location_id)
        self.pods.add(pod)
        self.db.commit()
        return {"id": pod.id, "name": pod.name, "price": float(pod.price), "status": pod.status, "location_id": pod.location_id}

    def update_pod(self, pod_id: int, name=None, price=None, location_id=None, status=None):
        p = self.pods.get(pod_id)
        if not p:
            raise AppError("POD not found", 404)
        if name is not None: p.name = name
        if price is not None: p.price = price
        if location_id is not None: p.location_id = location_id
        if status is not None: p.status = status
        self.db.commit()
        return {"id": p.id, "name": p.name, "price": float(p.price), "status": p.status, "location_id": p.location_id}

    def list_users(self):
        users = self.users.list_all()
        return [{"id": u.id, "email": u.email, "full_name": u.full_name, "role": u.role.name} for u in users]

    def admin_update_user(self, user_id: int, full_name: str | None = None, role_name: str | None = None):
        u = self.users.get_by_id(user_id)
        if not u:
            raise AppError("User not found", 404)
        if full_name: u.full_name = full_name
        if role_name:
            r = self.users.get_role_by_name(role_name)
            if not r:
                r = Role(name=role_name)
                self.db.add(r); self.db.flush()
            u.role_id = r.id
        self.db.commit()
        return {"id": u.id, "email": u.email, "full_name": u.full_name, "role": u.role.name}

    def admin_delete_user(self, user_id: int):
        u = self.users.get_by_id(user_id)
        if not u:
            return
        self.users.delete(u)
        self.db.commit()
