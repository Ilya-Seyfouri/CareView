from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_carer,logger
from app.database import get_db
from app.database_models import User, Client as DBClient

router = APIRouter()




@router.get("/carer/me/clients")
async def get_assigned_clients(current_carer = Depends(get_current_carer),
                               db: Session = Depends(get_db)):
    logger.info(f"Getting assigned clients - {current_carer.email}")

    db_carer = db.query(User).filter(User.email == current_carer.email, User.role == "carer").first()
    if not db_carer:
        logger.warning(f"Carer not found: {current_carer.email}")
        raise HTTPException(status_code=404, detail=f"Carer at {current_carer.email} not found")

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


@router.get("/carer/me/clients/{client_id}")
async def get_assigned_client_by_id(client_id: str, current_carer = Depends(get_current_carer),
                                    db: Session = Depends(get_db)):
    logger.info(f"Getting client {client_id} - {current_carer.email}")

    db_carer = db.query(User).filter(User.email == current_carer.email, User.role == "carer").first()
    if not db_carer:
        logger.warning(f"Carer not found: {current_carer.email}")
        raise HTTPException(status_code=404, detail=f"Carer at {current_carer.email} not found")

    db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not db_client:
        logger.warning(f"Client not found: {client_id}")
        raise HTTPException(status_code=404, detail=f"Client ID of {client_id} not found")

    # Check if client is assigned to this carer
    if db_client not in db_carer.assigned_clients:
        logger.warning(f"Unauthorized access attempt: {current_carer.email} -> {client_id}")
        raise HTTPException(status_code=403, detail=f"Client ID {client_id} not assigned to you")

    return {
        "id": db_client.id,
        "name": db_client.name,
        "age": db_client.age,
        "room": db_client.room,
        "date_of_birth": db_client.date_of_birth,
        "support_needs": db_client.support_needs
    }

