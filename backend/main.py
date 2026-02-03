from fastapi import FastAPI
from database import engine, Base
import models # Import file models để nó nhận diện các class

from routers import users, auth, classes

# Lệnh tạo bảng (vẫn giữ ở đây để chạy lúc khởi động)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- KẾT NỐI ROUTER ---
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(classes.router)

@app.get("/")
def read_root():
    return {"message": "Hệ thống LMS Backend (Modularized) đang chạy!"}