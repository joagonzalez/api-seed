# rest-api-seed
![Python](https://img.shields.io/badge/restapi-v0.0.1-orange)![Python](https://img.shields.io/badge/fastApi-v0.61.1-blue)
![Python](https://img.shields.io/badge/uvicorn-v0.12.1-blue)
![Python](https://img.shields.io/badge/pymsteams-v0.1.13-blue)
![Python](https://img.shields.io/badge/python-v3.8.5-blue)
![Python](https://img.shields.io/badge/platform-linux--64%7Cwin--64-lightgrey)

This service implements a scalable rest-api seed using fastApi. Parametriztion for the app is loaded from *src/config/settings.py*. Different endpoints were develped in order to have templates for a variety of features, for example:

- Async tasks: Celery with RabbitMQ as message broker
- Users CRUD: SQLAlchemy and Flask models
- Microsoft Teams: Pymsteams and requests

**Content**
- [Getting started](#getting-started)
- [Endpoints](#endpoints)
- [Mock server](#mock-server)
- [Build](#docker)
- [Run](#run)
- [References](#references)


## Getting started

Dir structure of repo
```
├── dashboard
├── mock-server
└── src
    ├── config
    ├── logs
    ├── services
    └── utilities

7 directories
```
