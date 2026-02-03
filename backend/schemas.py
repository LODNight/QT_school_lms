from pydantic import BaseModel
from typing import Optional
from datetime import date

# --- KHUÔN CHO USER ---
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

# Khuôn mẫu cho cái Token trả về
class Token(BaseModel):
    access_token: str
    token_type: str

# Khuôn mẫu dữ liệu bên trong Token (để sau này giải mã ra)
class TokenData(BaseModel):
    username: Optional[str] = None


# --- KHUÔN CHO KHÓA HỌC (COURSE) ---
class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
   
class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True

# --- KHUÔN CHO LỚP HỌC (CLASS) --
class ClassBase(BaseModel):
    name: str
    course_id: int
    teacher_id: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: bool = True

class ClassCreate(ClassBase):
    pass

class ClassResponse(ClassBase):
    id: int
    # Để hiển thị tên môn và tên GV thay vì chỉ hiện ID số
    course: Optional[CourseResponse] = None 
    teacher: Optional[UserResponse] = None

    class Config:
        from_attributes = True