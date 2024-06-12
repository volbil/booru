from sqlalchemy.ext.asyncio import AsyncSession
from app.service import get_or_create_tag
from app.utils import is_valid_tag_name
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from app.models import Image


async def get_image(session: AsyncSession, image_id: str):
    return await session.scalar(
        select(Image)
        .filter(Image.id == image_id)
        .options(joinedload(Image.tags))
    )


async def update_image(
    session: AsyncSession,
    image_id: str,
    description: str | None,
    source: str | None,
    tags: str | None,
):
    image = await get_image(session, image_id)
    image.description = description
    image.source = source

    image_tags = []

    if tags is not None:
        for name in tags.split(" "):
            if not is_valid_tag_name(name):
                continue

            tag = await get_or_create_tag(session, name)

            image_tags.append(tag)

    image.tags = image_tags

    session.add(image)
    await session.commit()

    return image


async def trash_image(session: AsyncSession, image_id: str):
    image = await get_image(session, image_id)
    image.trash = True
    session.add(image)
    await session.commit()

    return image
