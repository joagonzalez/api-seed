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
        'VERSION': '0.1.0',
    },
    'SWAGGER': {
        'DOCS_URL': '/docs',
        'REDOC_URL': '/redoc_docs',
    },
    'JWT': {
        'SECRET_KEY': 'some-secret-key'
    },
    'DATABASE': {
        'SQLALCHEMY': {
            'PREFIX': 'DB.',
            'CONFIG': {
                'DB.URL': 'sqlite:///./sql_app.db',
                'DB.ECHO': True
            }
        }
    },
}
