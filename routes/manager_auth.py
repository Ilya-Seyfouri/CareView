from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_manager,logger
from app.database2 import get_db, hash_password
from app.database_models import User, Client as DBClient, Schedule as DBSchedule
from app.models import UpdateManager
manager_auth_router = APIRouter()





#Manager Routes



@manager_auth_router.get("/manager/me")
async def get_manager(current_manager: dict = Depends(get_current_manager),
                      db: Session = Depends(get_db)):
    logger.info(f"Getting manager details - {current_manager['user']['email']}")

    db_manager = db.query(User).filter(User.email == current_manager["user"]["email"], User.role == "manager").first()
    if not db_manager:
        logger.warning(f"Manager not found: {current_manager['user']['email']}")
        raise HTTPException(status_code=404, detail=f"Manager not found: {current_manager['user']['email']}")

    return {
        "email": db_manager.email,
        "name": db_manager.name,
        "department": db_manager.department,
    }





@manager_auth_router.put("/manager/me")
async def update_manager(new_data: UpdateManager,
                         current_manager: dict = Depends(get_current_manager),
                         db: Session = Depends(get_db)):
    logger.info(f"Updating manager profile - {current_manager['user']['email']}")

    try:
        db_manager = db.query(User).filter(User.email == current_manager["user"]["email"], User.role == "manager").first()
        if not db_manager:
            raise HTTPException(status_code=404, detail=f"Manager not found: {current_manager['user']['email']}")

        update_data = new_data.dict(exclude_unset=True)

        # Update fields
        for field, value in update_data.items():
            if field == "password":
                db_manager.password_hash = hash_password(value)
            elif hasattr(db_manager, field):
                setattr(db_manager, field, value)

        db.commit()
        logger.info(f"Manager profile updated successfully: {current_manager['user']['email']}")
        return {"success": True}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating manager profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update profile")




@manager_auth_router.get("/manager/dashboard")
async def get_manager_dashboard(current_manager: dict = Depends(get_current_manager),
                                db: Session = Depends(get_db)):
    logger.info(f"Getting manager dashboard - {current_manager['user']['email']}")

    # Get this week's date range
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    week_start = monday.strftime("%Y-%m-%d")
    week_end = sunday.strftime("%Y-%m-%d")

    # Basic counts using user table with roles
    total_clients = db.query(DBClient).count()
    total_carers = db.query(User).filter(User.role == "carer").count()

    #This weeks schedule
    week_schedules = db.query(DBSchedule).filter(
        DBSchedule.date >= week_start,
        DBSchedule.date <= week_end
    ).all()

    # Simple weekly stats
    total_visits = len(week_schedules)
    completed_visits = len([s for s in week_schedules if s.status == "completed"])

    # Completion rate
    if total_visits > 0:
        completion_rate = round((completed_visits / total_visits) * 100)
    else:
        completion_rate = 0

    return {
        "basic_stats": {
            "clients": total_clients,
            "carers": total_carers,
        },
        "this_week": {
            "completion_rate": f"{completion_rate}%",
            "completed_visits": completed_visits,
            "total_visits": total_visits,
        }
    }