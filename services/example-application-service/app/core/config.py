import os
import secrets
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = "Some_Project"


class DevelopmentConfig(Settings):
    DEBUG: bool = True


class ProductionConfig(Settings):
    DEBUG: bool = False


class TestingConfig(Settings):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_name = os.environ.get("SETTINGS_CONFIGURATION", "development")
    return config_cls_dict[config_name]()


settings = get_settings()
