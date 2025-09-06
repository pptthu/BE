# src/domain/models/ibooking_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.booking import Booking

class IBookingRepository(ABC):
    @abstractmethod
    def add(self, booking: Booking) -> Booking:
        pass

    @abstractmethod
    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        pass

    @abstractmethod
    def list(self) -> List[Booking]:
        pass

    @abstractmethod
    def update(self, booking: Booking) -> Booking:
        pass

    @abstractmethod
    def delete(self, booking_id: int) -> bool:
        pass
