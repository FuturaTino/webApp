from fastapi import APIRouter 
from api import users, captures

all_routers = APIRouter()

all_routers.include_router(users.router,tags=["users"])
all_routers.include_router(captures.router,tags=["captures"])

