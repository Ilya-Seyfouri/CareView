from starlette.status import HTTP_400_BAD_REQUEST

from app.database import hash_password
from app.auth import get_current_manager, create_access_token
from fastapi import APIRouter, HTTPException, status, Depends

from app.models import Carer, Patient, Family,UpdatePatient, UpdateFamily, UpdateCarer, UpdateManager,VisitLog,UpdateVisitLog
from app.database import carers, managers, familys, patients


manager_router = APIRouter()





# Creating Models

@manager_router.post("/manager/create/carer")

async def create_carer(carer: Carer,current_manager:dict = Depends(get_current_manager)):

   if carer.email in carers:
       return {"Error": "Carer with this email is already signed up"}



   hashed_pw = hash_password(carer.password)
   carers[carer.email] = {
        "email": carer.email,
        "name": carer.name,
        "password": hashed_pw,
        "phone": carer.phone,
        "assigned_patients": carer.assigned_patients
    }

   return {"message": "Carer created", "data": carers[carer.email]}


@manager_router.post("/manager/create/patient")
async def create_patient(patient: Patient, current_manager: dict = Depends(get_current_manager)):
    if patient.id in patients:
        return {"Error": "Patient has already been assigned to this ID"}
    patients[patient.id] = {
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "room": patient.room,
        "date_of_birth": patient.date_of_birth,
        "medical_history": patient.medical_history,
        "visit_logs": {}
    }

    return {"message": "Patient Created", "data": patients[patient.id], "usertype": current_manager["user-type"]}


@manager_router.post("/manager/create/family-member")
async def create_family(family: Family, current_manager: dict = Depends(get_current_manager)):
    if family.email in familys:
        return {"Error": "This email is already in use"}


    hashed_pw = hash_password(family.password)
    familys[family.email] = {
        "email": family.email,
        "id": family.id,
        "name": family.name,
        "phone": family.phone,
        "password": hashed_pw,
        "assigned_patients": family.assigned_patients

    }
    return {"message": "Family Member Created", "data": familys[family.email]}




# Getting all Models

@manager_router.get("/manager/patients")
async def get_all_patients(current_manager: dict = Depends(get_current_manager)):
    return {"patients": list(patients.values())}


@manager_router.get("/manager/carers")
async def get_all_carers(current_manager: dict = Depends(get_current_manager)):
    return {"carers": list(carers.values())}


@manager_router.get("/manager/families")
async def get_all_families(current_manager: dict = Depends(get_current_manager)):
    return {"families": list(familys.values())}


@manager_router.get("/manager/managers")
async def get_all_managers(current_manager: dict = Depends(get_current_manager)):
    return {"managers": list(managers.values())}


# Get Manager by email
@manager_router.get("/manager/me")
async def get_manager(current_manager: dict = Depends(get_current_manager)):
    return current_manager


@manager_router.put("/manager/me")
async def update_manager(new_data: UpdateManager, current_manager: dict = Depends(get_current_manager)):
    current_email = current_manager["user"]["email"]
    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")
    new_password = update_data.get("password")

    # Handle email change if requested
    if new_email and new_email != current_email:
        # Check if new email already exists
        if new_email in managers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        # Move the carer data from old email key to new email key
        managers[new_email] = current_manager["user"]
        del managers[current_email]

        # Update our reference to point to the new location

    if new_password:
        current_manager["user"]["password"] = hash_password(new_password)
        update_data.pop("password")

    # Apply all field updates
    current_manager["user"].update(update_data)

    response = {"success": True, "updated": current_manager}
    if new_email and new_email != current_email:   #new email = Create new token - will automatically log in using frontend
       new_token = await create_access_token(data={"sub": new_email})
       response["new_token"] = new_token
    return response


# Updating all models

