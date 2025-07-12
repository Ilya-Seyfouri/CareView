from starlette.status import HTTP_400_BAD_REQUEST

from app.database import hash_password
from app.auth import get_current_manager, create_access_token
from fastapi import APIRouter, HTTPException, status, Depends

from app.models import Carer, Patient, Family, UpdatePatient, UpdateFamily, UpdateCarer, UpdateManager, VisitLog, \
    UpdateVisitLog
from app.database import carers, managers, familys, patients

manager_router = APIRouter()

# -----------------------------
# Routes for current manager's own account
# -----------------------------

@manager_router.get("/manager/me")
async def get_manager(current_manager: dict = Depends(get_current_manager)):
    return current_manager


@manager_router.put("/manager/me")
async def update_manager(new_data: UpdateManager, current_manager: dict = Depends(get_current_manager)):
    current_email = current_manager["user"]["email"]
    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")
    new_password = update_data.get("password")

    # Handle email update
    if new_email and new_email != current_email:
        if new_email in managers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        managers[new_email] = current_manager["user"]
        del managers[current_email]

    # Handle password update
    if new_password:
        current_manager["user"]["password"] = hash_password(new_password)
        update_data.pop("password")

    current_manager["user"].update(update_data)

    response = {"success": True, "updated": current_manager}
    if new_email and new_email != current_email:
        new_token = await create_access_token(data={"sub": new_email})
        response["new_token"] = new_token
    return response


# -----------------------------
# Creation Routes
# -----------------------------

@manager_router.post("/manager/create/carer")
async def create_carer(carer: Carer, current_manager: dict = Depends(get_current_manager)):
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


# -----------------------------
# Get All Records
# -----------------------------

@manager_router.get("/manager/patients")
async def get_all_patients(current_manager: dict = Depends(get_current_manager)):
    all_patients = []
    for patient in patients.values():
        patient_data = patient.copy()
        if "visit_logs" in patient_data:
            patient_data["visit_logs"] = list(patient_data["visit_logs"].keys())
        all_patients.append(patient_data)

    return {"patients": all_patients}


@manager_router.get("/manager/carers")
async def get_all_carers(current_manager: dict = Depends(get_current_manager)):
    return {"carers": list(carers.values())}


@manager_router.get("/manager/families")
async def get_all_families(current_manager: dict = Depends(get_current_manager)):
    return {"families": list(familys.values())}


@manager_router.get("/manager/managers")
async def get_all_managers(current_manager: dict = Depends(get_current_manager)):
    return {"managers": list(managers.values())}


# -----------------------------
# Patient Management (By ID)
# -----------------------------

@manager_router.get("/manager/patient/{patient_id}")
async def get_patient_id(patient_id: str, current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return {"patient": patients[patient_id]}


@manager_router.put("/manager/patient/{patient_id}")
async def update_patient(patient_id: str, new_data: UpdatePatient,
                         current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    current = patients[patient_id]
    update_data = new_data.dict(exclude_unset=True)
    new_id = update_data.get("id")

    if new_id and new_id != patient_id:
        if new_id in patients:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This patient ID is already in use!")
        patients[new_id] = current
        del patients[patient_id]
        patient_id = new_id

    patients[patient_id].update(update_data)
    return {"message": "Patient updated", "data": patients[patient_id]}


@manager_router.delete("/manager/patient/{patient_id}")
async def delete_patient(patient_id: str, current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    del patients[patient_id]
    return {"message": f"Patient with id {patient_id} deleted"}


# -----------------------------
# Carer Management (By Email)
# -----------------------------

@manager_router.get("/manager/carer/{email}")
async def get_carer_email(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in carers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carer not found")
    return {"carer": carers[email]}


@manager_router.put("/manager/carer/{email}")
async def update_carer_as_manager(email: str, new_data: UpdateCarer, current_manager: dict = Depends(get_current_manager)):
    if email not in carers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carer not found")

    carer = carers[email]
    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")
    new_password = update_data.get("password")

    if new_email and new_email != email:
        if new_email in carers:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        carers[new_email] = carer
        del carers[email]

    if new_password:
        carer["password"] = hash_password(new_password)
        update_data.pop("password")

    carer.update(update_data)
    return {"success": True, "updated": carer}


@manager_router.delete("/manager/carer/{email}")
async def delete_carer(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in carers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carer not found")
    orphaned_patients = carers[email].get("assigned_patients", [])
    del carers[email]
    return {
        "message": f"Carer with email {email} deleted",
        "patients_needing_reassignment": orphaned_patients
    }


# -----------------------------
# Family Member Management (By Email)
# -----------------------------

@manager_router.get("/manager/family/{email}")
async def get_family_email(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in familys:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family member not found")
    return {"family": familys[email]}


@manager_router.put("/manager/family/{email}")
async def edit_family_email(email: str, new_data: UpdateFamily, current_manager: dict = Depends(get_current_manager)):
    if email not in familys:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family member not found")

    family_member = familys[email]
    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")
    new_password = update_data.get("password")

    if new_email and new_email != email:
        if new_email in familys:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        familys[new_email] = family_member
        del familys[email]

    if new_password:
        family_member["password"] = hash_password(new_password)
        update_data.pop("password")

    family_member.update(update_data)
    return {"success": True, "updated": family_member}


@manager_router.delete("/manager/family/{email}")
async def delete_family(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in familys:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family member not found")
    del familys[email]
    return {"message": f"Family member with email {email} deleted"}


# -----------------------------
# Visit Log Routes (Nested under patient)
# -----------------------------

@manager_router.get("/manager/patient/{patient_id}/visit-logs")
async def get_patient_visit_logs(patient_id: str, current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    patient = patients[patient_id]
    return {
        "patient_id": patient_id,
        "patient_name": patient.get("name"),
        "visit_logs": patient.get("visit_logs", {})
    }


@manager_router.post("/manager/patient/{patient_id}/visit-log")
async def create_visit_log(patient_id: str, visitlog: VisitLog, current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Visit Log with this ID already exists")

    the_patient["visit_logs"][visitlog.id] = visit_log
    return {"message": "Visit log created successfully", "visit_log": visit_log}


@manager_router.get("/manager/patient/{patient_id}/visit-logs/{visit_log_id}")
async def get_specific_visit_log(patient_id: str, visit_log_id: str, current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    visit_logs = patients[patient_id].get("visit_logs", {})
    if visit_log_id not in visit_logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit log not found")

    return {
        "patient_id": patient_id,
        "patient_name": patients[patient_id].get("name"),
        "visit_log": visit_logs[visit_log_id]
    }


@manager_router.put("/manager/patient/{patient_id}/visit-log/{visit_log_id}")
async def edit_visit_log(patient_id: str, visit_log_id: str, new_data: UpdateVisitLog,
                         current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    visit_logs = patients[patient_id].get("visit_logs", {})
    if visit_log_id not in visit_logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit log not found")

    visit_log = visit_logs[visit_log_id]
    update_data = new_data.dict(exclude_unset=True)
    visit_log.update(update_data)

    return {"success": True, "updated": visit_log}


@manager_router.delete("/manager/patient/{patient_id}/visit-log/{visit_log_id}")
async def delete_visit_log(patient_id: str, visit_log_id: str, current_manager: dict = Depends(get_current_manager)):
    if patient_id not in patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    visit_logs = patients[patient_id].setdefault("visit_logs", {})
    deleted_log = visit_logs.pop(visit_log_id, None)

    if deleted_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit log not found")

    return {"message": "Visit log deleted successfully", "deleted_log": deleted_log}
