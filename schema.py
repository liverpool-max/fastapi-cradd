from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    username: str
    password: str
    class Config:
        extra = "forbid"
    

class UserDeleteSchema(BaseModel):
    username: str
    class Config:
        extra = "forbid"


class UserUpdateScheme(BaseModel):
    password : str
    new_password : str
    class Config:
        extra = "forbid"
