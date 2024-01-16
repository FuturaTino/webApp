from fastapi import APIRouter,HTTPException,Depends, status ,Response

from schemas.users import UserInDB, UserOutDB,LoginInDB,UserResponse
from schemas.captures import CaptureInfo, CaptureStatus, CaptureReponse

from crud.users import get_users, get_user, get_user_by_email, get_user_by_username, create_user, delete_users
from crud.captures import get_user_captures

from core.auth import create_access_token, verify_password, get_password_hash

from sqlalchemy.orm import Session
from core.dependencies import get_db
from typing import List 

router = APIRouter()

@router.post("/register",tags=["Auth"])
def register(user: UserInDB, db:Session = Depends(get_db)):
    if get_user_by_email(db, email=user.email) is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    elif get_user_by_username(db, username=user.username) is not None:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = create_user(db=db, user=user)

    return {
        "message":"User created successfully",
        "user":UserOutDB(**db_user.__dict__)
    }

@router.post("/login",tags=["Auth"])
def login(user: LoginInDB, db:Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user is None:
        db_user = get_user_by_username(db, username=user.username)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
    if db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Password incorrect")
    
    access_token = create_access_token(username=db_user.username)

    return {
        "message":"Login successfully",
        "user":UserOutDB(**db_user.__dict__),
        "token": access_token
    }


@router.get("/users/", response_model=List[UserResponse])
def read_users(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    
    users_captures = list(map(lambda user: get_user_captures(db, user_id=user.id), users)) # return List[List[models.Capture]] 
    # Construct response_model, remeber return pydantic model ,not db model
    infos = list(map(lambda user_captures: list(map(lambda capture: CaptureInfo(**capture.__dict__), user_captures)), users_captures))
    statuses = list(map(lambda user_captures: list(map(lambda capture: CaptureStatus(**capture.__dict__), user_captures)), users_captures))
    ids = list(map(lambda user_captures: list(map(lambda capture: capture.id, user_captures)), users_captures))
    owner_ids = list(map(lambda user_captures: list(map(lambda capture: capture.owner_id, user_captures)), users_captures))

    each_user_captures = map(lambda id, info, status, owner_id: map(lambda id, info, status, owner_id: CaptureReponse(id=id, info=info, status=status, owner_id=owner_id), id, info, status, owner_id), ids, infos, statuses, owner_ids)

    response = map(lambda user,user_captures: UserResponse(
    email=user.email,
    id=user.id,
    username=user.username,
    is_active=user.is_active,
    captures=user_captures
), users,each_user_captures)
    return response

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id:int, db:Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user_captures = get_user_captures(db, user_id=user_id)

    # Construct response_model  from db 2 pydantic model, pydantic need info and status instance.
    infos = map(lambda capture: CaptureInfo(**capture.__dict__), db_user_captures)
    statuses = map(lambda capture: CaptureStatus(**capture.__dict__), db_user_captures) 
    ids = map(lambda capture: capture.id, db_user_captures)
    owner_id = map(lambda capture: capture.owner_id, db_user_captures)

    captures = map(lambda id, info, status, owner_id: CaptureReponse(id=id, info=info, status=status, owner_id=owner_id), ids, infos, statuses, owner_id)
    response = UserResponse(**db_user.__dict__, captures=captures)
    # response = UserOutDB(**db_user.__dict__)
    return response


@router.delete("/users/{user_id}", responses={200: {"description": "User deleted"}, 404: {"description": "User not found"}})
def delete_users(user_id:int, db:Session = Depends(get_db)):
    return delete_users(db=db,user_id=user_id)