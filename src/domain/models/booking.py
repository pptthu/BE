from datetime import datetime
from typing import Optional

class Booking:
    def __init__(
        self,
        id: Optional[int],
        user_id: int,
        pod_id: int,
        start_time: datetime,
        end_time: datetime,
        status: str,
        created_at: datetime,
        updated_at: datetime,
        total_price: Optional[float] = None
    ):
        self.id = id
        self.user_id = user_id
        self.pod_id = pod_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.total_price = total_price