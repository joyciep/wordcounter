import os
import pytest
from httpx import AsyncClient
from starlette import status
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from app.db.session import Base
from app.main import get_application
from app.db.repositories.wordcount import WordCountRepository
from app.api.wordcount import get_word_count_repository
from tests.test_cases import test_scraper_data, test_invalid_requests_data


# use test database for tests
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_test_word_count_repository():
    try:
        session = async_session()
        yield WordCountRepository(session)
    finally:
        await session.close()


async def initialize_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
async def application():
    app = get_application()
    await initialize_test_db()
    app.dependency_overrides[get_word_count_repository] = get_test_word_count_repository
    yield app
    # remove test database
    os.remove("./test.db")


@pytest.mark.asyncio
@patch("requests.get")
async def test_word_count_api(mock_request, application):
    mock_request.return_value.content = test_scraper_data[0]["content"]
    mock_request.return_value.status_code = status.HTTP_200_OK
    async with AsyncClient(app=application, base_url="http://test") as ac:
        data = {"url": "https://example.com", "word": test_scraper_data[0]["word"]}
        response = await ac.post("/wordcount", json=data)
        # request again for testing retrieving word count from db
        second_response = await ac.post("/wordcount", json=data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ok"
    assert data["count"] == test_scraper_data[0]["count"]

    assert second_response.status_code == status.HTTP_200_OK
    data = second_response.json()
    assert data["status"] == "ok"
    assert data["count"] == test_scraper_data[0]["count"]


@pytest.mark.asyncio
@patch("requests.get")
async def test_word_count_api_scraper_failed(mock_request, application):
    mock_request.return_value.content = test_scraper_data[0]["content"]
    mock_request.return_value.status_code = status.HTTP_403_FORBIDDEN
    async with AsyncClient(app=application, base_url="http://test") as ac:
        data = {"url": "https://example.com", "word": test_scraper_data[0]["word"]}
        response = await ac.post("/wordcount", json=data)
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    data = response.json()
    assert data["status"] == "failed to get URL content"
    assert data["count"] == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("test_case", test_invalid_requests_data)
async def test_word_count_api_invalid_requests(test_case, application):
    async with AsyncClient(app=application, base_url="http://test") as ac:
        response = await ac.post("/wordcount", json=test_case)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
