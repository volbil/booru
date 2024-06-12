from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Tag
from app import constants


async def get_or_create_tag(session: AsyncSession, name: str):
    if not (tag := await session.scalar(select(Tag).filter(Tag.name == name))):
        tag = Tag(
            **{
                "type": constants.TAG_GENERAL,
                "images_count": 0,
                "name": name,
            }
        )
        session.add(tag)

    return tag
