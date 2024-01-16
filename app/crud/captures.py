from sqlalchemy.orm import Session
from models.captures import Capture

from schemas.captures import CaptureInDB

def get_capture(db:Session, capture_id:int):
    return db.query(Capture).filter(Capture.id == capture_id).first()

def get_captures(db:Session, skip:int = 0, limit: int = 100):
    return db.query(Capture).offset(skip).limit(limit).all()


def get_user_captures(db:Session, user_id:int, skip:int = 0, limit: int = 100):
    return db.query(Capture).filter(Capture.owner_id == user_id).offset(skip).limit(limit).all()

def create_capture(db:Session, capture:CaptureInDB, user_id:int):

    db_capture = Capture(**capture.__dict__) # pydantic schemas is meant to provide the data .
    db.add(db_capture)
    db.commit()
    db.refresh(db_capture)
    return {
        "message":"Capture created successfully", 
        "uuid": capture.uuid
    }


def update_capture_status(db:Session, task_id:str, latest_run_current_stage:str,latest_run_status:str):
    db_capture = db.query(Capture).filter(Capture.uuid == task_id).first()
    if db_capture is not None:
        db_capture.latest_run_current_stage = latest_run_current_stage
        db_capture.latest_run_status = latest_run_status 
        db.commit()
        db.refresh(db_capture)
        return db_capture
    else:
        return {"message": "Capture not found"}

def update_capture_info(db:Session, task_id:str,source_url:str, result_url:str):
    db_capture = db.query(Capture).filter(Capture.uuid == task_id).first()
    if db_capture is not None:
        db_capture.source_url = source_url
        db_capture.result_url = result_url 
        db.commit()
        db.refresh(db_capture)
        return db_capture
    else:
        return {"message": "Capture not found"}

def delete_capture(db:Session, capture_id:int):
    db_capture = db.query(Capture).filter(Capture.id == capture_id).first()
    if db_capture is not None:
        db.delete(db_capture)
        db.commit()
        return {
            "message":"Capture deleted successfully", 
        }
    else:
        return {"message": "Capture not found"} 
