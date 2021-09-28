from fastapi import status
from starlette.responses import JSONResponse

from app.core.configuration_utils import config


async def response(
        detail=config.get("defaultAnswer"),
        status_code=status.HTTP_200_OK,
        **kwargs
):
    return {"detail": detail, "status": status_code, **kwargs}
