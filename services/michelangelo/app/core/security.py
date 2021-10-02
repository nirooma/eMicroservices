from typing import Optional

from app.models import User
from passlib.context import CryptContext
from app.crud import users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate(username: str, password: str) -> Optional[User]:
    """ Authenticate user via username and password """
    user: User = await users.get_user_by_username(username)
    if not user:
        return
    verified_password: bool = verify_password(password, user.password)
    if verified_password is False:
        return
    return user
