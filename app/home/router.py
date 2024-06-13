from app.utils import pagination, frontend_pagination
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request, Query
from app.database import get_session
from typing import Annotated
from fastapi import Depends
from app import templates
from . import service


router = APIRouter()


@router.get("/")
async def home(
    request: Request,
    session: AsyncSession = Depends(get_session),
    page: Annotated[int, Query(min=1)] = 1,
    q: str | None = None,
):
    limit, offset = pagination(page, 4)
    result = await service.get_images(session, limit, offset)
    total = await service.count_images(session)

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
            "pagination": frontend_pagination(page, limit, total, "/"),
            "request": request,
            "images": images,
            "tags": tags,
        },
    )
