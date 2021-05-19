from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class Roles(BaseModel):
    name: str

class User(BaseModel):
    name: str = 'John'
    lastname: str = 'Doe'
    enabled: bool = False
    created: datetime = datetime.now()
    roles: Optional[List[Roles]] = []

class UserRequest(User):
    username: str
    password: str

class UserResponse(BaseModel):
    message: str