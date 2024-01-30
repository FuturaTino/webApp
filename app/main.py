from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.database import Base
from db.database import SessionLocal, engine
from core.router import all_routers
from core.dependencies import get_db
from typing import List
from fastapi import APIRouter
from fastapi import Request
from crud.captures import get_captures
from core.dependencies import get_db
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/admin",tags=["index"])
def read_root(request:Request,db:Session = Depends(get_db)):
    captures = get_captures(db)

    return templates.TemplateResponse("index.html", {"request": request,"captures": captures})

app.include_router(all_routers)

if __name__ == "__main__":
    import uvicorn

    # 检测是否有worker，是否有redis数据库
    
    uvicorn.run("main:app", host="127.0.0.1",reload=True)

# 1. 包引入、 模块 python基础 需要补一下
# 2. celery自定义任务中，对数据库的引用
# 3.保证每一个任务的STATUS都能在停止后继续进行