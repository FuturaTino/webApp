from sqlalchemy.orm import Session
from . import models, schemas

# User CRUD
def create_user(db:Session, user: schemas.UserCreate): 
    # fake_hashed_password = user.password + "notreallyhased"
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit() 
    db.refresh(db_user)
    return db_user 

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

def create_capture(db:Session, capture:schemas.CaptureCreate):
    db_capture = models.Capture(**capture.model_dump()) # pydantic schemas is meant to provide the data .
    db.add(db_capture)
    db.commit()
    db.refresh(db_capture)
    return db_capture

def update_capture(db:Session, capture_id:int, capture:schemas.CaptureCreate):
    db_capture = db.query(models.Capture).filter(models.Capture.id == capture_id).first()
    if db_capture is not None:
        db_capture.name = capture.name
        db_capture.description = capture.description
        db_capture.image = capture.image
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

def create_user_capture(db:Session, capture:schemas.CaptureCreate, user_id:int):
    
    # Turn pydantic model format data to db model format data
    #  pydantic schemas is meant to provide the data in a compelex json format
    db_capture = models.Capture(
        uuid=capture.info.uuid,
        slug=capture.info.slug,
        title=capture.info.title,
        work_type=capture.info.work_type,
        date=capture.info.date,
        source_url=capture.info.source_url,
        result_url=capture.info.result_url,
        latest_run_status=capture.status.latest_run_status,
        latest_run_progress=capture.status.latest_run_progress,
        latest_run_current_stage=capture.status.latest_run_current_stage,
        owner_id=user_id
    )

    db.add(db_capture)
    db.commit()
    db.refresh(db_capture)
    return {
        "message":"Capture created successfully", 
        "uuid": capture.info.uuid,
    }