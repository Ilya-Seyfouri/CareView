from pydantic import BaseModel, EmailStr, Field
from typing import List,Optional,Dict
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
    phone: str
    assigned_patients: Optional[List[str]] = []


class UpdateVisitLog(BaseModel):
    id: Optional[str] = None
    date: Optional[datetime] = None
    showered: Optional[bool] = None
    meds_given: Optional[str] = None
    toilet: Optional[bool] = None
    changed_clothes: Optional[bool] = None
    ate_food: Optional[str] = None
    notes: Optional[str] = None
    mood: Optional[List[str]] = None


class VisitLog(BaseModel):
    id: str
    date: datetime
    showered: bool
    meds_given: str
    toilet: bool
    changed_clothes: bool
    ate_food: str
    notes:str
    mood: Optional[List[str]] = []
    carer_name: str
    carer_number: Optional[str] = None



class Patient(BaseModel):
    id: str
    name: str
    age: int
    room: str
    date_of_birth: date
    medical_history: str
    visit_logs: Optional[Dict[str,dict]] = Field(default_factory=dict)

class Family(BaseModel):
    id: str
    email: EmailStr
    name: str
    password: str
    phone: str
    assigned_patients: Optional[List[str]] = []


class Manager(BaseModel):
    email : EmailStr
    name: str
    password: str
    department: str






class UpdateCarer(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    medical_history: Optional[str] = None




class UpdatePatient(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    age: Optional[int] = None
    room: Optional[str] = None
    date_of_birth: Optional[date] = None
    medical_history: Optional[str] = None


class UpdateFamily(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None


class UpdateManager(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    department: Optional[str] = None

