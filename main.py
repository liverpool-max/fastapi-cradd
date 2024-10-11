from fastapi import FastAPI,Depends
from db import get_db
from sqlalchemy.orm import Session
from schema import *
from service import *

app = FastAPI()

@app.get("/")
def health_check():
    return {"msg":"health check passed"}

@app.post("/user")
def create_user(item: UserCreateSchema, db: Session = Depends(get_db)):
    message = create_user_in_db(data = item, db = db)
    return message


@app.delete("/user")
def delete_user(item: UserDeleteSchema, db: Session = Depends(get_db)):
    message = delete_user_in_db(data = item, db = db)
    return message

@app.get("/user")
def get_user(username: str, db : Session = Depends(get_db)):
    message = get_user_in_db(username = username, db = db)
    return message


@app.put("/password")
def change_password(username:str, item : UserUpdateScheme, db : Session = Depends(get_db)):
    message = changed_password_in_db(current_username = username, data = item, db = db)
    return message


@app.delete("/all_user")
def reset_my_base():
    message=reset_base()
    return {"Message":"Your base has reseted"}