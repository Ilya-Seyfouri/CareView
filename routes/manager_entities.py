import uuid

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_manager, logger
from app.database2 import get_db, hash_password
from app.database_models import User, Client as DBClient
from app.models import Client, Family, Carer, UpdateClient, UpdateFamily, UpdateCarer
manager_entities_router = APIRouter()



#Manager Routes



@manager_entities_router.post("/manager/create/carer")
async def create_carer(carer: Carer, current_manager: dict = Depends(get_current_manager),
                       db: Session = Depends(get_db)):
    logger.info(f"Creating carer {carer.email} - requested by {current_manager['user']['email']}")

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
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating carer: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create carer {carer.email}")





@manager_entities_router.post("/manager/create/client")
async def create_client(client: Client, current_manager: dict = Depends(get_current_manager),
                        db: Session = Depends(get_db)):
    logger.info(f"Creating client {client.name} - requested by {current_manager['user']['email']}")

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

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating client: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create client")






@manager_entities_router.post("/manager/create/family-member")
async def create_family(family: Family, current_manager: dict = Depends(get_current_manager),
                        db: Session = Depends(get_db)):
    logger.info(f"Creating family member {family.email} - requested by {current_manager['user']['email']}")

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
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating family member: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create family member {family.email}")





#Manager Get Routes


@manager_entities_router.get("/manager/clients")
async def get_all_clients(current_manager: dict = Depends(get_current_manager),
                          db: Session = Depends(get_db)):
    logger.info(f"Getting all clients - requested by {current_manager['user']['email']}")

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




@manager_entities_router.get("/manager/carers")
async def get_all_carers(current_manager: dict = Depends(get_current_manager),
                         db: Session = Depends(get_db)):
    logger.info(f"Getting all carers - requested by {current_manager['user']['email']}")

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




@manager_entities_router.get("/manager/families")
async def get_all_families(current_manager: dict = Depends(get_current_manager),
                           db: Session = Depends(get_db)):
    logger.info(f"Getting all families - requested by {current_manager['user']['email']}")

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




#Manager Client routes



@manager_entities_router.get("/manager/client/{client_id}")
async def get_client_by_id(client_id: str, current_manager: dict = Depends(get_current_manager),
                           db: Session = Depends(get_db)):
    logger.info(f"Getting client {client_id} - requested by {current_manager['user']['email']}")

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





@manager_entities_router.put("/manager/client/{client_id}")
async def update_client(client_id: str, new_data: UpdateClient,
                        current_manager: dict = Depends(get_current_manager),
                        db: Session = Depends(get_db)):
    logger.info(f"Updating client {client_id} - requested by {current_manager['user']['email']}")

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
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating client: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update client")





@manager_entities_router.delete("/manager/client/{client_id}")
async def delete_client(client_id: str, current_manager: dict = Depends(get_current_manager),
                        db: Session = Depends(get_db)):
    logger.info(f"Deleting client {client_id} - requested by {current_manager['user']['email']}")

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
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting client: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete client {client_id}")




#Manager Client routes


@manager_entities_router.get("/manager/carer/{email}")
async def get_carer_email(email: str, current_manager: dict = Depends(get_current_manager),
                          db: Session = Depends(get_db)):
    logger.info(f"Getting carer {email} - requested by {current_manager['user']['email']}")

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


@manager_entities_router.put("/manager/carer/{email}")
async def update_carer_as_manager(email: str, new_data: UpdateCarer,
                                  current_manager: dict = Depends(get_current_manager),
                                  db: Session = Depends(get_db)):
    logger.info(f"Updating carer {email} - requested by {current_manager['user']['email']}")

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
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating carer: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update carer")






@manager_entities_router.delete("/manager/carer/{email}")
async def delete_carer(email: str, current_manager: dict = Depends(get_current_manager),
                       db: Session = Depends(get_db)):
    logger.info(f"Deleting carer {email} - requested by {current_manager['user']['email']}")

    try:
        db_carer = db.query(User).filter(User.email == email, User.role == "carer").first()
        if not db_carer:
            raise HTTPException(status_code=404, detail=f"Carer {email} not found")

        db.delete(db_carer)
        db.commit()

        logger.info(f"Carer deleted successfully: {email}")
        return {"message": f"Carer {email} deleted"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting carer: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete carer {email}")




#Manager Family routes


@manager_entities_router.get("/manager/family/{email}")
async def get_family_email(email: str, current_manager: dict = Depends(get_current_manager),
                           db: Session = Depends(get_db)):
    logger.info(f"Getting family member {email} - requested by {current_manager['user']['email']}")

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


@manager_entities_router.put("/manager/family/{email}")
async def edit_family_email(email: str, new_data: UpdateFamily,
                            current_manager: dict = Depends(get_current_manager),
                            db: Session = Depends(get_db)):
    logger.info(f"Updating family member {email} - requested by {current_manager['user']['email']}")

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
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating family member: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update family member")


@manager_entities_router.delete("/manager/family/{email}")
async def delete_family(email: str, current_manager: dict = Depends(get_current_manager),
                        db: Session = Depends(get_db)):
    logger.info(f"Deleting family member {email} - requested by {current_manager['user']['email']}")

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
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting family member: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete family member {email}")



#Manager Assignment Routes



@manager_entities_router.post("/manager/client/{client_id}/assign-carer/{carer_email}")
async def assign_carer_to_client(client_id: str, carer_email: str,
                                 current_manager: dict = Depends(get_current_manager),
                                 db: Session = Depends(get_db)):
    logger.info(
        f"Assigning carer {carer_email} to client {client_id} - requested by {current_manager['user']['email']}")

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
    except Exception as e:
        db.rollback()
        logger.error(f"Error assigning carer to client: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to assign carer {carer_email} to client {client_id}")






@manager_entities_router.delete("/manager/client/{client_id}/unassign-carer/{carer_email}")
async def unassign_carer_from_client(client_id: str, carer_email: str,
                                     current_manager: dict = Depends(get_current_manager),
                                     db: Session = Depends(get_db)):
    logger.info(
        f"Unassigning carer {carer_email} from client {client_id} - requested by {current_manager['user']['email']}")

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
    except Exception as e:
        db.rollback()
        logger.error(f"Error unassigning carer from client: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to unassign carer {carer_email} from Client {client_id}")







@manager_entities_router.post("/manager/client/{client_id}/assign-family/{family_email}")
async def assign_family_to_client(client_id: str, family_email: str,
                                  current_manager: dict = Depends(get_current_manager),
                                  db: Session = Depends(get_db)):
    logger.info(
        f"Assigning family {family_email} to client {client_id} - requested by {current_manager['user']['email']}")

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




@manager_entities_router.delete("/manager/client/{client_id}/unassign-family/{family_email}")
async def unassign_family_from_client(client_id: str, family_email: str,
                                      current_manager: dict = Depends(get_current_manager),
                                      db: Session = Depends(get_db)):
    logger.info(
        f"Unassigning family {family_email} from client {client_id} - requested by {current_manager['user']['email']}")

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





@manager_entities_router.get("/manager/client/{client_id}/team")
async def get_client_care_team(client_id: str, current_manager: dict = Depends(get_current_manager),
                               db: Session = Depends(get_db)):
    logger.info(f"Getting care team for client {client_id} - requested by {current_manager['user']['email']}")

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

