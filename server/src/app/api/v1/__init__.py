"""API v1 router aggregation."""

from fastapi import APIRouter
from .endpoints import user_router


api_router = APIRouter()

# Include sub routers
api_router.include_router(user_router, prefix="/user", tags=["User"])


__all__ = ["api_router"]