# Khởi tạo các repository (sẽ được cung cấp ở Phần 3)
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.booking_repository import BookingRepository
from src.infrastructure.repositories.pod_repository import PODRepository
from src.infrastructure.repositories.location_repository import LocationRepository
from src.infrastructure.repositories.service_repository import ServiceRepository

user_repo = UserRepository()
booking_repo = BookingRepository()
pod_repo = PODRepository()
location_repo = LocationRepository()
service_repo = ServiceRepository()
