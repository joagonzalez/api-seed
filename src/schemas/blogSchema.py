from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    username: str = 'John'
    lastname: str = 'Doe'
    enabled: bool = False
    created: datetime = None
    roles: list = None
