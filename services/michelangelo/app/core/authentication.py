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
    return request.user.user


class BearerAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'bearer':
                return
            user: User = await get_current_user(token=credentials)

        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        # TODO: You'd want to verify the username and password here.
        return AuthCredentials(["authenticated"]), SimpleUser(user)


middleware = [
    Middleware(AuthenticationMiddleware, backend=BearerAuthBackend())
]
