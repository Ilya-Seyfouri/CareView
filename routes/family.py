from routes.managers import familys
from app.models import UpdateFamily
from fastapi import APIRouter

family_router = APIRouter()

# Get Family member by email
@family_router.get("/get-family/{email}")
async def get_family(email: str):
    if email not in familys:
        return {"error": "Family member not found"}
    return {"family_member": familys[email]}


@family_router.put("/update/family/{email}")
async def update_family(email: str, new_data: UpdateFamily):
    if email not in familys:  # Check if family member exists
        return {"error": "Family member not found"}

    current = familys[email]  # Get current data
    update_data = new_data.dict(exclude_unset=True)  # Prepare update data
    new_email = update_data.get("email")  # Check if new email provided

    if new_email and new_email != email:  # If email is changing
        if new_email in familys:  # Check uniqueness
            return {"error": "This email is already in use!"}
        familys[new_email] = current  # Move to new key
        del familys[email]  # Delete old
        email = new_email  # Update var

    familys[email].update(update_data)  # Update fields
    return {"message": "Family member updated", "data": familys[email]}