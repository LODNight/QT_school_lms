from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Import các module hàng xóm
from database import get_db
import models, schemas 
import security

from routers.auth import get_current_user

# Tạo một Router riêng cho User
router = APIRouter(
    prefix = "/users",
    tags = ["users"]
) 

# API Tạo User
@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Check trùng username
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username đã tồn tại")
    
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
def read_users(
    skip: int=0, 
    limit: int=100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Khóa bảo mật
):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# API Lấy thông tin bản thân
@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """ Trả về thông tin của chính user đang đăng nhập """
    print(current_user)
    print(models.User.username)
    return current_user
