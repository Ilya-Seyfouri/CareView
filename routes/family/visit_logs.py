from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_family,logger
from app.database import get_db
from app.database_models import User



router = APIRouter()




@router.get("/family/me/clients/visit-logs")
async def get_all_family_visit_logs(current_family = Depends(get_current_family),
                                    db: Session = Depends(get_db)):
    logger.info(f"Getting all visit logs for family - {current_family.email}")

    db_family = db.query(User).filter(User.email == current_family.email, User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family.email}")
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family.email}")

    clients_visit_logs = []
    for client in db_family.assigned_clients:
        visit_log_ids = [visit_log.id for visit_log in client.visit_logs]
        clients_visit_logs.append({
            "client_id": client.id,
            "client_name": client.name,
            "visit_logs": visit_log_ids
        })

    return {"clients_visit_logs": clients_visit_logs}


@router.get("/family/me/clients/{client_id}/visit-logs")
async def get_client_visit_logs(client_id: str, current_family = Depends(get_current_family),
                                db: Session = Depends(get_db)):
    logger.info(f"Getting visit logs for client {client_id} - {current_family.email}")

    db_family = db.query(User).filter(User.email == current_family.email, User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family.email}")
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family.email}")

    # Check if client is assigned to this family member
    db_client = None
    for client in db_family.assigned_clients:
        if client.id == client_id:
            db_client = client
            break

    if not db_client:
        logger.warning(f"Client not assigned to family: {client_id}")
        raise HTTPException(status_code=403, detail=f"Client {client_id} not assigned to family member")

    # Get visit logs for this specific client
    visit_logs = []
    for log in db_client.visit_logs:
        visit_logs.append({
            "id": log.id,
            "carer_name": log.carer_name,
            "carer_number": log.carer_number,
            "date": log.date,
            "personal_care_completed": log.personal_care_completed,
            "care_reminders_provided": log.care_reminders_provided,
            "toilet": log.toilet,
            "changed_clothes": log.changed_clothes,
            "ate_food": log.ate_food,
            "notes": log.notes,
            "mood": log.mood
        })

    return {"client_id": client_id, "visit_logs": visit_logs}







@router.get("/family/me/visit-logs/{visit_log_id}")
async def get_specific_visit_log(visit_log_id: str, current_family = Depends(get_current_family),
                                 db: Session = Depends(get_db)):
    logger.info(f"Getting visit log {visit_log_id} - {current_family.email}")

    db_family = db.query(User).filter(User.email == current_family.email, User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family.email}")
        raise HTTPException(status_code=404, detail=f"Family member not found: {current_family.email}")

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



