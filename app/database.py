import os

import bcrypt
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.database_models import AuditLog



# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:dev-password-not-for-production@localhost:5432/careview")


# Create database URL


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
    except Exception as e:
        db.rollback()



