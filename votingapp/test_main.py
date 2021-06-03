import pytest
from httpx import AsyncClient

from .main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello! Welcome to votingapp. Head on to the docs to get started."
    }


@pytest.mark.asyncio
async def test_read_users():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_read_inexistent_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/999999999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@pytest.mark.asyncio
async def test_read_existent_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "email": "user 1",
        "id": 1,
        "is_active": True,
        "elections": [],
    }


@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/",
            json={
                "email": "test test",
                "password": "test123",
            },
        )
    assert response.status_code == 200
    assert response.json() == {
        {"email": "test test", "id": 4, "is_active": "true", "elections": []}
    }
