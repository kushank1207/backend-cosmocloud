from fastapi import FastAPI, HTTPException, Path, Query, status
from typing import Optional
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from . import crud
from .models import Student, StudentsResponse

app = FastAPI()

@app.get("/")
async def welcome_message():
    return {"message": "It is running"}

@app.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_student(student: Student):
    """
    Create a new student entry.
    If successful, returns the created student data with a 201 status code.
    If not, raises a 400 HTTP Exception.
    """
    created_student = await crud.create_student(student)
    if created_student:
        return JSONResponse(content=created_student, status_code=status.HTTP_201_CREATED)
    raise HTTPException(status_code=400, detail="Error creating student")

@app.get("/students", response_model=StudentsResponse)
async def list_students(country: Optional[str] = Query(None), age: Optional[int] = Query(None, gt=0)):
    """ List all students, optionally filtered by country and age. """
    # print("country", country)
    # print("age", age)
    students_list = await crud.list_students(country=country, age=age)
    response_data = {"data": students_list}
    json_response_data = jsonable_encoder(response_data, exclude_none=True)
    return JSONResponse(content=json_response_data)

@app.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: str = Path(..., title="The ID of the student to retrieve")):
    """
    Retrieve a student by their ID.
    If the student is not found, raises a 404 HTTP Exception.
    """
    student = await crud.get_student(student_id)
    if student:
        return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.patch("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_student(student_id: str, student: Student):
    """
    Update a student's information.
    If the update is successful, returns a 204 status code.
    If not, raises a 404 HTTP Exception.
    """
    successful = await crud.update_student(student_id, student)
    if successful:
        return JSONResponse(content={}, status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Student not found or no update made")

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: str = Path(..., title="The ID of the student to delete")):
    """
    Delete a student by their ID.
    If the deletion is successful, returns a 204 status code.
    If not, raises a 404 HTTP Exception.
    """
    successful = await crud.delete_student(student_id)
    if successful:
        return JSONResponse(content={}, status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=404, detail="Student not found")
