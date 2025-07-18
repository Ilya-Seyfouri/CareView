import os
import logging
from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database2 import verify_password, get_db
from app.database_models import User
from app.models import Token, LoginRequest




security = HTTPBearer()
logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 480



# Get user from single users table
def get_user(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    return {
        "user": {
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
            "role": user.role
        },
        "user-type": user.role,
        "db_user": user
    }

#Authenticate against single users table
async def authenticate_user(email: str, password: str, db: Session):

    user_data = get_user(email, db)
    if not user_data:
        return False

    db_user = user_data["db_user"]
    if not verify_password(password, str(db_user.password_hash)):
        return False

    return {
        "user": user_data["user"],
        "user-type": user_data["user-type"]
    }



async def create_access_token(data: dict):
    copy_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    copy_data.update({"exp": expire})
    return jwt.encode(copy_data, SECRET_KEY, algorithm=ALGORITHM)




# Get current user - works for all roles
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





# Check if user is carer or manager
async def get_current_carer(current_user: dict = Depends(get_current_user)):
    if current_user["user-type"] not in ["carer", "manager"]:
        raise HTTPException(status_code=403, detail="Carer access required")
    return current_user





# Check if user is family or manager
async def get_current_family(current_user: dict = Depends(get_current_user)):

    if current_user["user-type"] not in ["family", "manager"]:
        raise HTTPException(status_code=403, detail="Family access required")
    return current_user



#Check if user is manager
async def get_current_manager(current_user: dict = Depends(get_current_user)):
    if current_user["user-type"] != "manager":
        raise HTTPException(status_code=403, detail="Manager access required")
    return current_user




#Check if user is admin
async def get_current_admin(current_user: dict = Depends(get_current_user)):
    if current_user["user-type"] != "admin":
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
        data={"sub": user["user"]["email"]}
    )
    logger.info(f"Successful login for {user['user']['email']}")
    return {"access_token": access_token, "token_type": "bearer"}