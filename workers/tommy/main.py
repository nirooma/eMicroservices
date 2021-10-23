import datetime
import logging
from typing import Optional, Any

from fastapi import FastAPI
from redis import Redis
from starlette import status
from starlette.responses import JSONResponse

from app.core.cache import CacheManager
from app.core.logging import configure_logging

logger = logging.getLogger(__name__)

# init loggers at the beginning
configure_logging()

app = FastAPI()

cacher: Optional[CacheManager] = None


@app.on_event("startup")
async def startup_event():
    global cacher
    if cacher is None:
        cacher = CacheManager()


@app.get("/api/get")
async def get_cache(name: str):
    """ Get from cache """
    global cacher
    return cacher.get(name=name)


@app.post("/api/set")
async def set_cache(name: str, value: Any, ex=None, px=None, nx=False, xx=False, keepttl=False):
    """ Set to cache """
    return cacher.set(name, value, ex, px, nx, xx, keepttl)


@app.get("/health")
async def health() -> JSONResponse:
    """Internal use only - Do not use with a client API"""

    return JSONResponse(
        {
            "Status": status.HTTP_200_OK,
            "Timestamp": datetime.datetime.now().ctime(),
        }
    )
