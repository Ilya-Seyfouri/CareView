from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_family,logger
from app.database import get_db
from app.database_models import User, Client as DBClient


router = APIRouter()





@router.get("/family/me/clients")
async def get_family_clients(current_family = Depends(get_current_family),
                             db: Session = Depends(get_db)):
    logger.info(f"Getting family clients - {current_family.email}")

    db_family = db.query(User).filter(User.email == current_family.email, User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family.email}")
        raise HTTPException(status_code=404, detail=f"Family member at {current_family.email} not found")

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





@router.get("/family/me/clients/{client_id}")
async def get_family_client_by_id(client_id: str, current_family = Depends(get_current_family),
                                  db: Session = Depends(get_db)):
    logger.info(f"Getting client {client_id} - {current_family.email}")

    db_family = db.query(User).filter(User.email == current_family.email, User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family.email}")
        raise HTTPException(status_code=404, detail=f"Family member at {current_family.email} not found")

    db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not db_client:
        logger.warning(f"Client not found: {client_id}")
        raise HTTPException(status_code=404, detail=f"Client {client_id} not found")

    # Check if client is assigned to this family member
    if db_client not in db_family.assigned_clients:
        logger.warning(f"Unauthorized access attempt: {['email']} -> {client_id}")
        raise HTTPException(status_code=403,
                            detail=f"Client {client_id} not assigned to family member {current_family.email}")

    return {
        "id": db_client.id,
        "name": db_client.name,
        "age": db_client.age,
        "room": db_client.room,
        "date_of_birth": db_client.date_of_birth,
        "support_needs": db_client.support_needs
    }


