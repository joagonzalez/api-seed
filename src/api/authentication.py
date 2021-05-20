from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, HTTPException

from src.models.user import User
from src.config.settings import config
from src.services.security.hashing import Hash
from src.services.security.jwt import token
from src.services.databaseService import database
from src.schemas.authentication import LoginSchema
from src.services.loggerService import loggerService


router = APIRouter()

@router.post('/login', tags=['Authentication'])
async def login(request: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(database.get_db_session)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect username or password")

    # JWT Generation
    access_token_expires = timedelta(minutes=config['JWT']['ACCESS_TOKEN_EXPIRE_MINUTES'])
    access_token = token.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
