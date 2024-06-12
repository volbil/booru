from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile, Form, Depends
from fastapi import APIRouter, Request
from app.database import get_session
from app.utils import redirect
from typing import Annotated
from app import templates
from . import service


router = APIRouter()


@router.get("/upload")
async def upload_page(request: Request):
    return templates.TemplateResponse(
        "pages/upload.html",
        {
            "request": request,
        },
    )


@router.post("/upload")
async def upload_file(
    request: Request,
    file: UploadFile,
    description: Annotated[str | None, Form()] = None,
    source: Annotated[str | None, Form()] = None,
    tags: Annotated[str | None, Form()] = None,
    session: AsyncSession = Depends(get_session),
):
    image = await service.process_upload(
        session, file, description, source, tags
    )

    return redirect(request, f"/image/{image.id}")
