from typing import List

from fastapi import Depends, APIRouter, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.security import get_password_hash
from app.db.session import get_session
from app.models.user import User
from app.schemas.user import UserCreationResponse

router = APIRouter()


@router.post("/", response_model=UserCreationResponse)
async def create_user(
        user: User, session: AsyncSession = Depends(get_session)
) -> User:
    user = User(
        id=user.id,
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


@router.get("/", response_model=List[UserCreationResponse])
async def all_users(session: AsyncSession = Depends(get_session)):
    """ Return all the available users in the db """
    _users = await session.execute(select(User))
    users = _users.scalars().all()
    return users


@router.get('/{id_}')
async def get_filtered_user(id_: int, session: AsyncSession = Depends(get_session)):
    stmt = select(User).where(User.username == 'nirooma')
    user = await session.execute(stmt)
    user = user.scalars().all()
    print('*' * 30)
    print(user)
    if user is None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No User Found!"
        )
    return {"x": 1}
