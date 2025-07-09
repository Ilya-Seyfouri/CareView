from pydantic import BaseModel, EmailStr
from typing import List,Optional
from datetime import date,datetime

class Carer(BaseModel):
    email: EmailStr
    name: str
    password: str
    phone: float


class Patient(BaseModel):
    id: str
    name: str
    age: int
    room: str
    date_of_birth: date


class Family(BaseModel):
    id: str
    email: EmailStr
    name: str
    password: str
    phone: float


class Manager(BaseModel):
    email : EmailStr
    name: str
    password: str
    department: str


class UpdateCarer(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None


class UpdatePatient(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    room: Optional[str] = None
    date_of_birth: Optional[date] = None


class UpdateFamily(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[float] = None


class UpdateManager(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    department: Optional[str] = None

