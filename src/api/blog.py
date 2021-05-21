from typing import Optional, List
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import null
from fastapi import APIRouter, Depends, HTTPException, Response, status
from starlette.status import HTTP_202_ACCEPTED

from src.schemas.blog import Blog
from src.schemas.authentication import LoginSchema
from src.models.blog import Blog as BlogModel
from src.services.security.oauth2 import oauth
from src.services.loggerService import loggerService
from src.services.databaseService import database


router = APIRouter()


@router.get('/',tags=['Blog'], status_code=status.HTTP_200_OK)
async def get_all_blogs(db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = db.query(BlogModel).all()
    return result


@router.get('/{id}',tags=['Blog'], status_code=status.HTTP_200_OK)
async def get_blog(id: int, response: Response, db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = db.query(BlogModel).filter(BlogModel.id == id).first()
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User requested does not exist!')

    return result


@router.post('/', tags=['Blog'], status_code=status.HTTP_201_CREATED)
async def create_blog(request: Blog, db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    new_blog = BlogModel(title=request.title, body=request.body)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog


@router.put('/',tags=['Blog'], status_code=status.HTTP_202_ACCEPTED)
async def blog(id: int, request: Blog, db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = db.query(BlogModel).filter(BlogModel.id == id)

    if not result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} does not exist!')

    result.update(request)
    db.commit()

    return {'result': f'User with id {id} updated!'}

@router.delete('/{id}',tags=['Blog'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(database.get_db_session), current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = db.query(BlogModel).filter(BlogModel.id == id).delete(synchronize_session=False)
    db.commit()

    if not result:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='User could not be deleted!')

    return {'result': f'User {id} deleted!'}