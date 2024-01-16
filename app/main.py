from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from db.database import Base
from db.database import SessionLocal, engine
from core.router import all_routers
from core.dependencies import get_db

from typing import List

from fastapi import APIRouter

Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(all_routers)

def read_root():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="title" type="text">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

# app.include_router(users.router)
app.get("/", response_class=HTMLResponse)(read_root)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0",reload=True)