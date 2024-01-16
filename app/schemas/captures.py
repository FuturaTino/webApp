from typing import Union,List
from pydantic import BaseModel 

# Capture
class CaptureStatus(BaseModel):
    latest_run_status:str
    latest_run_current_stage:str

class CaptureInfo(BaseModel):
    uuid:str
    slug:str 
    title:str
    work_type: Union[str, None] = None
    date: Union[str, None] = None 
    source_url: Union[str, None] = None
    result_url: Union[str, None] = None


class CaptureBase(BaseModel):
    info: CaptureInfo
    status: CaptureStatus

class CaptureInDB(CaptureBase):
    pass

class Capture(CaptureBase):
    id:int 
    owner_id: Union[int, None] = None

    class Config:
        orm_model = True
