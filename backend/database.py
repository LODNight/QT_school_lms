from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Chuỗi kết nối (Connection String)
# Lưu ý: Tui đặt tên DB mới là 'school_lms_v2' để không đụng hàng cái cũ
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/school_lms_v2"

# 2. Tạo Engine (Cổ máy kết nối)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Tạo SessionLocal (Phiên làm việc)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class cho các Models kế thừa
Base = declarative_base()

# 5. Hàm phụ trợ để lấy DB Session (Dependency Injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()