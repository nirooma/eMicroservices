from fastapi import APIRouter, Depends

from app.crud import users
from app.models.users import User_Pydantic

router = APIRouter()


@router.get("/me/", response_model=User_Pydantic)
async def current_user(user: User_Pydantic = Depends(users.get_current_user)):
    return user
