from jinja2_fragments.fastapi import Jinja2Blocks
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.database import sessionmanager
from app.utils import get_settings
from fastapi import FastAPI
import arel


settings = get_settings()
templates = Jinja2Blocks(directory="app/templates")


def create_app(init_db: bool = True) -> FastAPI:
    lifespan = None

    app = FastAPI(
        title="Booru",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.mount(
        "/static",
        StaticFiles(directory="app/static"),
        name="static",
    )

    app.mount(
        "/uploads",
        StaticFiles(directory=settings.backend.uploads),
        name="uploads",
    )

    # Hot reload for Jinja templates
    if settings.backend.debug:
        hot_reload = arel.HotReload(paths=[arel.Path("./app/templates/")])
        templates.env.globals["hot_reload"] = hot_reload
        templates.env.globals["DEBUG"] = True

        app.add_websocket_route(
            "/hot-reload", route=hot_reload, name="hot-reload"
        )

        app.add_event_handler("startup", hot_reload.startup)
        app.add_event_handler("shutdown", hot_reload.shutdown)

    # SQLAlchemy initialization process
    if init_db:
        sessionmanager.init(settings.database.endpoint)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    from .upload import router as upload_router
    from .image import router as image_router
    from .home import router as home_router

    app.include_router(upload_router)
    app.include_router(image_router)
    app.include_router(home_router)

    @app.get("/ping")
    async def ping_pong():
        return "pong"

    return app
