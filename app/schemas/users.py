from typing import List, Union
from pydantic import BaseModel
from schemas.captures import CaptureOutDB,CaptureReponse
from schemas.items import Item 

class UserBase(BaseModel):
    email: str
    username:str

class UserInDB(UserBase):
    password: str 


class LoginInDB(BaseModel):
    email: Union[str, None] = None
    username: Union[str, None] = None
    password: str
    
class UserOutDB(UserBase):
    id:int
    is_activate: Union[bool, None] = True
    captures: List[CaptureOutDB] = []
    class Config:
        orm_model = True
        
class UserResponse(UserBase):
    id:int
    is_activate: Union[str, None] = True
    captures: List[CaptureReponse] = []
    class Config:
        orm_model = True 

class UserNotFound(BaseModel):
    message: Union[str, None] = None

