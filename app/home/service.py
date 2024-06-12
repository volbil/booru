from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.models import Image


async def get_images(session: AsyncSession, limit: int, offset: int):
    return await session.scalars(
        select(Image)
        .filter(
            Image.trash == False,  # noqa: E712
        )
        .order_by(desc(Image.created))
        .limit(limit)
        .offset(offset)
    )
