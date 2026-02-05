from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas
from routers.auth import get_current_user

router = APIRouter(tags=["grades"])

@router.get("/classes/{class_id}/grade-board", response_model=schemas.GradeBoard)
def get_grade_board(class_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    
    categories = db.query(models.GradeCategory).filter(models.GradeCategory.class_id == class_id).all()

    categories = sorted(categories, key=lambda x: x.id)
    columns_data = [schemas.GradeColumn(id=c.id, name=c.name, weight=c.weight) for c in categories]

    enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.class_id == class_id,
        models.Enrollment.status.in_([models.EnrollmentStatus.ACTIVE, models.EnrollmentStatus.RESERVED])
    ).all()

    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(403, "Không có quyền xem bảng điểm")

    rows_data = []
    for enroll in enrollments:
        grades = db.query(models.Grade).filter(models.Grade.enrollment_id == enroll.id).all()
        
        # Biến đổi list grade thành dictionary
        score_map = {g.category_id: g.value for g in grades}

        # Tạo dòng dữ liệu
        row = schemas.StudentGradeRow(
            student_id=enroll.student.id,
            full_name=enroll.student.full_name,
            enrollment_id=enroll.id,
            scores=score_map
        )
        rows_data.append(row)

    return schemas.GradeBoard(columns=columns_data, rows=rows_data)

@router.post("/grades/update")
def update_grades(updates: List[schemas.GradeUpdate], db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    count = 0
    for item in updates:
        # Kiểm tra xem điểm này đã tồn tại chưa
        existing_grade = db.query(models.Grade).filter(
            models.Grade.enrollment_id == item.enrollment_id,
            models.Grade.category_id == item.category_id
        ).first()

        if existing_grade:
            existing_grade.value = item.value
            
        else:
            new_grade = models.Grade(
                enrollment_id=item.enrollment_id,
                category_id=item.category_id,
                value=item.value
            )
            db.add(new_grade)
        count += 1
    
    db.commit()
    return {"message": f"Đã lưu thành công {count} điểm số!"}