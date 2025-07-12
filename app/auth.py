
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter, HTTPException, status, Depends
import jwt  # This will work after installing PyJWT
from datetime import datetime, timedelta
from app.database import carers, managers, familys, verify_password
from app.models import Token, LoginRequest
from typing import List

# Auth.py - Login system, lets users login with their password + email and creates a token
# That token gives them a digital key to use other parts of the app




security = HTTPBearer()

# used to extract and verify the JWT token from incoming requests.


SECRET_KEY = "ilya"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480







def get_user(email: str):
    if email in carers:
        return {"user":carers[email], "user-type": "carer"}
    elif email in familys:
        return {"user":familys[email], "user-type": "family-member"}
    elif email in managers:
        return {"user":managers[email], "user-type": "manager"}
    return None


async def authenticate_user(email: str, password: str):
    user_data = get_user(email) #use the above function to get carer details
    if not user_data:
        return False
    user = user_data["user"]
    if not verify_password(password, user["password"]):
        return False
    return user_data



async def create_access_token(data: dict):
    copy_data = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    copy_data.update({"exp": expire})
    encoded_token = jwt.encode(copy_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token



#Check the token
#function will automatically run before any protected route, and FastAPI will extract the token from the Authorization: Bearer <token> header

async def get_current_carer(credentials: HTTPAuthorizationCredentials = Depends(security)):


    invalid = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
                            )
    try:
        #Decode the JWT token and get the data inside it (payload)
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")   #extract email from payload/token
        if email is None:
            raise invalid
    except jwt.PyJWTError:
        raise invalid  #token is expired / invalid




    carer = get_user(email=email)   #get carer using token ID
    if carer is None:
        raise invalid
    if carer["user-type"] != "carer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Carer role required."
        )
    return carer




async def get_current_family(credentials: HTTPAuthorizationCredentials = Depends(security)):
    invalid = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token and get the data inside it (payload)
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # extract email from payload/token
        if email is None:
            raise invalid
    except jwt.PyJWTError:
        raise invalid  # token is expired / invalid

    family = get_user(email=email)  # get carer using token ID
    if family is None:
        raise invalid
    if family["user-type"] != "family-member":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. family role required."
        )
    return family




async def get_current_manager(credentials: HTTPAuthorizationCredentials = Depends(security)):
    invalid = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the JWT token and get the data inside it (payload)
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")  # extract email from payload/token
        if email is None:
            raise invalid
    except jwt.PyJWTError:
        raise invalid  # token is expired / invalid

    manager = get_user(email=email)  # get carer using token ID
    if manager is None:
        raise invalid
    if manager["user-type"] != "manager":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. manager role required."
        )
    return manager

















auth_router = APIRouter()

#carer/login authenticates carer and JWT token request





@auth_router.post("/login", response_model=Token)
async def login_user(login: LoginRequest):
    try:

        user = await authenticate_user(login.email, login.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )


        # If successful login, create the token


        access_token = await create_access_token(
            data={"sub": user["user"]["email"]}  # 'sub' contains carer email
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
