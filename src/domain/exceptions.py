class AppError(Exception):
    """Ngoại lệ chuẩn của ứng dụng có kèm HTTP status code."""
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status
