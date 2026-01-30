from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import các module hàng xóm
from database import get_db
import models, schemas 
import security

# Tạo một Router riêng cho User
router = APIRouter(
    prefix = "/users",
    tags = ["users"]
) 

# API Tạo User
@router.post("/", response_model=schemas.UserResponse)
def create_user(use: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Check trùng username
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # 2. Mã hóa mật khẩu
    hashed_password = security.get_password_hash(user.password)
    
    # 3. Tạo User
    new_user = models.User(
        username=user.username,
        password_hash=hashed_password,
        full_name=user.full_name,
        email=user.email,
        role=user.role
    )
    
    # 4. Lưu vào DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# API Lấy danh sách Users
@router.get("/", response_model=List[schemas.UserResponse])
def read_users(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users
