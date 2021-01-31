import time
from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.models.modelName import ModelName


router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/item/{item}",tags=['users'])
async def get(item: int):
    return {"item": item}


@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}