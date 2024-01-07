from typing import Union,List
from pydantic import BaseModel 

class ItemBase(BaseModel):
    title: str 
    description: Union[str, None] = None 

class ItemCreate(ItemBase): # create
    pass

class Item(ItemBase): # read
    id:int 
    owner_id: int 

    class Config:
        orm_model = True 

# Capture
class CaptureStatus(BaseModel):
    uuid:str
    latest_run_status:str
    latest_run_progress:str
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

class CaptureCreate(CaptureBase):
    pass

class CaptureResponse(CaptureBase):
    pass
class Capture(CaptureBase):
    id:int 
    owner_id: int

    class Config:
        orm_model = True

# User 
class UserBase(BaseModel):
    email: str 

class UserCreate(UserBase):
    password: str 

class UserResponse(UserBase):
    id:int
    username: Union[str, None] = None 
    is_activate: Union[str, None] = True
    captures: List[Capture] = []
    class Config:
        orm_model = True
        
class User(UserBase):
    id:int
    username: Union[str, None] = None 
    is_activate: Union[str, None] = True
    items: List[Item] = []
    captures: List[Capture] = []
    class Config:
        orm_model = True 

class UserNotFound(BaseModel):
    message: Union[str, None] = None

