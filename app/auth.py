import os
import logging
from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import verify_password, get_db
from app.database_models import User
from app.models import Token, LoginRequest





security = HTTPBearer()
logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-not-for-production-use")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 480



# Get user from single users table
def get_user(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    return user


async def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email, db)
    if not user or not verify_password(password, str(user.password_hash)):
        return False
    return user




async def create_access_token(data: dict):
    copy_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    copy_data.update({"exp": expire})
    return jwt.encode(copy_data, SECRET_KEY, algorithm=ALGORITHM)




async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                           db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user(email=email, db=db)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user



async def get_current_carer(current_user = Depends(get_current_user)):
    if current_user.role not in ["carer", "manager"]:
        raise HTTPException(status_code=403, detail="Carer access required")
    return current_user




async def get_current_family(current_user = Depends(get_current_user)):
    if current_user.role not in ["family", "manager"]:
        raise HTTPException(status_code=403, detail="Family access required")
    return current_user


async def get_current_manager(current_user = Depends(get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Manager access required")
    return current_user



async def get_current_admin(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user





# Login endpoint
auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
async def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    logger.info(f"Login attempt for {login.email}")

    user = await authenticate_user(login.email, login.password, db)
    if not user:
        logger.warning(f"Failed login attempt for {login.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = await create_access_token(
        data={"sub": user.email}
    )
    logger.info(f"Successful login for {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}



@auth_router.get("/me")
async def get_me(current_user = Depends(get_current_user)):
    return {"user": {
        "email": current_user.email,
        "name": current_user.name,
        "phone": current_user.phone,
        "role": current_user.role
    }, "role": current_user.role}
