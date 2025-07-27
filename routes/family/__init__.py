from fastapi import APIRouter


from .clients import router as f_clients_router
from .visit_logs import router as f_visit_logs_router
from .schedules import router as f_schedules_router
from .profile import router as familydetails_router


router = APIRouter()

router.include_router(f_clients_router, tags=["Family Clients"])
router.include_router(f_visit_logs_router, tags=["Family Visit Logs"])
router.include_router(f_schedules_router, tags=["Family Clients Schedules"])
router.include_router(familydetails_router, tags=["Family Details"])

