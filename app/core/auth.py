from jose import JWTError,jwt 
from passlib.context import CryptContext

from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm 

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "563c5a7fb2d1b73dc7dfda946fa5ad7341ee2fd2fbea702a9d1e04b5e403a8c7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str):
    return pwd_context.hash(password)