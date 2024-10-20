import os
from pydantic_settings import BaseSettings
class Config(BaseSettings):
    ES_HOST: str = os.getenv("ES_HOST")
    ES_USER: str = os.getenv("ES_USER")
    ES_PASSWORD: str = os.getenv("ES_PASSWORD")

config: Config = Config()
