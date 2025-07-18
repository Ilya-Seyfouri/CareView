import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_carer,logger
from app.database2 import get_db, hash_password
from app.database_models import User, Client as DBClient, Schedule as DBSchedule, VisitLog as DBVisitLog
from app.models import UpdateCarer, VisitLog, UpdateVisitLog



carer_router = APIRouter()



#Carer Routes

@carer_router.get("/carer/me")
async def get_carer_details(current_carer: dict = Depends(get_current_carer),
                            db: Session = Depends(get_db)):
    logger.info(f"Getting carer details - {current_carer['user']['email']}")

    db_carer = db.query(User).filter(User.email == current_carer["user"]["email"], User.role == "carer").first()
    if not db_carer:
        logger.warning(f"Carer not found: {current_carer['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Carer at {current_carer['user']['email']} not found")

    return {
        "email": db_carer.email,
        "name": db_carer.name,
        "phone": db_carer.phone,
        "assigned_clients": [client.id for client in db_carer.assigned_clients],
    }





@carer_router.put("/carer/me")
async def update_carer(new_data: UpdateCarer, current_carer: dict = Depends(get_current_carer),
                       db: Session = Depends(get_db)):
    logger.info(f"Updating carer profile - {current_carer['user']['email']}")

    try:
        db_carer = db.query(User).filter(User.email == current_carer["user"]["email"], User.role == "carer").first()
        if not db_carer:
            raise HTTPException(status_code=404, detail=f"Carer at {current_carer['user']['email']} not found")

        update_data = new_data.dict(exclude_unset=True)

        # Regular update
        for field, value in update_data.items():
            if field == "password":
                db_carer.password_hash = hash_password(value)
            elif hasattr(db_carer, field):
                setattr(db_carer, field, value)

        db.commit()
        logger.info(f"Carer profile updated successfully: {current_carer['user']['email']}")
        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating carer profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update profile")





@carer_router.get("/carer/dashboard")
async def get_carer_dashboard(current_carer: dict = Depends(get_current_carer),
                              db: Session = Depends(get_db)):
    logger.info(f"Getting carer dashboard - {current_carer['user']['email']}")

    carer_email = current_carer["user"]["email"]

    # Get today's schedules
    today = datetime.now().date()
    today_schedules = db.query(DBSchedule).filter(
        DBSchedule.carer_email == carer_email,
        DBSchedule.date == today.strftime('%Y-%m-%d')
    ).all()

    # Calculate progress
    total_visits = len(today_schedules)
    completed_visits = len([s for s in today_schedules if s.status == "completed"])

    # Get assigned clients count
    db_carer = db.query(User).filter(User.email == carer_email, User.role == "carer").first()
    assigned_clients = len(db_carer.assigned_clients) if db_carer else 0

    return {
        "stats": {
            "assigned_clients": assigned_clients,
            "total_visits_today": total_visits,
            "completed_visits": completed_visits,
            "remaining_visits": total_visits - completed_visits
        },
        "today_schedules": [
            {
                "id": s.id,
                "client_id": s.client_id,
                "client_name": s.client.name if s.client else "Unknown",
                "start_time": s.start_time,
                "end_time": s.end_time,
                "status": s.status
            } for s in today_schedules
        ]
    }






#Client Carer Routes





@carer_router.get("/carer/me/clients")
async def get_assigned_clients(current_carer: dict = Depends(get_current_carer),
                               db: Session = Depends(get_db)):
    logger.info(f"Getting assigned clients - {current_carer['user']['email']}")

    db_carer = db.query(User).filter(User.email == current_carer["user"]["email"], User.role == "carer").first()
    if not db_carer:
        logger.warning(f"Carer not found: {current_carer['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Carer at {current_carer['user']['email']} not found")

    clients_list = []
    for client in db_carer.assigned_clients:
        clients_list.append({
            "id": client.id,
            "name": client.name,
            "age": client.age,
            "room": client.room,
            "support_needs": client.support_needs
        })

    return {"clients": clients_list}


@carer_router.get("/carer/me/clients/{client_id}")
async def get_assigned_client_by_id(client_id: str, current_carer: dict = Depends(get_current_carer),
                                    db: Session = Depends(get_db)):
    logger.info(f"Getting client {client_id} - {current_carer['user']['email']}")

    db_carer = db.query(User).filter(User.email == current_carer["user"]["email"], User.role == "carer").first()
    if not db_carer:
        logger.warning(f"Carer not found: {current_carer['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Carer at {current_carer['user']['email']} not found")

    db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not db_client:
        logger.warning(f"Client not found: {client_id}")
        raise HTTPException(status_code=404, detail=f"Client ID of {client_id} not found")

    # Check if client is assigned to this carer
    if db_client not in db_carer.assigned_clients:
        logger.warning(f"Unauthorized access attempt: {current_carer['user']['email']} -> {client_id}")
        raise HTTPException(status_code=403, detail=f"Client ID {client_id} not assigned to you")

    return {
        "id": db_client.id,
        "name": db_client.name,
        "age": db_client.age,
        "room": db_client.room,
        "date_of_birth": db_client.date_of_birth,
        "support_needs": db_client.support_needs
    }




