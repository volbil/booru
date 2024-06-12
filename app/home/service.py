from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Image


async def get_images(session: AsyncSession, limit: int, offset: int):
    return await session.scalars(select(Image).limit(limit).offset(offset))
