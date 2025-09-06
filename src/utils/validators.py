# src/utils/validators.py
import re

# Chỉ kiểm tra định dạng email chuẩn (không gửi mail xác thực)
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def is_valid_email(email: str) -> bool:
    if not isinstance(email, str):
        return False
    return bool(EMAIL_RE.fullmatch(email.strip()))

def is_valid_full_name(name: str) -> bool:
    """
    Yêu cầu:
    - Có ít nhất 2 từ (họ + tên), cách nhau bằng khoảng trắng
    - Chỉ chứa chữ cái (kể cả tiếng Việt có dấu), khoảng trắng, gạch nối, dấu '
    """
    if not isinstance(name, str):
        return False
    s = " ".join(name.split())  # chuẩn hoá khoảng trắng
    if len(s) < 3:
        return False
    parts = s.split(" ")
    if len(parts) < 2:
        return False

    ALLOWED = set(" -'’")
    # Tất cả ký tự phải là chữ cái unicode hoặc ký tự cho phép
    if any(not (ch.isalpha() or ch in ALLOWED) for ch in s):
        return False

    # Mỗi phần phải có ít nhất 1 ký tự chữ cái
    if any(not any(c.isalpha() for c in p) for p in parts):
        return False

    return True
