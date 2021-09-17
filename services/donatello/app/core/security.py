from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import users
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate(session: AsyncSession, *, username: str, password: str) -> Optional[User]:
    """ Authenticate user via username and password """
    user = await users.get_user_by_username(session, username=username)
    if not user:
        return
    if verify_password(password, user.password) is False:
        return
    return user
