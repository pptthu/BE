# domain/models/ibooking_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from datetime import datetime
from .booking import Booking

class IBookingRepository(ABC):
    @abstractmethod
    def add(self, booking: Booking) -> Booking:
        """Thêm một booking mới, trả về booking đã được gán id."""
        pass

    @abstractmethod
    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        """Lấy booking theo id, không có thì trả None."""
        pass

    @abstractmethod
    def list(self) -> List[Booking]:
        """Trả toàn bộ bookings (không filter/paging)."""
        pass

    @abstractmethod
    def update(self, booking: Booking) -> Booking:
        """Cập nhật booking, trả về booking sau cập nhật."""
        pass

    @abstractmethod
    def delete(self, booking_id: int) -> bool:
        """Xoá booking theo id. Trả True nếu xoá được, False nếu không tìm thấy."""
        pass

    # Tuỳ chọn: hỗ trợ filter + phân trang
    def list_filtered(
        self,
        status: Optional[str] = None,
        user_id: Optional[int] = None,
        pod_id: Optional[int] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        page: int = 1,
        limit: int = 20,
    ) -> Tuple[List[Booking], int]:
        """
        Mặc định không bắt buộc triển khai. Nếu repo cụ thể hỗ trợ thì override.
        Trả về (items, total).
        """
        return self.list(), len(self.list())
