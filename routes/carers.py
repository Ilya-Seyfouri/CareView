from app.database import carers, patients, hash_password,schedules
from app.models import UpdateCarer, VisitLog, UpdateVisitLog,UpdateSchedule
from app.auth import create_access_token, get_current_carer
from fastapi import APIRouter, HTTPException, status, Depends
from app.database import schedules

carer_router = APIRouter()


@carer_router.get("/carer/me")
async def get_carer_details(current_carer: dict = Depends(get_current_carer)):
    return current_carer


@carer_router.put("/carer/me")
async def update_carer(new_data: UpdateCarer, current_carer: dict = Depends(get_current_carer)):
    current_email = current_carer["user"]["email"]
    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")
    new_password = update_data.get("password")

    # Handle email update if provided and different from current
    if new_email and new_email != current_email:
        if new_email in carers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        # Move carer record to new email key
        carers[new_email] = current_carer["user"]
        del carers[current_email]

    # If password is being updated, hash it before saving
    if new_password:
        current_carer["user"]["password"] = hash_password(new_password)
        update_data.pop("password")

    # Update remaining fields
    current_carer["user"].update(update_data)

    response = {"success": True, "updated": current_carer}

    # Generate new token if email was changed
    if new_email and new_email != current_email:
        new_token = await create_access_token(data={"sub": new_email})
        response["new_token"] = new_token

    return response


# ----------------------------
# Patient routes (carer scope)
# ----------------------------

@carer_router.get("/carer/me/patients")
async def get_assigned_patients(current_carer: dict = Depends(get_current_carer)):
    assigned_patient_ids = current_carer["user"]["assigned_patients"]
    assigned_patient_data = []

    for pid in assigned_patient_ids:
        if pid in patients:
            patient = patients[pid]
            patient_summary = {
                "id": patient.get("id"),
                "name": patient.get("name"),
                "age": patient.get("age"),
                "room": patient.get("room"),
                "date_of_birth": patient.get("date_of_birth"),
                "medical_history": patient.get("medical_history")
            }
            assigned_patient_data.append(patient_summary)

    return assigned_patient_data


@carer_router.get("/carer/me/patients/{patient_id}")
async def get_assigned_patients_by_id(patient_id: str, current_carer: dict = Depends(get_current_carer)):
    patient_list = current_carer["user"]["assigned_patients"]

    if patient_id not in patient_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient not assigned to you"
        )

    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    patient_data = patients[patient_id].copy()

    # Replace full visit logs with just their IDs
    if "visit_logs" in patient_data:
        patient_data["visit_logs"] = list(patient_data["visit_logs"].keys())

    return {"patient": patient_data}


@carer_router.get("/carer/me/patients/{patient_id}/visit-logs")
async def get_patient_visit_logs(patient_id: str, current_carer: dict = Depends(get_current_carer)):
    patient_list = current_carer["user"]["assigned_patients"]

    if patient_id not in patient_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient not assigned to you"
        )

    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    patient = patients[patient_id]
    return {
        "patient_id": patient_id,
        "patient_name": patient.get("name"),
        "visit_logs": patient.get("visit_logs", {})
    }


@carer_router.post("/carer/me/patients/{patient_id}/visit-log")
async def create_visit_log(patient_id: str, visitlog: VisitLog, current_carer: dict = Depends(get_current_carer)):
    patient_list = current_carer["user"]["assigned_patients"]

    if patient_id not in patient_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient not assigned to you"
        )

    the_patient = patients.get(patient_id)

    if not the_patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    visit_log = {
        "carer_number": current_carer["user"]["phone"],
        "carer_name": current_carer["user"]["name"],
        "id": visitlog.id,
        "date": visitlog.date,
        "showered": visitlog.showered,
        "meds_given": visitlog.meds_given,
        "toilet": visitlog.toilet,
        "changed_clothes": visitlog.changed_clothes,
        "ate_food": visitlog.ate_food,
        "notes": visitlog.notes,
        "mood": visitlog.mood or []
    }

    if visitlog.id in the_patient["visit_logs"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Visit Log with this ID already exists"
        )

    the_patient["visit_logs"][visitlog.id] = visit_log

    return {
        "message": "Visit log created successfully",
        "visit_log": visit_log
    }


@carer_router.get("/carer/me/patients/{patient_id}/visit-logs/{visit_log_id}")
async def get_specific_visit_log(patient_id: str, visit_log_id: str, current_carer: dict = Depends(get_current_carer)):
    patient_list = current_carer["user"]["assigned_patients"]

    if patient_id not in patient_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient not assigned to you"
        )

    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    patient = patients[patient_id]
    visit_logs = patient.get("visit_logs", {})

    if visit_log_id not in visit_logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit log not found"
        )

    return {
        "patient_id": patient_id,
        "patient_name": patient.get("name"),
        "visit_log": visit_logs[visit_log_id]
    }


@carer_router.put("/carer/me/patients/{patient_id}/visit-logs/{visit_log_id}")
async def update_visit_log(patient_id: str, visit_log_id: str, new_data: UpdateVisitLog,
                           current_carer: dict = Depends(get_current_carer)):
    patient_list = current_carer["user"]["assigned_patients"]

    if patient_id not in patient_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient not assigned to you"
        )

    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    patient = patients[patient_id]

    if "visit_logs" not in patient or not patient["visit_logs"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No visit logs found for this patient"
        )

    visit_logs = patient["visit_logs"]

    if visit_log_id not in visit_logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit log not found"
        )

    visit_log = visit_logs[visit_log_id]
    update_data = new_data.dict(exclude_unset=True)
    visit_log.update(update_data)

    return {"success": True, "updated": visit_log}


@carer_router.get("/carer/me/schedules")
async def get_my_schedules(current_carer: dict = Depends(get_current_carer)):
    carer_email = current_carer["user"]["email"]
    carer_schedules = []

    for schedule in schedules.values():
        if schedule["carer_email"] == carer_email:
            enriched_schedule = schedule.copy()

            # Add patient details
            if schedule["patient_id"] in patients:
                patient = patients[schedule["patient_id"]]
                enriched_schedule["patient_details"] = {
                    "id": patient["id"],
                    "name": patient["name"],
                    "room": patient["room"],
                    "age": patient["age"],
                    "medical_history": patient["medical_history"]
                }

            carer_schedules.append(enriched_schedule)

    # Sort by start time
    carer_schedules.sort(key=lambda x: x["start_time"])

    return {"schedules": carer_schedules}


@carer_router.put("/carer/me/schedules/{schedule_id}/status")
async def update_schedule_status(schedule_id: str, new_status: str, current_carer: dict = Depends(get_current_carer)):
    """FIXED: Update schedule status - parameter name changed"""

    if schedule_id not in schedules:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    schedule = schedules[schedule_id]
    carer_email = current_carer["user"]["email"]

    # Verify this schedule belongs to the carer
    if schedule["carer_email"] != carer_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,  # FIXED: No more attribute error
            detail="You can only update your own schedules"
        )

    # Validate status
    valid_statuses = ["scheduled", "in_progress", "completed", "cancelled"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )

    schedule["status"] = new_status

    return {"message": f"Schedule status updated to {new_status}", "schedule": schedule}
