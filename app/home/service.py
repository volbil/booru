from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from sqlalchemy.orm import joinedload
from app.models import Image


async def count_images(session: AsyncSession):
    return await session.scalar(
        select(func.count(Image.id)).filter(
            Image.trash == False,  # noqa: E712
        )
    )


async def get_images(session: AsyncSession, limit: int, offset: int):
    return await session.scalars(
        select(Image)
        .filter(
            Image.trash == False,  # noqa: E712
        )
        .options(joinedload(Image.tags))
        .order_by(desc(Image.created))
        .limit(limit)
        .offset(offset)
    )
