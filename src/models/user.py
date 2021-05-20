from sqlalchemy import Column, Integer, String
from src.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    password = Column(String)