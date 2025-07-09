from routes.managers import carers
from app.models import UpdateCarer
from fastapi import APIRouter


carer_router = APIRouter()

@carer_router.get("/get-carer/{email}")
async def get_carer(email: str):
    if email not in carers:
        return {"error": "Carer not found"}
    return {"carer": carers[email]}


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