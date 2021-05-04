import uvicorn

from src.config.settings import config

# TODO jwt, sqlalchemy, usersClass, 
# TODO incorporar clases apis cisco, teams, formio, infoblox, modelos, tests

if __name__ == '__main__':
    uvicorn.run(    
        "src:app",
        host=config['SERVER']['HOSTNAME'],
        port=config['SERVER']['PORT'],
        log_level=config['SERVER']['LOG_LEVEL'],
        reload=config['SERVER']['RELOAD'],
        workers=config['SERVER']['WORKERS']
    )