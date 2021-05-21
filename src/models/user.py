from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from src.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    username = Column(String, primary_key=True)
    password = Column(String)
    name = Column(String)
    lastname = Column(String)
    email = Column(String)
    enabled = Column(Boolean)
    created = Column(DateTime)