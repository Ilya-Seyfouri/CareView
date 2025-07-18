import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_manager, logger
from app.database2 import get_db, log_action
from app.database_models import User, Client as DBClient, Schedule as DBSchedule, VisitLog as DBVisitLog
from app.models import VisitLog, UpdateVisitLog,UpdateSchedule, CreateSchedule


manager_operations_router = APIRouter()



#Manager VisitLog routes


@manager_operations_router.post("/manager/client/{client_id}/visit-log")
async def create_visit_log(client_id: str, visitlog: VisitLog,
                           current_manager: dict = Depends(get_current_manager),
                           db: Session = Depends(get_db)):
    logger.info(f"Creating visit log for client {client_id} - requested by {current_manager['user']['email']}")

    try:
        db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail=f"Client {client_id} not found")

        # Generate automatic ID
        visit_log_id = f"VL{str(uuid.uuid4())[:8].upper()}"

        # Ensure ID is unique
        while db.query(DBVisitLog).filter(DBVisitLog.id == visit_log_id).first():
            visit_log_id = f"VL{str(uuid.uuid4())[:8].upper()}"

        # Create visit log
        new_visit_log = DBVisitLog(
            id=visit_log_id,
            client_id=client_id,
            carer_name=visitlog.carer_name,
            carer_number=visitlog.carer_number,
            date=visitlog.date,
            personal_care_completed=visitlog.personal_care_completed,
            care_reminders_provided=visitlog.care_reminders_provided,
            toilet=visitlog.toilet,
            changed_clothes=visitlog.changed_clothes,
            ate_food=visitlog.ate_food,
            notes=visitlog.notes,
            mood=visitlog.mood
        )

        db.add(new_visit_log)
        db.commit()



        logger.info(f"Visit log created successfully: {visit_log_id}")
        log_action(db, current_manager['user']['email'], "created","visit_log", visit_log_id)

        return {"message": "Visit log created", "id": visit_log_id}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating visit log: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create visit log")






@manager_operations_router.get("/manager/client/{client_id}/visit-logs")
async def get_client_visit_logs(client_id: str, current_manager: dict = Depends(get_current_manager),
                                db: Session = Depends(get_db)):
    logger.info(f"Getting visit logs for client {client_id} - requested by {current_manager['user']['email']}")

    db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not db_client:
        logger.warning(f"Client not found: {client_id}")
        raise HTTPException(status_code=404, detail=f"Client {client_id} not found")

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






@manager_operations_router.get("/manager/client/{client_id}/visit-logs/{visit_log_id}")
async def get_specific_visit_log(client_id: str, visit_log_id: str,
                                 current_manager: dict = Depends(get_current_manager),
                                 db: Session = Depends(get_db)):
    logger.info(
        f"Getting visit log {visit_log_id} for client {client_id} - requested by {current_manager['user']['email']}")

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
        "date": db_visit_log.date,
        "personal_care_completed": db_visit_log.personal_care_completed,
        "care_reminders_provided": db_visit_log.care_reminders_provided,
        "toilet": db_visit_log.toilet,
        "changed_clothes": db_visit_log.changed_clothes,
        "ate_food": db_visit_log.ate_food,
        "notes": db_visit_log.notes,
        "mood": db_visit_log.mood
    }






@manager_operations_router.put("/manager/client/{client_id}/visit-log/{visit_log_id}")
async def edit_visit_log(client_id: str, visit_log_id: str, new_data: UpdateVisitLog,
                         current_manager: dict = Depends(get_current_manager),
                         db: Session = Depends(get_db)):
    logger.info(f"Updating visit log {visit_log_id} - requested by {current_manager['user']['email']}")

    try:
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

        db_visit_log.last_updated_by = current_manager["user"]["email"]
        db_visit_log.last_updated_at = datetime.now()
        db.commit()



        logger.info(f"Visit log updated successfully: {visit_log_id}")
        log_action(db, current_manager['user']['email'], "updated","visit_log", visit_log_id)

        return {"success": True, "id": visit_log_id}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating visit log: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update visit log")






