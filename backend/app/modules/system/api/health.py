from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.modules.core.database import get_db

router = APIRouter()


@router.get("")
async def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"
        raise HTTPException(status_code=503, detail="Database connection error")

    return {"status": "ok", "database": db_status}
