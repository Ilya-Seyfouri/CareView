import uuid

from app.auth import get_current_manager, create_access_token
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
import random

from app.models import Carer, Client, Family, UpdateClient, UpdateFamily, UpdateCarer, UpdateManager, VisitLog, \
    UpdateVisitLog, Schedule, UpdateSchedule, CreateSchedule
from app.database import carers, managers, familys, clients, schedules, updates, deleted, created, hash_password, admins

manager_router = APIRouter()


# -----------------------------
# Routes for current manager's own account
# -----------------------------

@manager_router.get("/manager/me")
async def get_manager(current_manager: dict = Depends(get_current_manager)):
    return current_manager

@manager_router.get("/manager/dashboard")
async def get_manager_dashboard(current_manager: dict = Depends(get_current_manager)):
    now = datetime.now()
    today = now.date()


    # 1. OPERATIONAL STATISTICS


    # Count today's schedules and carers on duty
    visits_today = 0
    completed_today = 0
    carers_on_duty = set()

    for schedule in schedules.values():
        try:
            # Handle string dates from database
            schedule_date = datetime.strptime(schedule["date"], "%Y-%m-%d").date()

            if schedule_date == today:
                visits_today += 1
                carers_on_duty.add(schedule["carer_email"])

                if schedule.get("status") == "completed":
                    completed_today += 1

        except (ValueError, KeyError):
            continue

    # 2. RECENT ACTIVITY FEED

    activities = []

    # Get recent created activities
    recent_created = list(created.items())[-10:]
    for log_key, log_data in recent_created:
        activity_type = "unknown"
        icon = "📝"

        if "Client Created" in log_key:
            icon = "👤"
            title = f"New client added: {log_data.get('Client name', 'Unknown')}"
            description = f"Added by {log_data.get('created by', 'Unknown')}"
        elif "Carer Created" in log_key:
            icon = "👩‍⚕️"
            title = f"New carer registered: {log_data.get('Carer name', 'Unknown')}"
            description = f"Added by {log_data.get('created by', 'Unknown')}"
        elif "Family Member Created" in log_key:
            icon = "👨‍👩‍👧‍👦"
            title = f"Family member added: {log_data.get('Family name', 'Unknown')}"
            description = f"Added by {log_data.get('created by', 'Unknown')}"
        elif "Visit Log Created" in log_key:
            icon = "✅"
            title = f"Visit log submitted for Client {log_data.get('Client ID', 'Unknown')}"
            description = f"Logged by {log_data.get('created by', 'Unknown')}"
        elif "Schedule Created" in log_key:
            icon = "📅"
            title = "New visit scheduled"
            description = f"Created by {log_data.get('created by', 'Unknown')}"
        else:
            title = log_key.split(' - ')[0]
            description = f"By {log_data.get('created by', 'System')}"

        activities.append({
            "id": str(uuid.uuid4())[:8],
            "icon": icon,
            "title": title,
            "description": description,
            "timestamp": log_data.get("created at", now),
            "user": log_data.get("created by", "System")
        })

    # Get recent updates
    recent_updates = list(updates.items())[-5:]
    for log_key, log_data in recent_updates:
        activities.append({
            "id": str(uuid.uuid4())[:8],
            "icon": "✏️",
            "title": f"Record updated: {log_key.split(' - ')[0]}",
            "description": f"Updated by {log_data.get('updated by', 'Unknown')}",
            "timestamp": log_data.get("updated at", now),
            "user": log_data.get("updated by", "System")
        })

    # Sort by timestamp (most recent first)
    activities.sort(key=lambda x: x["timestamp"], reverse=True)

    # 3. COMPLETION RATE

    # Calculate actual completion rate from today's data
    if visits_today > 0:
        completion_rate = round((completed_today / visits_today) * 100, 1)
    else:
        completion_rate = 0

    # 4. ASSEMBLE DASHBOARD RESPONSE

    dashboard_data = {
        "timestamp": now,
        "manager": {
            "name": current_manager["user"]["name"],
            "email": current_manager["user"]["email"]
        },
        "operational_stats": {
            "active_clients": len(clients),
            "carers_on_duty": len(carers_on_duty),
            "visits_today": visits_today,
            "completed_today": completed_today,
            "completion_rate": completion_rate
        },
        "recent_activity": activities[:15]  # Show last 15 activities
    }

    return dashboard_data

