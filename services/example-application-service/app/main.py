import datetime
import logging
import platform

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from app.core.config import settings


logger = logging.getLogger(__name__)


def get_app_configuration():
    application = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    from app.core.logging import configure_logging
    configure_logging()

    return application


app = get_app_configuration()


@app.get("/health-check")
async def health_check(request: Request) -> JSONResponse:
    """Internal use only - Do not use with a client API"""
    print(settings.APP_ENVIRONMENT)
    logger.info(f"Health check called from IP #{request.scope.get('server')[0]}")
    return JSONResponse(
        {
            "Status": status.HTTP_200_OK,
            "Timestamp": datetime.datetime.now().ctime(),
            "DebugMode": settings.DEBUG,
            "OperatingSystem": platform.uname(),
            "DockerMode": settings.DOCKER_MODE,
            "AppMode": settings.APP_ENVIRONMENT
        }
    )
