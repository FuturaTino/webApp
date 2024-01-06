from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db:Session, user_id:int):
    return db.query(models.User).filter(models.User.id == user_id).first() 

def get_user_by_email(db:Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0 , limit:int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()  

def delete_users(db:Session, user_id:int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is not None:
        db.delete(db_user)
        db.commit()
        return {
            "message":"User deleted successfully", 
        }
    else:
        return {"message": "User not found"}


def create_user(db:Session, user: schemas.UserCreate): 
    # fake_hashed_password = user.password + "notreallyhased"
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit() 
    db.refresh(db_user)
    return db_user 

def get_items(db:Session, skip:int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db:Session, item:schemas.ItemCreate, user_id:int):
    db_item = models.Item(**item.model_dump(),owner_id = user_id) # pydantic schemas is meant to provide the data .
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_captures(db:Session, skip:int = 0, limit: int = 100):
    return db.query(models.Capture).offset(skip).limit(limit).all()

def create_user_capture(db:Session, capture:schemas.CaptureCreate, user_id:int):
    db_capture = models.Capture(**capture.model_dump(),owner_id = user_id) # pydantic schemas is meant to provide the data .
    db.add(db_capture)
    db.commit()
    db.refresh(db_capture)
    return db_capture