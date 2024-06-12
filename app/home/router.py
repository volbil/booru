from jinja2_fragments.fastapi import Jinja2Blocks
from fastapi import APIRouter, Request


templates = Jinja2Blocks(directory="app/templates")
router = APIRouter()


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "pages/home.html",
        {
            "request": request,
        },
    )
