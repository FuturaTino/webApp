from fastapi import APIRouter, Depends, HTTPException, status

from schemas.items import Item, ItemCreate
from crud.items import get_items, create_user_item


from sqlalchemy.orm import Session
from core.dependencies import get_db
from typing import List

router = APIRouter()

@router.get("/items/", response_model=List[Item])
def read_items(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    return items

@router.post("/users/{user_id}/items/", response_model=Item)
def create_item_for_users(user_id:int, item:ItemCreate, db:Session = Depends(get_db)):
    return create_user_item(db=db, item=item, user_id=user_id)
