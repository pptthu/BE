# src/domain/models/pod.py
from datetime import datetime
from decimal import Decimal
from typing import Optional


class Pod:
    def __init__(
        self,
        id: int,
        name: str,
        price: Decimal,
        status: str,
        location_id: Optional[int],
        created_at: datetime,
        updated_at: datetime,
        description: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.price = price
        self.status = status
        self.location_id = location_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.description = description

    def __repr__(self) -> str:
        return f"<Pod id={self.id} name={self.name} price={self.price} status={self.status}>"
