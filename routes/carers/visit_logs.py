import uuid
from datetime import datetime

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_carer,logger
from app.database import get_db, log_action
from app.database_models import User, Client as DBClient, Schedule as DBSchedule, VisitLog as DBVisitLog
from app.models import UpdateCarer, VisitLog, UpdateVisitLog


router = APIRouter()

@router.get("/carer/me/clients/{client_id}/visit-logs")
async def get_client_visit_logs(client_id: str, current_carer = Depends(get_current_carer),
                                db: Session = Depends(get_db)):
    logger.info(f"Getting visit logs for client {client_id} - {current_carer.email}")

    db_carer = db.query(User).filter(User.email == current_carer.email, User.role == "carer").first()
    if not db_carer:
        logger.warning(f"Carer not found: {current_carer.email}")
        raise HTTPException(status_code=404, detail=f"Carer at {current_carer.email} not found")

    db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not db_client:
        logger.warning(f"Client not found: {client_id}")
        raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found")

    # Check if client is assigned to this carer
    if db_client not in db_carer.assigned_clients:
        logger.warning(f"Unauthorized access attempt: {current_carer.email} -> {client_id}")
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







@router.get("/carer/me/clients/{client_id}/visit-logs/{visit_log_id}")
async def get_specific_visit_log(client_id: str, visit_log_id: str,
                                 current_carer = Depends(get_current_carer),
                                 db: Session = Depends(get_db)):
    logger.info(f"Getting visit log {visit_log_id} for client {client_id} - {current_carer.email}")

    db_carer = db.query(User).filter(User.email == current_carer.email, User.role == "carer").first()
    if not db_carer:
        logger.warning(f"Carer not found: {current_carer.email}")
        raise HTTPException(status_code=404, detail=f"Carer at {current_carer.email} not found")

    db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not db_client:
        logger.warning(f"Client not found: {client_id}")
        raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found")

    # Check if client is assigned to this carer
    if db_client not in db_carer.assigned_clients:
        logger.warning(f"Unauthorized access attempt: {current_carer.email} -> {client_id}")
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








@router.post("/carer/me/clients/{client_id}/visit-log")
async def create_visit_log(client_id: str, visitlog: VisitLog,
                           current_carer = Depends(get_current_carer),
                           db: Session = Depends(get_db)):
    logger.info(f"Creating visit log for client {client_id} - {current_carer.email}")

    try:
        db_carer = db.query(User).filter(User.email == current_carer.email, User.role == "carer").first()
        if not db_carer:
            raise HTTPException(status_code=404, detail=f"Carer at {current_carer.email} not found")

        db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found")

        # Check if client is assigned to this carer
        if db_client not in db_carer.assigned_clients:
            logger.warning(f"Unauthorized access attempt: {current_carer.email} -> {client_id}")
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
        log_action(db, current_carer.email, "created", "visit_log", visit_log_id)

        logger.info(f"Visit log created successfully: {visit_log_id}")
        return {"message": "Visit log created", "id": visit_log_id}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating visit log: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create visit log")







@router.put("/carer/me/clients/{client_id}/visit-logs/{visit_log_id}")
async def update_visit_log(client_id: str, visit_log_id: str, new_data: UpdateVisitLog,
                           current_carer = Depends(get_current_carer),
                           db: Session = Depends(get_db)):
    logger.info(f"Updating visit log {visit_log_id} for client {client_id} - {current_carer.email}")

    try:
        db_carer = db.query(User).filter(User.email == current_carer.email, User.role == "carer").first()
        if not db_carer:
            raise HTTPException(status_code=404, detail=f"Carer at {current_carer.email} not found")

        db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail=f"Client with ID {client_id} not found")

        # Check if client is assigned to this carer
        if db_client not in db_carer.assigned_clients:
            logger.warning(f"Unauthorized access attempt: {current_carer.email} -> {client_id}")
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

        db_visit_log.last_updated_by = current_carer.email
        db_visit_log.last_updated_at = datetime.now()
        db.commit()
        log_action(db, current_carer.email, "created", "visit_log", visit_log_id)

        logger.info(f"Visit log updated successfully: {visit_log_id}")
        return {"success": True, "id": visit_log_id}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating visit log: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update visit log {visit_log_id}")


