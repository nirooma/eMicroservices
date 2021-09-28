import time
from fastapi import FastAPI, Request

import psycopg2
from app.db.session import init_db
from app.core.config import settings
from app.urls import api_router

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    try:
        init_db(app)
    except psycopg2.Error as error:
        print('Error', error)


@app.get("/health")
async def health(request: Request):
    return 200
