from app.core.config import settings
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise, run_async
from fastapi import FastAPI
models = [
    "app.models",
    "aerich.models",
]

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": models,
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": models},
        generate_schemas=False,
        add_exception_handlers=True,
    )