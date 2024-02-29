from fastapi import APIRouter,HTTPException,Depends, status ,Response
from fastapi import Form
from schemas.users import UserInDB, UserOutDB,LoginInDB,UserResponse
from schemas.captures import CaptureInfo, CaptureStatus, CaptureReponse

from crud.users import get_users, get_user, get_user_by_email, get_user_by_username, create_user, delete_a_user
from crud.captures import get_user_captures

from core.auth import create_access_token, verify_password, get_password_hash,get_current_user,verify_token

from sqlalchemy.orm import Session
from core.dependencies import get_db
from typing import List 

router = APIRouter()

@router.post("/auth/register")
def register(username: str = Form(...),
            # email: str = Form(None),
            password: str = Form(...),
            db:Session = Depends(get_db)):
    if get_user_by_username(db, username=username) is not None:
        raise HTTPException(status_code=400, detail="Username already registered")
    # user = UserInDB(username=username, email="", password=get_password_hash(password))
    user = UserInDB(username=username, email="", password=get_password_hash(password))
    db_user = create_user(db=db, user=user)

    return {
        "message":"User created successfully",
        "user":UserOutDB(**db_user.__dict__)
    }

@router.post("/auth/login")
def login(username: str = Form(...),password: str = Form(...), db:Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found")
        
    # if db_user.password != get_password_hash(password) : 即使是相同的密码，由于盐的随机性，每次生成的哈希值也会不同。
    if verify_password(password, db_user.password) == False: 
        raise HTTPException(status_code=400, detail="Password incorrect")
    
    access_token = create_access_token(username=db_user.username)

    return {
        "message":"Login successfully",
        "user":UserOutDB(**db_user.__dict__),
        "token": access_token
    }

# check if token is valid
@router.get("/auth/token")
def check_token(token:str =None):
    try:
        username = verify_token(token)
        return {"message":"Token is valid","username":username}
    except:
        raise HTTPException(status_code=400, detail="Token is invalid or expired")

