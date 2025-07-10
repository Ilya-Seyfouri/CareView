
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import APIRouter, HTTPException, status, Depends
import jwt  # This will work after installing PyJWT
from datetime import datetime, timedelta
from app.database import carers, managers, familys, hash_password, verify_password
from app.models import Token, LoginRequest


# Auth.py - Login system, lets users login with their password + email and creates a token
# That token gives them a digital key to use other parts of the app




security = HTTPBearer()

# used to extract and verify the JWT token from incoming requests.


SECRET_KEY = "ilya"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480







def get_carer(email: str):
    if email not in carers:
        return None
    return carers[email]


def authenticate_carer(email: str, password: str):
    carer = get_carer(email) #use the above function to get carer details
    if not carer:
        return False
    if not verify_password(password, carer["password"]):
        return False
    return carer



def create_access_token(data: dict):
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


    carer = get_carer(email=email)   #get carer using token ID
    if carer is None:
        raise invalid
    return carer





auth_router = APIRouter()

#carer/login authenticates carer and JWT token request




