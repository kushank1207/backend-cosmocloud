# app/crud.py

from fastapi import FastAPI, HTTPException, Body, Path, Query
from .database import db
from .models import Student
from bson import ObjectId
from typing import Dict, Optional, List

async def create_student(student: Student = Body(...)):
    new_student_result = await db["students"].insert_one(student.dict())
    created_student_id = new_student_result.inserted_id
    if created_student_id:
        return {"id": str(created_student_id)}
    raise HTTPException(status_code=500, detail="Student could not be created")

async def get_student(student_id: str) -> dict:
    # Find student by ID
    return await db["students"].find_one({"_id": ObjectId(student_id)})

async def update_student(student_id: str, student: Student = Body(...)) -> bool:
    student_update = student.dict(exclude_unset=True)
    if student_update:
        await db["students"].update_one({"_id": ObjectId(student_id)}, {"$set": student_update})
        updated_student_data = await db["students"].find_one({"_id": ObjectId(student_id)})
        if updated_student_data:
            return True
    raise HTTPException(status_code=404, detail=f"Student with id {student_id} not found")

async def delete_student(student_id: str) -> bool:
    # Delete student by ID
    result = await db["students"].delete_one({"_id": ObjectId(student_id)})
    return result.deleted_count > 0

def serialize_student(student):
    # Exclude the '_id' field from the serialized response
    student.pop('_id', None)
    # Ensure 'address' is included even if it's None; this is optional and can be adjusted
    if 'address' not in student:
        student['address'] = None
    return student

async def list_students(country: Optional[str] = None, age: Optional[int] = None) -> List[Dict]:
    query = {}
    # Check if 'country' filter is provided and adjust the query accordingly
    if country:
        query['address.country'] = country  # Make sure the path 'address.country' matches your document structure
    # Check if 'age' filter is provided and adjust the query accordingly
    if age is not None:
        query['age'] = {"$gte": age}  # This will find students with age greater than or equal to the provided value

    print("query", query)
    
    projection = {"address": 0}

    students_cursor = db['students'].find(query, projection)
    # students_cursor = db['students'].find(query)
    students_list = await students_cursor.to_list(length=100)
    return [serialize_student(student) for student in students_list]

