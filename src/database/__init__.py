from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config.settings import config

SQLALCHEMY_DATABASE_URL = config['DATABASE']['SQLALCHEMY']['CONFIG']['DB.URL']
SQLALCHEMY_DATABASE_ECHO = config['DATABASE']['SQLALCHEMY']['CONFIG']['DB.ECHO']

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # SQLite requires the next arg:
    connect_args={
        "check_same_thread": False
    },
    echo=True
)
#The sessionmaker factory generates new Session objects when called
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# The new base class will be given a metaclass that produces appropriate Table objects and makes the 
# appropriate mapper() calls based on the information provided declaratively in the class and any subclasses of the class:
Base = declarative_base()
