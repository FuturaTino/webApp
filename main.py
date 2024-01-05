from typing import Union 
from fastapi import FastAPI ,Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel,Field 
import uuid
app = FastAPI()

class CaptureStatus(BaseModel):
    id:str
    latest_run_status:str
    latest_run_progress:str
    latest_run_current_stage:str

class CaptureInfo(BaseModel):
    id:str
    slug:str 
    title:str
    work_type: Union[str, None] = None
    date: Union[str, None] = None 
    source_url: Union[str, None] = None
    result_url: Union[str, None] = None

class User(BaseModel):
    username: Union[str, None] = None
    email: Union[str, None] = None
    image_url: Union[str, None] = None

class Capture(BaseModel):
    info: CaptureInfo
    status: CaptureStatus
    user: User 
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/capture/create",response_model=Capture)
def create_capture(username:str, title:str,work_type:Union[str, None]=None):
        id = str(uuid.uuid4())
        if work_type == None:
             work_type = "reconstruction"
        date = "2021-07-01"
        slug = title + "-" + username + "-" + date
        info = CaptureInfo(id=id,slug=slug,title=title,work_type=work_type,date=date)
        status = CaptureStatus(id=id,latest_run_status="running",latest_run_progress="0%",latest_run_current_stage="reconstruction")
        user = User(username=username)
        capture = Capture(info=info,status=status,user=user)

        # save capture to database
        pass 
        return capture


@app.get("/capture/query/{id}",response_model=Capture)
def read_capture(id:str):

    # retrive capture from database
    title = "test"
    type = "reconstruction"
    date = "2021-07-01"
    username = "zhangsan"
    slug = title + "-" + username + "-" + date
    source_url = "test"
    result_url = "test"
    info = CaptureInfo(id=id,slug=slug,title=title,type=type,date=date,source_url=source_url,result_url=result_url)
    status = CaptureStatus(id=id,latest_run_status="running",latest_run_progress="0%",latest_run_current_stage="reconstruction")
    user = User(username=username)
    capture = Capture(info=info,status=status,user=user)

    return capture  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)