from fastapi import Header, HTTPException 

from db.database import SessionLocal
async def get_token_header(x_token:str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    
async def get_query_token(token:str):
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
    

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db # yield is a keyword that is used like return, except the function will return a generator.
    finally:
        db.close()
