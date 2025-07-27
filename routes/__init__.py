
# Main routes package initialization
# This file makes the routes directory a Python package and
# imports all the organized sub-routers

from fastapi import APIRouter

# Import all the organized routers
from .manager import router as manager_router
from .family import router as family_router
from .carers import router as carers_router
from routes.admin.admin import admin_router

# Create the main router that combines all sub-routers
main_router = APIRouter()

# Include all routers with their appropriate tags
main_router.include_router(manager_router, tags=["Manager"])
main_router.include_router(family_router, tags=["Family"])
main_router.include_router(carers_router, tags=["Carers"])

main_router.include_router(admin_router, tags=["Admin"])

# Export what should be available when importing from routes
__all__ = [
    "manager_router",
    "family_router",
    "carers_router",
    "admin_router",
    "main_router"
]