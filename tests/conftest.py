from collections.abc import Generator

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.injections import get_session
from app.main import create_app
from app.models import DbModel, UserModel

@fixture(scope="function")
def app() -> FastAPI:
    return create_app()

@fixture(scope="function")
def session(app: FastAPI) -> Generator[Session]:
    engine = create_engine("sqlite:///test.db")
    DbModel.metadata.create_all(bind=engine)
    try:
        with (session := Session(bind=engine)).begin():
            app.dependency_overrides[get_session] = lambda: session
            yield session
            session.rollback()
    finally:
        DbModel.metadata.drop_all(engine)
        engine.dispose()

@fixture(scope="function")
def test_client(app: FastAPI, session: Session) -> Generator[TestClient]:
    with TestClient(app=app) as test_client:
        yield test_client

@fixture(scope="function")
def test_user(session: Session) -> UserModel:
    user = UserModel(username="testuser", password="testpassword")
    session.add(user)
    session.flush()
    return user

