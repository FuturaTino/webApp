from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas

from app.crud import crud
from db.database import SessionLocal, engine

from dependencies import get_db

from typing import List

from fastapi import APIRouter
from api import items, users, captures

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(captures.router) 
@app.get("/")
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
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0",reload=True)