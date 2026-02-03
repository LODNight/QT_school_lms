from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas
from routers.auth import get_current_user

router = APIRouter(
    tags=["academic"] # Gom nhóm trên Swagger
)

# --- API MÔN HỌC (COURSES) ---

@router.get("/courses/", response_model=List[schemas.CourseResponse])
def read_courses(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
    ):
    return db.query(models.Course).all()

@router.post("/courses/", response_model=schemas.CourseResponse)
def create_course(
    course: schemas.CourseCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
    ):
    new_course = models.Course(name=course.name, description=course.description)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

# --- API LỚP HỌC (CLASSES) ---

@router.get("/classes/", response_model=List[schemas.ClassResponse])
def read_classes(
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)):
    # Lấy danh sách lớp, join sẵn với bảng Course và Teacher để lấy tên hiển thị
    return db.query(models.Class).all()

@router.post("/classes/", response_model=schemas.ClassResponse)
def create_class(
    cls: schemas.ClassCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)):
    # Kiểm tra tên lớp đã tồn tại chưa
    if db.query(models.Class).filter(models.Class.name == cls.name).first():
        raise HTTPException(status_code=400, detail="Class name already exists")

    # Kiểm tra course_id có tồn tại không
    db_course = db.query(models.Course).filter(models.Course.id == cls.course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Kiểm tra teacher_id có tồn tại không
    db_teacher = db.query(models.User).filter(models.User.id == cls.teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # (Tùy chọn) Kiểm tra user này có phải là giáo viên không
    if db_teacher.role != models.UserRole.TEACHER:
        raise HTTPException(status_code=400, detail="User is not a teacher")
    
    new_class = models.Class(
        name=cls.name,
        course_id=cls.course_id,
        teacher_id=cls.teacher_id,
        start_date=cls.start_date,
        end_date=cls.end_date,
        is_active=cls.is_active
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class