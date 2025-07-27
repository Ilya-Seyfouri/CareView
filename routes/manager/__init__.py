# imports and combines all sub routers into 1

from fastapi import APIRouter

from .profile import router as m_auth_router
from .manager_carers import router as m_carers_router
from .manager_families import router as m_family_router
from .manager_clients import router as m_client_router
from .schedules import router as m_schedules_router
from .visit_logs import router as m_visit_log_router

router = APIRouter()

# Include all the sub-routers
router.include_router(m_auth_router, tags=["Manager Auth"])
router.include_router(m_carers_router, tags=["Manager Carers"])
router.include_router(m_family_router, tags=["Manager Families"])
router.include_router(m_client_router, tags=["Manager Clients"])
router.include_router(m_visit_log_router, tags=["Manager VisitLogs"])
router.include_router(m_schedules_router, tags=["Manager Schedules"])