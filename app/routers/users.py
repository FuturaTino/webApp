from fastapi import APIRouter
from db import crud , models, schemas
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
        return 201, {"message": "User created successfully"}

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

@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id:int, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Construct response_model
    response = schemas.UserResponse(**db_user.__dict__)
    return response


@router.delete("/users/{user_id}", responses={200: {"description": "User deleted"}, 404: {"description": "User not found"}})
def delete_users(user_id:int, db:Session = Depends(get_db)):
    return crud.delete_users(db=db,user_id=user_id)