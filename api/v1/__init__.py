from fastapi import APIRouter

from .reviews import review_router
from .monitoring import health_check_router

v1_router = APIRouter()

v1_router.include_router(review_router, prefix="/reviews", tags=["reviews"])