@manager_router.put("/manager/me")
async def update_manager(new_data: UpdateManager, current_manager: dict = Depends(get_current_manager)):
    current_email = current_manager["user"]["email"]
    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")
    new_password = update_data.get("password")

    # Handle email update
    if new_email and new_email != current_email:
        if new_email in managers or new_email in carers or new_email in familys:
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
    if carer.email in carers or carer.email in managers or carer.email in familys:
        return {"Error": "Carer with this email is already signed up"}

    hashed_pw = hash_password(carer.password)
    carers[carer.email] = {
        "email": carer.email,
        "name": carer.name,
        "password": hashed_pw,
        "phone": carer.phone,
        "assigned_clients": carer.assigned_clients
    }

    created[f"Carer Created - {carer.email} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Carer name": carer.name,
        "created by": current_manager["user"]["name"],
        "created at": datetime.now()
    }

    return {"message": "Carer created", "data": carers[carer.email]}


@manager_router.post("/manager/create/client")
async def create_client(client: Client, current_manager: dict = Depends(get_current_manager)):
    if client.id in clients:
        return {"Error": "Client has already been assigned to this ID"}
    clients[client.id] = {
        "id": client.id,
        "name": client.name,
        "age": client.age,
        "room": client.room,
        "date_of_birth": client.date_of_birth,
        "support_needs": client.support_needs,
        "visit_logs": {}
    }

    created[f"Client Created - {client.id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Client name": client.name,
        "created by": current_manager["user"]["name"],
        "created at": datetime.now()
    }

    return {"message": "Client Created", "data": clients[client.id], "usertype": current_manager["user-type"]}


@manager_router.post("/manager/create/family-member")
async def create_family(family: Family, current_manager: dict = Depends(get_current_manager)):
    if family.email in familys or family.email in managers or family.email in carers:
        return {"Error": "This email is already in use"}

    hashed_pw = hash_password(family.password)
    familys[family.email] = {
        "email": family.email,
        "id": family.id,
        "name": family.name,
        "phone": family.phone,
        "password": hashed_pw,
        "assigned_clients": family.assigned_clients
    }

    created[f"Family Member Created - {family.email} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Family name": family.name,
        "created by": current_manager["user"]["name"],
        "created at": datetime.now()
    }

    return {"message": "Family Member Created", "data": familys[family.email]}


# -----------------------------
# Get All Records
# -----------------------------

@manager_router.get("/manager/clients")
async def get_all_clients(current_manager: dict = Depends(get_current_manager)):
    all_clients = []
    for client in clients.values():
        client_data = client.copy()
        if "visit_logs" in client_data:
            client_data["visit_logs"] = list(client_data["visit_logs"].keys())
        all_clients.append(client_data)

    return {"clients": all_clients}


@manager_router.get("/manager/carers")
async def get_all_carers(current_manager: dict = Depends(get_current_manager)):
    return {"carers": list(carers.values())}


@manager_router.get("/manager/families")
async def get_all_families(current_manager: dict = Depends(get_current_manager)):
    return {"families": list(familys.values())}


@manager_router.get("/manager/managers")
async def get_all_managers(current_manager: dict = Depends(get_current_manager)):
    return {"managers": list(managers.values())}


@manager_router.get("/manager/create_logs")
async def get_create_logs(current_manager: dict = Depends(get_current_manager)):
    return created

@manager_router.get("/manager/deleted_logs")
async def get_deleted_logs(current_manager: dict = Depends(get_current_manager)):
    return deleted

@manager_router.get("/manager/updated_logs")
async def get_updated_logs(current_manager: dict = Depends(get_current_manager)):
    return updates




# -----------------------------
# Client Management (By ID)
# -----------------------------

@manager_router.get("/manager/client/{client_id}")
async def get_client_id(client_id: str, current_manager: dict = Depends(get_current_manager)):
    if client_id not in clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return {"client": clients[client_id]}


@manager_router.put("/manager/client/{client_id}")
async def update_client(client_id: str, new_data: UpdateClient,
                         current_manager: dict = Depends(get_current_manager)):
    if client_id not in clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    current = clients[client_id]
    update_data = new_data.dict(exclude_unset=True)
    new_id = update_data.get("id")

    if new_id and new_id != client_id:
        if new_id in clients:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This client ID is already in use!")
        clients[new_id] = current
        del clients[client_id]
        client_id = new_id

    updates[f"Client Info Updated - {client_id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Client Name": clients[client_id]["name"],
        "updated by": current_manager["user"]["name"],
        "updated at": datetime.now()
    }

    clients[client_id].update(update_data)
    return {"message": "Client updated", "data": clients[client_id]}


