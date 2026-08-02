from typing import Optional, Dict, Any, Callable
from fastapi import Request, Response
from enum import Enum

class APIVersion(str, Enum):
    V1 = "v1"
    V2 = "v2"

DEFAULT_VERSION = APIVersion.V1

def get_version_from_path(path: str) -> Optional[APIVersion]:
    if "/v1/" in path:
        return APIVersion.V1
    if "/v2/" in path:
        return APIVersion.V2
    return None

def fallback_version(version: APIVersion) -> Optional[APIVersion]:
    """Define fallback logic."""
    if version == APIVersion.V2:
        return APIVersion.V1
    return None
