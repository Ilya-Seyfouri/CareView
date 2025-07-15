from app.auth import get_current_admin
from app.database import  hash_password
from fastapi import APIRouter, Depends
from app.models import Manager
from app.database import managers


admin_router = APIRouter()


@admin_router.delete("/admin/manager/{email}")
async def delete_manager(email: str, current_admin: dict = Depends(get_current_admin)):
    if email not in managers:
        return {"error": "Manager not found"}
    del managers[email]
    return {"message": f"Manager with email {email} deleted"}

@admin_router.post("/admin/manager")
async def create_manager(manager: Manager, current_admin: dict = Depends(get_current_admin)):
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


@admin_router.get("/admin/managers")
async def get_managers(current_admin: dict = Depends(get_current_admin)):
    return managers