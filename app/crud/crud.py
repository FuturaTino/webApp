from sqlalchemy.orm import Session

from ..models import models
from ..schemas import schemas

# User CRUD
def create_user(db:Session, user: schemas.UserCreate): 
    # fake_hashed_password = user.password + "notreallyhased"
    db_user = models.User(email=user.email,username=user.username)
    db.add(db_user)
    db.commit() 
    db.refresh(db_user)
    return db_user 

def delete_users(db:Session, user_id:int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_user_captures = db.query(models.Capture).filter(models.Capture.owner_id == user_id)
    if db_user is not None:
        # 级联删除，删除用户的同时删除用户的所有capture
        db.delete(db_user)
        db.commit()

        return {
            "message":"User deleted successfully", 
        }
    else:
        return {"message": "User not found"}

def get_user(db:Session, user_id:int):
    return db.query(models.User).filter(models.User.id == user_id).first() 

def get_user_by_username(db:Session, username:str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db:Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0 , limit:int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()  

# Capture CRUD

def get_capture(db:Session, capture_id:int):
    return db.query(models.Capture).filter(models.Capture.id == capture_id).first()

def get_user_captures(db:Session, user_id:int, skip:int = 0, limit: int = 100):
    return db.query(models.Capture).filter(models.Capture.owner_id == user_id).offset(skip).limit(limit).all()

def create_capture(db:Session, capture:schemas.CaptureCreate, user_id:int):
    d1 = vars(capture.info)
    d2 = vars(capture.status)
    d1.update(d2) 
    db_capture = models.Capture(**d1,owner_id=user_id) # pydantic schemas is meant to provide the data .
    db.add(db_capture)
    db.commit()
    db.refresh(db_capture)
    return {
        "message":"Capture created successfully", 
        "uuid": capture.info.uuid,
    }


def update_capture_status(db:Session, task_id:str, latest_run_current_stage:str,latest_run_status:str):
    db_capture = db.query(models.Capture).filter(models.Capture.uuid == task_id).first()
    if db_capture is not None:
        db_capture.latest_run_current_stage = latest_run_current_stage
        db_capture.latest_run_status = latest_run_status 
        db.commit()
        db.refresh(db_capture)
        return db_capture
    else:
        return {"message": "Capture not found"}

def update_capture_info(db:Session, task_id:str,source_url:str, result_url:str):
    db_capture = db.query(models.Capture).filter(models.Capture.uuid == task_id).first()
    if db_capture is not None:
        db_capture.source_url = source_url
        db_capture.result_url = result_url 
        db.commit()
        db.refresh(db_capture)
        return db_capture
    else:
        return {"message": "Capture not found"}

def delete_capture(db:Session, capture_id:int):
    db_capture = db.query(models.Capture).filter(models.Capture.id == capture_id).first()
    if db_capture is not None:
        db.delete(db_capture)
        db.commit()
        return {
            "message":"Capture deleted successfully", 
        }
    else:
        return {"message": "Capture not found"} 



# Item CRUD
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

