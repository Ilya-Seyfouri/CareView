from routes.managers import carers,patients
from app.models import UpdateCarer
from fastapi import APIRouter


carer_router = APIRouter()

@carer_router.get("/get-carer/{email}")
async def get_carer(email: str):
    # ✅ Check if the given email exists in the carers dictionary
    if email not in carers:
        return {"error": "Carer not found"}

    # ✅ Get the carer's full info (a dictionary)
    carer = carers[email]

    # ✅ Get the list of assigned patient IDs (could be empty if none assigned)
    assigned_patient_ids = carer.get("Assigned Patients", [])

    # ✅ Prepare a list to store full patient data for each assigned patient
    assigned_patient_data = []

    # 🔁 Loop over each assigned patient ID
    for pid in assigned_patient_ids:
        # ✅ Get patient info from the patients dictionary
        patient = patients.get(pid)
        if patient:
            # ✅ If the patient exists, add their data to the result list
            assigned_patient_data.append(patient)

    # ✅ Return both the carer's profile and the full details of their assigned patients
    return {
        "carer": carer,
        "assigned_patients": assigned_patient_data
    }


@carer_router.put("/update/carer/{email}")
async def update_carer(email: str, new_data: UpdateCarer):
    if email not in carers:  # Check if carer exists
        return {"error": "Carer not found"}

    current = carers[email]  # Get current carer data
    update_data = new_data.dict(exclude_unset=True)  # Prepare update data
    new_email = update_data.get("email")  # Check if new email provided

    if new_email and new_email != email:  # If new email is different
        if new_email in carers:  # Check for email uniqueness
            return {"error": "This email is already in use!"}
        carers[new_email] = current  # Move data to new email key
        del carers[email]  # Delete old key
        email = new_email  # Update variable

    carers[email].update(update_data)  # Update fields
    return {"message": "Carer updated", "data": carers[email]}