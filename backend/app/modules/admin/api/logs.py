from fastapi import APIRouter, Depends
from app.api.v1.deps import get_admin_user
from app.modules.user.user import User
import logging

router = APIRouter()

@router.get("/logs")
def get_logs(
    admin: User = Depends(get_admin_user)
):
    # Retrieve recent logs from the root logger's handlers.
    # In a real app, read from a file or external log aggregator.
    root_logger = logging.getLogger()
    logs = []
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            with open(handler.baseFilename, 'r') as f:
                logs = f.readlines()[-100:]
            break
    
    return {"logs": logs}