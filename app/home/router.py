from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request
from app.database import get_session
from fastapi import Depends
from app import templates

from app.models import Tag


router = APIRouter()


@router.get("/")
async def home(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    test_tag = Tag(
        **{
            "images_count": 0,
            "type": "general",
            "name": "hui",
        }
    )
    session.add(test_tag)
    await session.commit()
    return templates.TemplateResponse(
        "pages/home.html",
        {
            "request": request,
        },
    )
