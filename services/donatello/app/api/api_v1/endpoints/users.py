from typing import List

from fastapi import Depends, APIRouter, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.security import get_password_hash

from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreationResponse, UserResponse

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(
        user: UserCreationResponse, session: AsyncSession = Depends(get_session)
) -> User:
    user = User(
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.get("/", response_model=List[UserResponse])
async def all_users(session: AsyncSession = Depends(get_session)):
    """ Return all the available users in the db """
    _users = await session.execute(select(User))
    users = _users.scalars().all()
    return users


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_users(session: AsyncSession = Depends(get_session)):
    user = await session.execute(select(User))
    await session.delete(user.first())
    
