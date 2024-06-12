from fastapi import APIRouter, Request
from app import templates


router = APIRouter()


@router.get("/upload")
async def upload(request: Request):
    return templates.TemplateResponse(
        "pages/upload.html",
        {
            "request": request,
        },
    )
