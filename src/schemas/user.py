from pydantic import BaseModel
from typing import Optional, List


class Roles(BaseModel):
    name: str


class User(BaseModel):
    name: str = 'John'
    lastname: str = 'Doe'
    email: str
    enabled: bool = False
    roles: Optional[List[Roles]] = []


class UserRequest(User):
    username: str
    password: str


class UserResponse(BaseModel):
    message: str