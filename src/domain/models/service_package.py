from typing import Optional

class ServicePackage:
    def __init__(
        self,
        id: Optional[int],
        name: str,
        description: Optional[str],
        price: float,
        created_at,
        updated_at,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.price = float(price)
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f"<ServicePackage id={self.id} name={self.name} price={self.price}>"