@manager_router.put("/manager/patient/{patient_id}")
async def update_patient(patient_id: str, new_data: UpdatePatient, current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:  # Check if patient exists
        return {"error": "Patient not found"}

    current = patients[patient_id]  # Get current patient data
    update_data = new_data.dict(exclude_unset=True)  # Prepare update data
    new_id = update_data.get("id")  # Check if new ID provided

    if new_id and new_id != patient_id:  # If ID changed
        if new_id in patients:  # Check for ID uniqueness
            return {"error": "This patient ID is already in use!"}
        patients[new_id] = current  # Move data to new ID key
        del patients[patient_id]  # Delete old key
        patient_id = new_id  # Update variable

    patients[patient_id].update(update_data)  # Update fields
    return {"message": "Patient updated", "data": patients[patient_id]}





# Deletion

@manager_router.delete("/manager/carer/{email}")
async def delete_carer(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in carers:
        return {"error": "Carer not found"}
    orphaned_patients = carers[email].get("assigned_patients", [])

    del carers[email]
    return {
        "message": f"Carer with email {email} deleted",
        "patients_needing_reassignment": orphaned_patients}


@manager_router.delete("/manager/patient/{patient_id}")
async def delete_patient(patient_id: str, current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:
        return {"error": "Patient not found"}
    del patients[patient_id]
    return {"message": f"Patient with id {patient_id} deleted"}


@manager_router.delete("/manager/family/{email}")
async def delete_family(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in familys:
        return {"error": "Family member not found"}
    del familys[email]
    return {"message": f"Family member with email {email} deleted"}




@manager_router.get("/manager/patient/{patient_id}")
async def get_patient_id(patient_id: str, current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    return {"patient": patients[patient_id]}


@manager_router.get("/manager/carer/{email}")
async def get_carer_email(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in carers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carer not found"
        )

    return {"carer": carers[email]}


@manager_router.put("/manager/carer/{email}")
async def update_carer_as_manager(email: str, new_data: UpdateCarer,
                                  current_manager: dict = Depends(get_current_manager)):
    # Check if carer exists
    if email not in carers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carer not found"
        )

    carer = carers[email]

    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")
    new_password = update_data.get("password")

    # Handle email change if requested
    if new_email and new_email != email:
        # Check if new email already exists
        if new_email in carers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        # Move the carer data from old email key to new email key
        carers[new_email] = carer
        del carers[email]

    # Handle password hashing if password is being updated
    if new_password:
        carer["password"] = hash_password(new_password)
        update_data.pop("password")  # Remove from update_data to avoid double-updating

    # Apply all other field updates
    carer.update(update_data)

    response = {"success": True, "updated": carer}

    return response


@manager_router.get("/manager/family/{email}")
async def get_family_email(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in familys:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found"
        )

    return {"family": familys[email]}


@manager_router.put("/manager/family/{email}")
async def edit_family_email(email: str, new_data: UpdateFamily, current_manager: dict = Depends(get_current_manager)):
    if email not in familys:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found"
        )

    family_member = familys[email]

    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")
    new_password = update_data.get("password")

    # Handle email change if requested
    if new_email and new_email != email:
        # Check if new email already exists
        if new_email in familys:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        # Move the family data from old email key to new email key
        familys[new_email] = family_member
        del familys[email]

    # Handle password hashing if password is being updated
    if new_password:
        family_member["password"] = hash_password(new_password)
        update_data.pop("password")  # Remove from update_data to avoid double-updating

    # Apply all other field updates
    family_member.update(update_data)

    return {"success": True, "updated": family_member}





@manager_router.post("/manager/patient/{patient_id}/visit-log")
async def create_visit_log(patient_id: str, visitlog: VisitLog, current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    # Check if patient exists in global patients dictionary


    the_patient = patients[patient_id]

    visit_log = {
        "carer_name": current_manager["user"]["name"],
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


@manager_router.delete("/manager/patient/{patient_id}/visit-log/{visit_log_id}")
async def delete_visit_log(patient_id: str, visit_log_id: str,current_manager: dict = Depends(get_current_manager)):

    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    patient = patients[patient_id]

    if "visit_logs" not in patient:
        patient["visit_logs"] = {}

    visit_logs = patient["visit_logs"]

    deleted_log = visit_logs.pop(visit_log_id, None)

    if deleted_log is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visit log not found"
            )

    return {
        "message": "Visit Log Deleted",
        "deleted_log": deleted_log

    }


@manager_router.put("/manager/patient/{patient_id}/visit-log/{visit_log_id}")
async def edit_visit_log(patient_id: str, visit_log_id: str, new_data: UpdateVisitLog, current_manager: dict = Depends(get_current_manager)):

    if patient_id not in patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Patient not found"
        )

    patient = patients[patient_id]

    if "visit_logs" not in patient or not patient["visit_logs"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit Log with this ID not found"
        )

    visit_logs = patient["visit_logs"]

    if visit_log_id not in visit_logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit log with this ID not found"
        )

    # Get the specific visit log to update
    visit_log = visit_logs[visit_log_id]

    # Update the visit log
    update_data = new_data.dict(exclude_unset=True)
    visit_log.update(update_data)

    return {"success": True, "updated": visit_log}





