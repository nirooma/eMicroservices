from typing import Any, Union

from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from datetime import datetime, timedelta
import json
from jose import jwt


ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/accounts/login")


def create_access_token(data: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": json.dumps(data)}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str, *,  secret_key: str = settings.SECRET_KEY, algorithms=None) -> dict:
    if algorithms is None:
        algorithms = [ALGORITHM]

    return jwt.decode(token, secret_key, algorithms)