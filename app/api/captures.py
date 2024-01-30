from fastapi import APIRouter,HTTPException, Depends, Form,UploadFile

from schemas.captures import  CaptureInDB,CaptureOutDB,CaptureReponse, CaptureInfo, CaptureStatus
from schemas.users import UserResponse

from crud.captures import get_captures, get_capture, get_user_captures, create_capture, update_capture_status,delete_a_capture,STATUS
from crud.users import get_user_by_username

from core.dependencies import get_db
from core.auth import get_current_user
# from core.colmap.colmap_app import process
from colmap_app import process
from sqlalchemy.orm import Session

from typing import List 
from uuid import uuid4
from datetime import datetime
from dotenv import load_dotenv,find_dotenv
import os 
from pathlib import Path 
import shutil

router = APIRouter()
load_dotenv(find_dotenv('.env'))
backend_dir = Path(__file__).parent.parent
STORAGE_DIR = backend_dir / os.getenv("STORAGE_DIR")

@router.get("/captures/all", response_model=List[CaptureReponse],summary="获取所有作品的信息")
def read_captures(skip:int = 0, limit:int = 100, db:Session = Depends(get_db)):
    db_captures = get_captures(db, skip=skip, limit=limit)
    
    captures_out_db = list(map(lambda capture: CaptureOutDB(**capture.__dict__), db_captures))
    
    # Construct response_model
    ids = map(lambda capture: capture.id, captures_out_db)
    infos = map(lambda capture: CaptureInfo(**capture.__dict__), captures_out_db)
    statuses = map(lambda capture: CaptureStatus(**capture.__dict__), captures_out_db)
    owner_ids = map(lambda capture: capture.owner_id, captures_out_db)

    response = map(lambda id, info, status, owner_id: CaptureReponse(id=id, info=info, status=status, owner_id=owner_id), ids, infos, statuses, owner_ids)


    return response

@router.get("/captures/{capture_id}", response_model=CaptureReponse,summary="根据作品id,获取所有作品中某个作品的信息")
def read_capture(capture_id:int, db:Session = Depends(get_db),current_username:str = Depends(get_current_user)):
    db_capture = get_capture(db, capture_id=capture_id)
    if db_capture is None:
        raise HTTPException(status_code=404, detail="Capture not found")
    
    
    # Construct response_model
    info = CaptureInfo(**db_capture.__dict__)
    status = CaptureStatus(**db_capture.__dict__)
    id = db_capture.id
    owner_id = db_capture.owner_id
    capture = CaptureReponse(id=id, info=info, status=status, owner_id=owner_id)
    return capture


@router.post("/captures/my/create",summary="在拥有token的前提下，该用户创建一个作品" )
async def create_file(file: UploadFile, title:str = Form(),db:Session = Depends(get_db),current_username:str = Depends(get_current_user)):
    uuid = str(uuid4())
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    work_type = "reconstruction"
    slug = title + "-" + date
    db_user = get_user_by_username(db, username=current_username)
    video_location = Path(STORAGE_DIR) / uuid / f"{uuid}.mp4"

    # Create capture in db
    kwargs = {
        "uuid":uuid,
        "title":title,
        "slug":slug,
        "date":date,
        "work_type":work_type,
        "source_url":str(video_location),
        "result_url":None,
        "latest_run_status":None,
        "latest_run_current_stage":None,
        "owner_id":db_user.id
    }
    capture = CaptureInDB(**kwargs)
    create_capture(db=db, capture=capture,user_id=db_user.id)

    # Save the file
    if not video_location.parent.exists():
        video_location.parent.mkdir(parents=True)
    with open(video_location, "wb+") as file_object:
        file_object.write(await file.read())

    return {"filename": file.filename, "title": title,"uuid":uuid,"message":"File saved successfully"}

@router.get("/captures/my/show", response_model=UserResponse,summary="在拥有token的前提下，获取当前用户的信息与所有作品")
def read_user(db:Session = Depends(get_db),current_username:str = Depends(get_current_user)):
    db_user = get_user_by_username(db, username=current_username)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user_captures = get_user_captures(db, user_id=db_user.id)

    # Construct response_model  from db 2 pydantic model, pydantic need info and status instance.
    infos = map(lambda capture: CaptureInfo(**capture.__dict__), db_user_captures)
    statuses = map(lambda capture: CaptureStatus(**capture.__dict__), db_user_captures) 
    ids = map(lambda capture: capture.id, db_user_captures)
    owner_id = map(lambda capture: capture.owner_id, db_user_captures)

    captures = map(lambda id, info, status, owner_id: CaptureReponse(id=id, info=info, status=status, owner_id=owner_id), ids, infos, statuses, owner_id)
    response = UserResponse(**db_user.__dict__, captures=captures)
    # response = UserOutDB(**db_user.__dict__)
    return response

# 暂无用户认证，用于admin测试，不可以公开api
@router.post("/captures/process",summary="无需token,处理某个作品")
def enqueued_capture(uuid:str, db:Session = Depends(get_db)):
    try:
        process.apply_async((uuid,),task_id=uuid)
        update_capture_status(db=db, uuid=uuid, status=STATUS['Queued'])
    except Exception as e:
        print(e)
        update_capture_status(db=db, uuid=uuid, status=STATUS['Failed'])
        raise HTTPException(status_code=500, detail=e)

    return {"message":f"{uuid} is queued for processing"}

@router.post("/captures/train",summary="无需token,训练某个作品")
def train_capture(uuid:str, db:Session = Depends(get_db)):
    try:
        # train.apply_async((uuid,),task_id=uuid)
        pass # 训练功能暂未实现
        update_capture_status(db=db, uuid=uuid, status=STATUS['Reconstructing'])
    except Exception as e:
        print(e)
        update_capture_status(db=db, uuid=uuid, status=STATUS['Failed'])
        raise HTTPException(status_code=500, detail=e)
    
    return {"message":f"{uuid} is reconstructing"}

@router.post("/captures/refresh",summary="无需token,刷新某个作品的状态")
def refresh_capture(uuid:str, db:Session = Depends(get_db)):
    return {"message":"refresh capture"}

@router.delete("/captures/delete",summary="无需token,删除某个作品")
def delete_capture(uuid:str, db:Session = Depends(get_db)):
    try:
        shutil.rmtree(STORAGE_DIR / uuid)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=e)
    try:
        delete_a_capture(db=db, uuid=uuid)
        return {"message":"delete capture"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=e)
