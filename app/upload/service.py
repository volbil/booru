from sqlalchemy.ext.asyncio import AsyncSession
from app.service import get_or_create_tag
from fastapi import UploadFile
from app.models import Image
from uuid import uuid4
import aiofiles.os
import aiofiles
import os

from app.utils import (
    is_valid_tag_name,
    get_settings,
    utcnow,
)


async def create_folder(path):
    if not await aiofiles.os.path.exists(path):
        try:
            await aiofiles.os.mkdir(path)
        except FileExistsError:
            pass


async def create_folders(path):
    folder_path = os.path.dirname(path)
    folders = folder_path.split("/")
    current_path = "/"

    for folder in folders:
        current_path = os.path.join(current_path, folder)
        await create_folder(current_path)

    return current_path


async def process_upload(
    session: AsyncSession,
    file: UploadFile,
    description: str | None,
    source: str | None,
    tags: str | None,
):
    settings = get_settings()
    image_tags = []

    if tags is not None:
        for name in tags.split(" "):
            if not is_valid_tag_name(name):
                continue

            tag = await get_or_create_tag(session, name)

            image_tags.append(tag)

    now = utcnow()
    path_now = now.strftime("%d-%m-%y")
    extension = file.content_type.split("/")[-1]
    name = str(uuid4())

    path = f"{settings.backend.uploads}/{path_now}/{name}.{extension}"

    await create_folders(path)

    async with aiofiles.open(path, "wb") as f:
        await f.write(file.file.read())

    image = Image(
        **{
            "id": uuid4(),
            "description": description,
            "uploaded_by": "volbil",  # TODO: change to request user
            "tags": image_tags,
            "source": source,
            "created": now,
            "updated": now,
            "path": path,
            "meta": {},
        }
    )

    session.add(image)
    await session.commit()

    return image
