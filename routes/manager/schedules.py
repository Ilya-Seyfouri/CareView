import uuid

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_manager, logger
from app.database import get_db, log_action
from app.database_models import User, Client as DBClient, Schedule as DBSchedule
from app.models import UpdateSchedule, CreateSchedule



router = APIRouter()



@router.get("/manager/schedules")
async def get_all_schedules(current_manager  = Depends(get_current_manager),
                            db: Session = Depends(get_db)):
    logger.info(f"Getting all schedules - requested by {current_manager.email}")

    schedules = db.query(DBSchedule).all()

    schedules_list = []
    for schedule in schedules:
        schedules_list.append({
            "id": schedule.id,
            "carer_email": schedule.carer_email,
            "client_id": schedule.client_id,
            "date": schedule.date,
            "start_time": schedule.start_time,
            "end_time": schedule.end_time,
            "shift_type": schedule.shift_type,
            "status": schedule.status,
            "notes": schedule.notes
        })

    return {"schedules": schedules_list}





@router.get("/manager/schedules/{schedule_id}")
async def get_schedule(schedule_id: str, current_manager = Depends(get_current_manager),
                       db: Session = Depends(get_db)):
    logger.info(f"Getting schedule {schedule_id} - requested by {current_manager.email}")

    db_schedule = db.query(DBSchedule).filter(DBSchedule.id == schedule_id).first()
    if not db_schedule:
        logger.warning(f"Schedule not found: {schedule_id}")
        raise HTTPException(status_code=404, detail=f"Schedule {schedule_id} not found")

    return {
        "id": db_schedule.id,
        "carer_email": db_schedule.carer_email,
        "client_id": db_schedule.client_id,
        "date": db_schedule.date,
        "start_time": db_schedule.start_time,
        "end_time": db_schedule.end_time,
        "shift_type": db_schedule.shift_type,
        "status": db_schedule.status,
        "notes": db_schedule.notes,
    }


@router.post("/manager/schedules")
async def create_schedule(schedule_data: CreateSchedule,
                          current_manager = Depends(get_current_manager),
                          db: Session = Depends(get_db)):
    logger.info(f"Creating schedule - requested by {current_manager.email}")

    try:
        # Validate carer and client exist
        db_carer = db.query(User).filter(User.email == schedule_data.carer_email).first()
        db_client = db.query(DBClient).filter(DBClient.id == schedule_data.client_id).first()

        if not db_carer:
            raise HTTPException(status_code=404, detail=f"Carer {schedule_data.carer_email} not found")
        if not db_client:
            raise HTTPException(status_code=404, detail=f"Client {schedule_data.client_id} not found")

        # ===== SCHEDULE CONFLICT PREVENTION =====
        # Check for existing schedules on the same date for this carer
        existing_schedules = db.query(DBSchedule).filter(
            DBSchedule.carer_email == schedule_data.carer_email,
            DBSchedule.date == schedule_data.date,
            DBSchedule.status.in_(["scheduled", "in_progress"])  # Don't check cancelled/completed
        ).all()

        # Check for time overlaps
        for existing in existing_schedules:
            # Convert times to comparable format (assuming HH:MM format)
            new_start = schedule_data.start_time
            new_end = schedule_data.end_time
            existing_start = existing.start_time
            existing_end = existing.end_time

            # Check if times overlap
            # Overlap occurs if: new_start < existing_end AND new_end > existing_start
            if new_start < existing_end and new_end > existing_start:
                raise HTTPException(
                    status_code=409,
                    detail=f"Schedule conflict: Carer {schedule_data.carer_email} already scheduled {existing_start}-{existing_end} on {schedule_data.date}"
                )

        # ===== END CONFLICT PREVENTION =====

        # Create schedule (rest of your existing code)
        schedule_id = f"SCH{str(uuid.uuid4())[:8].upper()}"
        new_schedule = DBSchedule(
            id=schedule_id,
            carer_email=schedule_data.carer_email,
            client_id=schedule_data.client_id,
            date=schedule_data.date,
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time,
            shift_type=schedule_data.shift_type,
            notes=schedule_data.notes,
        )

        db.add(new_schedule)
        db.commit()

        logger.info(f"Schedule created successfully: {schedule_id}")
        log_action(db, current_manager.email, "created", "schedule", schedule_id)

        return {"message": "Schedule created", "schedule_id": schedule_id}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error creating schedule: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Validation error creating schedule: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"Database error creating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error creating schedule: {str(e)}")


@router.put("/manager/schedules/{schedule_id}")
async def update_schedule(schedule_id: str, update_data: UpdateSchedule,
                          current_manager = Depends(get_current_manager),
                          db: Session = Depends(get_db)):
    logger.info(f"Updating schedule {schedule_id} - requested by {current_manager.email}")

    try:
        db_schedule = db.query(DBSchedule).filter(DBSchedule.id == schedule_id).first()
        if not db_schedule:
            raise HTTPException(status_code=404, detail=f"Schedule {schedule_id} not found")

        update_fields = update_data.dict(exclude_unset=True)

        # Validate carer if being updated
        if "carer_email" in update_fields:
            if not db.query(User).filter(User.email == update_fields['carer_email']).first():
                raise HTTPException(status_code=404, detail=f"Carer {update_fields['carer_email']} not found")

        # Validate client if being updated
        if "client_id" in update_fields:
            if not db.query(DBClient).filter(DBClient.id == update_fields['client_id']).first():
                raise HTTPException(status_code=404, detail=f"Client {update_fields['client_id']} not found")



        # Update fields
        for field, value in update_fields.items():
            if hasattr(db_schedule, field):
                setattr(db_schedule, field, value)

        db.commit()


        logger.info(f"Schedule updated successfully: {schedule_id}")
        return {"message": "Schedule updated", "schedule_id": schedule_id}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error updating schedule {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error updating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update schedule")







@router.delete("/manager/schedules/{schedule_id}")
async def delete_schedule(schedule_id: str, current_manager = Depends(get_current_manager),
                          db: Session = Depends(get_db)):
    logger.info(f"Deleting schedule {schedule_id} - requested by {current_manager.email}")

    try:
        db_schedule = db.query(DBSchedule).filter(DBSchedule.id == schedule_id).first()
        if not db_schedule:
            raise HTTPException(status_code=404, detail=f"Schedule {schedule_id} not found")

        db.delete(db_schedule)
        db.commit()

        logger.info(f"Schedule deleted successfully: {schedule_id}")
        return {"message": "Schedule deleted"}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error deleting schedule {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error deleting schedule: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete schedule")



