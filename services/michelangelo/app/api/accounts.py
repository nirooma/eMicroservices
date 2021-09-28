from typing import List

from fastapi import Depends, APIRouter, status, HTTPException
from app.models.users import User_Pydantic, UserIn_Pydantic
from app.models import User

from app.core import security
from app.crud import users
from app.core.jwt import create_access_token
from app.schemas.token import Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.configuration_utils import config

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload:  UserIn_Pydantic):
    user = await users.create_user(payload)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=config.get("errors")["loginError"]
        )
    print("sending some welcome email")
    print("sending messages to the queue.")


@router.post('/login', status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_payload: OAuth2PasswordRequestForm = Depends()):
    user = await security.authenticate(form_payload.username, form_payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=config.get("errors")["loginError"],
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"username": user.username, "email": user.email, "phone": user.phone}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User_Pydantic)
async def read_users_me(current_user: User = Depends(users.get_current_user)):
    return current_user