@manager_router.delete("/manager/client/{client_id}")
async def delete_client(client_id: str, current_manager: dict = Depends(get_current_manager)):
    if client_id not in clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    deleted[f"Client deleted - {client_id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Client name": clients[client_id]["name"],
        "deleted by": current_manager["user"]["name"],
        "deleted at": datetime.now()
    }

    del clients[client_id]

    return {"message": f"Client with id {client_id} deleted"}


# -----------------------------
# Carer Management (By Email)
# -----------------------------

@manager_router.get("/manager/carer/{email}")
async def get_carer_email(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in carers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carer not found")
    return {"carer": carers[email]}


@manager_router.put("/manager/carer/{email}")
async def update_carer_as_manager(email: str, new_data: UpdateCarer,
                                  current_manager: dict = Depends(get_current_manager)):
    if email not in carers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carer not found")

    carer = carers[email]
    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")
    new_password = update_data.get("password")

    if new_email and new_email != email:
        if new_email in carers or new_email in managers or new_email in familys:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        carers[new_email] = carer
        del carers[email]

    if new_password:
        carer["password"] = hash_password(new_password)
        update_data.pop("password")

    carer.update(update_data)

    updates[f"Carer Details Updated - {carer['email']} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Carer Name": carer["name"],
        "updated by": current_manager["user"]["name"],
        "updated at": datetime.now()
    }

    return {"success": True, "updated": carer}


@manager_router.delete("/manager/carer/{email}")
async def delete_carer(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in carers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carer not found")
    orphaned_clients = carers[email].get("assigned_clients", [])

    deleted[f"Carer Deleted - {email} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Carer Name": carers[email]["name"],
        "deleted by": current_manager["user"]["name"],
        "deleted at": datetime.now()
    }
    del carers[email]

    return {
        "message": f"Carer with email {email} deleted",
        "clients_needing_reassignment": orphaned_clients
    }





# -----------------------------
# View Assignment Routes
# -----------------------------


@manager_router.get("/manager/client/{client_id}/assignments")
async def get_client_assignments(
        client_id: str,
        current_manager: dict = Depends(get_current_manager)
):

    if client_id not in clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    client = clients[client_id]

    # Find carers assigned to this client
    assigned_carers = []
    for carer_email, carer in carers.items():
        if client_id in carer["assigned_clients"]:
            assigned_carers.append({
                "email": carer_email,
                "name": carer["name"],
                "phone": carer["phone"]
            })

    # Find family members assigned to this client
    assigned_family = []
    for family_email, family_member in familys.items():
        if client_id in family_member["assigned_clients"]:
            assigned_family.append({
                "email": family_email,
                "name": family_member["name"],
                "phone": family_member["phone"]
            })

    return {
        "client": {
            "id": client["id"],
            "name": client["name"],
            "age": client["age"],
            "room": client["room"]
        },
        "assigned_carers": assigned_carers,
        "assigned_family_members": assigned_family,
        "total_carers": len(assigned_carers),
        "total_family": len(assigned_family)
    }



# -----------------------------
# Client-Focused Assignment Routes
# -----------------------------

@manager_router.post("/manager/client/{client_id}/assign-carer/{carer_email}")
async def assign_carer_to_client(
        client_id: str,
        carer_email: str,
        current_manager: dict = Depends(get_current_manager)
):

    # Check if client exists
    if client_id not in clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    # Check if carer exists
    if carer_email not in carers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carer not found"
        )

    carer = carers[carer_email]
    client = clients[client_id]

    # Check if already assigned
    if client_id in carer["assigned_clients"]:
        return {
            "message": "Carer already assigned to this client",
            "client_id": client_id,
            "client_name": client["name"],
            "carer_name": carer["name"],
            "carer_email": carer_email
        }

    # Add client to carer's assigned list
    carer["assigned_clients"].append(client_id)

    # Log the assignment
    created[f"Carer Assignment - {carer_email} to {client_id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Client ID": client_id,
        "Client Name": client["name"],
        "Carer Email": carer_email,
        "Carer Name": carer["name"],
        "assigned by": current_manager["user"]["name"],
        "assigned at": datetime.now()
    }

    return {
        "message": "Carer successfully assigned to client",
        "client": {
            "id": client_id,
            "name": client["name"],
            "room": client["room"]
        },
        "carer": {
            "email": carer_email,
            "name": carer["name"],
            "phone": carer["phone"]
        },
        "assigned_by": current_manager["user"]["name"]
    }


@manager_router.delete("/manager/client/{client_id}/unassign-carer/{carer_email}")
async def unassign_carer_from_client(
        client_id: str,
        carer_email: str,
        current_manager: dict = Depends(get_current_manager)
):

    # Check if client exists
    if client_id not in clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    # Check if carer exists
    if carer_email not in carers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carer not found"
        )

    carer = carers[carer_email]
    client = clients[client_id]

    # Check if carer is assigned to this client
    if client_id not in carer["assigned_clients"]:
        return {
            "message": "Carer was not assigned to this client",
            "client_id": client_id,
            "client_name": client["name"],
            "carer_name": carer["name"],
            "carer_email": carer_email
        }

    # Remove client from carer's assigned list
    carer["assigned_clients"].remove(client_id)

    # Log the unassignment
    deleted[f"Carer Unassignment - {carer_email} from {client_id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Client ID": client_id,
        "Client Name": client["name"],
        "Carer Email": carer_email,
        "Carer Name": carer["name"],
        "unassigned by": current_manager["user"]["name"],
        "unassigned at": datetime.now()
    }

    return {
        "message": "Carer successfully unassigned from client",
        "client": {
            "id": client_id,
            "name": client["name"],
            "room": client["room"]
        },
        "carer": {
            "email": carer_email,
            "name": carer["name"]
        },
        "unassigned_by": current_manager["user"]["name"]
    }


