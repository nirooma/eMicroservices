from starlette.authentication import (
    AuthenticationBackend, AuthenticationError,
    AuthCredentials, BaseUser
)
from fastapi import Request
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware

import binascii

from app.crud.users import get_current_user
from app.models import User


class SimpleUser(BaseUser):
    def __init__(self, user: User) -> None:
        self.user = user

    @property
    async def is_authenticated(self) -> bool:
        return True

    @property
    async def display_name(self) -> str:
        return self.user.username

    def __repr__(self):
        return self.user


def get_user(request: Request):
    if request.user.is_authenticated:
        return request.user.user


class BearerAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        permissions = []
        if "Authorization" not in request.headers and not request.cookies.get("SessionToken"):
            return

        credentials = request.cookies.get("SessionToken") or request.headers["Authorization"].split()[1]
        user: User = await get_current_user(token=credentials)
        if not user:
            return
        if user.is_superuser:
            permissions.append("is_superuser")
        if user.is_staff:
            permissions.append("is_staff")

        permissions.append("authenticated")
        return AuthCredentials(permissions), SimpleUser(user)


middleware = [
    Middleware(AuthenticationMiddleware, backend=BearerAuthBackend())
]
