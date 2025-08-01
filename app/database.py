import os

import bcrypt
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import logging

from app.database_models import AuditLog



# Load environment variables
load_dotenv()

#d

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "careview")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "dev-password-not-for-production")


# Create database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)


# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# Password hashing
def hash_password(password: str) -> str:
    if not password:
        raise ValueError("Password cannot be empty")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")

    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))




#Audit Log function
def log_action(db: Session, user_email: str, action: str, entity_type: str, entity_id: str):
    try:
        audit_log = AuditLog(
            user_email=user_email,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id
        )
        db.add(audit_log)
        db.commit()
        logger.info(f"AUDIT: {user_email} {action} {entity_type} {entity_id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to log audit action: {str(e)}")



#Recent activity of audit logs for manager dashboard
def get_recent_activity(db: Session, limit: int = 20):
    try:
        return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
    except Exception:
        return []