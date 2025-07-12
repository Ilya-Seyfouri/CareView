from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
from datetime import date, datetime, time

class Schedule(BaseModel):
    id: str = Field(..., min_length=1)
    carer_email: EmailStr
    patient_id: str = Field(..., min_length=1)
    date: str = Field(..., min_length=1)
    start_time: str = Field(..., min_length=1)
    end_time: str = Field(..., min_length=1)
    shift_type: str = Field(..., min_length=1)
    status: str = Field(..., min_length=1)
    notes: Optional[str] = Field(None, max_length=500)
    created_by: EmailStr
    created_at: datetime

class CreateSchedule(BaseModel):
    carer_email: EmailStr
    patient_id: str = Field(..., min_length=1, max_length=50)
    date: str = Field(..., min_length=1)
    start_time: str = Field(..., min_length=1)
    end_time: str = Field(..., min_length=1)
    shift_type: str = Field(..., min_length=1)
    notes: Optional[str] = Field(None, max_length=500)

class UpdateSchedule(BaseModel):
    carer_email: Optional[EmailStr] = None
    patient_id: Optional[str] = Field(None, min_length=1, max_length=50)
    date: Optional[str] = Field(None, min_length=1)
    start_time: Optional[str] = Field(None, min_length=1)
    end_time: Optional[str] = Field(None, min_length=1)
    shift_type: Optional[str] = Field(None, min_length=1)
    status: Optional[str] = Field(None, min_length=1)
    notes: Optional[str] = Field(None, max_length=500)

class Token(BaseModel):
    access_token: str = Field(..., min_length=1)
    token_type: str = Field(..., min_length=1)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=5, max_length=100)

class Carer(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=5, max_length=100)
    phone: str = Field(..., min_length=1)
    assigned_patients: Optional[List[str]] = []

class UpdateVisitLog(BaseModel):
    id: Optional[str] = Field(None, min_length=1, max_length=50)
    date: Optional[datetime] = None
    showered: Optional[bool] = None
    meds_given: Optional[str] = Field(None, max_length=500)
    toilet: Optional[bool] = None
    changed_clothes: Optional[bool] = None
    ate_food: Optional[str] = Field(None, max_length=300)
    notes: Optional[str] = Field(None, max_length=1000)
    mood: Optional[List[str]] = None

class VisitLog(BaseModel):
    id: str = Field(..., min_length=1, max_length=50)
    date: datetime
    showered: bool
    meds_given: str = Field(..., min_length=1, max_length=500)
    toilet: bool
    changed_clothes: bool
    ate_food: str = Field(..., min_length=1, max_length=300)
    notes: str = Field(..., min_length=1, max_length=1000)
    mood: Optional[List[str]] = []
    carer_name: str = Field(..., min_length=1, max_length=100)
    carer_number: Optional[str] = None

class Patient(BaseModel):
    id: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    room: str = Field(..., min_length=1, max_length=20)
    date_of_birth: str = Field(..., min_length=1)
    medical_history: str = Field(..., min_length=1, max_length=2000)
    visit_logs: Optional[Dict[str, dict]] = Field(default_factory=dict)

class Family(BaseModel):
    id: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=5, max_length=100)
    phone: str = Field(..., min_length=1)
    assigned_patients: Optional[List[str]] = []

class Manager(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=5, max_length=100)
    department: str = Field(..., min_length=1, max_length=100)

class UpdateCarer(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=5, max_length=100)
    phone: Optional[str] = Field(None, min_length=1)
    medical_history: Optional[str] = Field(None, max_length=2000)

class UpdatePatient(BaseModel):
    id: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    age: Optional[int] = Field(None, ge=0, le=150)
    room: Optional[str] = Field(None, min_length=1, max_length=20)
    date_of_birth: Optional[str] = Field(None, min_length=1)
    medical_history: Optional[str] = Field(None, min_length=1, max_length=2000)

class UpdateFamily(BaseModel):
    id: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=5, max_length=100)
    phone: Optional[str] = Field(None, min_length=1)

class UpdateManager(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=5, max_length=100)
    department: Optional[str] = Field(None, min_length=1, max_length=100)