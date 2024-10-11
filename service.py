from models import User
from schema import *
from sqlalchemy.orm import Session
from exception import UserNotFoundException
import psycopg2
from settings import DATABASE_URL
import bcrypt


def create_user_in_db(*, data: UserCreateSchema, db: Session):
    hashed_password = bcrypt.hashpw(data.password.encode("utf-8"),bcrypt.gensalt())
    new_user = User(username=data.username,password=hashed_password.decode("utf-8"))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"New user is created"}


def delete_user_in_db(*, data: UserDeleteSchema, db: Session):
    user_in_db = db.query(User).filter(User.username == data.username).first()
    db.delete(user_in_db)
    db.commit()
    return {"message":"User is deleted"}


def get_user_in_db(*, username: str, db : Session):
    user_in_db = db.query(User).filter(User.username == username).first()
    if not user_in_db:
        raise UserNotFoundException
    return {"Your username": {user_in_db.username}}

def changed_password_in_db(current_username:str, data: UserUpdateScheme, db : Session):
    hashed_password = bcrypt.hashpw(data.new_password.encode("utf-8"),bcrypt.gensalt())
    is_correct_user = db.query(User).filter_by(username = current_username).first()
    if not is_correct_user:
        raise UserNotFoundException
    if not bcrypt.checkpw(data.password.encode("utf-8"),is_correct_user.password.encode("utf-8")):
        raise UserNotFoundException
    
    db.query(User).filter(User.username==current_username).update({"password":hashed_password.decode("utf-8")})
    db.commit()
    return {"message":"Password is changed"}


def reset_base():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("DELETE FROM users;")

    cur.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1;")
    conn.commit()
    cur.close()
    conn.close()


        







    