from typing import Optional
from jose import JWTError, jwt
from datetime import datetime, timedelta

from src.config.settings import config
from src.schemas.token import TokenData


class TokenJwt():
    SECRET_KEY = config['JWT']['SECRET_KEY']
    ALGORITHM = config['JWT']['ALGORITHM']
    ACCESS_TOKEN_EXPIRE_MINUTES = config['JWT']['ACCESS_TOKEN_EXPIRE_MINUTES']

    def __init__(self):
        pass


    def create_access_token(self, data: dict, expires_delta: Optional[timedelta]=None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt


    def verify_token(self, token: str, credentials_exception):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception

token = TokenJwt()