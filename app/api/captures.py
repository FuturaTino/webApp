from fastapi import APIRouter,HTTPException, Depends, Form,UploadFile

from schemas.captures import  CaptureInDB,CaptureOutDB,CaptureReponse, CaptureInfo, CaptureStatus
from schemas.users import UserResponse

from crud.captures import get_capture_by_uuid,get_captures, get_capture, get_user_captures, create_capture, update_capture_status,delete_a_capture,STATUS,update_capture_info
from crud.users import get_user_by_username

from models.captures import Capture

from core.dependencies import get_db
from core.auth import get_current_user
from core.oss import prepare_job,get_oss_image_url,get_oss_ply_url,delete_oss_file
from celeryApp import reconstruct

from sqlalchemy.orm import Session
from sqlalchemy import inspect
from typing import List 
from uuid import uuid4
from datetime import datetime
from dotenv import load_dotenv,find_dotenv
import os 
from pathlib import Path 
import shutil
router = APIRouter()
load_dotenv(find_dotenv('config.env'))
backend_dir = Path(__file__).parent.parent
STORAGE_DIR = backend_dir / os.getenv("STORAGE_DIR")

@router.get("/captures/all", response_model=List[CaptureReponse],summary="需要token，获取所有公开作品的信息")
def read_captures(skip:int = 0, limit:int = 100, db:Session = Depends(get_db),current_username:str = Depends(get_current_user)):
    db_captures = get_captures(db, skip=skip, limit=limit)

    # 获取最新的image_url和result_url
    def update_capture(capture):
        if capture.latest_run_status =="Success":
            image_url = get_oss_image_url(capture.uuid)
            result_url = get_oss_ply_url(capture.uuid)
            capture.image_url = image_url
            capture.result_url = result_url
            update_capture_info(db=db, uuid=capture.uuid, image_url=image_url, result_url=result_url)
            return capture
        else:
            return capture

    db_captures = list(map(update_capture, db_captures))

    #使用 SQLAlchemy 的 inspect 函数来获取 capture 数据库对象的公开属性
    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}
    captures_out_db = list(map(lambda capture: CaptureOutDB(**object_as_dict(capture)), db_captures))
    
    # Construct response_model
    ids = map(lambda capture: capture.id, captures_out_db)
    infos = map(lambda capture: CaptureInfo(**capture.__dict__), captures_out_db)
    statuses = map(lambda capture: CaptureStatus(**capture.__dict__), captures_out_db)
    owner_ids = map(lambda capture: capture.owner_id, captures_out_db)

    response = map(lambda id, info, status, owner_id: CaptureReponse(id=id, info=info, status=status, owner_id=owner_id), ids, infos, statuses, owner_ids)


    return response

@router.get("/captures/{uuid}", response_model=CaptureReponse,summary="需要token,根据作品uuid,获取某个作品的信息")
def read_capture(uuid:str, db:Session = Depends(get_db),current_username:str = Depends(get_current_user)):
    db_capture = get_capture_by_uuid(db,uuid=uuid)
    if db_capture is None:
        raise HTTPException(status_code=404, detail="Capture not found")
    image_url = get_oss_image_url(uuid)
    result_url = get_oss_ply_url(uuid)
    db_capture.image_url = image_url
    db_capture.result_url = result_url
    update_capture_info(db=db, uuid=uuid, image_url=image_url, result_url=result_url)
    
    # Construct response_model
    info = CaptureInfo(**db_capture.__dict__)
    status = CaptureStatus(**db_capture.__dict__)
    id = db_capture.id
    owner_id = db_capture.owner_id
    capture = CaptureReponse(id=id, info=info, status=status, owner_id=owner_id)

    return capture

