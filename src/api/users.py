import json
from os import stat
import time
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic.schema import model_schema
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from src.schemas.userSchema import UserResponse, UserRequest


router = APIRouter()

users = []


@router.get('/all',tags=['users'], response_model=UserResponse, status_code=200) 
async def get_users():
    result =  {}
    if len(users) == 0:
        raise HTTPException(status_code=404, detail='No users') 
    else:
        result['message'] = str(users)
        return result


@router.get('/',tags=['users'], response_model=UserResponse, status_code=200)
async def get_user(name: str):
    result =  {}

    for u in users:
        if name in u:
            result['message'] = u
            return result

    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='User not found!')

@router.post('/', tags=['users'], status_code=201, response_model=UserResponse)
async def create_user(user: UserRequest):
    result = {}

    if user.json() not in users:
        users.append(user.json())
        result['message'] = f'User {user.name} created!'
    else:
        raise HTTPException(status_code=HTTP_409_CONFLICT, detail='User already exists!')

    return result


@router.put('/',tags=['users'], response_model=UserResponse, status_code=200)
async def edit_user(user: UserRequest):
    return {'result': 'edito!'}


@router.delete('/',tags=['users'], response_model=UserResponse, status_code=200)
async def delete_user(user: UserRequest):
    return {'result': 'edito'}