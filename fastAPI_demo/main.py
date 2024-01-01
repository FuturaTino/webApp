from typing import Union 
from fastapi import FastAPI ,Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel 

app = FastAPI()


