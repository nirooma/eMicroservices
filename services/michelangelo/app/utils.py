import functools

from fastapi import status
from starlette.responses import JSONResponse

from app.core.configuration_utils import config
from app.models import User


def response(
        detail=config.get("defaultAnswer"),
        status_code=status.HTTP_200_OK,
        **kwargs
):
    return {"detail": detail, "status": status_code, **kwargs}


def permission(permission_list: list):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # if not user.is_superuser:
            return response(config.get("errors")["permissionError"], status_code=status.HTTP_401_UNAUTHORIZED)

        return wrapper
    return decorator
