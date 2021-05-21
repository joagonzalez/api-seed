from datetime import datetime
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str


class BlogResponse(Blog):
    id: int