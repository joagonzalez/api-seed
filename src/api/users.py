import json
import time
from os import stat
from pydantic.schema import model_schema
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from fastapi import APIRouter, Depends, HTTPException, Response, status
from src.schemas.user import UserResponse, UserRequest
from src.schemas.authentication import LoginSchema
from src.services.security.oauth2 import oauth

router = APIRouter()

users = []


@router.get('/all',tags=['Users'], response_model=UserResponse, status_code=200) 
async def get_users(current_user: LoginSchema=Depends(oauth.get_current_user)):
    result =  {}
    if len(users) == 0:
        raise HTTPException(status_code=404, detail='No users') 
    else:
        result['message'] = str(users)
        return result


@router.get('/',tags=['Users'], response_model=UserResponse, status_code=200)
async def get_user(name: str, current_user: LoginSchema=Depends(oauth.get_current_user)):
    result =  {}

    for u in users:
        if name in u:
            result['message'] = u
            return result

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='User not found!')

@router.post('/', tags=['Users'], status_code=201, response_model=UserResponse)
async def create_user(user: UserRequest, current_user: LoginSchema=Depends(oauth.get_current_user)):
    result = {}

    if user.json() not in users:
        users.append(user.json())
        result['message'] = f'User {user.name} created!'
    else:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail='User already exists!')

    return result


@router.put('/',tags=['Users'], response_model=UserResponse, status_code=200)
async def edit_user(user: UserRequest, current_user: LoginSchema=Depends(oauth.get_current_user)):
    return {'result': 'edito!'}


@router.delete('/',tags=['Users'], response_model=UserResponse, status_code=200)
async def delete_user(user: UserRequest):
    return {'result': 'edito'}