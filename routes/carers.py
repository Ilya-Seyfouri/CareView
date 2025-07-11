from app.database import carers,patients
from app.models import UpdateCarer, VisitLog
from app.database import hash_password
from app.auth import create_access_token, get_current_carer
from fastapi import APIRouter, HTTPException, status, Depends

carer_router = APIRouter()



@carer_router.get("/carer/me")
async def get_carer_details(current_carer: dict = Depends(get_current_carer)):
    return current_carer


@carer_router.get("/carer/me/patients")
async def get_assigned_patients(current_carer: dict = Depends(get_current_carer)):
    # Check if assigned_patients exists
    assigned_patient_ids = current_carer["user"]["assigned_patients"]

    # Get full patient data for each ID, skip if patient doesn't exist
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


@carer_router.get("/carer/me/patients/{id}")
async def get_assigned_patients_by_id(id: str, current_carer: dict = Depends(get_current_carer)):
    # Check if carer has assigned patients
    patient_list = current_carer["user"]["assigned_patients"]

    # Check if patient is assigned to this carer
    if id not in patient_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient not assigned to you"
        )

    # Check if patient exists in global patients
    if id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    return {"Patient": patients[id]}


@carer_router.put("/carer/me")
async def update_carer(new_data: UpdateCarer, current_carer: dict = Depends(get_current_carer)):
    current_email = current_carer["user"]["email"]
    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")
    new_password = update_data.get("password")

    # Handle email change if requested
    if new_email and new_email != current_email:
        # Check if new email already exists
        if new_email in carers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        # Move the carer data from old email key to new email key
        carers[new_email] = current_carer["user"]
        del carers[current_email]



        # Update our reference to point to the new location

    if new_password:
        current_carer["user"]["password"] = hash_password(new_password)
        update_data.pop("password")

    # Apply all field updates
    current_carer["user"].update(update_data)

    response = {"success": True, "updated": current_carer}

    if new_email and new_email != current_email:   #new email = Create new token - will automatically log in using frontend
       new_token = await create_access_token(data={"sub": new_email})
       response["new_token"] = new_token
    return response


@carer_router.post("/carer/me/patients/{patient_id}/visit-log")
async def create_visit_log(patient_id: str, visitlog: VisitLog, current_carer: dict = Depends(get_current_carer)):
    # Check if carer has assigned patients
    patient_list = current_carer["user"]["assigned_patients"]

    # Check if patient is assigned to this carer
    if patient_id not in patient_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Patient not assigned to you"
        )

    # Check if patient exists in global patients dictionary


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