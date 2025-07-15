from datetime import datetime

from app.database import carers, clients, hash_password, schedules, familys, managers
from app.models import UpdateCarer, VisitLog, UpdateVisitLog,UpdateSchedule
from app.auth import create_access_token, get_current_carer
from fastapi import APIRouter, HTTPException, status, Depends
from app.database import schedules,deleted,created

carer_router = APIRouter()


@carer_router.get("/carer/me")
async def get_carer_details(current_carer: dict = Depends(get_current_carer)):
    return current_carer

@carer_router.get("/carer/dashboard")
async def get_carer_dashboard(current_carer: dict = Depends(get_current_carer)):
    now = datetime.now()
    today = now.date()
    carer_email = current_carer["user"]["email"]

    # 1. GET CARER'S SCHEDULES FOR TODAY

    today_schedules = []
    upcoming_schedules = []

    for schedule in schedules.values():
        if schedule["carer_email"] == carer_email:
            try:
                # Convert schedule date string to date object
                schedule_date = datetime.strptime(schedule["date"], "%Y-%m-%d").date()

                if schedule_date == today:
                    today_schedules.append(schedule)
                elif schedule_date > today:
                    upcoming_schedules.append(schedule)

            except (ValueError, KeyError):
                continue

    # 2. FIND NEXT VISIT DETAILS

    next_visit = None

    # First check for remaining visits today
    pending_today = [s for s in today_schedules if s.get("status") != "completed"]

    if pending_today:
        # Sort by start time to get the next one
        pending_today.sort(key=lambda x: x.get("start_time", ""))
        next_schedule = pending_today[0]
    else:
        # Get next upcoming visit (future dates)
        if upcoming_schedules:
            upcoming_schedules.sort(key=lambda x: (x.get("date", ""), x.get("start_time", "")))
            next_schedule = upcoming_schedules[0]
        else:
            next_schedule = None

    if next_schedule:
        client_id = next_schedule["client_id"]
        client = clients.get(client_id, {})

        next_visit = {
            "schedule_id": next_schedule["id"],
            "client_id": client_id,
            "client_name": client.get("name", "Unknown"),
            "client_room": client.get("room", "N/A"),
            "date": next_schedule["date"],
            "start_time": next_schedule["start_time"],
            "end_time": next_schedule["end_time"],
            "shift_type": next_schedule.get("shift_type", ""),
            "notes": next_schedule.get("notes", ""),
            "support_needs": client.get("support_needs", "")
        }

    # 3. TODAYS PROGRESS

    total_visits_today = len(today_schedules)
    completed_visits_today = len([s for s in today_schedules if s.get("status") == "completed"])

    if total_visits_today > 0:
        progress_percentage = round((completed_visits_today / total_visits_today) * 100, 1)
    else:
        progress_percentage = 0

    todays_progress = {
        "total_visits": total_visits_today,
        "completed_visits": completed_visits_today,
        "remaining_visits": total_visits_today - completed_visits_today,
        "progress_percentage": progress_percentage
    }

    # 4. COMPLETED VISITS LIST

    completed_visits = []

    for schedule in today_schedules:
        if schedule.get("status") == "completed":
            client_id = schedule["client_id"]
            client = clients.get(client_id, {})

            completed_visits.append({
                "schedule_id": schedule["id"],
                "client_id": client_id,
                "client_name": client.get("name", "Unknown"),
                "client_room": client.get("room", "N/A"),
                "start_time": schedule["start_time"],
                "end_time": schedule["end_time"],
                "status": schedule["status"],
                "completed_at": schedule.get("completed_at", "Time not recorded"),
                "shift_type": schedule.get("shift_type", "")
            })

    # Sort completed visits by start time
    completed_visits.sort(key=lambda x: x["start_time"])

    # 5. FAMILY CONTACT INFORMATION

    family_contacts = []
    assigned_client_ids = current_carer["user"]["assigned_clients"]

    for client_id in assigned_client_ids:
        if client_id in clients:
            client = clients[client_id]

            # Find family members for this client
            client_family = []
            for family_email, family_member in familys.items():
                if client_id in family_member.get("assigned_clients", []):
                    client_family.append({
                        "name": family_member.get("name", "Unknown"),
                        "phone": family_member.get("phone", "No phone"),
                        "email": family_member.get("email", "No email"),
                        "relationship": "Family Member"  # Could be enhanced with actual relationship data
                    })

            if client_family:  # Only include clients who have family contacts
                family_contacts.append({
                    "client_id": client_id,
                    "client_name": client.get("name", "Unknown"),
                    "client_room": client.get("room", "N/A"),
                    "family_members": client_family
                })

    # 6. ALL SCHEDULED VISITS (Today + upcoming)


    all_scheduled_visits = []

    for schedule in today_schedules:
        client_id = schedule["client_id"]
        client = clients.get(client_id, {})

        all_scheduled_visits.append({
            "schedule_id": schedule["id"],
            "client_id": client_id,
            "client_name": client.get("name", "Unknown"),
            "client_room": client.get("room", "N/A"),
            "date": schedule["date"],
            "start_time": schedule["start_time"],
            "end_time": schedule["end_time"],
            "status": schedule.get("status", "scheduled"),
            "shift_type": schedule.get("shift_type", ""),
            "notes": schedule.get("notes", "")
        })

    # Sort by start time
    all_scheduled_visits.sort(key=lambda x: x["start_time"])


    dashboard_data = {
        "timestamp": now,
        "carer": {
            "name": current_carer["user"]["name"],
            "email": current_carer["user"]["email"],
            "phone": current_carer["user"]["phone"]
        },
        "next_visit": next_visit,
        "todays_progress": todays_progress,
        "completed_visits": completed_visits,
        "all_scheduled_visits": all_scheduled_visits,
        "family_contacts": family_contacts,
        "quick_stats": {
            "assigned_clients": len(assigned_client_ids),
            "total_visits_today": total_visits_today,
            "completed_today": completed_visits_today,
            "next_visit_time": next_visit["start_time"] if next_visit else "No upcoming visits"
        }
    }

    return dashboard_data


