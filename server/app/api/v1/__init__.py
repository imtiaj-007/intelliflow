"""API v1 router aggregation."""

from fastapi import APIRouter

from .endpoints import file_router, user_router, workflow_router

api_router = APIRouter()

# Include sub routers
api_router.include_router(user_router, prefix="/user", tags=["User"])
api_router.include_router(file_router, prefix="/file", tags=["File"])
api_router.include_router(workflow_router, prefix="/workflow", tags=["Workflow"])


__all__ = ["api_router"]
