from typing import List
from datetime import datetime
from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.authentication import LoginSchema
from src.schemas.user import UserEdit, UserResponse, UserRequest, User
from src.models.user import User as UserModel
from src.services.security.hashing import Hash
from src.services.security.oauth2 import oauth
from src.services.databaseService import database


router = APIRouter()


@router.get('/all',tags=['Users'], response_model=List[UserResponse], status_code=status.HTTP_200_OK) 
async def get_users(db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = db.query(UserModel).all()
        
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No users') 
    
    return result

@router.get('/',tags=['Users'], response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(username: str, db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = db.query(UserModel).filter(UserModel.username == username).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found!')

    return result


@router.post('/', tags=['Users'], response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserRequest, db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    created = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    password = Hash.bcrypt(user.password)

    new_user = UserModel(username = user.username, password = password,
                name = user.name, lastname = user.lastname, email=user.email,
                enabled = user.enabled, created=created)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if not new_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error trying to create blog!')

    return new_user


@router.put('/',tags=['Users'], status_code=status.HTTP_202_ACCEPTED)
async def edit_user(username: str, user: UserEdit, db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = db.query(UserModel).filter(UserModel.username == username)
    password = Hash.bcrypt(user.password)

    if not result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with username {username} does not exist!')

    result.update({'name': user.name, 'lastname': user.lastname,
                    'email': user.email, 'enabled': user.enabled,
                    'password': password})
    db.commit()

    return {'result': f'User with username {username} updated!'}


@router.delete('/',tags=['Users'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(username: str, db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = db.query(UserModel).filter(UserModel.username == username).delete(synchronize_session=False)
    db.commit()

    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='User could not be deleted!')