from typing import Optional
from fastapi.param_functions import Query
from fastapi import APIRouter, Security, status, Request, Response

from src.services.loggerService import loggerService
from src.services.security.oauth2 import oauth
from src.services.eoxService import CiscoEoXApi
from src.schemas.authentication import LoginSchema


router = APIRouter()

@router.get("/eox_by_sn/", tags=['Cisco'], status_code=status.HTTP_200_OK)
async def get_by_sn(sn: str, current_user: LoginSchema=Security(oauth.get_current_user, scopes=["cisco"])):
    sn = sn.lower()
    loggerService.info(f"Getting EoX information from Cisco API for {sn}.")
    eoxApi = CiscoEoXApi()
    result = eoxApi.get_eox_by_sn(sn)
    loggerService.debug(result)
    return result


@router.get("/eox_by_version/", tags=['Cisco'], status_code=status.HTTP_200_OK)
async def get_by_version(version: str, os: Optional[str] = None, current_user: LoginSchema=Security(oauth.get_current_user, scopes=["cisco"])):
    version = version.lower()
    loggerService.info(f"Getting EoX information from Cisco API for {version}.")
    eoxApi = CiscoEoXApi()
    result = eoxApi.get_eox_by_soft_rel(version=version, os=os)
    loggerService.debug(result)
    return result