from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Image


async def get_image(session: AsyncSession, image_id: str):
    return await session.scalar(select(Image).filter(Image.id == image_id))
