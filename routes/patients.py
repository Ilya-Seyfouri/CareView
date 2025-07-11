from app.database import patients
from fastapi import APIRouter

patient_router = APIRouter()


@patient_router.get("/patient/{id}")
async def get_patient(id: str):
    if id not in patients:
        return {"error": "Patient not found"}
    return {"patient": patients[id]}


@patient_router.get("/patient/{id}/visit-log")
async def get_patient_visit_log(id: str):
    if id not in patients[id]:
        return{"Error":"No patient with this ID"}
