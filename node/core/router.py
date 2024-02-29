from fastapi import APIRouter 
from api import users, captures,auth


all_routers = APIRouter()

all_routers.include_router(auth.router,tags=["Auth"])
all_routers.include_router(users.router,tags=["Users"])
all_routers.include_router(captures.router,tags=["Captures"])