from fastapi import FastAPI

from api import router

def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def create_app():
    app_ = FastAPI(
        title="Hedwig a crawler for the web",
        description="Hedwig is a web crawler that can be used to crawl the web and extract information from websites",
        version="0.1.0",
    )
    init_routers(app_=app_)
    return app_

app = create_app()