#Visit Log Carer Routes

@carer_router.get("/carer/me/clients/{client_id}/visit-logs")
async def get_client_visit_logs(client_id: str, current_carer: dict = Depends(get_current_carer),
                                db: Session = Depends(get_db)):
    logger.info(f"Getting visit logs for client {client_id} - {current_carer['user']['email']}")

    db_carer = db.query(User).filter(User.email == current_carer["user"]["email"], User.role == "carer").first()
    if not db_carer:
        logger.warning(f"Carer not found: {current_carer['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Carer at {current_carer['user']['email']} not found")

    db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not db_client:
        logger.warning(f"Client not found: {client_id}")
        raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found")

    # Check if client is assigned to this carer
    if db_client not in db_carer.assigned_clients:
        logger.warning(f"Unauthorized access attempt: {current_carer['user']['email']} -> {client_id}")
        raise HTTPException(status_code=403,
                            detail=f"Client {client_id} is not assigned to {current_carer['user']['name']}")

    visit_logs = []
    for log in db_client.visit_logs:
        visit_logs.append({
            "id": log.id,
            "carer_name": log.carer_name,
            "date": log.date,
            "personal_care_completed": log.personal_care_completed,
            "notes": log.notes
        })

    return {"client_id": client_id, "visit_logs": visit_logs}







@carer_router.get("/carer/me/clients/{client_id}/visit-logs/{visit_log_id}")
async def get_specific_visit_log(client_id: str, visit_log_id: str,
                                 current_carer: dict = Depends(get_current_carer),
                                 db: Session = Depends(get_db)):
    logger.info(f"Getting visit log {visit_log_id} for client {client_id} - {current_carer['user']['email']}")

    db_carer = db.query(User).filter(User.email == current_carer["user"]["email"], User.role == "carer").first()
    if not db_carer:
        logger.warning(f"Carer not found: {current_carer['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Carer at {current_carer['user']['email']} not found")

    db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not db_client:
        logger.warning(f"Client not found: {client_id}")
        raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found")

    # Check if client is assigned to this carer
    if db_client not in db_carer.assigned_clients:
        logger.warning(f"Unauthorized access attempt: {current_carer['user']['email']} -> {client_id}")
        raise HTTPException(status_code=403,
                            detail=f"Client {client_id} is not assigned to {current_carer['user']['name']}")

    db_visit_log = db.query(DBVisitLog).filter(
        DBVisitLog.client_id == client_id,
        DBVisitLog.id == visit_log_id
    ).first()

    if not db_visit_log:
        logger.warning(f"Visit log not found: {visit_log_id}")
        raise HTTPException(status_code=404, detail=f"Visit log {visit_log_id} not found")

    return {
        "id": db_visit_log.id,
        "client_id": client_id,
        "carer_name": db_visit_log.carer_name,
        "carer_number": db_visit_log.carer_number,
        "date": db_visit_log.date,
        "personal_care_completed": db_visit_log.personal_care_completed,
        "care_reminders_provided": db_visit_log.care_reminders_provided,
        "toilet": db_visit_log.toilet,
        "changed_clothes": db_visit_log.changed_clothes,
        "ate_food": db_visit_log.ate_food,
        "notes": db_visit_log.notes,
        "mood": db_visit_log.mood
    }








@carer_router.post("/carer/me/clients/{client_id}/visit-log")
async def create_visit_log(client_id: str, visitlog: VisitLog,
                           current_carer: dict = Depends(get_current_carer),
                           db: Session = Depends(get_db)):
    logger.info(f"Creating visit log for client {client_id} - {current_carer['user']['email']}")

    try:
        db_carer = db.query(User).filter(User.email == current_carer["user"]["email"], User.role == "carer").first()
        if not db_carer:
            raise HTTPException(status_code=404, detail=f"Carer at {current_carer['user']['email']} not found")

        db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found")

        # Check if client is assigned to this carer
        if db_client not in db_carer.assigned_clients:
            logger.warning(f"Unauthorized access attempt: {current_carer['user']['email']} -> {client_id}")
            raise HTTPException(status_code=403,
                                detail=f"Client {client_id} is not assigned to {current_carer['user']['name']}")

        # Generate automatic ID
        visit_log_id = f"VL{str(uuid.uuid4())[:8].upper()}"

        while db.query(DBVisitLog).filter(DBVisitLog.id == visit_log_id).first():
            visit_log_id = f"VL{str(uuid.uuid4())[:8].upper()}"

        # Create visit log
        new_visit_log = DBVisitLog(
            id=visit_log_id,
            client_id=client_id,
            carer_name=current_carer["user"]["name"],
            carer_number=current_carer["user"]["phone"],
            date=visitlog.date,
            personal_care_completed=visitlog.personal_care_completed,
            care_reminders_provided=visitlog.care_reminders_provided,
            toilet=visitlog.toilet,
            changed_clothes=visitlog.changed_clothes,
            ate_food=visitlog.ate_food,
            notes=visitlog.notes,
            mood=visitlog.mood or [],
        )

        db.add(new_visit_log)
        db.commit()

        logger.info(f"Visit log created successfully: {visit_log_id}")
        return {"message": "Visit log created", "id": visit_log_id}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating visit log: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create visit log")







