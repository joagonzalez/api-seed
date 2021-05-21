config = {
    'ENVIRONMENT': 'local',
    'SERVER': {
        'HOSTNAME': '0.0.0.0',
        'PORT': 5000,
        'DEBUG': True,
        'RELOAD': True,
        'LOG_LEVEL': 'debug',
        'WORKERS': 5
    },
    'API': {
        'TITLE': 'REST API SEED',
        'DESCRIPTION': 'Minimal rest api setup',
        'VERSION': '1.0.0',
        'USER': {
            'USERNAME': 'netops',
            'PASSWORD': 'netops_2021',
            'NAME': 'Joaquin',
            'LASTNAME': 'Gonzalez',
            'EMAIL': 'joagonzalez@gmail.com',
            'ENABLED': True
        }
    },
    'SWAGGER': {
        'DOCS_URL': '/docs',
        'REDOC_URL': '/redoc_docs',
    },
    'JWT': {
        'SECRET_KEY': "_!S0m3R4nd0mk3yf0rn3t0pst34m!_",
        'ALGORITHM': "HS256",
        'ACCESS_TOKEN_EXPIRE_MINUTES': 30
    },
    'DATABASE': {
        'SQLALCHEMY': {
            'PREFIX': 'DB.',
            'CONFIG': {
                'DB.URL': 'sqlite:///./src/database/sql_app.db',
                'DB.ECHO': True
            }
        }
    },
    'LOGGING': {
        'LOGGER': 'app_production',
        'LEVEL': 'DEBUG',
        'FORMAT': "%(asctime)s - %(name)s - %(process)s - %(levelname)s - %(message)s",
        'DATEFMT' : "%d-%b-%y %H:%M:%S" 
    }
}
