from fastapi import APIRouter, Depends
from app.api.v1.deps import get_admin_user
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/")
def get_admin_status(
    admin=Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    return {"status": "ok"}


