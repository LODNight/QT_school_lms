from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Giả lập database (Sau này sẽ nối MySQL thật)
fake_students_db = [
    {"id": "HS001", "name": "Nguyễn Văn A", "class": "10A1"},
    {"id": "HS002", "name": "Trần Thị B", "class": "10A1"}
]

class Student(BaseModel):
    id: str
    name: str
    class_name: str = "Unknown"

@app.get("/")
def read_root():
    return {"message": "Welcome to LMS API System"}

@app.get("/students", response_model=List[Student])
def get_students():
    return fake_students_db