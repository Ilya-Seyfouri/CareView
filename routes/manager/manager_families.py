from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_manager, logger
from app.database import get_db, hash_password
from app.database_models import User, Client as DBClient
from app.models import Family,UpdateFamily


router = APIRouter()






@router.post("/manager/create/family-member")
async def create_family(family: Family, current_manager = Depends(get_current_manager),
                        db: Session = Depends(get_db)):
    logger.info(f"Creating family member {family.email} - requested by {current_manager.email}")

    try:
        # Check email doesn't exist
        existing = db.query(User).filter(User.email == family.email).first()
        if existing:
            raise HTTPException(status_code=422, detail=f"Email {family.email} already exists")

        # Create family member
        db_family = User(
            email=family.email,
            family_id=family.id,
            name=family.name,
            password_hash=hash_password(family.password),
            phone=family.phone,
            role="family"
        )
        db.add(db_family)
        db.commit()

        # Add client assignments if provided
        if family.assigned_clients:
            for client_id in family.assigned_clients:
                db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
                if db_client:
                    db_family.assigned_clients.append(db_client)
            db.commit()

        logger.info(f"Family member created successfully: {family.email}")
        return {"message": "Family member created", "email": family.email}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error creating family member {family.email}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error creating family member {family.email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create family member")


@router.get("/manager/families")
async def get_all_families(current_manager = Depends(get_current_manager),
                           db: Session = Depends(get_db)):
    logger.info(f"Getting all families - requested by {current_manager.email}")

    families = db.query(User).filter(User.role == "family").all()
    families_list = []
    for family in families:
        families_list.append({
            "email": family.email,
            "id": family.family_id,
            "name": family.name,
            "phone": family.phone,
            "assigned_clients": [client.id for client in family.assigned_clients]
        })
    return {"families": families_list}








@router.get("/manager/family/{email}")
async def get_family_email(email: str, current_manager = Depends(get_current_manager),
                           db: Session = Depends(get_db)):
    logger.info(f"Getting family member {email} - requested by {current_manager.email}")

    db_family = db.query(User).filter(User.email == email, User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {email}")
        raise HTTPException(status_code=404, detail=f"Family member {email} not found")

    return {
        "email": db_family.email,
        "id": db_family.family_id,
        "name": db_family.name,
        "phone": db_family.phone,
        "assigned_clients": [client.id for client in db_family.assigned_clients]
    }


@router.put("/manager/family/{email}")
async def edit_family_email(email: str, new_data: UpdateFamily,
                            current_manager = Depends(get_current_manager),
                            db: Session = Depends(get_db)):
    logger.info(f"Updating family member {email} - requested by {current_manager.email}")

    try:
        db_family = db.query(User).filter(User.email == email, User.role == "family").first()
        if not db_family:
            raise HTTPException(status_code=404, detail=f"Family member {email} not found")

        update_data = new_data.dict(exclude_unset=True)

        for field, value in update_data.items():
            if field == "password":
                db_family.password_hash = hash_password(value)
            elif hasattr(db_family, field):
                setattr(db_family, field, value)
        db.commit()

        logger.info(f"Family member updated successfully: {email}")
        return {"success": True, "email": email}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error updating family member {email}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error updating family member {email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update family member")


@router.delete("/manager/family/{email}")
async def delete_family(email: str, current_manager = Depends(get_current_manager),
                        db: Session = Depends(get_db)):
    logger.info(f"Deleting family member {email} - requested by {current_manager.email}")

    try:
        db_family = db.query(User).filter(User.email == email, User.role == "family").first()
        if not db_family:
            raise HTTPException(status_code=404, detail=f"Family member {email} not found")

        db.delete(db_family)
        db.commit()

        logger.info(f"Family member deleted successfully: {email}")
        return {"message": f"Family member {email} deleted"}

    except HTTPException:
        raise
    except ValueError as e:
        db.rollback()
        logger.error(f"Validation error deleting family member {email}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        logger.error(f"Database error deleting family member {email}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete family member")








@router.post("/manager/client/{client_id}/assign-family/{family_email}")
async def assign_family_to_client(client_id: str, family_email: str,
                                  current_manager = Depends(get_current_manager),
                                  db: Session = Depends(get_db)):
    logger.info(
        f"Assigning family {family_email} to client {client_id} - requested by {current_manager.email}")

    try:
        db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
        db_family = db.query(User).filter(User.email == family_email, User.role == "family").first()

        if not db_client:
            raise HTTPException(status_code=404, detail=f"Client {client_id} not found")
        if not db_family:
            raise HTTPException(status_code=404, detail=f"Family member {family_email} not found")

        if db_client in db_family.assigned_clients:
            return {"message": "Already assigned"}

        db_family.assigned_clients.append(db_client)
        db.commit()

        logger.info(f"Family assigned successfully: {family_email} -> {client_id}")
        return {"message": "Family member assigned to client"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error assigning family to client: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to assign family member {family_email} to Client {client_id}")




@router.delete("/manager/client/{client_id}/unassign-family/{family_email}")
async def unassign_family_from_client(client_id: str, family_email: str,
                                      current_manager = Depends(get_current_manager),
                                      db: Session = Depends(get_db)):
    logger.info(
        f"Unassigning family {family_email} from client {client_id} - requested by {current_manager.email}")

    try:
        db_client = db.query(DBClient).filter(DBClient.id == client_id).first()
        db_family = db.query(User).filter(User.email == family_email, User.role == "family").first()

        if not db_client or not db_family:
            raise HTTPException(status_code=404, detail=f"Client {client_id} or family member {family_email} not found")

        if db_client not in db_family.assigned_clients:
            return {"message": f"Client {client_id} isnt assigned to {family_email}"}

        db_family.assigned_clients.remove(db_client)
        db.commit()



        logger.info(f"Family unassigned successfully: {family_email} from {client_id}")
        return {"message": "Family member unassigned from client"}



    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error unassigning family from client: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to unassign family member {family_email} from Client {client_id}")
