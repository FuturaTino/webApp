from typing import List, Union
from pydantic import BaseModel
from schemas.captures import Capture 
from schemas.items import Item 

class UserBase(BaseModel):
    email: str 
    username:str

class UserInDB(UserBase):
    password: str 

class UserOutDB(UserBase):
    id:int
    is_activate: Union[bool, None] = True
    captures: List[Capture] = []
    class Config:
        orm_model = True
        
class User(UserBase):
    id:int
    is_activate: Union[str, None] = True
    items: List[Item] = []
    captures: List[Capture] = []
    class Config:
        orm_model = True 

class UserNotFound(BaseModel):
    message: Union[str, None] = None

