from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request
from app.database import get_session
from fastapi import Depends
from app import templates
from . import service


router = APIRouter()


@router.get("/image/{image_id}")
async def image_page(
    request: Request,
    image_id: str,
    session: AsyncSession = Depends(get_session),
):
    image = await service.get_image(session, image_id)

    return templates.TemplateResponse(
        "pages/image.html",
        {
            "request": request,
            "image": image,
        },
    )
