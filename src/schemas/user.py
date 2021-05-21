from datetime import datetime
from src.database import Base
from pydantic import BaseModel
from typing import Optional, List


class Roles(BaseModel):
    name: str

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str = 'John'
    lastname: str = 'Doe'
    email: str = 'johndoe@test'
    enabled: bool = True
    created: datetime = None

    class Config:
        orm_mode = True


class UserRequest(User):
    username: str
    password: str


class UserResponse(User):
    username: str


class UserEdit(BaseModel):
    name: str = ''
    lastname: str = ''
    email: str = ''
    enabled: bool = True
    password: str = ''

    class Config:
        orm_mode = True