@carer_router.put("/carer/me")
async def update_carer(new_data: UpdateCarer, current_carer: dict = Depends(get_current_carer)):
    current_email = current_carer["user"]["email"]
    update_data = new_data.dict(exclude_unset=True)
    new_email = update_data.get("email")
    new_password = update_data.get("password")

    # Handle email update if provided and different from current
    if new_email and new_email != current_email:
        if new_email in carers or new_email in managers or new_email in familys:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        # Move carer record to new email key
        carers[new_email] = current_carer["user"]
        del carers[current_email]

    # If password is being updated, hash it before saving
    if new_password:
        current_carer["user"]["password"] = hash_password(new_password)
        update_data.pop("password")

    # Update remaining fields
    current_carer["user"].update(update_data)

    response = {"success": True, "updated": current_carer}

    # Generate new token if email was changed
    if new_email and new_email != current_email:
        new_token = await create_access_token(data={"sub": new_email})
        response["new_token"] = new_token

    return response


# ----------------------------
# Client routes (carer scope)
# ----------------------------

@carer_router.get("/carer/me/clients")
async def get_assigned_clients(current_carer: dict = Depends(get_current_carer)):
    assigned_client_ids = current_carer["user"]["assigned_clients"]
    assigned_client_data = []

    for cid in assigned_client_ids:
        if cid in clients:
            client = clients[cid]
            client_summary = {
                "id": client.get("id"),
                "name": client.get("name"),
                "age": client.get("age"),
                "room": client.get("room"),
                "date_of_birth": client.get("date_of_birth"),
                "support_needs": client.get("support_needs")
            }
            assigned_client_data.append(client_summary)

    return assigned_client_data


@carer_router.get("/carer/me/clients/{client_id}")
async def get_assigned_clients_by_id(client_id: str, current_carer: dict = Depends(get_current_carer)):
    client_list = current_carer["user"]["assigned_clients"]

    if client_id not in client_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client not assigned to you"
        )

    if client_id not in clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    client_data = clients[client_id].copy()

    # Replace full visit logs with just their IDs
    if "visit_logs" in client_data:
        client_data["visit_logs"] = list(client_data["visit_logs"].keys())

    return {"client": client_data}


@carer_router.get("/carer/me/clients/{client_id}/visit-logs")
async def get_client_visit_logs(client_id: str, current_carer: dict = Depends(get_current_carer)):
    client_list = current_carer["user"]["assigned_clients"]

    if client_id not in client_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client not assigned to you"
        )

    if client_id not in clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    client = clients[client_id]
    return {
        "client_id": client_id,
        "client_name": client.get("name"),
        "visit_logs": client.get("visit_logs", {})
    }


