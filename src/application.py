from fastapi import FastAPI, Depends

from src.config.settings import config
from src.constants.prompt import PROMPT
from src.api.users import router as users

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
        print(PROMPT)

    def configureApis(self):
        ''' REGISTER API ROUTERS '''
        self.include_router(users, prefix='/users')    