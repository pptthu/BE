class AppError(Exception):
    status_code = 400
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        if status_code:
            self.status_code = status_code

class NotFound(AppError):
    status_code = 404

class Unauthorized(AppError):
    status_code = 401

class Forbidden(AppError):
    status_code = 403
