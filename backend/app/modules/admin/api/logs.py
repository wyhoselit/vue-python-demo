"""Admin log retrieval API endpoints."""
import json
import os
from fastapi import APIRouter, Depends
from app.api.v1.deps import get_admin_user
from app.modules.core.config import settings
from app.modules.admin.utils.redactor import redact_sensitive_data

router = APIRouter()

@router.get("/logs")
def get_tracing_logs(
    tail: int = 100,
    admin=Depends(get_admin_user)
):
    """Retrieve system tracing logs.

    Args:
        tail: Number of most recent lines to retrieve.
        admin: Dependency to verify admin user privileges.

    Returns:
        A list of redacted JSON log entries.
    """
    log_file_path = settings.LOG_FILE_PATH
    logs = []
    if os.path.exists(log_file_path):
        with open(log_file_path, "r") as f:
            # Read last lines, assume pythonjsonlogger format (one JSON per line)
            all_lines = f.readlines()
            for line in all_lines[-tail:]:
                try:
                    logs.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Failed to decode log line: {line.strip()}, error: {e}")
                    continue
    
    return {"logs": redact_sensitive_data(logs)}

