from typing import Any, Union, Optional
import logging
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from datetime import datetime, timedelta
import json
from jose import jwt

logger = logging.getLogger(__name__)

ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/accounts/login")


def create_access_token(data: Union[str, Any], expires_delta: timedelta = None, general_use=False) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": json.dumps(data), "general_use": general_use}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str, *,  secret_key: str = settings.SECRET_KEY, algorithms=None) -> Union[dict, bool]:
    if algorithms is None:
        algorithms = [ALGORITHM]
    try:
        return jwt.decode(token, secret_key, algorithms)
    except ValueError as e:
        return False
