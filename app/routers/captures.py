from fastapi import APIRouter
from db import crud , models, schemas
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import List 
router = APIRouter()

@router.get("/captures/", response_model=List[schemas.CaptureResponse])
def read_captures(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    captures = crud.get_captures(db, skip=skip, limit=limit)

    # Construct response_model
    info = map(lambda capture: schemas.CaptureInfo(**capture.__dict__), captures)
    status = map(lambda capture: schemas.CaptureStatus(**capture.__dict__), captures)
    response = map(lambda info, status: schemas.CaptureResponse(info=info, status=status), info, status)
    return response

@router.get("/captures/{capture_id}", response_model=schemas.CaptureResponse)
def read_capture(capture_id:int, db:Session = Depends(get_db)):
    db_capture = crud.get_capture(db, capture_id=capture_id)
    if db_capture is None:
        raise HTTPException(status_code=404, detail="Capture not found")
    
    # Construct response_model
    info = schemas.CaptureInfo(**db_capture.__dict__)
    status = schemas.CaptureStatus(**db_capture.__dict__)
    response = schemas.CaptureResponse(info=info, status=status) #class attr needs to be passed as kwargs
    return response

@router.post("/users/{user_id}/captures/" )
def create_capture_for_users(user_id:int, capture:schemas.CaptureCreate, db:Session = Depends(get_db)):
    return crud.create_user_capture(db=db, capture=capture, user_id=user_id)

@router.patch("/captures/{capture_id}" )
def update_capture(capture_id:int, capture:schemas.CaptureCreate, db:Session = Depends(get_db)):
    return crud.update_capture(db=db, capture_id=capture_id, capture=capture)

@router.delete("/captures/{capture_id}", responses={200: {"description": "Capture deleted"}, 404: {"description": "Capture not found"}})
def delete_capture(capture_id:int, db:Session = Depends(get_db)):
    return crud.delete_capture(db=db,capture_id=capture_id)