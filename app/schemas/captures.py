from typing import Union,List
from pydantic import BaseModel 

class CaptureStatus(BaseModel):
    latest_run_status:Union[str, None] =None 
    latest_run_current_stage:Union[str,None] = None

class CaptureInfo(BaseModel):
    uuid:str
    slug:str 
    title:str
    work_type: Union[str, None] = None
    date: Union[str, None] = None 
    source_url: Union[str, None] = None
    result_url: Union[str, None] = None

class CaptureBase(BaseModel):
    uuid:str 
    slug:str 
    title:str 
    work_type: Union[str, None] = None 
    date: Union[str, None] = None
    source_url: Union[str, None] = None
    result_url: Union[str, None] = None
    latest_run_status: Union[str, None] = None
    latest_run_current_stage: Union[str, None] = None

class CaptureInDB(CaptureBase):
    owner_id:int 


class CaptureOutDB(CaptureBase):
    id:int 
    owner_id: Union[int, None] = None

    class Config:
        orm_model = True

class CaptureReponse(BaseModel):
    id:int 
    owner_id: Union[int, None] = None
    info:CaptureInfo
    status:CaptureStatus

