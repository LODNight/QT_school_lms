from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import security

# Tạo bảng nếu chưa có (đề phòng)
models.Base.metadata.create_all(bind=engine)

def create_admin_user():
    db = SessionLocal()
    try:
        username = "admin"
        password = "123456" # Mật khẩu
        
        # 1. Kiểm tra xem user có tồn tại không
        user = db.query(models.User).filter(models.User.username == username).first()
        
        hashed_password = security.get_password_hash(password)
        
        if user:
            print(f"User '{username}' exists. Updating password...")
            user.password_hash = hashed_password
            user.role = "admin" 
        else:
            print(f"User '{username}' does not exist. Creating new user...")
            user = models.User(
                username=username,
                password_hash=hashed_password,
                full_name="Administrator",
                email="admin@school.com",
                role="admin"
            )
            db.add(user)
            
        db.commit()
        print("---------------------------------------------------")
        print(f"SUCCESS! Updated user '{username}' with password '{password}'")
        print(f"Hash in DB: {hashed_password}")
        print("You can now login!")
        print("---------------------------------------------------")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
