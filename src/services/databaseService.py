from sqlalchemy import exc
from src.models.user import User
from src.config.settings import config
from src.services.security.hashing import Hash
from src.database import SessionLocal
from src.services.loggerService import loggerService

class Database():

    def __init__(self):
        pass


    def init_defaults(self, db):
        try:
            NETOPS_PASS = os.environ['NETOPS_PASS']
        except Exception as e:
            loggerService.error('NETOPS_PASS missing!')
            NETOPS_PASS = config['API']['PASSWORD']
        hashed_password = Hash.bcrypt(NETOPS_PASS)
        netops_user = {
            'username': config['API']['USERNAME'],
            'password': hashed_password
        }
        self.create_default_user(netops_user, db)


    def create_default_user(self, user, db):
        new_user = User(
            username=user['username'], password=user['password']
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