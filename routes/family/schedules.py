from datetime import datetime

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_family,logger
from app.database import get_db
from app.database_models import User, Schedule as DBSchedule


router = APIRouter()

@router.get("/family/me/schedules")
async def get_client_schedules(current_family = Depends(get_current_family),
                               db: Session = Depends(get_db)):
    logger.info(f"Getting schedules for family - {current_family.email}")

    db_family = db.query(User).filter(User.email == current_family.email, User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family.email}")
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family.email}")

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








@router.get("/family/me/today")
async def get_todays_care_schedule(current_family = Depends(get_current_family),
                                   db: Session = Depends(get_db)):
    logger.info(f"Getting today's care schedule for family - {current_family.email}")

    db_family = db.query(User).filter(User.email == current_family.email, User.role == "family").first()
    if not db_family:
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family.email}")

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







@router.get("/family/me/schedules/upcoming")
async def get_upcoming_schedules(current_family = Depends(get_current_family),
                                 db: Session = Depends(get_db)):
    logger.info(f"Getting upcoming schedules for family - {current_family.email}")

    db_family = db.query(User).filter(User.email == current_family.email, User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family.email}")
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family.email}")

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






@router.get("/family/me/schedules/{schedule_id}")
async def get_schedule_by_id(schedule_id: str, current_family = Depends(get_current_family),
                             db: Session = Depends(get_db)):
    logger.info(f"Getting schedule {schedule_id} - {current_family.email}")

    db_family = db.query(User).filter(User.email == current_family.email, User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family.email}")
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family.email}")

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