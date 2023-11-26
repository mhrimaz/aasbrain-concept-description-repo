import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    app_name: str = "AAS Brain Concept Description Repository API"
    mongo_db_name: str = "concept_description_db"
    db_backend: str = os.getenv("BACKEND", "redis")
    db_uri: str = os.getenv("DB_URI", "redis://127.0.0.1:6019")
    debug: bool = os.getenv("DEBUG", False)


@lru_cache()
def get_config():
    return Config()
