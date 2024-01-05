from typing import Union,List
from pydantic import BaseModel 

class ItemBase(BaseModel):
    title: str 
    description: Union[str, None] = None 

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id:int 
    owner_id: int 

    class Config:
        orm_model = True 

class UserBase(BaseModel):
    email: str 

class UserCreate(UserBase):
    password: str 

class User(UserBase):
    id:int 
    is_activate: bool
    items: List[Item] = []
    
    class Config:
        orm_model = True 