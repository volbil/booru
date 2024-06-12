from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request
from app.database import get_session
from app.utils import pagination
from fastapi import Depends
from app import templates
from . import service


router = APIRouter()


@router.get("/")
async def home(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    page = 1
    limit, offset = pagination(page)
    result = await service.get_images(session, limit, offset)

    images = []
    tags = []

    for image in result.unique():
        images.append(image)

        for tag in image.tags:
            if tag not in tags:
                tags.append(tag)

    return templates.TemplateResponse(
        "pages/home.html",
        {
            "request": request,
            "images": images,
            "tags": tags,
        },
    )
