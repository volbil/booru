from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.database import sessionmanager
from app.utils import get_settings
from fastapi import FastAPI


def create_app(init_db: bool = True) -> FastAPI:
    settings = get_settings()
    lifespan = None

    # SQLAlchemy initialization process
    if init_db:
        sessionmanager.init(settings.database.endpoint)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if sessionmanager._engine is not None:
                await sessionmanager.close()

    app = FastAPI(
        title="Booru",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    from .home import router as home_router

    app.include_router(home_router)

    @app.get("/ping")
    async def ping_pong():
        return "pong"

    return app
