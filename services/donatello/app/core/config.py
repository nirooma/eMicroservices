import enum
import os
import platform
import secrets
from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class AppEnvironments(enum.Enum):
    ePRODUCTION = "production"
    eDEVELOPMENT = "development"
    eTEST = "test"


class BaseConfiguration(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = "Cloud Project"
    DOCKER_MODE: bool = False if platform.uname().system == "Darwin" else True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://localhost:5672")
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
    DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "Asia/Jerusalem")


class DevelopmentConfig(BaseConfiguration):
    APP_ENVIRONMENT = AppEnvironments.eDEVELOPMENT.value
    DEBUG: bool = True
    DATABASE_URL: str = os.getenv(
        "DONATELLO_DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@donatello-db:5432/fastapi"
    )


class ProductionConfig(BaseConfiguration):
    APP_ENVIRONMENT = AppEnvironments.ePRODUCTION.value
    DEBUG: bool = False


class TestConfig(BaseConfiguration):
    APP_ENVIRONMENT = AppEnvironments.eTEST.value
    DEBUG: bool = True


@lru_cache()
def get_settings():
    """
    Load config based on environment
    :return:
    """
    config_cls = {
        "production": ProductionConfig,
        "development": DevelopmentConfig,
        "test": TestConfig,
    }

    return config_cls.get(os.getenv("APP_ENVIRONMENT"), DevelopmentConfig)()


settings = get_settings()
