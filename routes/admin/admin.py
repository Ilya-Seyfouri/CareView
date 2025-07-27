import logging

from fastapi import APIRouter, HTTPException,Depends
from sqlalchemy.orm import Session

from app.auth import get_current_admin
from app.database import get_db, hash_password
from app.database_models import User, Client as DBClient, Schedule as DBSchedule, VisitLog as DBVisitLog
from app.models import Manager, UpdateManager




logger = logging.getLogger(__name__)
admin_router = APIRouter()


#Admin routes

@admin_router.get("/admin/managers")
async def get_managers(current_admin: dict = Depends(get_current_admin),
                       db: Session = Depends(get_db)):
    logger.info(f"Getting all managers - requested by {current_admin['user']['email']}")
    managers = db.query(User).filter(User.role == 'manager').all()

    managers_list = []
    for manager in managers:
        managers_list.append({
            "email": manager.email,
            "name": manager.name,
            "department": manager.department,
        })

    return {"managers": managers_list}








@admin_router.post("/admin/create/manager")
async def create_manager(manager: Manager, current_admin: dict = Depends(get_current_admin),
                         db: Session = Depends(get_db)):
    logger.info(f"Creating manager {manager.email} - requested by {current_admin['user']['email']}")

    try:
        # Check if manager already exists
        if db.query(User).filter(User.email == manager.email).first():
            raise HTTPException(status_code=422, detail="Manager already exists")

        # Create manager
        db_manager = User(
            email=manager.email,
            name=manager.name,
            department=manager.department,
            password_hash=hash_password(manager.password),
            role="manager"
        )

        db.add(db_manager)
        db.commit()

        logger.info(f"Manager created successfully: {manager.email}")
        return {"message": "Manager created", "email": manager.email}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating manager: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create manager")




@admin_router.get("/admin/managers/{email}")
async def get_manager_by_email(email: str, current_admin: dict = Depends(get_current_admin),
                               db: Session = Depends(get_db)):
    logger.info(f"Getting manager {email} - requested by {current_admin['user']['email']}")
    db_manager = db.query(User).filter(User.email == email, User.role == 'manager').first()
    if not db_manager:
        logger.warning(f"Manager not found: {email}")
        raise HTTPException(status_code=404, detail="Manager not found")

    return {
        "email": db_manager.email,
        "name": db_manager.name,
        "department": db_manager.department,
    }







@admin_router.put("/admin/managers/{email}")
async def update_manager(email: str, new_data: UpdateManager,
                         current_admin: dict = Depends(get_current_admin),
                         db: Session = Depends(get_db)):
    logger.info(f"Updating manager {email} - requested by {current_admin['user']['email']}")

    try:
        db_manager = db.query(User).filter(User.email == email, User.role == 'manager').first()
        if not db_manager:
            raise HTTPException(status_code=404, detail="Manager not found")

        update_data = new_data.dict(exclude_unset=True)

        # Regular update
        for field, value in update_data.items():
            if field == "password":
                db_manager.password_hash = hash_password(value)
            elif hasattr(db_manager, field):
                setattr(db_manager, field, value)

        db.commit()
        logger.info(f"Manager updated successfully: {email}")
        return {"success": True, "email": email}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating manager: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update manager")





@admin_router.delete("/admin/managers/{email}")
async def delete_manager(email: str, current_admin: dict = Depends(get_current_admin),
                         db: Session = Depends(get_db)):
    logger.info(f"Deleting manager {email} - requested by {current_admin['user']['email']}")

    try:
        db_manager = db.query(User).filter(User.email == email, User.role == 'manager').first()
        if not db_manager:
            raise HTTPException(status_code=404, detail="Manager not found")

        db.delete(db_manager)
        db.commit()

        logger.info(f"Manager deleted successfully: {email}")
        return {"message": f"Manager {email} deleted"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting manager: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete manager")






@admin_router.get("/admin/dashboard")
async def get_admin_dashboard(current_admin: dict = Depends(get_current_admin),
                              db: Session = Depends(get_db)):
    logger.info(f"Getting admin dashboard - requested by {current_admin['user']['email']}")

    # Get system counts using User table with roles
    total_managers = db.query(User).filter(User.role == 'manager').count()
    total_carers = db.query(User).filter(User.role == 'carer').count()
    total_families = db.query(User).filter(User.role == 'family').count()
    total_clients = db.query(DBClient).count()
    total_schedules = db.query(DBSchedule).count()
    total_visit_logs = db.query(DBVisitLog).count()

    return {
        "system_stats": {
            "managers": total_managers,
            "carers": total_carers,
            "families": total_families,
            "clients": total_clients,
            "schedules": total_schedules,
            "visit_logs": total_visit_logs
        }
    }


@admin_router.get("/admin/stats")
async def get_system_stats(current_admin: dict = Depends(get_current_admin),
                           db: Session = Depends(get_db)):
    logger.info(f"Getting system stats - requested by {current_admin['user']['email']}")

    return {
        "managers": db.query(User).filter(User.role == 'manager').count(),
        "carers": db.query(User).filter(User.role == 'carer').count(),
        "families": db.query(User).filter(User.role == 'family').count(),
        "clients": db.query(DBClient).count(),
        "schedules": db.query(DBSchedule).count(),
        "visit_logs": db.query(DBVisitLog).count(),
    }