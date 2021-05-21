from typing import List
from datetime import datetime
from sqlalchemy.orm.session import Session
from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.blog import Blog, BlogResponse
from src.schemas.authentication import LoginSchema
from src.models.blog import Blog as BlogModel
from src.services.security.oauth2 import oauth
from src.services.databaseService import database


router = APIRouter()


@router.get('/all',tags=['Blog'], response_model=List[BlogResponse], status_code=status.HTTP_200_OK)
async def get_blogs(db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = db.query(BlogModel).all()
    return result


@router.get('/{id}',tags=['Blog'], response_model=BlogResponse, status_code=status.HTTP_200_OK)
async def get_blog(id: int, db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = db.query(BlogModel).filter(BlogModel.id == id).first()
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User requested does not exist!')

    return result


@router.post('/', tags=['Blog'], response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def create_blog(request: Blog, db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    created = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    new_blog = BlogModel(title=request.title, body=request.body, created=created)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    if not new_blog:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error trying to create blog!')

    return new_blog


@router.put('/',tags=['Blog'], status_code=status.HTTP_202_ACCEPTED)
async def blog(id: int, request: Blog, db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = db.query(BlogModel).filter(BlogModel.id == id)

    if not result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} does not exist!')

    result.update({'title': request.title, 'body': request.body})
    db.commit()

    return {'result': f'User with id {id} updated!'}

@router.delete('/{id}',tags=['Blog'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = db.query(BlogModel).filter(BlogModel.id == id).delete(synchronize_session=False)
    db.commit()

    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='User could not be deleted!')