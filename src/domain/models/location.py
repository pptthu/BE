# domain/models/location.py
class Location:
    def __init__(
        self,
        id: int,
        name: str,
        address: str,
        capacity: int,
        created_at,
        updated_at
    ):
        self.id = id
        self.name = name          # Tên địa điểm (ví dụ: "POD Quận 1")
        self.address = address    # Địa chỉ cụ thể
        self.capacity = capacity  # Sức chứa (bao nhiêu người/phòng)
        self.created_at = created_at
        self.updated_at = updated_at