@manager_router.post("/manager/client/{client_id}/assign-family/{family_email}")
async def assign_family_to_client(
        client_id: str,
        family_email: str,
        current_manager: dict = Depends(get_current_manager)
):

    # Check if client exists
    if client_id not in clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    # Check if family member exists
    if family_email not in familys:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found"
        )

    family_member = familys[family_email]
    client = clients[client_id]

    # Check if already assigned
    if client_id in family_member["assigned_clients"]:
        return {
            "message": "Family member already assigned to this client",
            "client_id": client_id,
            "client_name": client["name"],
            "family_name": family_member["name"],
            "family_email": family_email
        }

    # Add client to family member's assigned list
    family_member["assigned_clients"].append(client_id)

    # Log the assignment
    created[f"Family Assignment - {family_email} to {client_id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Client ID": client_id,
        "Client Name": client["name"],
        "Family Email": family_email,
        "Family Name": family_member["name"],
        "assigned by": current_manager["user"]["name"],
        "assigned at": datetime.now()
    }

    return {
        "message": "Family member successfully assigned to client",
        "client": {
            "id": client_id,
            "name": client["name"],
            "room": client["room"]
        },
        "family_member": {
            "email": family_email,
            "name": family_member["name"],
            "phone": family_member["phone"]
        },
        "assigned_by": current_manager["user"]["name"]
    }


@manager_router.delete("/manager/client/{client_id}/unassign-family/{family_email}")
async def unassign_family_from_client(
        client_id: str,
        family_email: str,
        current_manager: dict = Depends(get_current_manager)
):

    # Check if client exists
    if client_id not in clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    # Check if family member exists
    if family_email not in familys:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Family member not found"
        )

    family_member = familys[family_email]
    client = clients[client_id]

    # Check if family member is assigned to this client
    if client_id not in family_member["assigned_clients"]:
        return {
            "message": "Family member was not assigned to this client",
            "client_id": client_id,
            "client_name": client["name"],
            "family_name": family_member["name"],
            "family_email": family_email
        }

    # Remove client from family member's assigned list
    family_member["assigned_clients"].remove(client_id)

    # Log the unassignment
    deleted[
        f"Family Unassignment - {family_email} from {client_id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Client ID": client_id,
        "Client Name": client["name"],
        "Family Email": family_email,
        "Family Name": family_member["name"],
        "unassigned by": current_manager["user"]["name"],
        "unassigned at": datetime.now()
    }

    return {
        "message": "Family member successfully unassigned from client",
        "client": {
            "id": client_id,
            "name": client["name"],
            "room": client["room"]
        },
        "family_member": {
            "email": family_email,
            "name": family_member["name"]
        },
        "unassigned_by": current_manager["user"]["name"]
    }


# -----------------------------
# Client Team Management Routes
# -----------------------------

