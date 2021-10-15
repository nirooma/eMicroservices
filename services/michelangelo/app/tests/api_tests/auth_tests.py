import asyncio
from starlette import status
from starlette.responses import Response
from starlette.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer
from app.models import User

LOGIN_URL = "http://localhost:8001/api/v1/accounts/login"
REGISTER_URL = "http://localhost:8001/api/v1/accounts/register"

UNAUTHORIZED_USER = {
    "username": "admin",
    "password": "a"
}

AUTHORIZED_USER_NO_ACTIVE = {
    "username": "nirooma",
    "password": "a"
}

AUTHORIZED_USER = {
    "username": "admin",
    "password": "admin"
}


def test_unauthorized_user(client_with_db):
    """ User try to connect with invalid credentials """
    response: Response = client_with_db.post(LOGIN_URL, data=UNAUTHORIZED_USER)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "SessionToken" not in response.cookies
    assert "access_token" not in response._content.decode()


def test_not_active_authorize_user(client_with_db):
    """ User exists in the dibi but is not active yet """
    response: Response = client_with_db.post(LOGIN_URL, data=AUTHORIZED_USER_NO_ACTIVE)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "SessionToken" not in response.cookies
    assert "access_token" not in response._content.decode()


def test_authorize_user(client_with_db):
    """ Normal login, user exists in the dibi and he is active """
    response: Response = client_with_db.post(LOGIN_URL, data=AUTHORIZED_USER)
    assert response.status_code == status.HTTP_200_OK
    assert "SessionToken" in response.cookies
    assert "access_token" in response._content.decode()




