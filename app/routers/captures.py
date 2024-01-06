from fastapi import APIRouter
from db import crud , models, schemas
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from typing import List 
router = APIRouter()

@router.get("/captures/", response_model=List[schemas.Capture])
def read_captures(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    captures = crud.get_captures(db, skip=skip, limit=limit)
    return captures