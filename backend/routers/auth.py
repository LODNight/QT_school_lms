from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, security

router = APIRouter(tags=["authentication"])

# API Đăng nhập (Lấy Token)
# URL sẽ là: /token
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Tìm user trong DB
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    # 2. Kiểm tra User có tồn tại không VÀ Mật khẩu có khớp không
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sai username hoặc password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Nếu đúng hết -> Tạo Token
    # access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username} # "sub" là subject (chủ nhân token)
    )
    
    # 4. Trả Token về cho Client
    return {"access_token": access_token, "token_type": "bearer"}