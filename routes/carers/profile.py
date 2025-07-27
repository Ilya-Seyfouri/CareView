from datetime import datetime

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_carer,logger
from app.database import get_db, hash_password
from app.database_models import User, Schedule as DBSchedule
from app.models import UpdateCarer

router = APIRouter()


@router.get("/carer/me")
async def get_carer_details(current_carer = Depends(get_current_carer),
                            db: Session = Depends(get_db)):
    logger.info(f"Getting carer details - {current_carer.email}")

    db_carer = db.query(User).filter(User.email == current_carer.email, User.role == "carer").first()
    if not db_carer:
        logger.warning(f"Carer not found: {current_carer.email}")
        raise HTTPException(status_code=404, detail=f"Carer at {current_carer.email} not found")

    return {
        "email": db_carer.email,
        "name": db_carer.name,
        "phone": db_carer.phone,
        "assigned_clients": [client.id for client in db_carer.assigned_clients],
    }





@router.put("/carer/me")
async def update_carer(new_data: UpdateCarer, current_carer = Depends(get_current_carer),
                       db: Session = Depends(get_db)):
    logger.info(f"Updating carer profile - {current_carer.email}")

    try:
        db_carer = db.query(User).filter(User.email == current_carer.email, User.role == "carer").first()
        if not db_carer:
            raise HTTPException(status_code=404, detail=f"Carer at {current_carer.email} not found")

        update_data = new_data.dict(exclude_unset=True)

        # Regular update
        for field, value in update_data.items():
            if field == "password":
                db_carer.password_hash = hash_password(value)
            elif hasattr(db_carer, field):
                setattr(db_carer, field, value)

        db.commit()
        logger.info(f"Carer profile updated successfully: {current_carer.email}")
        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating carer profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update profile")





@router.get("/carer/dashboard")
async def get_carer_dashboard(current_carer = Depends(get_current_carer),
                              db: Session = Depends(get_db)):
    logger.info(f"Getting carer dashboard - {current_carer.email}")

    carer_email = current_carer.email

    # Get today's schedules
    today = datetime.now().date()
    today_schedules = db.query(DBSchedule).filter(
        DBSchedule.carer_email == carer_email,
        DBSchedule.date == today.strftime('%Y-%m-%d')
    ).all()

    # Calculate progress
    total_visits = len(today_schedules)
    completed_visits = len([s for s in today_schedules if s.status == "completed"])

    # Get assigned clients count
    db_carer = db.query(User).filter(User.email == carer_email, User.role == "carer").first()
    assigned_clients = len(db_carer.assigned_clients) if db_carer else 0

    return {
        "stats": {
            "assigned_clients": assigned_clients,
            "total_visits_today": total_visits,
            "completed_visits": completed_visits,
            "remaining_visits": total_visits - completed_visits
        },
        "today_schedules": [
            {
                "id": s.id,
                "client_id": s.client_id,
                "client_name": s.client.name if s.client else "Unknown",
                "start_time": s.start_time,
                "end_time": s.end_time,
                "status": s.status
            } for s in today_schedules
        ]
    }

