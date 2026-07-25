from fastapi import APIRouter
from pydantic import BaseModel
from typing import List


class User(BaseModel):
    id: int
    name: str
    email: str
    status: str


router = APIRouter()


@router.get("", response_model=List[User])
async def get_users():
    return [
        {"id": 1, "name": "Alice Chen", "email": "alice@example.com", "status": "active"},
        {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "status": "active"},
        {"id": 3, "name": "Carol Davis", "email": "carol@example.com", "status": "inactive"},
        {"id": 4, "name": "David Wilson", "email": "david@example.com", "status": "active"},
        {"id": 5, "name": "Eva Martinez", "email": "eva@example.com", "status": "pending"},
    ]