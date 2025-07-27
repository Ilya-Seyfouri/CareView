from fastapi import APIRouter
from .clients import router as c_client_router
from .profile import router as carerdetail_router
from .schedules import router as carer_schedule_router
from .visit_logs import router as carer_vl_router


router = APIRouter()

router.include_router(c_client_router,tags=["Carer Clients"])

router.include_router(carerdetail_router,tags=["Carer Details"])

router.include_router(carer_schedule_router, tags=["Carer Schedule"])

router.include_router(carer_vl_router,tags=["Carer Visit Logs"])






