from fastapi import Depends, FastAPI, HTTPException,APIRouter,Request
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from db.database import Base
from db.database import SessionLocal, engine
from core.router import all_routers
from core.dependencies import get_db
from crud.captures import get_captures
from core.auth import get_current_user

app = FastAPI()
app.include_router(all_routers)
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="app/templates")
origins = [
    "http://localhost:8000",  # Allow requests from this origin
    "http://127.0.0.1:8000",  # Also allow requests from this origin
    "http://192.168.31.17:5173",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    # 检测是否有worker，是否有redis数据库

    uvicorn.run("main:app", host="0.0.0.0",port=8000,reload=True)
