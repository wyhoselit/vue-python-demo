from fastapi import APIRouter
from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_users: int
    active_sessions: int
    api_calls_24h: int


router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    return {
        "total_users": 1250,
        "active_sessions": 42,
        "api_calls_24h": 15420,
    }