@manager_router.get("/manager/client/{client_id}/team")
async def get_client_care_team(
        client_id: str,
        current_manager: dict = Depends(get_current_manager)
):

    if client_id not in clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    client = clients[client_id]

    # Find all carers assigned to this client
    assigned_carers = []
    for carer_email, carer in carers.items():
        if client_id in carer["assigned_clients"]:
            assigned_carers.append({
                "email": carer_email,
                "name": carer["name"],
                "phone": carer["phone"]
            })

    # Find all family members assigned to this client
    assigned_family = []
    for family_email, family_member in familys.items():
        if client_id in family_member["assigned_clients"]:
            assigned_family.append({
                "email": family_email,
                "name": family_member["name"],
                "phone": family_member["phone"]
            })

    return {
        "client": {
            "id": client["id"],
            "name": client["name"],
            "age": client["age"],
            "room": client["room"],
            "support_needs": client["support_needs"]
        },
        "care_team": {
            "carers": assigned_carers,
            "family_members": assigned_family
        },
        "team_summary": {
            "total_carers": len(assigned_carers),
            "total_family_members": len(assigned_family),
            "total_team_size": len(assigned_carers) + len(assigned_family)
        }
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
        if new_email in familys or new_email in carers or new_email in managers:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
        familys[new_email] = family_member
        del familys[email]

    if new_password:
        family_member["password"] = hash_password(new_password)
        update_data.pop("password")

    updates[
        f"Family Details Updated - {family_member['email']} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Family name": family_member["name"],
        "updated by": current_manager["user"]["name"],
        "updated at": datetime.now()
    }

    family_member.update(update_data)
    return {"success": True, "updated": family_member}


@manager_router.delete("/manager/family/{email}")
async def delete_family(email: str, current_manager: dict = Depends(get_current_manager)):
    if email not in familys:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family member not found")

    deleted[f"Family Member Deleted - {email} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Family Name:": familys[email]["name"],
        "deleted by": current_manager["user"]["name"],
        "deleted at": datetime.now()
    }
    del familys[email]
    return {"message": f"Family member with email {email} deleted"}


# -----------------------------
# Visit Log Routes (Nested under client)
# -----------------------------

@manager_router.get("/manager/client/{client_id}/visit-logs")
async def get_client_visit_logs(client_id: str, current_manager: dict = Depends(get_current_manager)):
    if client_id not in clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    client = clients[client_id]
    return {
        "client_id": client_id,
        "client_name": client.get("name"),
        "visit_logs": client.get("visit_logs", {})
    }


@manager_router.post("/manager/client/{client_id}/visit-log")
async def create_visit_log(client_id: str, visitlog: VisitLog, current_manager: dict = Depends(get_current_manager)):
    if client_id not in clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    the_client = clients[client_id]
    visit_log = {
        "carer_name": current_manager["user"]["name"],
        "id": visitlog.id,
        "date": visitlog.date,
        "personal_care_completed": visitlog.personal_care_completed,
        "care_reminders_provided": visitlog.care_reminders_provided,
        "toilet": visitlog.toilet,
        "changed_clothes": visitlog.changed_clothes,
        "ate_food": visitlog.ate_food,
        "notes": visitlog.notes,
        "mood": visitlog.mood or []
    }

    if visitlog.id in the_client["visit_logs"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Visit Log with this ID already exists")

    created[f"Visit Log Created - {visitlog.id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Client ID": client_id,
        "created by": current_manager["user"]["name"],
        "created at": datetime.now()
    }

    the_client["visit_logs"][visitlog.id] = visit_log
    return {"message": "Visit log created successfully", "visit_log": visit_log}


@manager_router.get("/manager/client/{client_id}/visit-logs/{visit_log_id}")
async def get_specific_visit_log(client_id: str, visit_log_id: str,
                                 current_manager: dict = Depends(get_current_manager)):
    if client_id not in clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    visit_logs = clients[client_id].get("visit_logs", {})
    if visit_log_id not in visit_logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit log not found")

    return {
        "client_id": client_id,
        "client_name": clients[client_id].get("name"),
        "visit_log": visit_logs[visit_log_id]
    }


@manager_router.put("/manager/client/{client_id}/visit-log/{visit_log_id}")
async def edit_visit_log(client_id: str, visit_log_id: str, new_data: UpdateVisitLog,
                         current_manager: dict = Depends(get_current_manager)):
    if client_id not in clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    visit_logs = clients[client_id].get("visit_logs", {})
    if visit_log_id not in visit_logs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit log not found")

    visit_log = visit_logs[visit_log_id]
    update_data = new_data.dict(exclude_unset=True)
    visit_log.update(update_data)

    updates[f"Visit Log Updated - {visit_log_id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Client ID": client_id,
        "updated by": current_manager["user"]["name"],
        "updated at": datetime.now()
    }

    return {"success": True, "updated": visit_log}


@manager_router.delete("/manager/client/{client_id}/visit-log/{visit_log_id}")
async def delete_visit_log(client_id: str, visit_log_id: str, current_manager: dict = Depends(get_current_manager)):
    if client_id not in clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    visit_logs = clients[client_id].setdefault("visit_logs", {})
    deleted_log = visit_logs.pop(visit_log_id, None)

    if deleted_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Visit log not found")

    deleted[f"Visit Log Deleted - {visit_log_id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "Client ID": client_id,
        "deleted by": current_manager["user"]["name"],
        "deleted at": datetime.now()
    }

    return {"message": "Visit log deleted successfully", "deleted_log": deleted_log}


# -----------------------------
# Schedule Routes
# -----------------------------

@manager_router.post("/manager/schedules")
async def create_schedule(schedule_data: CreateSchedule, current_manager: dict = Depends(get_current_manager)):
    # Validate carer and client exist
    if schedule_data.carer_email not in carers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carer not found")
    if schedule_data.client_id not in clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    # Create schedule
    schedule_id = f"SCH{str(uuid.uuid4())[:8].upper()}"

    new_schedule = {
        "id": schedule_id,
        "carer_email": schedule_data.carer_email,
        "client_id": schedule_data.client_id,
        "date": schedule_data.date,
        "start_time": schedule_data.start_time,
        "end_time": schedule_data.end_time,
        "shift_type": schedule_data.shift_type,
        "status": "scheduled",
        "notes": schedule_data.notes,
        "created_by": current_manager["user"]["email"],
        "created_at": datetime.now()
    }

    schedules[schedule_id] = new_schedule

    created[f"Schedule Created - {schedule_id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "created by": current_manager["user"]["name"],
        "created at": datetime.now()
    }

    return {"message": "Schedule created successfully", "schedule": new_schedule}


@manager_router.get("/manager/schedules")
async def get_all_schedules(current_manager: dict = Depends(get_current_manager)):
    enriched_schedules = []

    for schedule in schedules.values():
        enriched_schedule = schedule.copy()

        # Add carer details
        if schedule["carer_email"] in carers:
            carer = carers[schedule["carer_email"]]
            enriched_schedule["carer_details"] = {
                "name": carer["name"],
                "phone": carer["phone"]
            }

        # Add client details
        if schedule["client_id"] in clients:
            client = clients[schedule["client_id"]]
            enriched_schedule["client_details"] = {
                "name": client["name"],
                "room": client["room"],
                "age": client["age"]
            }

        enriched_schedules.append(enriched_schedule)

    return {"schedules": enriched_schedules}


@manager_router.get("/manager/schedules/{schedule_id}")
async def get_schedule(schedule_id: str, current_manager: dict = Depends(get_current_manager)):
    if schedule_id not in schedules:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    return {"schedule": schedules[schedule_id]}


@manager_router.delete("/manager/schedules/{schedule_id}")
async def delete_schedule(schedule_id: str, current_manager: dict = Depends(get_current_manager)):
    if schedule_id not in schedules:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    deleted_schedule = schedules.pop(schedule_id)

    deleted[f"Schedule Deleted - {schedule_id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {

        "deleted by": current_manager["user"]["name"],
        "deleted at": datetime.now()
    }

    return {
        "message": "Schedule deleted successfully",
        "deleted_schedule": deleted_schedule
    }





@manager_router.put("/manager/schedules/{schedule_id}")
async def update_schedule(schedule_id: str, update_data: UpdateSchedule,
                          current_manager: dict = Depends(get_current_manager)):
    if schedule_id not in schedules:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")

    schedule = schedules[schedule_id]
    update_fields = update_data.dict(exclude_unset=True)

    # Validate carer if being updated
    if "carer_email" in update_fields and update_fields["carer_email"] not in carers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carer not found")

    # Validate client if being updated
    if "client_id" in update_fields and update_fields["client_id"] not in clients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    # Update the schedule
    schedule.update(update_fields)

    updates[f"Schedule Updated - {schedule_id} - {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"] = {
        "updated by": current_manager["user"]["name"],
        "updated at": datetime.now()
    }

    return {"message": "Schedule updated successfully", "schedule": schedule}