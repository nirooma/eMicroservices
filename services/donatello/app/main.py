import datetime
import logging
import platform
from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse

from fastapi.templating import Jinja2Templates
from app.core.logging import configure_logging
from app.api.api_v1.api import api_router
from app.core.config import settings

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="app/templates")

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# configure_logging()

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health() -> JSONResponse:
    """Internal use only - Do not use with a client API"""
    return JSONResponse(
        {
            "Status": status.HTTP_200_OK,
            "Timestamp": datetime.datetime.now().ctime(),
            "DebugMode": settings.DEBUG,
            "OperatingSystem": platform.uname(),
            "DockerMode": settings.DOCKER_MODE,
            "AppMode": settings.APP_ENVIRONMENT,
        }
    )


@app.get("/", response_class=HTMLResponse)
async def hello_world(request: Request):
    return templates.TemplateResponse("hello_world.html", context={"request": request})
