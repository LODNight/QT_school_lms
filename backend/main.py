from fastapi import FastAPI
from database import engine, Base
import models # Import file models để nó nhận diện các class

# LỆNH QUAN TRỌNG: Tạo toàn bộ bảng vào Database
# Nó sẽ tự kết nối MySQL -> Tạo DB school_lms_v2 (nếu chưa có thì phải tạo DB rỗng trước) -> Tạo Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hệ thống LMS Backend đang chạy!"}