from fastapi import APIRouter
from app.api.versioning import APIVersion, fallback_version

# Registry for available versions
AVAILABLE_VERSIONS: dict[str, APIRouter] = {}

def get_router_for_version(version: APIVersion) -> APIRouter:
    """Get router for a specific version, with fallback support."""
    router = AVAILABLE_VERSIONS.get(version.value)
    if router is None:
        fallback = fallback_version(version)
        if fallback:
            router = AVAILABLE_VERSIONS.get(fallback.value)
    return router

def register_version(version: APIVersion, router: APIRouter):
    """Register a router for a specific API version."""
    AVAILABLE_VERSIONS[version.value] = router
