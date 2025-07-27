from datetime import datetime

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_carer,logger
from app.database import get_db
from app.database_models import Schedule as DBSchedule

router = APIRouter()




@router.get("/carer/me/schedules")
async def get_my_schedules(current_carer = Depends(get_current_carer),
                           db: Session = Depends(get_db)):
    logger.info(f"Getting schedules - {current_carer.email}")

    carer_email = current_carer.email

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






@router.get("/carer/me/schedules/{schedule_id}")
async def get_my_schedule_by_id(schedule_id: str, current_carer = Depends(get_current_carer),
                                db: Session = Depends(get_db)):
    logger.info(f"Getting schedule {schedule_id} - {current_carer.email}")

    carer_email = current_carer.email

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






@router.put("/carer/me/schedules/{schedule_id}/status")
async def update_schedule_status(schedule_id: str, new_status: str,
                                 current_carer = Depends(get_current_carer),
                                 db: Session = Depends(get_db)):
    logger.info(f"Updating schedule {schedule_id} status to {new_status} - {current_carer.email}")

    try:
        carer_email = current_carer.email

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