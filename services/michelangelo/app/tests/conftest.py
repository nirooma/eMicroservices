import asyncio
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from main import app
from app.models import User

from tortoise.contrib.test import finalizer, initializer


@pytest.fixture()
def client() -> Generator:
    initializer(["app.models"])
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture()
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()
