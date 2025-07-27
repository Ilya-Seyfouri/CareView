from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_family,logger
from app.database import get_db, hash_password
from app.database_models import User
from app.models import UpdateFamily


router = APIRouter()








@router.get("/family/me")
async def get_family_details(current_family = Depends(get_current_family),
                             db: Session = Depends(get_db)):
    logger.info(f"Getting family details - {current_family.email}")

    db_family = db.query(User).filter(User.email == current_family["user"]["email"], User.role == "family").first()
    if not db_family:
        logger.warning(f"Family member not found: {current_family.email}")
        raise HTTPException(status_code=404, detail=f"Family member at {current_family.email} not found")

    return {
        "email": db_family.email,
        "id": db_family.family_id,
        "name": db_family.name,
        "phone": db_family.phone,
        "assigned_clients": [client.id for client in db_family.assigned_clients],
    }



@router.put("/family/me")
async def update_family(new_data: UpdateFamily, current_family = Depends(get_current_family),
                        db: Session = Depends(get_db)):
    logger.info(f"Updating family profile - {current_family.email}")

    try:
        db_family = db.query(User).filter(User.email == current_family.email, User.role == "family").first()
        if not db_family:
            raise HTTPException(status_code=404, detail=f"Family member at {current_family.email} not found")

        update_data = new_data.dict(exclude_unset=True)

        # Regular update
        for field, value in update_data.items():
            if field == "password":
                db_family.password_hash = hash_password(value)
            elif hasattr(db_family, field):
                setattr(db_family, field, value)

        db.commit()
        logger.info(f"Family profile updated successfully: {current_family.email}")
        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating family profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update profile")

