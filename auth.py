from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

# 1. Initialize the context with a secure algorithm
# 2. manages the secure hashing and verification of passwords in Python applications
pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

# load all parameters from dotenv
load_dotenv()

# Secret Key
SECRET_KEY: str = os.getenv("SECRET_KEY", '')

# Algorithm
ALGORITHM: str = os.getenv("ALGORITHM", '')

# Token expiry time
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 30)

# hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# verify incoming password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# decode access token
def decode_access_token(token:str):
    try: 
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None