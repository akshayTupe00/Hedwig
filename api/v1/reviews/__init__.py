from fastapi import APIRouter

from .reviews import review_router

reviews_router = APIRouter()

review_router.include_router(reviews_router, prefix="/reviews", tags=["reviews"])