from app.auth import hash_password,verify_password
from fastapi import FastAPI, APIRouter
from app.models import Carer, Patient, Family, Manager, UpdateCarer, UpdatePatient, UpdateFamily, UpdateManager
from app.database import carers, managers, familys, patients

manager_router = APIRouter()





# Creating Models

@manager_router.post("/create/carer")
async def create_carer(carer: Carer):
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


@manager_router.post("/create/patient")
async def create_patient(patient: Patient):
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

    return {"message": "Patient Created", "data": patients[patient.id]}


@manager_router.post("/create/family-member")
async def create_family(family: Family):
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


@manager_router.post("/create/manager")
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


# Getting all Models

@manager_router.get("/get-all/patients")
async def get_all_patients():
    return {"patients": list(patients.values())}


@manager_router.get("/get-all/carers")
async def get_all_carers():
    return {"carers": list(carers.values())}


@manager_router.get("/get-all/families")
async def get_all_families():
    return {"families": list(familys.values())}


@manager_router.get("/get-all/managers")
async def get_all_managers():
    return {"managers": list(managers.values())}


# Get Manager by email
@manager_router.get("/get-manager/{email}")
async def get_manager(email: str):
    if email not in managers:
        return {"error": "Manager not found"}
    return {"manager": managers[email]}


# Updating all models

@manager_router.put("/update/patient/{patient_id}")
async def update_patient(patient_id: str, new_data: UpdatePatient):
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


@manager_router.put("/update/manager/{email}")
async def update_manager(email: str, new_data: UpdateManager):
    if email not in managers:
        return {"error": "Manager not found"}

    current = managers[email]
    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")

    if new_email and new_email != email and new_email in managers:
        return {"Error": "This email is already in use!"}

    # If email changed, move data to new key
    if new_email and new_email != email:
        managers[new_email] = current
        del managers[email]
        email = new_email

    current.update(update_data)

    return {"message": "Manager updated", "data": current}
# Deletion

@manager_router.delete("/delete/carer/{email}")
async def delete_carer(email: str):
    if email not in carers:
        return {"error": "Carer not found"}
    del carers[email]
    return {"message": f"Carer with email {email} deleted"}


@manager_router.delete("/delete/patient/{patient_id}")
async def delete_patient(patient_id: str):
    if patient_id not in patients:
        return {"error": "Patient not found"}
    del patients[patient_id]
    return {"message": f"Patient with id {patient_id} deleted"}


@manager_router.delete("/delete/family/{email}")
async def delete_family(email: str):
    if email not in familys:
        return {"error": "Family member not found"}
    del familys[email]
    return {"message": f"Family member with email {email} deleted"}


@manager_router.delete("/delete/manager/{email}")
async def delete_manager(email: str):
    if email not in managers:
        return {"error": "Manager not found"}
    del managers[email]
    return {"message": f"Manager with email {email} deleted"}
