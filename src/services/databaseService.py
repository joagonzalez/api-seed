import os
from sqlalchemy import exc
from datetime import datetime

from src.models.user import User
from src.models.blog import Blog
from src.database import SessionLocal
from src.services.security.hashing import Hash
from src.services.loggerService import loggerService
from src.config.settings import config


class Database():

    def __init__(self):
        pass


    def init_defaults(self, db):
        try:
            PASSWORD = os.environ['PASSWORD']
        except Exception as e:
            loggerService.warning('PASSWORD missing!')
            
            USERNAME = config['API']['USER']['USERNAME']
            PASSWORD = config['API']['USER']['PASSWORD']
            NAME = config['API']['USER']['NAME']
            LASTNAME = config['API']['USER']['LASTNAME']
            EMAIL = config['API']['USER']['EMAIL']
            ENABLED = config['API']['USER']['ENABLED']
            CREATED = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

        hashed_password = Hash.bcrypt(PASSWORD)
        user = {
            'username': USERNAME,
            'password': hashed_password,
            'name': NAME,
            'lastname': LASTNAME,
            'email': EMAIL,
            'enabled': ENABLED,
            'created': CREATED
        }

        self.create_default_user(user, db)


    def create_default_user(self, user, db):
        new_user = User(
            username=user['username'], password=user['password'],
            name=user['name'], lastname=user['lastname'], email=user['email'],
            enabled=user['enabled'], created=user['created']
        )
        
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        except exc.IntegrityError:
            db.rollback()
        finally:
            db.close()
            

    def get_db_session(self):
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

database = Database()