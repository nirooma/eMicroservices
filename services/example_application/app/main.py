from app.core.config import settings
import datetime
import platform

from fastapi import Depends, FastAPI, Request, status, Response
from fastapi.responses import JSONResponse


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.get("/health-check")
async def health_check():
    """ Internal use only - Do not use with a client API """

    return JSONResponse(
        {
            "status": status.HTTP_200_OK,
            "timestamp": datetime.datetime.now().ctime(),
            "debugMode": settings.DEBUG,
            "OperatingSystem": platform.uname()
        }
    )


