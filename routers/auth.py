from fastapi import APIRouter,HTTPException,Depends,status
from sqlmodel import Session,select
from database import engine
from models import User
from passlib.context import CryptContext
from schemas import SignupRequest,LoginRequest
from datetime import datetime,timedelta
from jose import jwt,JWTError
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

router = APIRouter(prefix="/auth",tags=["auth"])

security = HTTPBearer()


# CREATE HASHED PASSWORD

pwd_context = CryptContext(schemes=["Bcrypt"], deprecated = "auto")

# HELPER FUNCTION

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)


# JWT CONFIGURATION

SECRET_KEY = "secretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CREATE JWT TOKEN FUNCTION

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm = ALGORITHM)


# SIGNUP ROUTE

@router.post("/signup")
def signup(data:SignupRequest):
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.email==data.email)).first()
        if existing_user:
            raise HTTPException(status_code=400,detail="Email already registered.")
        
        new_user = User(
            name = data.name,
            email = data.email,
            hashed_password=hash_password(data.password)
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        return {"message":"Signup successfull."}
    

# LOGIN ROUTE

@router.post("/login")
def login(data:LoginRequest):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == data.email)).first()
        if not user or not verify_password(data.password,user.hashed_password):
             raise HTTPException(status_code=400,detail="Invalid email or password.")
        
        token = create_access_token({"user_id":(user.id)})

        return {"access_token":token,"token_type":"bearer"}
    

# GET USER FUNCTION.(CORE FUNCTION)


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
):
    credential_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail="Could not validate credential",headers={"WWW-Authenticate":"Bearer"})

    try:
        token = credentials.credentials
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise credential_exception
    except JWTError:
        raise credential_exception
    
    with Session(engine) as session:
        user = session.get(User,int(user_id))
        
        if user is None:
            raise credential_exception
        
        return user


