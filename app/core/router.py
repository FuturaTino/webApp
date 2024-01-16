from fastapi import APIRouter 
from api import users, items, captures

all_routers = APIRouter()

all_routers.include_router(users.router,tags=["users"])
all_routers.include_router(items.router,tags=["items"])
all_routers.include_router(captures.router,tags=["captures"])

