from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Float, Enum, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # Dùng để lấy thời gian hiện tại
from database import Base
import enum

# --- CÁC ENUM (Định nghĩa trạng thái cố định) ---

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"

class EnrollmentStatus(str, enum.Enum):
    ACTIVE = "active"       # Đang học
    RESERVED = "reserved"   # Đang bảo lưu
    COMPLETED = "completed" # Đã hoàn thành
    DROPPED = "dropped"     # Thôi học/Nghỉ ngang

class SessionStatus(str, enum.Enum):
    SCHEDULED = "scheduled"     # Lịch cứng
    COMPLETED = "completed"     # Đã học xong
    CANCELLED = "cancelled"     # Hủy buổi này
    RESCHEDULED = "rescheduled" # Dời lịch

# --- MODELS ---

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password_hash = Column(String(255))
    full_name = Column(String(100))
    role = Column(Enum(UserRole), default=UserRole.STUDENT)
    email = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)

    classes_taught = relationship("Class", back_populates="teacher")
    enrollments = relationship("Enrollment", back_populates="student")
    registrations = relationship("CourseRegistration", back_populates="student") # MỚI: Liên kết đăng ký chờ

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    description = Column(String(255), nullable=True)
    
    classes = relationship("Class", back_populates="course")
    registrations = relationship("CourseRegistration", back_populates="course") # MỚI

class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    teacher_id = Column(Integer, ForeignKey("users.id"))
    
    # --- CẬP NHẬT THEO YÊU CẦU CỦA BẠN ---
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # Ngày tạo
    start_date = Column(Date, nullable=True) # Ngày khai giảng
    end_date = Column(Date, nullable=True)   # Ngày bế giảng dự kiến
    is_active = Column(Boolean, default=True) # Trạng thái lớp (Đang chạy / Đã đóng)
    # -------------------------------------

    course = relationship("Course", back_populates="classes")
    teacher = relationship("User", back_populates="classes_taught")
    enrollments = relationship("Enrollment", back_populates="classroom")
    grade_categories = relationship("GradeCategory", back_populates="classroom")
    sessions = relationship("ClassSession", back_populates="classroom") # MỚI: Lịch học chi tiết

# [MỚI] Bảng quản lý Học viên đăng ký (Đã đóng tiền nhưng chưa có lớp)
class CourseRegistration(Base):
    __tablename__ = "course_registrations"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    is_paid = Column(Boolean, default=False) # Đã đóng tiền chưa?
    status = Column(String(50), default="waiting") # waiting (chờ lớp) / assigned (đã xếp)
    note = Column(Text, nullable=True)

    student = relationship("User", back_populates="registrations")
    course = relationship("Course", back_populates="registrations")

# [CẬP NHẬT] Bảng Enrollment: Thêm trạng thái bảo lưu/hoàn thành
class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    join_date = Column(Date)
    
    # --- MỚI ---
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE)
    status_date = Column(Date, nullable=True) # Ngày thay đổi trạng thái (VD: Ngày bắt đầu bảo lưu)
    reason_note = Column(Text, nullable=True) # Lý do (VD: Bảo lưu do ốm, Hoàn thành xuất sắc...)
    # -----------

    student = relationship("User", back_populates="enrollments")
    classroom = relationship("Class", back_populates="enrollments")
    grades = relationship("Grade", back_populates="enrollment")

# [MỚI] Bảng quản lý Lịch học & Dời lịch
class ClassSession(Base):
    __tablename__ = "class_sessions"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    
    original_date = Column(DateTime) # Ngày học theo lịch gốc
    actual_date = Column(DateTime, nullable=True) # Ngày học thực tế (nếu bị dời)
    
    status = Column(Enum(SessionStatus), default=SessionStatus.SCHEDULED)
    room = Column(String(20), nullable=True) # Phòng học
    note = Column(String(255), nullable=True) # Lý do dời lịch

    classroom = relationship("Class", back_populates="sessions")

# --- GIỮ NGUYÊN PHẦN ĐIỂM SỐ ---
class GradeCategory(Base):
    __tablename__ = "grade_categories"
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    name = Column(String(50))
    weight = Column(Float)
    
    classroom = relationship("Class", back_populates="grade_categories")
    grades = relationship("Grade", back_populates="category")

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"))
    category_id = Column(Integer, ForeignKey("grade_categories.id"))
    value = Column(Float)
    
    enrollment = relationship("Enrollment", back_populates="grades")
    category = relationship("GradeCategory", back_populates="grades")