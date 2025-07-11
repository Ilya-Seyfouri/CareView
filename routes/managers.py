from app.auth import hash_password,verify_password,get_current_manager,get_user
from fastapi import APIRouter, HTTPException, status, Depends

from app.models import Carer, Patient, Family, Manager, UpdateCarer, UpdatePatient, UpdateFamily, UpdateManager
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
        "Assigned Patients": carer.assigned_patients
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
        "Date of Birth:": patient.date_of_birth,
        "Medical History": patient.medical_history
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
        "phone-number": family.phone,
        "password": hashed_pw,
        "Assigned Patients": family.assigned_patients

    }
    return {"message": "Family Member Created", "data:": familys[family.email]}




# Getting all Models

@manager_router.get("manager/get-all/patients")
async def get_all_patients(current_manager: dict = Depends(get_current_manager)):
    return {"patients": list(patients.values())}


@manager_router.get("/manager/get-all/carers")
async def get_all_carers(current_manager: dict = Depends(get_current_manager)):
    return {"carers": list(carers.values())}


@manager_router.get("/manager/get-all/families")
async def get_all_families(current_manager: dict = Depends(get_current_manager)):
    return {"families": list(familys.values())}


@manager_router.get("/manager/get-all/managers")
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
        managers[new_email] = current_manager["email"]
        del managers[current_email]

        # Update our reference to point to the new location
        current_manager["user"].update(update_data)

    if new_password:
        current_manager["user"]["password"] = hash_password(new_password)
        update_data.pop("password")

    # Apply all field updates
    current_manager.update(update_data)

    return {"success": True, "updated": current_manager}


# Updating all models

@manager_router.put("/update/patient/{patient_id}")
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

@manager_router.delete("/delete/carer/{email}")
async def delete_carer(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in carers:
        return {"error": "Carer not found"}
    del carers[email]
    return {"message": f"Carer with email {email} deleted"}


@manager_router.delete("/delete/patient/{patient_id}")
async def delete_patient(patient_id: str, current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:
        return {"error": "Patient not found"}
    del patients[patient_id]
    return {"message": f"Patient with id {patient_id} deleted"}


@manager_router.delete("/delete/family/{email}")
async def delete_family(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in familys:
        return {"error": "Family member not found"}
    del familys[email]
    return {"message": f"Family member with email {email} deleted"}


