from fastapi import APIRouter

from internal.schemas.dto.monitoring.health_check import Health_Check
health_check_router = APIRouter()

@health_check_router.get("/health_check")
async def health_check():
  return Health_Check(version="1.0.0", status="ok")
  