from routes.managers import patients
from app.models import UpdatePatient
from fastapi import APIRouter

patient_router = APIRouter()


@patient_router.get("/get-patient/{id}")
async def get_patient(id: str):
    if id not in patients:
        return {"error": "Patient not found"}
    return {"patient": patients[id]}
