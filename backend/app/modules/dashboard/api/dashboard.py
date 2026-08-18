from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_users: int
    active_sessions: int
    api_calls_24h: int


class RealtimeDataPoint(BaseModel):
    timestamp: str
    requests: int
    avg_response_time: float
    status2xx: int
    status4xx: int
    status5xx: int
    active_users: int


router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    return {
        "total_users": 1250,
        "active_sessions": 42,
        "api_calls_24h": 15420,
    }


@router.get("/realtime", response_model=list[RealtimeDataPoint])
async def get_dashboard_realtime():
    now = datetime.now()
    return [
        {
            "timestamp": now.isoformat(),
            "requests": 10,
            "avg_response_time": 25.5,
            "status2xx": 8,
            "status4xx": 1,
            "status5xx": 1,
            "active_users": 3,
        }
    ]