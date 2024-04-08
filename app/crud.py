from typing import Dict, List, Optional

from bson import ObjectId
from fastapi import HTTPException, Body

from .database import db
from .models import Student

async def create_student(student: Student) -> Dict[str, str]:
    """Create a new student record in the database."""
    new_student_result = await db["students"].insert_one(student.dict())
    created_student_id = new_student_result.inserted_id
    return {"id": str(created_student_id)} if created_student_id else None

async def get_student(student_id: str) -> Optional[dict]:
    """Retrieve a student record by its ID."""
    return await db["students"].find_one({"_id": ObjectId(student_id)})

async def update_student(student_id: str, student: Student = Body(...)) -> bool:
    """Update an existing student record."""
    student_update = student.dict(exclude_unset=True)
    if student_update:
        await db["students"].update_one({"_id": ObjectId(student_id)}, {"$set": student_update})
        updated_student_data = await db["students"].find_one({"_id": ObjectId(student_id)})
        if updated_student_data:
            return True
    raise HTTPException(status_code=404, detail=f"Student with id {student_id} not found")

async def delete_student(student_id: str) -> bool:
    """Delete a student record by its ID."""
    result = await db["students"].delete_one({"_id": ObjectId(student_id)})
    return result.deleted_count > 0

async def list_students(country: Optional[str] = None, age: Optional[int] = None) -> List[Dict]:
    """List students, optionally filtered by country and age."""
    query = {}
    if country:
        query['address.country'] = country
    if age is not None:
        query['age'] = {"$gte": age}
    # print("Query:", query)

    students_cursor = db['students'].find(query, {"address": 0})
    students_list = await students_cursor.to_list(length=100)
    return [serialize_student(student) for student in students_list]

def serialize_student(student):
    # Exclude the '_id' field from the serialized response
    student.pop('_id', None)
    if 'address' not in student:
        student['address'] = None
    return student
