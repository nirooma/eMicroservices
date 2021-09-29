import logging

import psycopg2
from fastapi import FastAPI, Request

from app.core.authentication import middleware
from app.core.logging import configure_logging
from app.db.session import init_db
from app.core.config import settings
from app.urls import api_router


logger = logging.getLogger(__name__)

# init loggers at the beginning
configure_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    middleware=middleware
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    try:
        init_db(app)
    except psycopg2.Error as error:
        logger.error(f"error initialize db {error=}")


@app.get("/health")
async def health(request: Request):
    return 200