# 先上传文件到oss,然后post调度服务器，上传formdata,title，uuid,返回成功信息后，前端再发送预训练和训练请求。
@router.post("/captures/my/create",summary="在拥有token的前提下,该用户创建一个作品" )
async def create_file(title:str = Form(),uuid:str=Form(), db:Session = Depends(get_db),current_username:str = Depends(get_current_user)):
    # uuid = str(uuid4())
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    work_type = "reconstruction"
    slug = title + "-" + date
    db_user = get_user_by_username(db, username=current_username)
    video_location = "video/" + f"{uuid}.mp4" # oss路径

    # Create capture in db
    kwargs = {
        "uuid":uuid,
        "title":title,
        "slug":slug,
        "date":date,
        "work_type":work_type,
        "source_url":str(video_location),
        "image_url":None,
        "result_url":None,
        "latest_run_status":None,
        "latest_run_current_stage":None,
        "owner_id":db_user.id
    }
    capture = CaptureInDB(**kwargs)
    create_capture(db=db, capture=capture,user_id=db_user.id)

    return {"title": title,"uuid":uuid,"message":"Capture saved successfully"}

@router.get("/captures/my/show",summary="在拥有token的前提下,获取当前用户的信息与所有作品")
def read_user(db:Session = Depends(get_db),current_username:str = Depends(get_current_user)):
    db_user = get_user_by_username(db, username=current_username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_captures = get_user_captures(db, user_id=db_user.id)

    # 获取最新的image_url和result_url
    def update_capture(capture):
        if capture.latest_run_status =="Success":
            image_url = get_oss_image_url(capture.uuid)
            result_url = get_oss_ply_url(capture.uuid)
            capture.image_url = image_url
            capture.result_url = result_url
            update_capture_info(db=db, uuid=capture.uuid, image_url=image_url, result_url=result_url)
            return capture
        else:
            return capture
    
    db_captures:List[Capture] = list(map(update_capture, db_captures))
    

    # Construct response_model
    ids = list(map(lambda capture: capture.id, db_captures))
    infos = list(map(lambda capture: CaptureInfo(**capture.__dict__), db_captures))
    statuses = list(map(lambda capture: CaptureStatus(**capture.__dict__), db_captures))
    owner_ids = list(map(lambda capture: capture.owner_id, db_captures))

    captures:List[CaptureReponse] = []
    for id,info,status,owner_id in zip(ids,infos,statuses,owner_ids):
        captures.append(CaptureReponse(id=id, info=info, status=status, owner_id=owner_id))

    response = UserResponse(id=db_user.id, username=db_user.username, captures=captures)
    # print(response)
    return response


@router.post("/captures/process",summary="需要token，将某个作品加入队列")
def enqueued_capture(uuid:str, db:Session = Depends(get_db),current_username:str = Depends(get_current_user)):
    try:

        # 开启预处理，与训练模型
        # task link https://docs.celeryq.dev/en/stable/userguide/calling.html
        update_capture_status(db=db, uuid=uuid, status=STATUS['Queued'])
        reconstruct.apply_async(args=(uuid,),task_id=uuid)

        # process.apply_async(args=(uuid,),task_id=uuid,
        #                     link=reconstruct.si(uuid).set(queue="gs",
        #                                                   routing_key="gs.low",
        #                                                   ignore_result=True,
        #                                                   task_id=uuid),
        #                     ignore_result=True,
        #                     queue="colmap",
        #                     routing_key="colmap.low")
    except Exception as e:
        update_capture_status(db=db, uuid=uuid, status=STATUS['Failed'])
        raise HTTPException(status_code=500, detail=e)

    return {"message":f"{uuid} is queued for processing"}

@router.post("/captures/refresh",summary="无需token,刷新某个作品的状态至最原始创建状态")
def refresh_capture(uuid:str, db:Session = Depends(get_db)):
    return {"message":"refresh capture"}

@router.delete("/captures/delete",summary="需要token,删除某个作品")
def delete_capture(uuid:str, db:Session = Depends(get_db),current_username:str = Depends(get_current_user)):
    try:
        # 检验，发送请求的用户是否是capture的owner
        db_user = get_user_by_username(db, username=current_username)
        capture = get_capture_by_uuid(db, uuid=uuid)
        if capture.owner_id != db_user.id:
            raise HTTPException(status_code=400, detail="Forbidden")

        # 删除数据库中的记录
        delete_a_capture(db=db, uuid=uuid)
        # 删除oss中的文件
        for prefix,postfix in [("video",".mp4"),("image",".png"),("ply",".ply")]:
            oss_key = f"{prefix}/{uuid}{postfix}"
            delete_oss_file(oss_key)
        return {"message":"deleted capture"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=e)
