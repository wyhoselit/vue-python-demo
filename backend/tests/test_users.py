import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_users_list(client: AsyncClient):
    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for user in data:
        assert "id" in user
        assert "name" in user
        assert "email" in user
        assert "status" in user
        assert isinstance(user["id"], int)
        assert isinstance(user["name"], str)
        assert isinstance(user["email"], str)
        assert isinstance(user["status"], str)