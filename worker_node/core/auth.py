from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext

from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm 

from datetime import timedelta,datetime
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "563c5a7fb2d1b73dc7dfda946fa5ad7341ee2fd2fbea702a9d1e04b5e403a8c7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 14


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str):
    return pwd_context.hash(password)


def create_access_token(username:str,expires_delta:timedelta = timedelta(days=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "sub": username,
        "exp": expire.timestamp()
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt 
    
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

def get_current_user(token:str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    username:str = payload.get("sub") 
    return username
    