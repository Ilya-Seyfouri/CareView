from botocore.auth import BearerAuth
from pydantic import BaseModel, EmailStr, Field
from typing import List,Optional
from datetime import date,datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: str
    password: str

class Carer(BaseModel):
    email: EmailStr
    name: str
    password: str
    phone: float
    assigned_patients: List[Optional[str]] = []





class VisitLog(BaseModel):
    #carer_email : EmailStr
    #carer_number: str
    #carer_name: str
    #patient_id: str
    #patient_name: str
    date: datetime
    showered: bool
    meds_given: str
    toilet: bool
    changed_clothes: bool
    ate_food: str
    notes:str
    mood: Optional[List[str]] = []




class Patient(BaseModel):
    id: str
    name: str
    age: int
    room: str
    date_of_birth: date
    medical_history: str
    visit_logs: Optional[List[VisitLog]] = Field(default_factory=list)


class Family(BaseModel):
    id: str
    email: EmailStr
    name: str
    password: str
    phone: float
    assigned_patients: List[Optional[str]] = None


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

