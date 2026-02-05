from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from models import UserRole
from pydantic import Field


# --- USER ---
class UserBase(BaseModel):
    username: str
    full_name: str
    email: Optional[str] = None

class UserCreate(UserBase):
    password: str 
    role: UserRole = UserRole.STUDENT

class UserResponse(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True # Để Pydantic đọc được dữ liệu từ SQLAlchemy

# ---------- AUTH ----------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


# ---------- COURSE ----------
class CourseBase(BaseModel):
    name: str
    description: Optional[str] = None
   
class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int

    class Config:
        from_attributes = True

# ---------- CLASS ----------
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
    course: Optional[CourseResponse] = None 
    teacher: Optional[UserResponse] = None

    class Config:
        from_attributes = True


# ---------- GRADE ----------

class GradeUpdate(BaseModel):
    enrollment_id: int
    category_id: int
    value: float

class GradeColumn(BaseModel):
    id: int
    name: str
    weight: float

class StudentGradeRow(BaseModel):
    student_id: int
    full_name: str
    enrollment_id: int
    scores: dict[int, float] = {} 

class GradeBoard(BaseModel):
    columns: List[GradeColumn]
    rows: List[StudentGradeRow]