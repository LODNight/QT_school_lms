from sqlalchemy import (
    Column, Integer, String, Date, DateTime,
    ForeignKey, Float, Enum, Boolean, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


# =====================
# ENUMS
# =====================

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"


class EnrollmentStatus(str, enum.Enum):
    ACTIVE = "active"
    RESERVED = "reserved"
    COMPLETED = "completed"
    DROPPED = "dropped"


class SessionStatus(str, enum.Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"


class RegistrationStatus(str, enum.Enum):
    WAITING = "waiting"
    ASSIGNED = "assigned"


# =====================
# MODELS
# =====================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)

    email = Column(String(100))
    phone = Column(String(20))

    classes_taught = relationship("Class", back_populates="teacher")
    enrollments = relationship("Enrollment", back_populates="student")
    registrations = relationship("CourseRegistration", back_populates="student")

    def __repr__(self):
        return f"<User id={self.id} username={self.username} role={self.role}>"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))

    classes = relationship("Class", back_populates="course")
    registrations = relationship("CourseRegistration", back_populates="course")

    def __repr__(self):
        return f"<Course id={self.id} name={self.name}>"


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    start_date = Column(Date)
    end_date = Column(Date)
    is_active = Column(Boolean, default=True)

    course = relationship("Course", back_populates="classes")
    teacher = relationship("User", back_populates="classes_taught")
    enrollments = relationship("Enrollment", back_populates="classroom")
    grade_categories = relationship("GradeCategory", back_populates="classroom")
    sessions = relationship("ClassSession", back_populates="classroom")

    def __repr__(self):
        return f"<Class id={self.id} name={self.name}>"


class CourseRegistration(Base):
    __tablename__ = "course_registrations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    is_paid = Column(Boolean, default=False)
    status = Column(Enum(RegistrationStatus), default=RegistrationStatus.WAITING)
    note = Column(Text)

    student = relationship("User", back_populates="registrations")
    course = relationship("Course", back_populates="registrations")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)

    join_date = Column(Date, server_default=func.current_date())
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE)
    status_date = Column(Date)
    reason_note = Column(Text)

    student = relationship("User", back_populates="enrollments")
    classroom = relationship("Class", back_populates="enrollments")
    grades = relationship("Grade", back_populates="enrollment")


class ClassSession(Base):
    __tablename__ = "class_sessions"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)

    original_date = Column(DateTime, nullable=False)
    actual_date = Column(DateTime)
    status = Column(Enum(SessionStatus), default=SessionStatus.SCHEDULED)

    room = Column(String(20))
    note = Column(String(255))

    classroom = relationship("Class", back_populates="sessions")


class GradeCategory(Base):
    __tablename__ = "grade_categories"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    name = Column(String(50), nullable=False)
    weight = Column(Float, nullable=False)

    classroom = relationship("Class", back_populates="grade_categories")
    grades = relationship("Grade", back_populates="category")


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    enrollment_id = Column(Integer, ForeignKey("enrollments.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("grade_categories.id"), nullable=False)
    value = Column(Float, nullable=False)

    enrollment = relationship("Enrollment", back_populates="grades")
    category = relationship("GradeCategory", back_populates="grades")
