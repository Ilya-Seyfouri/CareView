from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Dict
from datetime import datetime


#Main Models

class Client(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=18, le=120)
    room: str = Field(..., min_length=1, max_length=20)
    date_of_birth: str = Field(..., min_length=10, max_length=10)  # YYYY-MM-DD
    support_needs: str = Field(..., min_length=5, max_length=2000)
    visit_logs: Optional[Dict[str, dict]] = Field(default_factory=dict)



class Carer(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    assigned_clients: Optional[List[str]] = []



class Family(BaseModel):
    id: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    assigned_clients: Optional[List[str]] = []



class Manager(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8, max_length=100)
    department: str = Field(..., min_length=2, max_length=100)




class VisitLog(BaseModel):
    date: datetime
    personal_care_completed: bool
    care_reminders_provided: str = Field(..., min_length=1, max_length=500)
    toilet: bool
    changed_clothes: bool
    ate_food: str = Field(..., min_length=1, max_length=300)
    notes: str = Field(..., min_length=1, max_length=1000)
    mood: Optional[List[str]] = []
    carer_name: str = Field(..., min_length=2, max_length=100)
    carer_number: Optional[str] = None
    created_at: Optional[datetime] = None



class CreateSchedule(BaseModel):
    carer_email: EmailStr
    client_id: str = Field(..., min_length=1, max_length=50)
    date: str = Field(..., min_length=10, max_length=10)  # YYYY-MM-DD
    start_time: str = Field(..., min_length=5, max_length=5)  # HH:MM
    end_time: str = Field(..., min_length=5, max_length=5)  # HH:MM
    shift_type: str = Field(..., min_length=1, max_length=50)
    notes: Optional[str] = Field(None, max_length=500)



class Schedule(BaseModel):
    carer_email: EmailStr
    client_id: str = Field(..., min_length=1)
    date: str = Field(..., min_length=1)
    start_time: str = Field(..., min_length=1)
    end_time: str = Field(..., min_length=1)
    shift_type: str = Field(..., min_length=1)
    status: str = Field(..., min_length=1)
    notes: Optional[str] = Field(None, max_length=500)
    created_at: datetime





#Update Models

class UpdateClient(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[int] = Field(None, ge=18, le=120)
    room: Optional[str] = Field(None, min_length=1, max_length=20)
    date_of_birth: Optional[str] = Field(None, min_length=10, max_length=10)
    support_needs: Optional[str] = Field(None, min_length=5, max_length=2000)



class UpdateCarer(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)



class UpdateFamily(BaseModel):
    id: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    phone: Optional[str] = Field(None, min_length=10, max_length=20)




class UpdateManager(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    department: Optional[str] = Field(None, min_length=2, max_length=100)



class UpdateVisitLog(BaseModel):
    id: Optional[str] = Field(None, min_length=1, max_length=50)
    date: Optional[datetime] = None
    personal_care_completed: Optional[bool] = None
    care_reminders_provided: Optional[str] = Field(None, max_length=500)
    toilet: Optional[bool] = None
    changed_clothes: Optional[bool] = None
    ate_food: Optional[str] = Field(None, max_length=300)
    notes: Optional[str] = Field(None, max_length=1000)
    mood: Optional[List[str]] = None



class UpdateSchedule(BaseModel):
    carer_email: Optional[EmailStr] = None
    client_id: Optional[str] = Field(None, min_length=1, max_length=50)
    date: Optional[str] = Field(None, min_length=10, max_length=10)
    start_time: Optional[str] = Field(None, min_length=5, max_length=5)
    end_time: Optional[str] = Field(None, min_length=5, max_length=5)
    shift_type: Optional[str] = Field(None, min_length=1, max_length=50)
    status: Optional[str] = Field(None, min_length=1, max_length=20)
    notes: Optional[str] = Field(None, max_length=500)




# AUTHENTICATION MODELS

class Token(BaseModel):
    access_token: str = Field(..., min_length=1)
    token_type: str = Field(..., min_length=1)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)

    @validator('email', pre=True)
    def clean_email(cls,v):
        return v.strip().lower() if v else v


