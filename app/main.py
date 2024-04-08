from fastapi import FastAPI, HTTPException, Path, status, Response, Query
from . import crud
from .models import Student, StudentsResponse
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "It is running"}

@app.post("/students", response_model=dict)
async def create_student_endpoint(student: Student):
    created_student = await crud.create_student(student)
    if created_student:
        return created_student
    raise HTTPException(status_code=400, detail="Error creating student")

@app.get("/students", response_model=StudentsResponse)
async def list_students_endpoint(country: Optional[str] = Query(None), age: Optional[int] = Query(None, gt=0)):
    print("country", country)
    print("age", age)
    students_list = await crud.list_students(country=country, age=age)
    response_data = {"data": students_list}
    json_compatible_response_data = jsonable_encoder(response_data, exclude_none=True)
    return JSONResponse(content=json_compatible_response_data)

@app.get("/students/{student_id}", response_model=Student)
async def get_student_endpoint(student_id: str = Path(..., title="The ID of the student to get")):
    student = await crud.get_student(student_id)
    if student:
        return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.patch("/students/{student_id}")
async def update_student_endpoint(student_id: str, student: Student):
    successful = await crud.update_student(student_id, student)
    if successful:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Student not found or no update made")

@app.delete("/students/{student_id}")
async def delete_student_endpoint(student_id: str = Path(..., title="The ID of the student to delete")):
    successful = await crud.delete_student(student_id)
    if successful:
        return {}
    raise HTTPException(status_code=404, detail="Student not found")