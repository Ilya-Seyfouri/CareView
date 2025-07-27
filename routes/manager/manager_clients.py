import uuid

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_manager, logger
from app.database import get_db
from app.database_models import Client as DBClient
from app.models import Client, UpdateClient


router = APIRouter()



@router.post("/manager/create/client")
async def create_client(client: Client, current_manager = Depends(get_current_manager),
                        db: Session = Depends(get_db)):
    logger.info(f"Creating client {client.name} - requested by {current_manager.email}")

    try:
        # Generate automatic ID
        client_id = f"C{str(uuid.uuid4())[:8].upper()}"

        # Ensure ID is unique
        while db.query(DBClient).filter(DBClient.id == client_id).first():
            client_id = f"C{str(uuid.uuid4())[:8].upper()}"

        # Create client
        db_client = DBClient(
            id=client_id,
            name=client.name,
            age=client.age,
            room=client.room,
            date_of_birth=client.date_of_birth,
            support_needs=client.support_needs
        )

        db.add(db_client)
        db.commit()

        logger.info(f"Client created successfully: {client_id}")
        return {"message": "Client created", "id": client_id}

    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error creating client {client.id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error creating client {client.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create client")





@router.get("/manager/clients")
async def get_all_clients(current_manager = Depends(get_current_manager),
                          db: Session = Depends(get_db)):
    logger.info(f"Getting all clients - requested by {current_manager.email}")

    clients = db.query(DBClient).all()
    clients_list = []
    for client in clients:
        clients_list.append({
            "id": client.id,
            "name": client.name,
            "age": client.age,
            "room": client.room,
            "support_needs": client.support_needs
        })
    return {"clients": clients_list}





@router.get("/manager/client/{client_id}")
async def get_client_by_id(client_id: str, current_manager = Depends(get_current_manager),
                           db: Session = Depends(get_db)):
    logger.info(f"Getting client {client_id} - requested by {current_manager.email}")

    db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not db_client:
        logger.warning(f"Client not found: {client_id}")
        raise HTTPException(status_code=404, detail=f"Client {client_id} not found")

    return {
        "id": db_client.id,
        "name": db_client.name,
        "age": db_client.age,
        "room": db_client.room,
        "date_of_birth": db_client.date_of_birth,
        "support_needs": db_client.support_needs
    }





@router.put("/manager/client/{client_id}")
async def update_client(client_id: str, new_data: UpdateClient,
                        current_manager = Depends(get_current_manager),
                        db: Session = Depends(get_db)):
    logger.info(f"Updating client {client_id} - requested by {current_manager.email}")

    try:
        db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail=f"Client {client_id} not found")

        update_data = new_data.dict(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_client, field):
                setattr(db_client, field, value)
        db.commit()

        logger.info(f"Client updated successfully: {client_id}")
        return {"success": True, "id": client_id}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error updating client {client_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error updating client {client_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update client")


@router.delete("/manager/client/{client_id}")
async def delete_client(client_id: str, current_manager = Depends(get_current_manager),
                        db: Session = Depends(get_db)):
    logger.info(f"Deleting client {client_id} - requested by {current_manager.email}")

    try:
        db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
        if not db_client:
            raise HTTPException(status_code=404, detail=f"Client {client_id} not found")

        db.delete(db_client)
        db.commit()

        logger.info(f"Client deleted successfully: {client_id}")
        return {"message": f"Client {client_id} deleted"}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error deleting client {client_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error deleting client {client_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete client")




@router.get("/manager/client/{client_id}/team")
async def get_client_care_team(client_id: str, current_manager = Depends(get_current_manager),
                               db: Session = Depends(get_db)):
    logger.info(f"Getting care team for client {client_id} - requested by {current_manager.email}")

    db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
    if not db_client:
        logger.warning(f"Client not found: {client_id}")
        raise HTTPException(status_code=404, detail=f"Client {client_id} not found")

    # Get assigned users (carers and family)
    assigned_users = db_client.assigned_users  # This accesses the many-to-many relationship

    carers = []
    family_members = []

    for user in assigned_users:
        if user.role == "carer":
            carers.append({
                "email": user.email,
                "name": user.name,
                "phone": user.phone,
                "role": "carer"
            })
        elif user.role == "family":
            family_members.append({
                "email": user.email,
                "name": user.name,
                "phone": user.phone,
                "role": "family",
                "family_id": user.family_id
            })

    return {
        "client_id": client_id,
        "client_name": db_client.name,
        "care_team": {
            "carers": carers,
            "family_members": family_members,
            "total_team_size": len(carers) + len(family_members)
        }
    }

