from sqlalchemy.orm import Session
from models.captures import Capture
from models.users import User
from schemas.captures import CaptureInDB
from schemas.captures import CaptureStatus
STATUS = {
    "Uploading":CaptureStatus(latest_run_current_stage="New", latest_run_status="Queued"),
    "Queued":CaptureStatus(latest_run_current_stage="New", latest_run_status="Queued"),
    "PreProcessing":CaptureStatus(latest_run_current_stage="Preprocessing", latest_run_status="Dispatched"),
    "Reconstructing":CaptureStatus(latest_run_current_stage="Reconstructing", latest_run_status="Dispatched"),
    "Failed":CaptureStatus(latest_run_current_stage="Finished", latest_run_status="Failed"),
    "Success":CaptureStatus(latest_run_current_stage="Finished", latest_run_status="Success"),

}

def get_capture(db:Session, capture_id:int):
    return db.query(Capture).filter(Capture.id == capture_id).first()

def get_captures(db:Session, skip:int = 0, limit: int = 100):
    return db.query(Capture).offset(skip).limit(limit).all()

def get_user_captures(db:Session, user_id:int, skip:int = 0, limit: int = 100):
    return db.query(Capture).filter(Capture.owner_id == user_id).offset(skip).limit(limit).all()

def get_user_captures_by_username(db:Session, username:str, skip:int = 0, limit: int = 100):
    owner_id = db.query(User).filter(User.username == username).first()
    if owner_id is not None:
        return db.query(Capture).filter(Capture.owner_id == owner_id.id).offset(skip).limit(limit).all()
    else:
        return None

def create_capture(db:Session, capture:CaptureInDB, user_id:int):
    db_capture = Capture(**capture.__dict__) # pydantic schemas is meant to provide the data .
    db.add(db_capture)
    db.commit()
    db.refresh(db_capture)
    return {
        "message":"Capture created successfully", 
        "uuid": capture.uuid
    }

def update_capture_status(db:Session, uuid:str, status:CaptureStatus):
    db_capture = db.query(Capture).filter(Capture.uuid == uuid).first()
    if db_capture is not None:
        db_capture.latest_run_current_stage = status.latest_run_current_stage
        db_capture.latest_run_status = status.latest_run_status
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

def delete_capture(db:Session, capture_id:int)->dict:
    db_capture = db.query(Capture).filter(Capture.id == capture_id).first()
    if db_capture is not None:
        db.delete(db_capture)
        db.commit()
        return {
            "message":"Capture deleted successfully", 
        }
    else:
        return {"message": "Capture not found"} 
