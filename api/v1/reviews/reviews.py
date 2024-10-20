from fastapi import APIRouter
from internal.services.reviews import scrape_reviews, get_job_id

review_router = APIRouter()

@review_router.get("/submit-job", tags=["reviews"])
async def submit_job(page: str):
    res, err = await get_job_id(page)
    if err:
        return {"error": err}
    return {"job_id": res}
