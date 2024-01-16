from sqlalchemy.orm import Session

from models.users import User
from models.captures import Capture

from schemas.users import UserInDB

def create_user(db:Session, user: UserInDB): 
    # fake_hashed_password = user.password + "notreallyhased"
    db_user = User(email=user.email,username=user.username)
    db.add(db_user)
    db.commit() 
    db.refresh(db_user)
    return db_user 

def delete_users(db:Session, user_id:int):
    db_user = db.query(User).filter(User.id == user_id).first()
    db_user_captures = db.query(Capture).filter(Capture.owner_id == user_id)
    if db_user is not None:
        # 级联删除，删除用户的同时删除用户的所有capture
        db.delete(db_user)
        db.commit()

        return {
            "message":"User deleted successfully", 
        }
    else:
        return {"message": "User not found"}

def get_user(db:Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first() 

def get_user_by_username(db:Session, username:str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db:Session, email:str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0 , limit:int = 100):
    return db.query(User).offset(skip).limit(limit).all()  
