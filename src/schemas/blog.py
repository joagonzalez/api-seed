from datetime import date, datetime
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True
    

class BlogResponse(Blog):
    id: int
    created: datetime
