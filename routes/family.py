from datetime import datetime

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_family,logger
from app.database2 import get_db, hash_password
from app.database_models import User, Client as DBClient, Schedule as DBSchedule
from app.models import UpdateFamily



family_router = APIRouter()


#Family Routes



@family_router.get("/family/me")
async def get_family_details(current_family: dict = Depends(get_current_family),
                             db: Session = Depends(get_db)):
    logger.info(f"Getting family details - {current_family['user']['email']}")

    db_family = db.query(User).filter(User.email == current_family["user"]["email"], User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Family member at {current_family['user']['email']} not found")

    return {
        "email": db_family.email,
        "id": db_family.family_id,
        "name": db_family.name,
        "phone": db_family.phone,
        "assigned_clients": [client.id for client in db_family.assigned_clients],
    }





@family_router.put("/family/me")
async def update_family(new_data: UpdateFamily, current_family: dict = Depends(get_current_family),
                        db: Session = Depends(get_db)):
    logger.info(f"Updating family profile - {current_family['user']['email']}")

    try:
        db_family = db.query(User).filter(User.email == current_family["user"]["email"], User.role == "family").first()
        if not db_family:
            raise HTTPException(status_code=404, detail=f"Family member at {current_family['user']['email']} not found")

        update_data = new_data.dict(exclude_unset=True)

        # Regular update
        for field, value in update_data.items():
            if field == "password":
                db_family.password_hash = hash_password(value)
            elif hasattr(db_family, field):
                setattr(db_family, field, value)

        db.commit()
        logger.info(f"Family profile updated successfully: {current_family['user']['email']}")
        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating family profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update profile")





#Family Client Routes




@family_router.get("/family/me/clients")
async def get_family_clients(current_family: dict = Depends(get_current_family),
                             db: Session = Depends(get_db)):
    logger.info(f"Getting family clients - {current_family['user']['email']}")

    db_family = db.query(User).filter(User.email == current_family["user"]["email"], User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Family member at {current_family['user']['email']} not found")

    clients_list = []
    for client in db_family.assigned_clients:
        clients_list.append({
            "id": client.id,
            "name": client.name,
            "age": client.age,
            "room": client.room,
            "support_needs": client.support_needs
        })

    return {"clients": clients_list}






@family_router.get("/family/me/clients/{client_id}")
async def get_family_client_by_id(client_id: str, current_family: dict = Depends(get_current_family),
                                  db: Session = Depends(get_db)):
    logger.info(f"Getting client {client_id} - {current_family['user']['email']}")

    db_family = db.query(User).filter(User.email == current_family["user"]["email"], User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Family member at {current_family['user']['email']} not found")

    db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not db_client:
        logger.warning(f"Client not found: {client_id}")
        raise HTTPException(status_code=404, detail=f"Client {client_id} not found")

    # Check if client is assigned to this family member
    if db_client not in db_family.assigned_clients:
        logger.warning(f"Unauthorized access attempt: {current_family['user']['email']} -> {client_id}")
        raise HTTPException(status_code=403,
                            detail=f"Client {client_id} not assigned to family member {current_family['user']['email']}")

    return {
        "id": db_client.id,
        "name": db_client.name,
        "age": db_client.age,
        "room": db_client.room,
        "date_of_birth": db_client.date_of_birth,
        "support_needs": db_client.support_needs
    }





#Family Visit Log Routes




@family_router.get("/family/me/clients/visit-logs")
async def get_all_family_visit_logs(current_family: dict = Depends(get_current_family),
                                    db: Session = Depends(get_db)):
    logger.info(f"Getting all visit logs for family - {current_family['user']['email']}")

    db_family = db.query(User).filter(User.email == current_family["user"]["email"], User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family['user']['email']}")

    clients_visit_logs = []
    for client in db_family.assigned_clients:
        visit_log_ids = [visit_log.id for visit_log in client.visit_logs]
        clients_visit_logs.append({
            "client_id": client.id,
            "client_name": client.name,
            "visit_logs": visit_log_ids
        })

    return {"clients_visit_logs": clients_visit_logs}





@family_router.get("/family/me/visit-logs/{visit_log_id}")
async def get_specific_visit_log(visit_log_id: str, current_family: dict = Depends(get_current_family),
                                 db: Session = Depends(get_db)):
    logger.info(f"Getting visit log {visit_log_id} - {current_family['user']['email']}")

    db_family = db.query(User).filter(User.email == current_family["user"]["email"], User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family['user']['email']}")

    # Find the visit log across all assigned clients
    for client in db_family.assigned_clients:
        for visit_log in client.visit_logs:
            if visit_log.id == visit_log_id:
                return {
                    "id": visit_log.id,
                    "client_id": client.id,
                    "client_name": client.name,
                    "carer_name": visit_log.carer_name,
                    "carer_number": visit_log.carer_number,
                    "date": visit_log.date,
                    "personal_care_completed": visit_log.personal_care_completed,
                    "care_reminders_provided": visit_log.care_reminders_provided,
                    "toilet": visit_log.toilet,
                    "changed_clothes": visit_log.changed_clothes,
                    "ate_food": visit_log.ate_food,
                    "notes": visit_log.notes,
                    "mood": visit_log.mood
                }

    logger.warning(f"Visit log not found: {visit_log_id}")
    raise HTTPException(status_code=404, detail=f"Visit log {visit_log_id} not found")




#Family Schedule Routes




@family_router.get("/family/me/schedules")
async def get_client_schedules(current_family: dict = Depends(get_current_family),
                               db: Session = Depends(get_db)):
    logger.info(f"Getting schedules for family - {current_family['user']['email']}")

    db_family = db.query(User).filter(User.email == current_family["user"]["email"], User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family['user']['email']}")

    # Get assigned client IDs
    assigned_client_ids = [client.id for client in db_family.assigned_clients]

    # Query schedules for assigned clients
    db_schedules = db.query(DBSchedule).filter(DBSchedule.client_id.in_(assigned_client_ids)).all()

    schedules_list = []
    for schedule in db_schedules:
        # Get carer info from User table
        carer = db.query(User).filter(User.email == schedule.carer_email, User.role == "carer").first()

        schedules_list.append({
            "id": schedule.id,
            "client_id": schedule.client_id,
            "client_name": schedule.client.name if schedule.client else "Unknown",
            "client_room": schedule.client.room if schedule.client else "Unknown",
            "carer_name": carer.name if carer else "Unknown",
            "carer_phone": carer.phone if carer else "Unknown",
            "date": schedule.date,
            "start_time": schedule.start_time,
            "end_time": schedule.end_time,
            "shift_type": schedule.shift_type,
            "status": schedule.status,
            "notes": schedule.notes
        })

    # Sort by date and start time
    schedules_list.sort(key=lambda x: (x["date"], x["start_time"]))

    return {"schedules": schedules_list}








@family_router.get("/family/me/today")
async def get_todays_care_schedule(current_family: dict = Depends(get_current_family),
                                   db: Session = Depends(get_db)):
    logger.info(f"Getting today's care schedule for family - {current_family['user']['email']}")

    db_family = db.query(User).filter(User.email == current_family["user"]["email"], User.role == "family").first()
    if not db_family:
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family['user']['email']}")

    # Get assigned client IDs
    assigned_client_ids = [client.id for client in db_family.assigned_clients]

    # Get today's schedules
    today = datetime.now().date().strftime("%Y-%m-%d")

    today_schedules = db.query(DBSchedule).filter(
        DBSchedule.client_id.in_(assigned_client_ids),
        DBSchedule.date == today
    ).order_by(DBSchedule.start_time).all()

    # Build schedule with status and details
    care_schedule = []
    for schedule in today_schedules:
        # Get carer info from User table
        carer = db.query(User).filter(User.email == schedule.carer_email, User.role == "carer").first()

        # Simple status messages
        if schedule.status == "completed":
            status_message = "✅ Completed"
        elif schedule.status == "in_progress":
            status_message = "🟢 Care happening now"
        elif schedule.status == "scheduled":
            status_message = "⏰ Scheduled"
        elif schedule.status == "cancelled":
            status_message = "❌ Cancelled"
        else:
            status_message = schedule.status

        care_schedule.append({
            "client_name": schedule.client.name if schedule.client else "Unknown",
            "client_room": schedule.client.room if schedule.client else "Unknown",

            "carer_name": carer.name if carer else "Unknown",
            "carer_phone": carer.phone if carer else "Unknown",

            "time": f"{schedule.start_time} - {schedule.end_time}",
            "shift_type": schedule.shift_type,
            "notes": schedule.notes,

            "status": schedule.status,
            "status_message": status_message,
            "completed_at": schedule.completed_at
        })

    # Simple summary
    total = len(today_schedules)
    completed = len([s for s in today_schedules if s.status == "completed"])
    happening_now = len([s for s in today_schedules if s.status == "in_progress"])
    upcoming = len([s for s in today_schedules if s.status == "scheduled"])

    return {
        "date": today,
        "care_schedule": care_schedule,
        "summary": {
            "total_today": total,
            "completed": completed,
            "happening_now": happening_now,
            "upcoming": upcoming
        }
    }







@family_router.get("/family/me/schedules/upcoming")
async def get_upcoming_schedules(current_family: dict = Depends(get_current_family),
                                 db: Session = Depends(get_db)):
    logger.info(f"Getting upcoming schedules for family - {current_family['user']['email']}")

    db_family = db.query(User).filter(User.email == current_family["user"]["email"], User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family['user']['email']}")

    # Get assigned client IDs
    assigned_client_ids = [client.id for client in db_family.assigned_clients]

    # Get current date
    today = datetime.now().date().strftime("%Y-%m-%d")

    # Query upcoming schedules
    db_schedules = db.query(DBSchedule).filter(
        DBSchedule.client_id.in_(assigned_client_ids),
        DBSchedule.date >= today,
        DBSchedule.status == "scheduled"
    ).all()

    upcoming_schedules = []
    for schedule in db_schedules:
        # Get carer info from User table
        carer = db.query(User).filter(User.email == schedule.carer_email, User.role == "carer").first()

        upcoming_schedules.append({
            "id": schedule.id,
            "client_id": schedule.client_id,
            "client_name": schedule.client.name if schedule.client else "Unknown",
            "client_room": schedule.client.room if schedule.client else "Unknown",
            "carer_name": carer.name if carer else "Unknown",
            "carer_phone": carer.phone if carer else "Unknown",
            "date": schedule.date,
            "start_time": schedule.start_time,
            "end_time": schedule.end_time,
            "shift_type": schedule.shift_type,
            "status": schedule.status
        })

    # Sort by date and start time
    upcoming_schedules.sort(key=lambda x: (x["date"], x["start_time"]))

    return {"schedules": upcoming_schedules}






@family_router.get("/family/me/schedules/{schedule_id}")
async def get_schedule_by_id(schedule_id: str, current_family: dict = Depends(get_current_family),
                             db: Session = Depends(get_db)):
    logger.info(f"Getting schedule {schedule_id} - {current_family['user']['email']}")

    db_family = db.query(User).filter(User.email == current_family["user"]["email"], User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family['user']['email']}")

    # Get assigned client IDs
    assigned_client_ids = [client.id for client in db_family.assigned_clients]

    # Find the schedule
    db_schedule = db.query(DBSchedule).filter(
        DBSchedule.id == schedule_id,
        DBSchedule.client_id.in_(assigned_client_ids)
    ).first()

    if not db_schedule:
        logger.warning(f"Schedule not found: {schedule_id}")
        raise HTTPException(status_code=404, detail=f"Schedule {schedule_id} not found")

    # Get carer info from User table
    carer = db.query(User).filter(User.email == db_schedule.carer_email, User.role == "carer").first()

    return {
        "id": db_schedule.id,
        "client_id": db_schedule.client_id,
        "client_name": db_schedule.client.name if db_schedule.client else "Unknown",
        "client_room": db_schedule.client.room if db_schedule.client else "Unknown",
        "carer_name": carer.name if carer else "Unknown",
        "carer_phone": carer.phone if carer else "Unknown",
        "carer_email": db_schedule.carer_email,
        "date": db_schedule.date,
        "start_time": db_schedule.start_time,
        "end_time": db_schedule.end_time,
        "shift_type": db_schedule.shift_type,
        "status": db_schedule.status,
        "notes": db_schedule.notes
    }