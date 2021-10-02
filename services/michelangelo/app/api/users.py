from typing import List

from fastapi import APIRouter, Depends

from app.crud import users
from app.schemas.users import User_Pydantic

router = APIRouter()


@router.get("/me/", response_model=User_Pydantic)
async def current_user(user: User_Pydantic = Depends(users.get_current_user)):
    return user


@router.get('/all_users', response_model=List[User_Pydantic])
async def all_users():
    return await users.all_users()
