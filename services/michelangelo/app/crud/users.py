import json
import logging
from functools import lru_cache

from fastapi import Depends, status, HTTPException
from app.schemas.users import User_Pydantic, UserIn_Pydantic
from app.models import User

from app.core import security
from app.core.jwt import oauth2_scheme
from jose import JWTError
from app.schemas.token import TokenData
from app.core.jwt import decode_access_token

logger = logging.getLogger(__name__)


async def all_users() -> User_Pydantic:
    return await User_Pydantic.from_queryset(User.all())


async def delete_all_users(i_know_what_im_doing=False):
    if not i_know_what_im_doing:
        return
    return await User.all().delete()


async def create_user(user: UserIn_Pydantic) -> User:
    user_data = user.dict().copy()
    password = user_data.pop("password")
    return await User.create(**user_data, password=security.get_password_hash(password))


async def get_user_by_username(username: str) -> User:
    return await User.filter(username=username).first()


async def get_user_by_email(email: str) -> User:
    return await User.filter(email=email).first()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        sub = json.loads(payload.get("sub"))
        username = sub["username"]
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def create_system_user():
    user = await get_user_by_username("admin")
    if not user:
        user = await User.create(
            username="admin",
            password=security.get_password_hash("admin"),
            is_superuser=True,
            is_active=True,
            email="admin@admin",
            phone="000000"
        )
    logger.info("system user has created to the dibi.")
    return user
