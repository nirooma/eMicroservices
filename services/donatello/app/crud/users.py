from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User


async def get_user_by_username(session: AsyncSession, username: str):
    res = await session.execute(select(User).filter_by(username=username))
    return res.scalar_one_or_none()

