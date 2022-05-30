from src.schemas.blog import Blog
from fastapi import FastAPI, Depends

from src.config.settings import config
from src.constants.prompt import PROMPT
from src.api.users import router as users
from src.api.blog import router as blog
from src.api.eox import router as eox
from src.api.vulnerabilities import router as vulnerabilities
from src.api.authentication import router as authentication
from src.services.databaseService import database
from src.database import SessionLocal, Base, engine


class Application(FastAPI):
    '''
    Wrapper for FAST API
    '''

    def __init__(self):
        ''' SWAGGER CONFIGURATION '''
        super().__init__(
            title=config['API']['TITLE'],
            description=config['API']['DESCRIPTION'],
            version=config['API']['VERSION'],
            docs_url=config['SWAGGER']['DOCS_URL'],
            redoc_url=config['SWAGGER']['REDOC_URL']            
        )


    def bootstrap(self):
        ''' SERVER CONFIGURATION '''
        self.debug = config['SERVER']['DEBUG']
        self.configureApis()
        self.configureDB()
        print(PROMPT)


    def configureApis(self):
        ''' REGISTER API ROUTERS '''
        self.include_router(authentication)    
        self.include_router(users, prefix='/users') 
        self.include_router(blog, prefix='/blog') 
        self.include_router(vulnerabilities, prefix='/vulnerabilities')
        self.include_router(eox, prefix='/eox')
        
    def configureDB(self):
        ''' INIT SQLITE DB '''
        Base.metadata.create_all(engine)
        db = SessionLocal()
        database.init_defaults(db)