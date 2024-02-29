from sqlalchemy.orm import Session
from models.items import Item
from models.captures import Capture

from schemas.items import ItemCreate

# Item CRUD
def get_items(db:Session, skip:int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def create_user_item(db:Session, item:ItemCreate, user_id:int):
    db_item = Item(**item.model_dump(),owner_id = user_id) # pydantic schemas is meant to provide the data .
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_captures(db:Session, skip:int = 0, limit: int = 100):
    return db.query(Capture).offset(skip).limit(limit).all()

