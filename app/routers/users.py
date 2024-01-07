from fastapi import APIRouter
from db import crud , models, schemas
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import List 
router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email) # Actually schema is pydantic model 
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user) 

@router.get("/users/", response_model=List[schemas.UserResponse])
def read_users(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    
    response = map(lambda user: schemas.UserResponse(
        email=user.email,
        id=user.id,
        username=user.username,
        is_active=user.is_active,
    ), users)
    return response

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id:int, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/users/{user_id}", responses={200: {"description": "User deleted"}, 404: {"description": "User not found"}})
def delete_users(user_id:int, db:Session = Depends(get_db)):
    return crud.delete_users(db=db,user_id=user_id)