@manager_operations_router.delete("/manager/client/{client_id}/visit-log/{visit_log_id}")
async def delete_visit_log(client_id: str, visit_log_id: str,
                           current_manager: dict = Depends(get_current_manager),
                           db: Session = Depends(get_db)):
    logger.info(f"Deleting visit log {visit_log_id} - requested by {current_manager['user']['email']}")

    try:
        db_visit_log = db.query(DBVisitLog).filter(
            DBVisitLog.client_id == client_id,
            DBVisitLog.id == visit_log_id
        ).first()

        if not db_visit_log:
            raise HTTPException(status_code=404, detail=f"Visit log {visit_log_id} not found")

        db.delete(db_visit_log)
        db.commit()



        logger.info(f"Visit log deleted successfully: {visit_log_id}")
        log_action(db, current_manager['user']['email'], "deleted","visit_log", visit_log_id)

        return {"message": "Visit log deleted"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting visit log: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete visit log {visit_log_id}")





#Manager Schedule Routes





@manager_operations_router.get("/manager/schedules")
async def get_all_schedules(current_manager: dict = Depends(get_current_manager),
                            db: Session = Depends(get_db)):
    logger.info(f"Getting all schedules - requested by {current_manager['user']['email']}")

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





@manager_operations_router.get("/manager/schedules/{schedule_id}")
async def get_schedule(schedule_id: str, current_manager: dict = Depends(get_current_manager),
                       db: Session = Depends(get_db)):
    logger.info(f"Getting schedule {schedule_id} - requested by {current_manager['user']['email']}")

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




@manager_operations_router.post("/manager/schedules")
async def create_schedule(schedule_data: CreateSchedule,
                          current_manager: dict = Depends(get_current_manager),
                          db: Session = Depends(get_db)):
    logger.info(f"Creating schedule - requested by {current_manager['user']['email']}")

    try:
        # Validate carer and client exist
        db_carer = db.query(User).filter(User.email == schedule_data.carer_email).first()
        db_client = db.query(DBClient).filter(DBClient.id == schedule_data.client_id).first()

        if not db_carer:
            raise HTTPException(status_code=404, detail=f"Carer {schedule_data.carer_email} not found")
        if not db_client:
            raise HTTPException(status_code=404, detail=f"Client {schedule_data.client_id} not found")

        # Check for schedule conflict


        # Create schedule
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
        log_action(db, current_manager['user']['email'], "created","schedule", schedule_id)

        return {"message": "Schedule created", "schedule_id": schedule_id}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create schedule")






@manager_operations_router.put("/manager/schedules/{schedule_id}")
async def update_schedule(schedule_id: str, update_data: UpdateSchedule,
                          current_manager: dict = Depends(get_current_manager),
                          db: Session = Depends(get_db)):
    logger.info(f"Updating schedule {schedule_id} - requested by {current_manager['user']['email']}")

    try:
        db_schedule = db.query(DBSchedule).filter(DBSchedule.id == schedule_id).first()
        if not db_schedule:
            raise HTTPException(status_code=404, detail=f"Schedule {schedule_id} not found")

        update_fields = update_data.dict(exclude_unset=True)

        # Validate carer if being updated
        if "carer_email" in update_fields:
            if not db.query(User).filter(User.email == update_fields["carer_email"]).first():
                raise HTTPException(status_code=404, detail=f"Carer {update_fields["carer_email"]} not found")

        # Validate client if being updated
        if "client_id" in update_fields:
            if not db.query(DBClient).filter(DBClient.id == update_fields["client_id"]).first():
                raise HTTPException(status_code=404, detail=f"Client {update_fields["client_id"]} not found")



        # Update fields
        for field, value in update_fields.items():
            if hasattr(db_schedule, field):
                setattr(db_schedule, field, value)

        db.commit()


        logger.info(f"Schedule updated successfully: {schedule_id}")
        return {"message": "Schedule updated", "schedule_id": schedule_id}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating schedule: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update schedule")







@manager_operations_router.delete("/manager/schedules/{schedule_id}")
async def delete_schedule(schedule_id: str, current_manager: dict = Depends(get_current_manager),
                          db: Session = Depends(get_db)):
    logger.info(f"Deleting schedule {schedule_id} - requested by {current_manager['user']['email']}")

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
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting schedule: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete schedule {schedule_id}")