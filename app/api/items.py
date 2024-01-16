from fastapi import APIRouter, Depends, HTTPException, status
from app.models import models
from app.schemas import schemas 
from app.crud import crud
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import List

router = APIRouter()

@router.get("/items/", response_model=List[schemas.Item])
def read_items(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_users(user_id:int, item:schemas.ItemCreate, db:Session = Depends(get_db)):
    return crud.create_user_item(db=db, item=item, user_id=user_id)
