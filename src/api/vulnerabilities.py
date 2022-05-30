from typing import Optional
from fastapi.param_functions import Query
from fastapi import APIRouter, Security, status

from src.services.vulnerabilitiesService import CiscoVulnApi
from src.services.security.oauth2 import oauth
from src.schemas.authentication import LoginSchema
from src.services.loggerService import loggerService


router = APIRouter()

@router.get("/vuln_by_version/", tags=['Cisco'], status_code=status.HTTP_200_OK)
async def get_by_sn(os: str, version: str, current_user: LoginSchema=Security(oauth.get_current_user, scopes=["cisco"])):
    os = os.lower()
    loggerService.info(f"Getting vulnerabilities information from Cisco API for {os}-{version}.")
    openVulApi = CiscoVulnApi()
    result = openVulApi.os(os, version)
    loggerService.debug(result)
    return result