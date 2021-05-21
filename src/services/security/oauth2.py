from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.services.security.jwt import token


class Oauth:
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="login")

    def __init__(self):
        pass

    def get_current_user(self, data: str = Depends(OAUTH2_SCHEME)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        return token.verify_token(data, credentials_exception)

oauth = Oauth()