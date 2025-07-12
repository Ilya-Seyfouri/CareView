from datetime import datetime

from app.database import familys, patients,carers,schedules
from fastapi import APIRouter, HTTPException, status, Depends
from app.database import hash_password
from app.auth import get_current_family, create_access_token
from app.models import UpdateFamily

family_router = APIRouter()

# Get Family member by email
@family_router.get("/family/me")
async def get_family_details(current_family: dict = Depends(get_current_family)):
    return current_family


@family_router.put("/family/me")
async def update_family(new_data: UpdateFamily, current_family: dict = Depends(get_current_family)):
    current_email = current_family["user"]["email"]
    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")
    new_password = update_data.get("password")

    if new_email and new_email != current_email:
        if new_email in familys:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        familys[new_email] = current_family["user"]  # Reassign data to new email key
        del familys[current_email]  # Delete old email key

    if new_password:
        current_family["user"]["password"] = hash_password(new_password)
        update_data.pop("password")  # Remove password from update dict

    current_family["user"].update(update_data)

    response = {"success": True, "updated": current_family}
    if new_email and new_email != current_email:
        new_token = await create_access_token(data={"sub": new_email})
        response["new_token"] = new_token

    return response


@family_router.get("/family/me/patients")
async def get_family_patients(current_family: dict = Depends(get_current_family)):
    patient_ids = current_family["user"]["assigned_patients"]
    assigned_patient_data = []

    for pid in patient_ids:
        if pid in patients:
            patient_data = patients[pid].copy()

            # Replace visit_logs with just the IDs
            if "visit_logs" in patient_data:
                patient_data["visit_logs"] = list(patient_data["visit_logs"].keys())

            assigned_patient_data.append(patient_data)

    return {"patients": assigned_patient_data}


# Specific route before dynamic path route
@family_router.get("/family/me/patients/visit_logs")
async def get_family_patients_visit_logs(current_family: dict = Depends(get_current_family)):
    patient_ids = current_family["user"]["assigned_patients"]
    assigned_patient_data = []

    for pid in patient_ids:
        if pid in patients:
            patient = patients[pid]
            patient_visit_logs = {
                "patient_id": pid,
                "patient_name": patient.get("name"),
                "visit_logs": patient.get("visit_logs", {})
            }
            assigned_patient_data.append(patient_visit_logs)

    return {"patients_visit_logs": assigned_patient_data}


@family_router.get("/family/me/patients/visit_logs/{visit_log_id}")
async def get_specific_visit_log(visit_log_id: str, current_family: dict = Depends(get_current_family)):
    patient_ids = current_family["user"]["assigned_patients"]

    for pid in patient_ids:
        if pid in patients:
            visit_logs = patients[pid].get("visit_logs", {})

            if visit_log_id in visit_logs:
                return {
                    "patient_id": pid,
                    "patient_name": patients[pid].get("name"),
                    "visit_log": visit_logs[visit_log_id]
                }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Visit log not found or not accessible to this family member"
    )


@family_router.get("/family/me/schedules")
async def get_patient_schedules(current_family: dict = Depends(get_current_family)):
    assigned_patient_ids = current_family["user"]["assigned_patients"]
    patient_schedules = []

    for schedule in schedules.values():
        if schedule["patient_id"] in assigned_patient_ids:
            enriched_schedule = schedule.copy()

            # Add patient details
            if schedule["patient_id"] in patients:
                patient = patients[schedule["patient_id"]]
                enriched_schedule["patient_details"] = {
                    "id": patient["id"],
                    "name": patient["name"],
                    "room": patient["room"]
                }

            # Add carer details
            if schedule["carer_email"] in carers:
                carer = carers[schedule["carer_email"]]
                enriched_schedule["carer_details"] = {
                    "name": carer["name"],
                    "phone": carer["phone"],
                    "email": carer["email"]
                }

            patient_schedules.append(enriched_schedule)

    # Sort by start time
    patient_schedules.sort(key=lambda x: x["start_time"])

    return {"schedules": patient_schedules}


@family_router.get("/family/me/schedules/upcoming")
async def get_upcoming_schedules(current_family: dict = Depends(get_current_family)):
    assigned_patient_ids = current_family["user"]["assigned_patients"]
    now = datetime.now()
    upcoming_schedules = []

    for schedule in schedules.values():
        if (schedule["patient_id"] in assigned_patient_ids and
                schedule["start_time"] > now and
                schedule["status"] == "scheduled"):

            enriched_schedule = schedule.copy()

            # Add patient details
            if schedule["patient_id"] in patients:
                patient = patients[schedule["patient_id"]]
                enriched_schedule["patient_details"] = {
                    "id": patient["id"],
                    "name": patient["name"],
                    "room": patient["room"]
                }

            # Add carer details
            if schedule["carer_email"] in carers:
                carer = carers[schedule["carer_email"]]
                enriched_schedule["carer_details"] = {
                    "name": carer["name"],
                    "phone": carer["phone"]
                }

            upcoming_schedules.append(enriched_schedule)

    # Sort by start time
    upcoming_schedules.sort(key=lambda x: x["start_time"])

    return {"schedules": upcoming_schedules}