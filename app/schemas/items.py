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