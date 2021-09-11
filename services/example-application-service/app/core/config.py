import os
import platform
import secrets
from functools import lru_cache
import enum
from pydantic import BaseSettings


class AppEnvironments(enum.Enum):
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    TEST = "test"


class BaseConfiguration(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = "Cloud Project"
    DOCKER_MODE: bool = False if platform.uname().system == "Darwin" else True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8


class DevelopmentConfig(BaseConfiguration):
    APP_ENVIRONMENT = AppEnvironments.DEVELOPMENT.value
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi"


class ProductionConfig(BaseConfiguration):
    APP_ENVIRONMENT = AppEnvironments.PRODUCTION.value
    DEBUG: bool = False


class TestConfig(BaseConfiguration):
    APP_ENVIRONMENT = AppEnvironments.TEST.value
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
        "test": TestConfig
    }

    return config_cls.get(os.getenv("APP_ENVIRONMENT"), DevelopmentConfig)()


settings = get_settings()
