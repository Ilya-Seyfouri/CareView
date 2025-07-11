
from app.auth import hash_password,verify_password
from fastapi import FastAPI, APIRouter
from app.models import Carer, Patient, Family, Manager, UpdateCarer, UpdatePatient, UpdateFamily, UpdateManager
from app.database import carers, managers, familys, patients


admin_router = APIRouter()


@admin_router.delete("/delete/manager/{email}")
async def delete_manager(email: str):
    if email not in managers:
        return {"error": "Manager not found"}
    del managers[email]
    return {"message": f"Manager with email {email} deleted"}

@admin_router.post("/create/manager")
async def create_manager(manager: Manager):
    if manager.email in managers:
        return {"Error": "This manager is already registered"}

    hashed_pw = hash_password(manager.password)
    managers[manager.email] = {
        "email": manager.email,
        "name": manager.name,
        "department": manager.department,
        "password": hashed_pw
    }

    return {"message": "Manager created", "data": managers[manager.email]}
