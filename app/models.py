from pydantic import BaseModel
from typing import Optional, List

class Address(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None

class Student(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    address: Optional[Address] = None

class StudentsResponse(BaseModel):
    data: List[Student]