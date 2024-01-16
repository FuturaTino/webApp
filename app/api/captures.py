from fastapi import APIRouter,HTTPException, Depends, Form,UploadFile
from app.models import models
from app.schemas import schemas
from app.crud import crud

from sqlalchemy.orm import Session
from dependencies import get_db
from typing import List 
from uuid import uuid4
from datetime import datetime
from dotenv import load_dotenv
import os 
from pathlib import Path 


router = APIRouter()
load_dotenv('.env')
STORAGE_DIR = os.getenv("STORAGE_DIR")

# wait for upgrade
@router.get("/captures/", response_model=List[schemas.Capture])
def read_captures(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    captures = crud.get_captures(db, skip=skip, limit=limit)

    # Construct response_model
    infos = map(lambda capture: schemas.CaptureInfo(**capture.__dict__), captures)
    statuses = map(lambda capture: schemas.CaptureStatus(**capture.__dict__), captures)
    ids = map(lambda capture: capture.id, captures)
    owner_ids = map(lambda capture: capture.owner_id, captures)
    
    captures = map(lambda id, info, status, owner_id: schemas.Capture(id=id, info=info, status=status, owner_id=owner_id), ids, infos, statuses, owner_ids)
    return captures

@router.get("/captures/{capture_id}", response_model=schemas.Capture)
def read_capture(capture_id:int, db:Session = Depends(get_db)):
    db_capture = crud.get_capture(db, capture_id=capture_id)
    if db_capture is None:
        raise HTTPException(status_code=404, detail="Capture not found")
    
    # Construct response_model
    info = schemas.CaptureInfo(**db_capture.__dict__)
    status = schemas.CaptureStatus(**db_capture.__dict__)
    id = db_capture.id
    owner_id = db_capture.owner_id
    capture = schemas.Capture(id=id, info=info, status=status, owner_id=owner_id)
    return capture

@router.get("/users/{user_id}/captures/", response_model=List[schemas.Capture])
def read_user_captures(user_id:int, skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    captures = crud.get_user_captures(db, user_id=user_id, skip=skip, limit=limit)

    # Construct response_model
    ids = map(lambda capture: capture.id, captures) 
    infos = map(lambda capture: schemas.CaptureInfo(**capture.__dict__), captures)
    statuses = map(lambda capture: schemas.CaptureStatus(**capture.__dict__), captures)
    owner_ids = map(lambda capture: capture.owner_id, captures)
    captures = map(lambda id, info, status, owner_id: schemas.Capture(id=id, info=info, status=status, owner_id=owner_id), ids, infos, statuses, owner_ids)
    return captures

@router.post("/users/{user_id}/captures/" )
async def create_file(user_id:int , file: UploadFile, title:str = Form(),db:Session = Depends(get_db)):
    uuid = str(uuid4())
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    work_type = "reconstruction"
    slug = title + "-" + date

    # Save the file
    # cwrd: app
    video_location = Path(STORAGE_DIR) / uuid / file.filename
    print(video_location)
    if not video_location.parent.exists():
        video_location.parent.mkdir(parents=True)
    with open(video_location, "wb+") as file_object:
        file_object.write(await file.read())

    capture = schemas.CaptureCreate(info=schemas.CaptureInfo(uuid=uuid, slug=slug, title=title, work_type=work_type, date=date), status=schemas.CaptureStatus(uuid=uuid, latest_run_status="processing", latest_run_current_stage="processing"))
    crud.create_capture(db=db, capture=capture,user_id=user_id)
    return {"filename": file.filename, "title": title,"message":"File saved successfully"}

@router.patch("/captures/{capture_id}" )
def update_capture(capture_id:int, capture:schemas.CaptureCreate, db:Session = Depends(get_db)):
    return crud.update_capture(db=db, capture_id=capture_id, capture=capture)

@router.delete("/captures/{capture_id}")
def delete_capture(capture_id:int, db:Session = Depends(get_db)):
    return crud.delete_capture(db=db,capture_id=capture_id)