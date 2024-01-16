from fastapi import APIRouter,HTTPException, Depends, Form,UploadFile

from schemas.captures import Capture, CaptureInfo, CaptureStatus, CaptureInDB
from crud.captures import get_captures, get_capture, get_user_captures, create_capture, delete_capture


from sqlalchemy.orm import Session
from core.dependencies import get_db
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
@router.get("/captures/", response_model=List[Capture])
def read_captures(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    captures = get_captures(db, skip=skip, limit=limit)

    # Construct response_model
    infos = map(lambda capture: CaptureInfo(**capture.__dict__), captures)
    statuses = map(lambda capture: CaptureStatus(**capture.__dict__), captures)
    ids = map(lambda capture: capture.id, captures)
    owner_ids = map(lambda capture: capture.owner_id, captures)
    
    captures = map(lambda id, info, status, owner_id: Capture(id=id, info=info, status=status, owner_id=owner_id), ids, infos, statuses, owner_ids)
    return captures

@router.get("/captures/{capture_id}", response_model=Capture)
def read_capture(capture_id:int, db:Session = Depends(get_db)):
    db_capture = get_capture(db, capture_id=capture_id)
    if db_capture is None:
        raise HTTPException(status_code=404, detail="Capture not found")
    
    # Construct response_model
    info = CaptureInfo(**db_capture.__dict__)
    status = CaptureStatus(**db_capture.__dict__)
    id = db_capture.id
    owner_id = db_capture.owner_id
    capture = Capture(id=id, info=info, status=status, owner_id=owner_id)
    return capture

@router.get("/users/{user_id}/captures/", response_model=List[Capture])
def read_user_captures(user_id:int, skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    captures = get_user_captures(db, user_id=user_id, skip=skip, limit=limit)

    # Construct response_model
    ids = map(lambda capture: capture.id, captures) 
    infos = map(lambda capture: CaptureInfo(**capture.__dict__), captures)
    statuses = map(lambda capture: CaptureStatus(**capture.__dict__), captures)
    owner_ids = map(lambda capture: capture.owner_id, captures)
    captures = map(lambda id, info, status, owner_id: Capture(id=id, info=info, status=status, owner_id=owner_id), ids, infos, statuses, owner_ids)
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

    capture = CaptureInDB(info=CaptureInfo(uuid=uuid, slug=slug, title=title, work_type=work_type, date=date), status=CaptureStatus(uuid=uuid, latest_run_status="processing", latest_run_current_stage="processing"))
    create_capture(db=db, capture=capture,user_id=user_id)
    return {"filename": file.filename, "title": title,"message":"File saved successfully"}

@router.patch("/captures/{capture_id}" )
def update_capture(capture_id:int, capture:CaptureInDB, db:Session = Depends(get_db)):
    return update_capture(db=db, capture_id=capture_id, capture=capture)

@router.delete("/captures/{capture_id}")
def delete_capture(capture_id:int, db:Session = Depends(get_db)):
    return delete_capture(db=db,capture_id=capture_id)