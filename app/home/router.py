from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request
from app.database import get_session
from fastapi import Depends
from app import templates
from . import service


router = APIRouter()


@router.get("/")
async def home(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    images = await service.get_images(session, 50, 0)
    return templates.TemplateResponse(
        "pages/home.html",
        {"request": request, "images": images},
    )
