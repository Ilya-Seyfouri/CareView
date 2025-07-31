import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_manager, logger
from app.database import get_db, log_action
from app.database_models import Client as DBClient, VisitLog as DBVisitLog
from app.models import VisitLog, UpdateVisitLog


router = APIRouter()



#Manager VisitLog routes


@router.post("/manager/client/{client_id}/visit-log")
async def create_visit_log(client_id: str, visitlog: VisitLog,
                           current_manager =  Depends(get_current_manager),
                           db: Session = Depends(get_db)):
    logger.info(f"Creating visit log for client {client_id} - requested by {current_manager.email}")

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



        logger.info(db, current_manager.email, "created", "visit_log", visit_log_id)
        log_action(db, current_manager.email, "created", "visit_log", visit_log_id)

        return {"message": "Visit log created", "id": visit_log_id}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error creating visit log {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error creating visit log: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create visit log")









@router.get("/manager/client/{client_id}/visit-logs")
async def get_client_visit_logs(client_id: str, current_manager = Depends(get_current_manager),
                                db: Session = Depends(get_db)):
    logger.info(f"Getting visit logs for client {client_id} - requested by {current_manager.email}")

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






@router.get("/manager/client/{client_id}/visit-logs/{visit_log_id}")
async def get_specific_visit_log(client_id: str, visit_log_id: str,
                                 current_manager = Depends(get_current_manager),
                                 db: Session = Depends(get_db)):
    logger.info(
        f"Getting visit log {visit_log_id} for client {client_id} - requested by {current_manager.email}")

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






@router.put("/manager/client/{client_id}/visit-log/{visit_log_id}")
async def edit_visit_log(client_id: str, visit_log_id: str, new_data: UpdateVisitLog,
                         current_manager = Depends(get_current_manager),
                         db: Session = Depends(get_db)):
    logger.info(f"Updating visit log {visit_log_id} - requested by {current_manager.email}")

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

        db_visit_log.last_updated_by = current_manager.email
        db_visit_log.last_updated_at = datetime.now()
        db.commit()



        logger.info(db, current_manager.email, "updated","visit_log", visit_log_id)

        return {"success": True, "id": visit_log_id}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error updating visit log {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error updating visit log: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update visit log")


@router.delete("/manager/client/{client_id}/visit-log/{visit_log_id}")
async def delete_visit_log(client_id: str, visit_log_id: str,
                           current_manager = Depends(get_current_manager),
                           db: Session = Depends(get_db)):
    logger.info(f"Deleting visit log {visit_log_id} - requested by {current_manager.email}")

    try:
        db_visit_log = db.query(DBVisitLog).filter(
            DBVisitLog.client_id == client_id,
            DBVisitLog.id == visit_log_id
        ).first()

        if not db_visit_log:
            raise HTTPException(status_code=404, detail=f"Visit log {visit_log_id} not found")

        db.delete(db_visit_log)
        db.commit()



        logger.info(db, current_manager.email, "deleted","visit_log", visit_log_id)

        return {"message": "Visit log deleted"}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error deleting visit log {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error deleting visit log: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete visit log")





