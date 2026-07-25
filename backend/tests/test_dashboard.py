import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_dashboard_stats(client: AsyncClient):
    response = await client.get("/api/v1/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_users" in data
    assert "active_sessions" in data
    assert "api_calls_24h" in data
    assert isinstance(data["total_users"], int)
    assert isinstance(data["active_sessions"], int)
    assert isinstance(data["api_calls_24h"], int)