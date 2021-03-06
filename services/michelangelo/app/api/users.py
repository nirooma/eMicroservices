import logging
from typing import List

from fastapi import APIRouter, Depends, Request
from starlette import status
from starlette.responses import Response
from starlette.authentication import requires
from app.crud import users
from app.schemas.users import User_Pydantic

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/me/", response_model=User_Pydantic)
async def current_user(user: User_Pydantic = Depends(users.get_current_user)):
    return user


@router.get('/all_users', response_model=List[User_Pydantic])
@requires(['is_superuser'])
async def all_users(request: Request):
    return await users.all_users()


@router.delete('/all_users', status_code=status.HTTP_204_NO_CONTENT)
@requires(['is_superuser'])
async def delete_all_users(request: Request):
    await users.delete_all_users(i_know_what_im_doing=True)
    logger.info("all users deleted from the dibi")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

