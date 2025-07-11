from app.database import familys, patients
from fastapi import APIRouter, HTTPException, status, Depends
from app.database import hash_password
from app.auth import get_current_family,create_access_token
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

            # Assign the existing family data to the new email key
            familys[new_email] = current_family["user"]
            del familys[current_email]          #Deleting old email key from dictonary
            ## Cause we deleted our old email key, we tell the code hey! were using new email key : point to the right data under the new email


        if new_password:
            current_family["user"]["password"] = hash_password(new_password)
            update_data.pop("password")


        current_family["user"].update(update_data)

        response = {"success": True, "updated": current_family}
        if new_email and new_email != current_email:  # new email = Create new token - will automatically log in using frontend
            new_token = await create_access_token(data={"sub": new_email})
            response["new_token"] = new_token

        return response



@family_router.get("/family/me/patients")
async def get_family_patients(current_family: dict = Depends(get_current_family)):
    patient_ids = current_family["user"]["assigned_patients"]

    assigned_patient_data = []
    for pid in patient_ids:
        if pid in patients:
            assigned_patient_data.append(patients[pid])
    return {"patients": assigned_patient_data}


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