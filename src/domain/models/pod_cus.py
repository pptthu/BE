class Pod:
    def __init__(
        self,
        id: int,
        name: str,
        location_id: int,
        price: float,
        status: str,
        created_at,
        updated_at
    ):
        self.id = id
        self.name = name                # Tên POD (vd: POD Room A1)
        self.location_id = location_id  # FK → Location.id
        self.price = price              # Giá thuê / giờ
        self.status = status            # Trạng thái (vd: available, booked, maintenance)
        self.created_at = created_at
        self.updated_at = updated_at
