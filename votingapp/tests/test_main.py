import pytest
from httpx import AsyncClient

from ..main import app


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


# @pytest.mark.asyncio
# async def test_create_inexistant_user():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.post(
#             "/users/",
#             json={
#                 "email": "test test",
#                 "password": "test123",
#             },
#         )
#     assert response.status_code == 200
#     assert response.json() == {"id": "3"}


@pytest.mark.asyncio
async def test_create_existant_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/",
            json={
                "email": "test test",
                "password": "test123",
            },
        )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


@pytest.mark.asyncio
async def test_create_election():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/elections/create?user_id=1",
            json={
                "title": "test election",
                "description": "testing.",
            },
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_read_elections():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/elections/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_read_candidates():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/elections/1")
    assert response.status_code == 200

# TODO: move tests to test database (that will be created from scratch for every test)