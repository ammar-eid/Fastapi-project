from fastapi import FastAPI,Path
from typing import Optional
from pydantic import BaseModel
from sympy.stats import StudentT

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int
    year: str
class UpdateStudent(BaseModel):
    name: Optional[str]
    age: Optional[int]
    year: Optional[str]

students={
    1:Student(name="ali",age=25,year="year 14"),
    2:Student(name="amr",age=15,year="year 10"),
}

@app.get("/")
def index():
    return {"name": "First Data"}


@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(description="this is the Student ID",gt=0,lt=10)):
    return students[student_id]

@app.get("/get-by-name/{student_id}")
def get_student(*,student_id,name : Optional[str] = None, age : int): # symbol * means that all fields is required except the optional one
    for id in students:
        if id == student_id or students[id].name == name or students[id].age == age:
            return students[id]
    return {"error":"Student not found"}


@app.post("/create-student/{student_id}")
def create_student(student_id:int,student: Student):
    if student_id in students:
        return {"error":"Student already exists"}
    students[student_id] = student
    return students[student_id]


@app.put("/update-student/{student_id}")
def update_student(*,student_id:int,student: UpdateStudent):
    if student_id not in students:
        return {"error":"Student already exists"}

    if not student.name:
        students[student_id].name = student.name
    if not student.age:
        students[student_id].age = student.age
    if not student.year:
        students[student_id].year = student.year

    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(*,student_id:int):
    if student_id not in students:
        return {"error":"Student not found"}

    del students[student_id]
    return {"success":"Student deleted"}