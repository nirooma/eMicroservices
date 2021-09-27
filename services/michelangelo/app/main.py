import time
from fastapi import FastAPI, Request

import psycopg2
from app.db.session import init_db

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    try:
        init_db(app)
    except psycopg2.Error as error:
        print('Error', error)


@app.get("/health")
async def health(request: Request):

    return 200