@carer_router.post("/carer/me/clients/{client_id}/visit-log")
async def create_visit_log(client_id: str, visitlog: VisitLog, current_carer: dict = Depends(get_current_carer)):
    client_list = current_carer["user"]["assigned_clients"]

    if client_id not in client_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client not assigned to you"
        )

    the_client = clients.get(client_id)

    if not the_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    visit_log = {
        "carer_number": current_carer["user"]["phone"],
        "carer_name": current_carer["user"]["name"],
        "id": visitlog.id,
        "date": visitlog.date,
        "personal_care_completed": visitlog.personal_care_completed,
        "care_reminders_provided": visitlog.care_reminders_provided,
        "toilet": visitlog.toilet,
        "changed_clothes": visitlog.changed_clothes,
        "ate_food": visitlog.ate_food,
        "notes": visitlog.notes,
        "mood": visitlog.mood or [],
        "created_at": datetime.now()
    }

    created[visitlog.id] = {
        "Visit Log": visitlog.id,
        "created at": datetime.now(),
        "created by": current_carer["user"]["name"],
    }

    if visitlog.id in the_client["visit_logs"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Visit Log with this ID already exists"
        )

    the_client["visit_logs"][visitlog.id] = visit_log



    return {
        "message": "Visit log created successfully",
        "visit_log": visit_log
    }


@carer_router.get("/carer/me/clients/{client_id}/visit-logs/{visit_log_id}")
async def get_specific_visit_log(client_id: str, visit_log_id: str, current_carer: dict = Depends(get_current_carer)):
    client_list = current_carer["user"]["assigned_clients"]

    if client_id not in client_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client not assigned to you"
        )

    if client_id not in clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    client = clients[client_id]
    visit_logs = client.get("visit_logs", {})

    if visit_log_id not in visit_logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit log not found"
        )

    return {
        "client_id": client_id,
        "client_name": client.get("name"),
        "visit_log": visit_logs[visit_log_id]
    }


@carer_router.put("/carer/me/clients/{client_id}/visit-logs/{visit_log_id}")
async def update_visit_log(client_id: str, visit_log_id: str, new_data: UpdateVisitLog,
                           current_carer: dict = Depends(get_current_carer)):
    client_list = current_carer["user"]["assigned_clients"]

    if client_id not in client_list:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Client not assigned to you"
        )

    if client_id not in clients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    client = clients[client_id]

    if "visit_logs" not in client or not client["visit_logs"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No visit logs found for this client"
        )

    visit_logs = client["visit_logs"]

    if visit_log_id not in visit_logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit log not found"
        )

    visit_log = visit_logs[visit_log_id]
    update_data = new_data.dict(exclude_unset=True)
    visit_log.update(update_data)

    name = current_carer["user"]["name"]
    time = datetime.now()

    visit_log["last_updated"] = {
        "updated_by": name,
        "timestamp": time
    }
    return {"success": True, "updated": visit_log}


@carer_router.get("/carer/me/schedules")
async def get_my_schedules(current_carer: dict = Depends(get_current_carer)):
    carer_email = current_carer["user"]["email"]
    carer_schedules = []

    for schedule in schedules.values():
        if schedule["carer_email"] == carer_email:
            enriched_schedule = schedule.copy()

            # Add client details
            if schedule["client_id"] in clients:
                client = clients[schedule["client_id"]]
                enriched_schedule["client_details"] = {
                    "id": client["id"],
                    "name": client["name"],
                    "room": client["room"],
                    "age": client["age"],
                    "support_needs": client["support_needs"]
                }

            carer_schedules.append(enriched_schedule)

    # Sort by start time
    carer_schedules.sort(key=lambda x: x["start_time"])

    return {"schedules": carer_schedules}


@carer_router.put("/carer/me/schedules/{schedule_id}/status")
async def update_schedule_status(schedule_id: str, new_status: str, current_carer: dict = Depends(get_current_carer)):

    if schedule_id not in schedules:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    schedule = schedules[schedule_id]
    carer_email = current_carer["user"]["email"]

    # Verify this schedule belongs to the carer
    if schedule["carer_email"] != carer_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own schedules"
        )

    # Validate status
    valid_statuses = ["scheduled", "in_progress", "completed", "cancelled"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {valid_statuses}"
        )

    schedule["status"] = new_status

    return {"message": f"Schedule status updated to {new_status}", "schedule": schedule}