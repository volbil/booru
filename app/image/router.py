from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request, Form
from app.database import get_session
from app.utils import redirect
from typing import Annotated
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
    tags = []

    for tag in image.tags:
        if tag not in tags:
            tags.append(tag)

    return templates.TemplateResponse(
        "pages/image.html",
        {
            "request": request,
            "image": image,
            "tags": tags,
        },
    )


@router.get("/image/{image_id}/edit")
async def image_edit_page(
    request: Request,
    image_id: str,
    session: AsyncSession = Depends(get_session),
):
    image = await service.get_image(session, image_id)

    return templates.TemplateResponse(
        "pages/edit.html",
        {
            "request": request,
            "image": image,
        },
    )


@router.post("/image/{image_id}/update")
async def image_update(
    request: Request,
    image_id: str,
    description: Annotated[str | None, Form()] = None,
    source: Annotated[str | None, Form()] = None,
    tags: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(get_session),
):
    image = await service.update_image(
        session, image_id, description, source, tags
    )

    return redirect(request, f"/image/{image.id}")


@router.post("/image/{image_id}/trash")
async def image_trash(
    request: Request,
    image_id: str,
    session: AsyncSession = Depends(get_session),
):
    await service.trash_image(session, image_id)
    return redirect(request, "/")
