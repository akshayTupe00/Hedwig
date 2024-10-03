from fastapi import APIRouter

from .health_check import health_check_router

monitoring_routers  = APIRouter()

monitoring_routers.include_router(health_check_router, prefix="/monitor", tags=["monitoring"] )