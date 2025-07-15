from datetime import datetime

from app.database import familys, clients, carers, schedules, managers
from fastapi import APIRouter, HTTPException, status, Depends
from app.database import hash_password
from app.auth import get_current_family, create_access_token
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
        if new_email in familys or new_email in carers or new_email in managers:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        familys[new_email] = current_family["user"]  # Reassign data to new email key
        del familys[current_email]  # Delete old email key

    if new_password:
        current_family["user"]["password"] = hash_password(new_password)
        update_data.pop("password")  # Remove password from update dict

    current_family["user"].update(update_data)

    response = {"success": True, "updated": current_family}
    if new_email and new_email != current_email:
        new_token = await create_access_token(data={"sub": new_email})
        response["new_token"] = new_token

    return response


@family_router.get("/family/me/clients")
async def get_family_clients(current_family: dict = Depends(get_current_family)):
    client_ids = current_family["user"]["assigned_clients"]
    assigned_client_data = []

    for cid in client_ids:
        if cid in clients:
            client_data = clients[cid].copy()

            # Replace visit_logs with just the IDs
            if "visit_logs" in client_data:
                client_data["visit_logs"] = list(client_data["visit_logs"].keys())

            assigned_client_data.append(client_data)

    return {"clients": assigned_client_data}


# Specific route before dynamic path route
@family_router.get("/family/me/clients/visit_logs")
async def get_family_clients_visit_logs(current_family: dict = Depends(get_current_family)):
    client_ids = current_family["user"]["assigned_clients"]
    assigned_client_data = []

    for cid in client_ids:
        if cid in clients:
            client = clients[cid]
            client_visit_logs = {
                "client_id": cid,
                "client_name": client.get("name"),
                "visit_logs": client.get("visit_logs", {})
            }
            assigned_client_data.append(client_visit_logs)

    return {"clients_visit_logs": assigned_client_data}


@family_router.get("/family/me/clients/visit_logs/{visit_log_id}")
async def get_specific_visit_log(visit_log_id: str, current_family: dict = Depends(get_current_family)):
    client_ids = current_family["user"]["assigned_clients"]

    for cid in client_ids:
        if cid in clients:
            visit_logs = clients[cid].get("visit_logs", {})

            if visit_log_id in visit_logs:
                return {
                    "client_id": cid,
                    "client_name": clients[cid].get("name"),
                    "visit_log": visit_logs[visit_log_id]
                }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Visit log not found or not accessible to this family member"
    )


@family_router.get("/family/me/schedules")
async def get_client_schedules(current_family: dict = Depends(get_current_family)):
    assigned_client_ids = current_family["user"]["assigned_clients"]
    client_schedules = []

    for schedule in schedules.values():
        if schedule["client_id"] in assigned_client_ids:
            enriched_schedule = schedule.copy()

            # Add client details
            if schedule["client_id"] in clients:
                client = clients[schedule["client_id"]]
                enriched_schedule["client_details"] = {
                    "id": client["id"],
                    "name": client["name"],
                    "room": client["room"]
                }

            # Add carer details
            if schedule["carer_email"] in carers:
                carer = carers[schedule["carer_email"]]
                enriched_schedule["carer_details"] = {
                    "name": carer["name"],
                    "phone": carer["phone"],
                    "email": carer["email"]
                }

            client_schedules.append(enriched_schedule)

    # Sort by start time
    client_schedules.sort(key=lambda x: x["start_time"])

    return {"schedules": client_schedules}


@family_router.get("/family/me/schedules/upcoming")
async def get_upcoming_schedules(current_family: dict = Depends(get_current_family)):
    assigned_client_ids = current_family["user"]["assigned_clients"]
    now = datetime.now()
    upcoming_schedules = []

    for schedule in schedules.values():
        if (schedule["client_id"] in assigned_client_ids and
                schedule["start_time"] > now and
                schedule["status"] == "scheduled"):

            enriched_schedule = schedule.copy()

            # Add client details
            if schedule["client_id"] in clients:
                client = clients[schedule["client_id"]]
                enriched_schedule["client_details"] = {
                    "id": client["id"],
                    "name": client["name"],
                    "room": client["room"]
                }

            # Add carer details
            if schedule["carer_email"] in carers:
                carer = carers[schedule["carer_email"]]
                enriched_schedule["carer_details"] = {
                    "name": carer["name"],
                    "phone": carer["phone"]
                }

            upcoming_schedules.append(enriched_schedule)

    # Sort by start time
    upcoming_schedules.sort(key=lambda x: x["start_time"])

    return {"schedules": upcoming_schedules}