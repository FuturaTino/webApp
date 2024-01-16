from fastapi import APIRouter
from app.models import models
from app.schemas import schemas
from app.crud import crud
from fastapi import HTTPException, Depends, status 
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import List 
router = APIRouter()



@router.post("/users/")
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    flag_email = crud.get_user_by_email(db, email=user.email) # Actually schema is pydantic model
    flag_username = crud.get_user_by_username(db, username=user.username)
    if flag_email and  flag_username:
        raise HTTPException(status_code=400, detail="Email and username already registered")
    elif flag_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    elif flag_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    else:
        crud.create_user(db=db, user=user) 
        return {"message": "User created successfully"}

@router.get("/users/", response_model=List[schemas.UserResponse])
def read_users(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    
    users_captures = list(map(lambda user: crud.get_user_captures(db, user_id=user.id), users)) # return List[List[models.Capture]] 
    # Construct response_model, remeber return pydantic model ,not db model
    infos = list(map(lambda user_captures: list(map(lambda capture: schemas.CaptureInfo(**capture.__dict__), user_captures)), users_captures))
    statuses = list(map(lambda user_captures: list(map(lambda capture: schemas.CaptureStatus(**capture.__dict__), user_captures)), users_captures))
    ids = list(map(lambda user_captures: list(map(lambda capture: capture.id, user_captures)), users_captures))
    owner_ids = list(map(lambda user_captures: list(map(lambda capture: capture.owner_id, user_captures)), users_captures))

    each_user_captures = map(lambda id, info, status, owner_id: map(lambda id, info, status, owner_id: schemas.Capture(id=id, info=info, status=status, owner_id=owner_id), id, info, status, owner_id), ids, infos, statuses, owner_ids)

    response = map(lambda user,user_captures: schemas.UserResponse(
    email=user.email,
    id=user.id,
    username=user.username,
    is_active=user.is_active,
    captures=user_captures
), users,each_user_captures)
    return response

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id:int, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user_captures = crud.get_user_captures(db, user_id=user_id)

    # Construct response_model  from db 2 pydantic model, pydantic need info and status instance.
    infos = map(lambda capture: schemas.CaptureInfo(**capture.__dict__), db_user_captures)
    statuses = map(lambda capture: schemas.CaptureStatus(**capture.__dict__), db_user_captures) 
    ids = map(lambda capture: capture.id, db_user_captures)
    owner_id = map(lambda capture: capture.owner_id, db_user_captures)

    captures = map(lambda id, info, status, owner_id: schemas.Capture(id=id, info=info, status=status, owner_id=owner_id), ids, infos, statuses, owner_id)
    response = schemas.UserResponse(**db_user.__dict__, captures=captures)
    # response = schemas.UserResponse(**db_user.__dict__)
    return response


@router.delete("/users/{user_id}", responses={200: {"description": "User deleted"}, 404: {"description": "User not found"}})
def delete_users(user_id:int, db:Session = Depends(get_db)):
    return crud.delete_users(db=db,user_id=user_id)