from fastapi import APIRouter, Depends, Request

from app.crud import users
from app.models import User
from app.models.users import User_Pydantic

router = APIRouter()


@router.get("/me/", response_model=User_Pydantic)
async def current_user(user: User = Depends(users.get_current_user)):
    return user
