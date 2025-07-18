import logging
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from routes.admin import admin_router
from routes.manager_auth import manager_auth_router
from routes.manager_operations import manager_operations_router
from routes.manager_entities import manager_entities_router
from routes.family import family_router
from routes.carers import carer_router
from app.auth import auth_router



# Configure logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)



# Create FastAPI app
app = FastAPI(
    title="CareView API",
    description="Professional care home management system",
)



# routers
app.include_router(auth_router, tags=["Authentication"])
app.include_router(carer_router, tags=["Carers"])
app.include_router(family_router, tags=["Families"])
app.include_router(manager_auth_router, tags=["Manager Auth"])
app.include_router(manager_operations_router, tags=["Manager Operations"])
app.include_router(manager_entities_router, tags=["Manager Entities"])
app.include_router(admin_router, tags=["Admin"])





# Health check endpoints
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "healthy",
        "message": "CareView API is running",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "CareView API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


#Error handlers

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error at {request.url.path}")

    simple_errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]

        if message.startswith("Value error, "):
            message = message.replace("Value error, ", "")

        simple_errors.append(f"{field}: {message}")

    return JSONResponse(
        status_code=422,
        content={
            "error": "Invalid data provided",
            "details": simple_errors
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP {exc.status_code} at {request.url.path}: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error at {request.url.path}: {str(exc)}")

    return JSONResponse(
        status_code=500,
        content={
            "error": "Something went wrong. Please try again."
        }
    )




# Startup/shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("CareView API starting up...")






@app.on_event("shutdown")
async def shutdown_event():
    logger.info("CareView API shutting down...")

