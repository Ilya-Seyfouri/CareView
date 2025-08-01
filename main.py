import logging
from sqlalchemy import text # we can use sql queries as strings
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException #Building the restAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from app.database import get_db
from app.database_models import User, Client as DBClient
from routes import main_router  # Updated import
from app.auth import auth_router
from fastapi.middleware.cors import CORSMiddleware




# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title="CareView API",
    description="Professional care home management system",
)


# Add this after app = FastAPI(...)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",  # We'll update this later
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(main_router)
app.include_router(auth_router)


# Checking database connectivity
@app.get("/health", tags=["Health"])
async def health_check():
    try:
        db = next(get_db())
        db.execute(text("SELECT 1")).fetchone()
        db.close()

        return {
            "status": "healthy",
            "service": "CareView API",
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        return JSONResponse(
            content={
                "status": "unhealthy",
                "service": "CareView API",
                "error": f"Database connection failed {e}",
                "timestamp": datetime.now().isoformat()
            },
            status_code=503
        )


# Monitoring system status
@app.get("/status", tags=["Health"])
async def system_status():
    try:
        db = next(get_db())

        return {
            "service": "CareView API",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "database": "connected",
            "users": db.query(User).count(),
            "clients": db.query(DBClient).count()
        }

    except Exception as e:
        return {
            "service": "CareView API",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "database": "disconnected",
            "error": str(e)
        }
    finally:
        try:
            db.close()
        except Exception:
            pass


# Error handlers
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
    logger.error(f"Error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Startup/shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("CareView API starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("CareView API shutting down...")

@app.get("/setup-demo-data")
async def setup_demo_data():
    try:
        from scripts.reset import reset_database
        reset_database()
        return {"message": "✅ Demo data created! Try logging in with admin@demo.com / password123"}
    except Exception as e:
        return {"error": str(e)}