@carer_router.put("/carer/me/clients/{client_id}/visit-logs/{visit_log_id}")
async def update_visit_log(client_id: str, visit_log_id: str, new_data: UpdateVisitLog,
                           current_carer: dict = Depends(get_current_carer),
                           db: Session = Depends(get_db)):
    logger.info(f"Updating visit log {visit_log_id} for client {client_id} - {current_carer['user']['email']}")

    try:
        db_carer = db.query(User).filter(User.email == current_carer["user"]["email"], User.role == "carer").first()
        if not db_carer:
            raise HTTPException(status_code=404, detail=f"Carer at {current_carer['user']['email']} not found")

        db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found")

        # Check if client is assigned to this carer
        if db_client not in db_carer.assigned_clients:
            logger.warning(f"Unauthorized access attempt: {current_carer['user']['email']} -> {client_id}")
            raise HTTPException(status_code=403,
                                detail=f"Client {client_id} is not assigned to {current_carer['user']['name']}")

        db_visit_log = db.query(DBVisitLog).filter(
            DBVisitLog.id == visit_log_id,
            DBVisitLog.client_id == client_id
        ).first()

        if not db_visit_log:
            raise HTTPException(status_code=404, detail=f"Visit log {visit_log_id} not found")

        update_data = new_data.dict(exclude_unset=True)

        # Update fields
        for field, value in update_data.items():
            if hasattr(db_visit_log, field):
                setattr(db_visit_log, field, value)

        db_visit_log.last_updated_by = current_carer["user"]["email"]
        db_visit_log.last_updated_at = datetime.now()
        db.commit()

        logger.info(f"Visit log updated successfully: {visit_log_id}")
        return {"success": True, "id": visit_log_id}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating visit log: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update visit log {visit_log_id}")






#Carer Schedule Routes



@carer_router.get("/carer/me/schedules")
async def get_my_schedules(current_carer: dict = Depends(get_current_carer),
                           db: Session = Depends(get_db)):
    logger.info(f"Getting schedules - {current_carer['user']['email']}")

    carer_email = current_carer["user"]["email"]

    # Query schedules for this carer
    db_schedules = db.query(DBSchedule).filter(DBSchedule.carer_email == carer_email).all()

    schedules_list = []
    for schedule in db_schedules:
        schedules_list.append({
            "id": schedule.id,
            "client_id": schedule.client_id,
            "client_name": schedule.client.name if schedule.client else "Unknown",
            "client_room": schedule.client.room if schedule.client else "Unknown",
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






@carer_router.get("/carer/me/schedules/{schedule_id}")
async def get_my_schedule_by_id(schedule_id: str, current_carer: dict = Depends(get_current_carer),
                                db: Session = Depends(get_db)):
    logger.info(f"Getting schedule {schedule_id} - {current_carer['user']['email']}")

    carer_email = current_carer["user"]["email"]

    db_schedule = db.query(DBSchedule).filter(
        DBSchedule.id == schedule_id,
        DBSchedule.carer_email == carer_email
    ).first()

    if not db_schedule:
        logger.warning(f"Schedule not found: {schedule_id}")
        raise HTTPException(status_code=404, detail=f"Schedule {schedule_id} not found")

    return {
        "id": db_schedule.id,
        "client_id": db_schedule.client_id,
        "client_name": db_schedule.client.name if db_schedule.client else "Unknown",
        "client_room": db_schedule.client.room if db_schedule.client else "Unknown",
        "client_support_needs": db_schedule.client.support_needs if db_schedule.client else "Unknown",
        "date": db_schedule.date,
        "start_time": db_schedule.start_time,
        "end_time": db_schedule.end_time,
        "shift_type": db_schedule.shift_type,
        "status": db_schedule.status,
        "notes": db_schedule.notes,
    }






@carer_router.put("/carer/me/schedules/{schedule_id}/status")
async def update_schedule_status(schedule_id: str, new_status: str,
                                 current_carer: dict = Depends(get_current_carer),
                                 db: Session = Depends(get_db)):
    logger.info(f"Updating schedule {schedule_id} status to {new_status} - {current_carer['user']['email']}")

    try:
        carer_email = current_carer["user"]["email"]

        db_schedule = db.query(DBSchedule).filter(
            DBSchedule.id == schedule_id,
            DBSchedule.carer_email == carer_email
        ).first()

        if not db_schedule:
            raise HTTPException(status_code=404, detail=f"Schedule {schedule_id} not found")

        # Validate status
        valid_statuses = ["scheduled", "in_progress", "completed", "cancelled"]
        if new_status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

        db_schedule.status = new_status

        # Set completion time if completed
        if new_status == "completed":
            db_schedule.completed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        db.commit()

        logger.info(f"Schedule status updated successfully: {schedule_id} -> {new_status}")
        return {
            "message": f"Schedule status updated to {new_status}",
            "schedule_id": schedule_id,
            "new_status": new_status
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating schedule status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update schedule status of {schedule_id}")