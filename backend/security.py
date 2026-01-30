from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

# 1. CẤU HÌNH BẢO MẬT
# Trong thực tế, cái này phải giấu kỹ trong file .env, không được để lộ
SECRET_KEY = "ko_the_tiet_lo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Token hết hạn sau 30 phút

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """ Kiểm tra mật khẩu nhập vào có khớp với mật khẩu đã mã hóa không """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """ Mã hóa mật khẩu """
    return pwd_context.hash(password)

# 2. HÀM TẠO TOKEN (Cấp vé)
def create_access_token(data: dict, expires_data: Optional[timedelta] = None):
    to_encode = data.copyy()
    if expires_data:
        expire = datetime.now() + expires_data
    else:
        expire = datetime.now() + timedelta(minutes=15)
    
    # Nhúng thời gian hết hạn vào token
    to_encode.update({"exp": expire})

    # Mã hóa toàn bộ dữ liệu thành chuỗi JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt