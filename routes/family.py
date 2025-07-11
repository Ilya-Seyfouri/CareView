from app.database import carers, managers, familys, patients
from app.models import UpdateFamily
from fastapi import APIRouter, HTTPException, status, Depends
from app.auth import hash_password, verify_password, create_access_token, get_current_carer, authenticate_user, get_current_family



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
        return {"success": True, "updated": current_family}



@family_router.get("/family/me/patients")
def get_family_patients(current_family: dict = Depends(get_current_family)):
    patient_ids = current_family["user"]["assigned_patients"]

    for pid in patient_ids:
        patient_data = patients[pid]
        return patient_data
