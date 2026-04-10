from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import APP_TITLE, STATIC_DIR
from app.db import Base, engine
from app.routes import actions, web


def create_app() -> FastAPI:
    app = FastAPI(title=APP_TITLE)

    Base.metadata.create_all(bind=engine)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    app.include_router(web.router)
    app.include_router(actions.router)
    return app


app = create_app()
