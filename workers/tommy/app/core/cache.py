import logging
import os
from typing import Optional, Any

from urllib.parse import urlparse

from redis import Redis

logger = logging.getLogger(__name__)


class CacheManager:
    REDIS_URL = os.getenv("REDIS_URL")

    def __init__(self):
        self.parse_url = urlparse(self.REDIS_URL)
        self.instance: Redis = self._connect()
        super().__init__()

    def _connect(self) -> Redis:
        return Redis(host=self.parse_url.hostname, port=self.parse_url.port)

    def ping(self) -> bool:
        return self.instance.ping()

    def get_instance(self) -> Redis:
        return self.instance

    def get(self, name) -> Any:
        pass
        value = self.instance.get(name=name)
        if value is not None:
            logger.info(f"Cache hit with value {name!r}")
            return value
        logger.info(f"Cache miss with value {name!r}")

    def set(
            self, name: str,
            value: Any,
            ex=None,
            px=None,
            nx=False,
            xx=False,
            keepttl=False
    ):
        logger.info(f"Cache set with value {value} for name {name!r}")
        return self.instance.set(name, value, ex, px, nx, xx, keepttl)

    def flush_all(self):
        return self.instance.flushall()
