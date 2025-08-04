
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_manager, logger
from app.database import get_db, hash_password
from app.database_models import User, Client as DBClient, Schedule
from app.models import Carer,UpdateCarer

router = APIRouter()



#Manager Routes



@router.post("/manager/create/carer")
async def create_carer(carer: Carer, current_manager = Depends(get_current_manager),
                       db: Session = Depends(get_db)):
    logger.info(f"Creating carer {carer.email} - requested by {current_manager.email}")

    try:
        # Check email doesn't exist
        existing = db.query(User).filter(User.email == carer.email).first()
        if existing:
            raise HTTPException(status_code=409, detail=f"Email {carer.email} already exists")

        # Create carer
        db_carer = User(
            email=carer.email,
            name=carer.name,
            password_hash=hash_password(carer.password),
            phone=carer.phone,
            role="carer"
        )
        db.add(db_carer)
        db.commit()

        # Add client assignments if provided
        if carer.assigned_clients:
            for client_id in carer.assigned_clients:
                db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
                if db_client:
                    db_carer.assigned_clients.append(db_client)
            db.commit()

        logger.info(f"Carer created successfully: {carer.email}")
        return {"message": "Carer created", "email": carer.email}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error creating carer {carer.email}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error creating carer {carer.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error, Failed to create carer")




@router.get("/manager/carers")
async def get_all_carers(current_manager = Depends(get_current_manager),
                         db: Session = Depends(get_db)):
    logger.info(f"Getting all carers - requested by {current_manager.email}")

    carers = db.query(User).filter(User.role == "carer").all()
    carers_list = []
    for carer in carers:
        carers_list.append({
            "email": carer.email,
            "name": carer.name,
            "phone": carer.phone,
            "assigned_clients": [client.id for client in carer.assigned_clients]
        })
    return {"carers": carers_list}












@router.get("/manager/carer/{email}")
async def get_carer_email(email: str, current_manager = Depends(get_current_manager),
                          db: Session = Depends(get_db)):
    logger.info(f"Getting carer {email} - requested by {current_manager.email}")

    db_carer = db.query(User).filter(User.email == email, User.role == "carer").first()
    if not db_carer:
        logger.warning(f"Carer not found: {email}")
        raise HTTPException(status_code=404, detail=f"Carer {email} not found")

    return {
        "email": db_carer.email,
        "name": db_carer.name,
        "phone": db_carer.phone,
        "assigned_clients": [client.id for client in db_carer.assigned_clients]
    }


@router.put("/manager/carer/{email}")
async def update_carer_as_manager(email: str, new_data: UpdateCarer,
                                  current_manager =  Depends(get_current_manager),
                                  db: Session = Depends(get_db)):
    logger.info(f"Updating carer {email} - requested by {current_manager.email}")

    try:
        db_carer = db.query(User).filter(User.email == email, User.role == "carer").first()
        if not db_carer:
            raise HTTPException(status_code=404, detail=f"Carer {email} not found")

        update_data = new_data.dict(exclude_unset=True)

        for field, value in update_data.items():
            if field == "password":
                db_carer.password_hash = hash_password(value)
            elif hasattr(db_carer, field):
                setattr(db_carer, field, value)
        db.commit()

        logger.info(f"Carer updated successfully: {email}")
        return {"success": True, "email": email}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error updating carer {email}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error updating carer {email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update carer")






@router.delete("/manager/carer/{email}")
async def delete_carer(email: str, current_manager = Depends(get_current_manager),
                       db: Session = Depends(get_db)):
    logger.info(f"Deleting carer {email} - requested by {current_manager.email}")

    try:
        db_carer = db.query(User).filter(User.email == email, User.role == "carer").first()
        if not db_carer:
            raise HTTPException(status_code=404, detail=f"Carer {email} not found")

        db.query(Schedule).filter(Schedule.carer_email == email).delete()

        db.delete(db_carer)
        db.commit()

        logger.info(f"Carer deleted successfully: {email}")
        return {"message": f"Carer {email} deleted"}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error deleting carer {email}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error deleting carer {email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete carer")







@router.post("/manager/client/{client_id}/assign-carer/{carer_email}")
async def assign_carer_to_client(client_id: str, carer_email: str,
                                 current_manager = Depends(get_current_manager),
                                 db: Session = Depends(get_db)):
    logger.info(
        f"Assigning carer {carer_email} to client {client_id} - requested by {current_manager.email}")

    try:
        db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
        db_carer = db.query(User).filter(User.email == carer_email, User.role == "carer").first()

        if not db_client:
            raise HTTPException(status_code=404, detail=f"Client {client_id} not found")
        if not db_carer:
            raise HTTPException(status_code=404, detail=f"Carer {carer_email} not found")

        if db_client in db_carer.assigned_clients:
            return {"message": "Already assigned"}

        db_carer.assigned_clients.append(db_client)
        db.commit()

        logger.info(f"Carer assigned successfully: {carer_email} -> {client_id}")
        return {"message": "Carer assigned to client"}

    except HTTPException:
        raise

    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error assigning carer to client {carer_email} {client_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Error assigning carer to client: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to assign carer {carer_email} to client {client_id}")






@router.delete("/manager/client/{client_id}/unassign-carer/{carer_email}")
async def unassign_carer_from_client(client_id: str, carer_email: str,
                                     current_manager = Depends(get_current_manager),
                                     db: Session = Depends(get_db)):
    logger.info(
        f"Unassigning carer {carer_email} from client {client_id} - requested by {current_manager.email}")

    try:
        db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
        db_carer = db.query(User).filter(User.email == carer_email, User.role == "carer").first()

        if not db_client or not db_carer:
            raise HTTPException(status_code=404, detail=f"Client {client_id} or carer {carer_email} not found")

        if db_client not in db_carer.assigned_clients:
            return {"message": f"Client {client_id} isn't assigned with Carer {carer_email}"}

        db_carer.assigned_clients.remove(db_client)
        db.commit()

        logger.info(f"Carer unassigned successfully: {carer_email} from {client_id}")
        return {"message": "Carer unassigned from client"}

    except HTTPException:
        raise

    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error unassigning carer from client {carer_email} {client_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Error unassigning carer from client: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to unassign carer {carer_email} from Client {client_id}")






