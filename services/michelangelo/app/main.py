import time
from fastapi import FastAPI, Request
import time
import requests
app = FastAPI()


@app.get("/health")
async def health(request: Request):
    return 200
