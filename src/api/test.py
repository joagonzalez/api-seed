import time
from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.schemas.schemaTest import schemaName


router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/item/{item}",tags=['users'])
async def get(item: int):
    return {"item": item}

@router.post("/item/",tags=['users'])
async def edit(item: int):
    return {"item": item}

@router.put("/item/",tags=['users'])
async def edit(item: int):
    return {"item": item}

@router.delete("/item/",tags=['users'])
async def edit(item: int):
    return {"item": item}

@router.get("/schemas/{schema_name}")
async def get_model(schema_name: schemaName):
    if schema_name == schemaName.alexnet:
        return {"model_name": schema_name, "message": "Deep Learning FTW!"}

    if schema_name.value == "lenet":
        return {"model_name": schema_name, "message": "LeCNN all the images"}

    return {"model_name": schema_name, "message": "Have some residuals"}