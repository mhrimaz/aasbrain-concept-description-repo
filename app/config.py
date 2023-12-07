#  MIT License
#
#  Copyright (c) 2023. Mohammad Hossein Rimaz
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of
#  this software and associated documentation files (the “Software”), to deal in
#  the Software without restriction, including without limitation the rights to use,
#  copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
#  Software, and to permit persons to whom the Software is furnished to do so, subject
#   to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
#  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
#  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    app_name: str = "AAS Brain Concept Description Repository API"
    db_backend: str = os.getenv("BACKEND", "redis")
    db_uri: str = os.getenv("DB_URI", "redis://127.0.0.1:6019")
    debug: bool = os.getenv("DEBUG", False)
    # Options for GraphDB
    semantic_namespace: Optional[str] = os.getenv("SEMANTIC_NAMESPACE", "https://aasbrain/")
    semantic_graphdb_repo: Optional[str] = os.getenv("SEMANTIC_GRAPHDB_REPO", "aas")
    # Options for MongoDB
    mongo_db_name: str = os.getenv("MONGO_DB_NAME", "concept_description_db")
    # Options for Redis

    # Options for Neo4j

    # Options for Hybrid


@lru_cache()
def get_config():
    return Config()
