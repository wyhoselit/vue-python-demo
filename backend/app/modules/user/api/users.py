from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.modules.core.database import get_db
from app.modules.user.user import User
from app.modules.core.security import verify_token
from pydantic import BaseModel
from typing import List
from app.api.v1.deps import get_admin_user, get_current_user

router = APIRouter()

class UserOut(BaseModel):
    id: int
    email: str
    roles: List[str] = []

    class Config:
        from_attributes = True

@router.get("/me", response_model=UserOut)
def get_me(user: User = Depends(get_current_user)):
    user_data = UserOut(
        id=user.id,
        email=user.email,
        roles=[role.name for role in user.roles]
    )
    return user_data

@router.get("", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db), admin: User = Depends(get_admin_user)):
    users = db.query(User).all()
    return [
        UserOut(
            id=user.id,
            email=user.email,
            roles=[role.name for role in user.roles]
        )
        for user in users
    ]
