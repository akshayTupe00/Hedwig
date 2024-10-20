from typing import Any
from playwright.async_api import async_playwright

from core.integrations.ai.google import process
from core.utils.crypto import generate_hash
from core.infrastructure.elastic.elastic import create_document
from internal.schemas.dao.reviews import ReviewRequest, StatusEnum
from internal.services.worker import ServiceWorker


class WebScraper(ServiceWorker):
    async def call(self, body: Any):
        print("Started scraping...")
        async with async_playwright() as p:
            try:
                print("Received request.", body)
                url = body.decode("utf-8")
                browser = await p.chromium.launch()
                page = await browser.new_page()
                print(f"Going to {url}")
                await page.goto(url)
                page_souce = await page.content()
                res = process(page_souce)
                return res
            except Exception as e:
                print(f"Error: {e}")
            finally:
                await browser.close()
                print("Finished scraping.")



async def scrape_reviews(page: str):
    return await scrape(page)


async def get_job_id(page: str) -> tuple:
    try:
        job_id = generate_hash(page)
        review_request = ReviewRequest(
            token_id=job_id,
            status=StatusEnum.IN_PROCESS,
            url=page,
        )

        review_request_dict = review_request.model_dump()
        print(review_request_dict)
        db_resp, e = await create_document(
            index_name="review_requests", doc_id=None, document=review_request_dict
        )
        if e:
            return None, e
        print(db_resp)
        return job_id, None
    except Exception as e:
        print(f"Error in getting job ID: {e}")
        return None, e
