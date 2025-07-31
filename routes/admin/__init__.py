
from fastapi import APIRouter
from .admin import admin_router

router = APIRouter()

router.include_router(admin_router, tags=["Admin"])