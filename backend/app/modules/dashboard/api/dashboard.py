import random
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
    avgResponseTime: float
    status2xx: int
    status4xx: int
    status5xx: int
    activeUsers: int


router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():

    #retun random value
    return {
        "total_users": random.randint(0, 1000),
        "active_sessions": random.randint(0, 100),
        "api_calls_24h": random.randint(0, 10000),
    }


@router.get("/realtime", response_model=list[RealtimeDataPoint])
async def get_dashboard_realtime():
    now = datetime.now()
    return [
        {
            "timestamp": now.isoformat(),
            "requests": random.randint(0, 1000),
            "avgResponseTime": random.uniform(0, 100),
            "status2xx": random.randint(0, 100),
            "status4xx": random.randint(0, 100),
            "status5xx": random.randint(0, 100),
            "activeUsers": random.randint(0, 100),
        }
    ]