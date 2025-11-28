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
        tags=["Users, Registration"],
    )

    app.include_router(
        routers.auth_router,
        prefix="/auth",
        tags=["Authentication"],
    )

    app.include_router(
        routers.ride_router,
        prefix="/rides",
        tags=["Rides"],
    )

    app.include_router(
        routers.participation_router,
        prefix="/rides/participations",
        tags=["Partitipation"],
    )
    return app