from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine

from app import routers
from app.models import DbModel

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    app.state.database_engine = create_engine("sqlite:///ride.db")
    DbModel.metadata.create_all(bind=app.state.database_engine)
    yield
    app.state.database_engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Ride App API",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.include_router(
        routers.user_router,
        prefix="/users",
        tags=["Users"],
    )
    return app