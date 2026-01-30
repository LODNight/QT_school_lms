from pydantic import BaseModel
from typing import Optional
from datetime import date

# 1. Khuôn mẫu chung cho User (Tránh viết lại nhiều lần)
class UserBase(BaseModel):
    username: str
    full_name: str
    email: Optional[str] = None
    role: str = "student" # Mặc định là học sinh

# 2. Khuôn dùng để TẠO user (Cần mật khẩu)
class UserCreate(UserBase):
    password: str 

# 3. Khuôn dùng để TRẢ VỀ dữ liệu (Không được trả về mật khẩu!)
class UserResponse(UserBase):
    id: int
    is_active: bool = True

    class Config:
        from_attributes = True # Để Pydantic đọc được dữ liệu từ SQLAlchemy